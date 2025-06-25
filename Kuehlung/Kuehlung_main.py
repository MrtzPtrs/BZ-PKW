from Kuehlung.Waermetauscher import Waermetauscher_Ka
from Kuehlung.Kuehlmittelpumpe import Kuehlmittelpumpe_Ka
from Kathode.Verdichter import Engine_Cooling

from Kuehlung.Waermetauscher import Waermetauscher_BZ
from Kuehlung.Kuehlmittelpumpe import Kuehlmittelpumpe_BZ
from Kathode.Zwischenkuehler import Zwischenkuehler_Cooling
from Kathode.Brennstoffzelle import BZ_Cooling
from Kuehlung.Combi_Ventil import Combi_Valve
from Fahrzeugmodell.Fahrzeugmodell import Inverter_Cooling

from Outsourced.Gasberechnungen import Gas
import numpy as np
class Kuehlung():
    def __init__(self, Eingabe, para, Nat, Calib, Kathode, Anode, Fahrzeugmodell):
        self.Eingabe = Eingabe
        self.para = para
        self.Nat = Nat
        self.Calib = Calib
        self.Ka = Kathode
        self.An = Anode
        self.FZ = Fahrzeugmodell

        self.Heat_Ex_Ka = Waermetauscher_Ka(para=self.para, Nat=self.Nat, Calib=self.Calib)
        self.Cooling_Pump_Ka = Kuehlmittelpumpe_Ka(para=self.para, Nat=self.Nat, Calib=self.Calib)
        self.Comp_Eng = Engine_Cooling(para=self.para, Nat=self.Nat, Calib=self.Calib)
        self.Inv_Cool = Inverter_Cooling(para=self.para, Nat=self.Nat, Calib=self.Calib)

        self.Heat_Ex_BZ = Waermetauscher_BZ(para=self.para, Nat=self.Nat, Calib=self.Calib)
        self.Cooling_Pump_BZ = Kuehlmittelpumpe_BZ(para=self.para, Nat=self.Nat, Calib=self.Calib)
        self.BZ_Cool = BZ_Cooling(para=self.para, Nat=self.Nat, Calib=self.Calib)
        self.Intercooler = Zwischenkuehler_Cooling(para=self.para, Nat=self.Nat, Calib=self.Calib)
        self.Combi_Valve = Combi_Valve(para=self.para, Nat=self.Nat, Calib=self.Calib)
        self.Gas = Gas(para=self.para, Nat=self.Nat)

        self.case_HT = 1

    def __call__(self, I_St, Temp_BZ, Temp_Coolant_HT, dt):
        if 'HT-Kreislauf':
            self.P_BZ_Heat = (self.Nat['EN_O'] - self.Nat['EN_H']) * self.Calib['NumCells'] * I_St - self.Ka.BZ_C.P_Stack - self.Ka.BZ_C.P_Heat_Gas - self.An.BZ_A.P_Heat_Gas
            C_p_BZ = 0.0006024590163540639*Temp_BZ + 0.2611760246077719 #gefittet aus AVL (generic Steel)
            C_BZ = self.Calib['Masse_BZ_therm'] * C_p_BZ
            C_Coolant_HT = self.Calib['V_Coolant_HT'] * self.Gas.rho_liquid_calc() * self.Gas.C_p_Liquid()
            C_BZ_System = C_BZ + C_Coolant_HT

            P_Max_WTau = max(self.Nat['eps'], self.Calib['P_Max_WTau'] * (Temp_BZ - self.para['temp_env']) / (self.Calib['Temp_BZ_Soll'] - self.Eingabe['Umgebung']['standard']['temp_U']))

            if self.case_HT == 0: #Kaltstart
                if Temp_BZ < self.Calib['Temp_BZ_min'] + self.Calib['HT_Hysterese']:
                    self.case_HT = 0
                elif Temp_BZ >= self.Calib['Temp_BZ_min'] + self.Calib['HT_Hysterese']:
                    self.case_HT = 1
            elif self.case_HT == 1: #Sollbereich
                if Temp_BZ <= self.Calib['Temp_BZ_min'] - self.Calib['HT_Hysterese']:
                    self.case_HT = 0
                elif Temp_BZ > self.Calib['Temp_BZ_min'] - self.Calib['HT_Hysterese'] and Temp_BZ < self.Calib['Temp_BZ_max'] + self.Calib['HT_Hysterese']:
                    self.case_HT = 1
                elif Temp_BZ >= self.Calib['Temp_BZ_max'] + self.Calib['HT_Hysterese']:
                    self.case_HT = 2
            elif self.case_HT == 2: #Wärmenotlauf
                if Temp_BZ < self.Calib['Temp_BZ_max'] - self.Calib['HT_Hysterese']:
                    self.case_HT = 1
                elif Temp_BZ >= self.Calib['Temp_BZ_max'] - self.Calib['HT_Hysterese']:
                    self.case_HT = 2

            if self.case_HT == 0:
                self.P_BZ_Heat_Cool = 0
            elif self.case_HT == 1:
                self.P_Cool_Extra = self.Calib['K_Temp_Regelung'] * (Temp_BZ - self.Calib['Temp_BZ_Soll']) #P-Regler
                self.P_BZ_Heat_Cool = np.clip(self.P_BZ_Heat + self.Ka.Intercooler.P_ZwK_Heat + self.P_Cool_Extra, 0, min(self.Calib['V_dot_max_HT'] * self.Gas.rho_liquid_calc() * self.Gas.C_p_Liquid() * self.para['dtemp_FC'], P_Max_WTau))
            elif self.case_HT == 2:
                self.P_BZ_Heat_Cool = min(self.Calib['V_dot_max_HT'] * self.Gas.rho_liquid_calc() * self.Gas.C_p_Liquid() * self.para['dtemp_FC'], P_Max_WTau)

            self.Temp_BZ = Temp_BZ + (self.P_BZ_Heat - self.P_BZ_Heat_Cool) / C_BZ_System * dt
            self.Temp_Coolant_HT = Temp_Coolant_HT + (self.P_BZ_Heat - self.P_BZ_Heat_Cool) / C_BZ_System * dt

            self.ptm_BZ = {'Init': {'pres': self.para['pres_env'],
                                    "temp": self.Temp_Coolant_HT - self.para['dtemp_FC'] / 2,
                                    "V_dot": np.clip(self.P_BZ_Heat_Cool / (self.Gas.C_p_Liquid() * self.para['dtemp_FC']) / self.Gas.rho_liquid_calc(), self.Calib['V_dot_min_HT'], self.Calib['V_dot_max_HT'])}}
            self.ptm_BZ['Init'] |= {'m_dot': self.ptm_BZ['Init']['V_dot'] * self.Gas.rho_liquid_calc()}
            self.ptm_BZ |= {'Pump_in': self.ptm_BZ['Init']}
            self.ptm_BZ |= {"Pump_out": self.Cooling_Pump_BZ(self.ptm_BZ["Pump_in"])}
            self.ptm_BZ |= {"BZ_in": self.ptm_BZ['Pump_out']}
            self.ptm_BZ |= {"BZ_out": self.BZ_Cool(self.ptm_BZ["BZ_in"])}
            self.ptm_BZ |= {"ZwK_in": self.ptm_BZ['Pump_out']}
            self.ptm_BZ |= {"ZwK_out": self.Intercooler(self.ptm_BZ["ZwK_in"], ptmx=self.Ka.ptmx['Comp_in'], P_ZwK_Heat=self.Ka.Intercooler.P_ZwK_Heat)}
            self.ptm_BZ |= {"Combi_Valve_out": self.Combi_Valve(ptm_BZ=self.ptm_BZ["BZ_out"], ptm_ZwK=self.ptm_BZ["ZwK_out"])}
            self.ptm_BZ |= {"Wtau_in": self.ptm_BZ['Combi_Valve_out']}
            self.ptm_BZ |= {'Wtau_out': self.Heat_Ex_BZ(self.ptm_BZ['Wtau_in'], P_BZ_Heat_Cool=self.P_BZ_Heat_Cool, Temp_Coolant_HT=self.Temp_Coolant_HT, P_Max_WTau=P_Max_WTau)}
            self.ptm_BZ |= {"Pump_in": self.ptm_BZ['Wtau_out']}
            pres_corr = self.ptm_BZ['Pump_in']['pres'] - self.para['pres_env']
            if pres_corr != 0:
                self.ptm_BZ |= {"Pump_out": self.Cooling_Pump_BZ(self.ptm_BZ["Pump_in"], pres_corr=pres_corr)}
                self.ptm_BZ |= {"BZ_in": self.ptm_BZ['Pump_out']}
                self.ptm_BZ |= {"BZ_out": self.BZ_Cool(self.ptm_BZ["BZ_in"])}
                self.ptm_BZ |= {"ZwK_in": self.ptm_BZ['Pump_out']}
                self.ptm_BZ |= {"ZwK_out": self.Intercooler(self.ptm_BZ["ZwK_in"], ptmx=self.Ka.ptmx['Comp_in'], P_ZwK_Heat=self.Ka.Intercooler.P_ZwK_Heat)}
                self.ptm_BZ |= {"Combi_Valve_out": self.Combi_Valve(ptm_BZ=self.ptm_BZ["BZ_out"], ptm_ZwK=self.ptm_BZ["ZwK_out"])}
                self.ptm_BZ |= {"Wtau_in": self.ptm_BZ['Combi_Valve_out']}
                self.ptm_BZ |= {'Wtau_out': self.Heat_Ex_BZ(self.ptm_BZ['Wtau_in'], P_BZ_Heat_Cool=self.P_BZ_Heat_Cool, Temp_Coolant_HT=self.Temp_Coolant_HT, P_Max_WTau=P_Max_WTau)}
                self.ptm_BZ |= {"Pump_in": self.ptm_BZ['Wtau_out']}

        if 'NT-Kreislauf':
            self.FZ.P_Inv_Heat += self.Ka.Comp.P_Comp_Engine * (1 - self.Calib['Eff_E_M_Inv'])
            self.ptm_Ka = {'Init': {'pres': self.para['pres_env'],
                                    "temp": self.para['temp_max_C_Co'],
                                    "m_dot": (self.Ka.Comp.P_Comp_Heat + self.FZ.P_Inv_Heat) / (self.para['temp_max_C_Co'] - self.para["temp_interc"]) / self.Gas.C_p_Liquid()}}
            self.ptm_Ka['Init'] |= {'V_dot': self.ptm_Ka['Init']['m_dot'] / self.Gas.rho_liquid_calc()}
            self.ptm_Ka |= {'Pump_in': self.ptm_Ka['Init']}
            self.ptm_Ka |= {"Pump_out": self.Cooling_Pump_Ka(self.ptm_Ka["Pump_in"], ptmx=self.Ka.ptmx['Comp_in'])}
            self.ptm_Ka |= {"Comp_Eng_in": self.ptm_Ka['Pump_out']}
            self.ptm_Ka |= {"Comp_Eng_out": self.Comp_Eng(self.ptm_Ka["Comp_Eng_in"], ptmx=self.Ka.ptmx['Comp_in'], P_Comp_Heat=self.Ka.Comp.P_Comp_Heat)}
            self.ptm_Ka |= {"Wtau_in": self.ptm_Ka['Comp_Eng_out']}
            self.ptm_Ka |= {'Wtau_out': self.Heat_Ex_Ka(self.ptm_Ka['Wtau_in'], ptmx=self.Ka.ptmx['Comp_in'], P_Ka=self.Ka.Comp.P_Comp_Heat + self.FZ.P_Inv_Heat)}
            self.ptm_Ka |= {'Inv_in': self.ptm_Ka['Wtau_out']}
            self.ptm_Ka |= {'Inv_out': self.Inv_Cool(self.ptm_Ka['Inv_in'], P_Inv_Heat=self.FZ.P_Inv_Heat)}
            self.ptm_Ka |= {"Pump_in": self.ptm_Ka['Wtau_out']}
            pres_corr = self.ptm_Ka['Pump_in']['pres'] - self.para['pres_env']
            if pres_corr != 0:
                self.ptm_Ka |= {"Pump_out": self.Cooling_Pump_Ka(self.ptm_Ka["Pump_in"], ptmx=self.Ka.ptmx['Comp_in'], pres_corr=pres_corr)}
                self.ptm_Ka |= {"Comp_Eng_in": self.ptm_Ka['Pump_out']}
                self.ptm_Ka |= {"Comp_Eng_out": self.Comp_Eng(self.ptm_Ka["Comp_Eng_in"], ptmx=self.Ka.ptmx['Comp_in'], P_Comp_Heat=self.Ka.Comp.P_Comp_Heat)}
                self.ptm_Ka |= {"Wtau_in": self.ptm_Ka['Comp_Eng_out']}
                self.ptm_Ka |= {'Wtau_out': self.Heat_Ex_Ka(self.ptm_Ka['Wtau_in'], ptmx=self.Ka.ptmx['Comp_in'], P_Ka=self.Ka.Comp.P_Comp_Heat + self.FZ.P_Inv_Heat)}
                self.ptm_Ka |= {'Inv_in': self.ptm_Ka['Wtau_out']}
                self.ptm_Ka |= {'Inv_out': self.Inv_Cool(self.ptm_Ka['Inv_in'], P_Inv_Heat=self.FZ.P_Inv_Heat)}
                self.ptm_Ka |= {"Pump_in": self.ptm_Ka['Wtau_out']}


