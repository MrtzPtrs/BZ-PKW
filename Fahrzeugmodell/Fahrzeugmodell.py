import numpy as np
import copy

from Outsourced.Gasberechnungen import Gas

class vehicle_modell():
    def __init__(self, Nat, para, Calib):
        self.Calib = Calib
        self.para = para
        self.Nat = Nat

        self.Gas = Gas(para=self.para, Nat=self.Nat)

        self.case_SoC = 2
        self.v_0 = 0
        self.v_1 = 0
        self.a = 0
        self.P_Inv_Heat = 0
    def F_L_calc(self, v):
        return 1 / 2 * self.Calib['Stirnfläche'] * self.Calib['c_W-Wert'] * self.Gas.rho_air_calc() * v ** 2
    def F_R_calc(self):
        return self.Calib['c_R-Wert'] * self.Calib['FZ_masse'] * self.Nat['earth_accelaration']
    def F_H_calc(self):
        return self.Calib['FZ_masse'] * self.Nat['earth_accelaration'] * self.para['Steigung'] / (100 ** 2 + self.para['Steigung'] ** 2) ** 0.5
    def F_M_calc(self, a):
        return self.Calib['FZ_masse'] * a
    def P_BoP_pre_AVL(self, P_BZ):
        return 1000 * (1.0281429716892687 * np.exp(0.018860253157894122 * P_BZ / 1000) - 1.0281429716892687) #aus AVL gefittet
    def P_BoP_pre_calc(self, P_BZ):
        return 1000 * (0.8776700397991233 * np.exp(0.02409166851389804 * P_BZ / 1000) - 0.8774665973887494) * (self.para['st_C'] / 1.5)**self.Calib['BoP_st_C_Korrektur']

    def __call__(self, t, t_0, t_1, SoC_0, P_max_BZ):
        First_Run = True
        self.P_BoP_pre = 1
        P_BoP_old = 10
        i = 0
        i_border = 5
        accuracy = 0.01

        while (self.P_BoP_pre < P_BoP_old * (1 - accuracy) or self.P_BoP_pre > P_BoP_old * (1 + accuracy)) and i <= i_border:
            self.Warn_zu_wenig_Leistung = False

            #Berechnung der Radleistung
            self.F_Fahrwid = self.F_L_calc(v=(self.v_0 + self.para['FZ_geschw'][t+1])/2) + self.F_R_calc() + self.F_H_calc() + self.F_M_calc(a=(self.para['FZ_geschw'][t+1] - self.v_0) / (t_1 - t_0))
            self.P_Rad = self.F_Fahrwid * (self.v_0 + self.para['FZ_geschw'][t+1])/2

            #Vorbestimmung der BoP_Leistungsaufnahme
            if First_Run == True:
                if self.P_Rad > 0:
                    P_EM_pre = min(self.P_Rad / self.Calib['Eff_E_M'] / self.Calib['Eff_mech'], self.Calib['P_max_E_M'])
                    P_HV_pre = min(P_EM_pre / self.Calib['Eff_E_M_Inv'] + self.P_BoP_pre_calc(P_EM_pre), P_max_BZ * self.Calib['Eff_BZ_Konv'] + self.Calib['P_max_Bat'] * self.Calib['Eff_Bat'])
                    P_BZ_pre = np.clip(P_HV_pre / self.Calib['Eff_BZ_Konv'],0, P_max_BZ)
                else:
                    P_BZ_pre = 0
                self.P_BoP_pre = max(self.Calib['P_BoP_min'], self.P_BoP_pre_calc(P_BZ_pre))

            if self.P_Rad > 0: # Antriebsmodus
                #SoC-Case-Bestimmung
                if self.case_SoC == 0:
                    if SoC_0 <= self.Calib['SoC_min'] + self.Calib['SoC_Hysterese']:
                        self.case_SoC = 0
                    elif SoC_0 > self.Calib['SoC_min'] + self.Calib['SoC_Hysterese']:
                        self.case_SoC = 1
                elif self.case_SoC == 1:
                    if SoC_0 <= self.Calib['SoC_min'] - self.Calib['SoC_Hysterese']:
                        self.case_SoC = 0
                    elif SoC_0 > self.Calib['SoC_min'] - self.Calib['SoC_Hysterese'] and SoC_0 < self.Calib['SoC_Soll_U'] + self.Calib['SoC_Hysterese']:
                        self.case_SoC = 1
                    elif SoC_0 >= self.Calib['SoC_Soll_U'] + self.Calib['SoC_Hysterese']:
                        self.case_SoC = 2
                elif self.case_SoC == 2:
                    if SoC_0 < self.Calib['SoC_Soll_U'] - self.Calib['SoC_Hysterese']:
                        self.case_SoC = 1
                    elif SoC_0 >= self.Calib['SoC_Soll_U'] - self.Calib['SoC_Hysterese'] and SoC_0 <= self.Calib['SoC_Soll_O'] + self.Calib['SoC_Hysterese']:
                        self.case_SoC = 2
                    elif SoC_0 > self.Calib['SoC_Soll_O'] + self.Calib['SoC_Hysterese']:
                        self.case_SoC = 3
                elif self.case_SoC == 3:
                    if SoC_0 > self.Calib['SoC_Soll_O'] - self.Calib['SoC_Hysterese']:
                        self.case_SoC = 3
                    elif SoC_0 <= self.Calib['SoC_Soll_O'] - self.Calib['SoC_Hysterese']:
                        self.case_SoC = 2

                #Sollleistungsberechnung
                self.P_mB = 0
                self.P_E_M_soll = min(self.P_Rad / self.Calib['Eff_E_M'] / self.Calib['Eff_mech'], 200000)
                self.P_HV_BUS_soll = self.P_E_M_soll / self.Calib['Eff_E_M_Inv'] + self.P_BoP_pre
                self.P_E_M = self.P_E_M_soll
                self.P_HV_BUS = self.P_HV_BUS_soll

                P_max_HV_BUS = min(self.Calib['P_max_E_M'] / self.Calib['Eff_E_M_Inv'] + self.P_BoP_pre, P_max_BZ * self.Calib['Eff_BZ_Konv'] + self.Calib['P_max_Bat'] * self.Calib['Eff_Bat'])
                if P_max_HV_BUS < self.P_HV_BUS:
                    self.Warn_zu_wenig_Leistung = True

                if self.case_SoC == 0:
                    P_Bat_loading = max(self.Calib['SoC_Konst_Antr'] * self.Calib['P_max_Bat'] * (SoC_0 - self.Calib['SoC_Soll']) / self.Calib['SoC_Soll'],
                                        self.Calib['P_max_Rekup_Bat'])  # negativ
                    self.P_BZ = np.clip((self.P_HV_BUS - P_Bat_loading) / self.Calib['Eff_BZ_Konv'], 0, P_max_BZ)
                    if self.P_BZ < (self.P_HV_BUS - P_Bat_loading) / self.Calib['Eff_BZ_Konv']:
                        self.P_Bat = min((self.P_HV_BUS - self.P_BZ * self.Calib['Eff_BZ_Konv']) / self.Calib['Eff_Bat'], 0)
                    else:
                        self.P_Bat = P_Bat_loading * self.Calib['Eff_Bat']

                    if self.P_BZ * self.Calib['Eff_BZ_Konv'] < self.P_HV_BUS:
                        self.Warn_zu_wenig_Leistung = True

                elif self.case_SoC == 1:
                    if self.P_E_M / self.Calib['Eff_E_M_Inv'] + self.P_BoP_pre_calc(P_max_BZ) < P_max_BZ * self.Calib['Eff_BZ_Konv']:
                        P_Bat_loading = max(self.Calib['SoC_Konst_Antr'] * self.Calib['P_max_Bat'] * (SoC_0 - self.Calib['SoC_Soll']) / self.Calib['SoC_Soll'],
                                            self.Calib['P_max_Rekup_Bat'])  # negativ
                        self.P_BZ = np.clip((self.P_HV_BUS / self.Calib['Eff_BZ_Konv'] - P_Bat_loading) / self.Calib['Eff_BZ_Konv'], 0, P_max_BZ)

                        if self.P_BZ < (self.P_HV_BUS - P_Bat_loading) / self.Calib['Eff_BZ_Konv']:
                            self.P_Bat = (self.P_HV_BUS - self.P_BZ * self.Calib['Eff_BZ_Konv']) / self.Calib['Eff_Bat']
                        else:
                            self.P_Bat = P_Bat_loading / self.Calib['Eff_Bat']
                    else:
                        self.P_BZ = np.clip(self.P_HV_BUS / self.Calib['Eff_BZ_Konv'], 0, P_max_BZ)
                        if self.P_BZ < self.P_HV_BUS / self.Calib['Eff_BZ_Konv']:
                            self.P_Bat = (self.P_HV_BUS - self.P_BZ * self.Calib['Eff_BZ_Konv']) / self.Calib['Eff_Bat']
                        else:
                            self.P_Bat = (self.P_HV_BUS - self.P_BZ * self.Calib['Eff_BZ_Konv']) * self.Calib['Eff_Bat']
                        if self.P_Bat > self.Calib['P_max_Bat']:
                            self.Warn_zu_wenig_Leistung = True
                            self.P_Bat = self.Calib['P_max_Bat']

                elif self.case_SoC == 2:
                    self.P_BZ = np.clip(self.P_HV_BUS / self.Calib['Eff_BZ_Konv'], 0, P_max_BZ)
                    if self.P_BZ < self.P_HV_BUS / self.Calib['Eff_BZ_Konv']:
                        self.P_Bat = (self.P_HV_BUS - self.P_BZ * self.Calib['Eff_BZ_Konv']) / self.Calib['Eff_Bat']
                    else:
                        self.P_Bat = (self.P_HV_BUS - self.P_BZ * self.Calib['Eff_BZ_Konv']) * self.Calib['Eff_Bat']
                    if self.P_Bat > self.Calib['P_max_Bat']:
                        self.Warn_zu_wenig_Leistung = True
                        self.P_Bat = self.Calib['P_max_Bat']

                elif self.case_SoC == 3:
                    P_Bat_loading = min(self.Calib['SoC_Konst_Antr'] * self.Calib['P_max_Bat'] * (SoC_0 - self.Calib['SoC_Soll']) / self.Calib['SoC_Soll'], self.Calib['P_max_Bat']) #positiv
                    self.P_BZ = np.clip((self.P_HV_BUS - P_Bat_loading) / self.Calib['Eff_BZ_Konv'], 0, P_max_BZ)
                    self.P_Bat = (self.P_HV_BUS - self.P_BZ * self.Calib['Eff_BZ_Konv']) / self.Calib['Eff_Bat']

                    if self.P_Bat > self.Calib['P_max_Bat']:
                        self.P_BZ = np.clip((self.P_Bat - self.Calib['P_max_Bat']) * self.Calib['Eff_Bat'] / self.Calib['Eff_BZ_Konv'] + self.P_BZ, 0, P_max_BZ)
                        self.P_Bat = self.Calib['P_max_Bat']
                        if self.P_BZ == P_max_BZ:
                            self.Warn_zu_wenig_Leistung = True

                self.dE_Bat = self.P_Bat * (t_1 - t_0)

            elif self.P_Rad < 0:
                # Rekuperationsmodus
                self.P_BZ = 0
                self.P_mB = 0
                E_Bat_l = self.Calib['Kap_Bat'] * (SoC_0 - 1)

                self.P_E_M_soll = self.P_Rad / self.Calib['Eff_E_M'] / self.Calib['Eff_mech']
                self.P_HV_BUS_soll = self.P_E_M_soll / self.Calib['Eff_E_M_Inv'] + self.P_BoP_pre
                self.P_E_M = self.P_E_M_soll
                self.P_HV_BUS = self.P_HV_BUS_soll
                if self.P_E_M < self.Calib["P_max_Rekup_E_M"] / self.Calib['Eff_E_M']:  # Wird die Rekuperationsleistung des Motors überschritten?
                    self.P_E_M = self.Calib["P_max_Rekup_E_M"] / self.Calib['Eff_E_M']
                    self.P_HV_BUS = self.P_E_M * self.Calib['Eff_E_M_Inv'] + self.P_BoP_pre
                if self.P_HV_BUS < self.Calib['P_max_Rekup_Bat']:  # Wird die Rekuperationsleistung der Batterie überschritten?
                    self.P_HV_BUS = self.Calib['P_max_Rekup_Bat']
                    self.P_E_M = (self.P_HV_BUS - self.P_BoP_pre) / self.Calib['Eff_E_M_Inv']
                self.P_Bat = (self.P_HV_BUS - self.P_BZ * self.Calib['Eff_BZ_Konv']) * self.Calib['Eff_Bat']
                self.dE_Bat = self.P_Bat * (t_1 - t_0)
                if self.dE_Bat < E_Bat_l:
                    self.dE_Bat = E_Bat_l
                    self.P_Bat = self.dE_Bat / (t_1 - t_0)
                    self.P_HV_BUS = self.P_Bat / self.Calib['Eff_Bat'] + self.P_BZ * self.Calib['Eff_BZ_Konv']
                    self.P_E_M = (self.P_HV_BUS - self.P_BoP_pre) / self.Calib['Eff_E_M_Inv']
                self.P_mB = (self.P_E_M_soll - self.P_E_M) / (self.Calib['Eff_E_M'] * self.Calib['Eff_mech'])

            elif self.P_Rad == 0:
                E_Bat_l = self.Calib['Kap_Bat'] * (SoC_0 - 1)

                self.P_E_M_soll = 0
                self.P_HV_BUS_soll = self.P_BoP_pre
                self.P_E_M = self.P_E_M_soll
                self.P_HV_BUS = self.P_HV_BUS_soll
                self.P_BZ = 0
                self.P_HV_BUS = self.P_BZ * self.Calib['Eff_BZ_Konv'] + self.P_BoP_pre
                self.P_Bat = self.P_HV_BUS / self.Calib['Eff_Bat']
                self.dE_Bat = self.P_Bat * (t_1 - t_0)
                if self.dE_Bat < E_Bat_l:
                    self.dE_Bat = E_Bat_l
                    self.P_Bat = self.dE_Bat / (t_1 - t_0)
                    self.P_HV_BUS = self.P_Bat / self.Calib['Eff_Bat'] + self.P_BZ * self.Calib['Eff_BZ_Konv']
                    self.P_E_M = (self.P_HV_BUS - self.P_BoP_pre) / self.Calib['Eff_E_M_Inv']
                self.P_mB = (self.P_E_M_soll - self.P_E_M) / (self.Calib['Eff_E_M'] * self.Calib['Eff_mech'])

            P_BoP_old = self.P_BoP_pre
            self.P_BoP_pre = max(self.Calib['P_BoP_min'], self.P_BoP_pre_calc(self.P_BZ))
            First_Run = False
            i += 1

        if self.Warn_zu_wenig_Leistung == True:
            print('Die Leistung am Zeitpunkt', t_1, 'ist nicht erreichbar.')
            # tats. Radleistung und Geschwindigkeit nach dt
            self.P_HV_BUS = self.P_Bat * self.Calib['Eff_Bat'] + self.P_BZ * self.Calib['Eff_BZ_Konv']
            self.P_E_M = (self.P_HV_BUS - self.P_BoP_pre) * self.Calib['Eff_E_M_Inv']
            self.P_Rad = self.P_E_M * self.Calib['Eff_E_M'] * self.Calib['Eff_mech']

            i=0
            acc = 0.0001
            increment = 0.1
            VZ_old = 1
            VZ_new = 0
            F_R = True
            P = self.P_Rad
            self.v_1 = self.para['FZ_geschw'][t]
            while (F_R == True or (P >= self.P_Rad * (1 + acc) or P <= self.P_Rad * (1 - acc))) and i <= 50:
                F = self.F_L_calc(v=(self.v_0 + self.v_1) / 2) + self.F_R_calc() + self.F_H_calc() + self.F_M_calc(a=(self.v_1 - self.v_0) / (t_1 - t_0))
                P = F * (self.v_0 + self.v_1) / 2
                if P > self.P_Rad:
                    self.v_1 = self.v_1 * (1 - increment)
                    VZ_new = 1
                elif P < self.P_Rad:
                    self.v_1 = self.v_1 * (1 + increment)
                    VZ_old = 0
                if VZ_new != VZ_old and F_R == False:
                    increment = increment * 0.5
                F_R = False
                i += 1
            self.a = (self.v_1 - self.v_0) / (t_1 - t_0)
        else:
            self.v_1 = self.para['FZ_geschw'][t+1]
            try:
                self.a = (self.para['FZ_geschw'][t_1+1] - self.para['FZ_geschw'][t]) / 2*(t_1 - t_0)
            except:
                self.a = (self.para['FZ_geschw'][t+1] - self.para['FZ_geschw'][t]) / (t_1 - t_0)
        self.v_0 = self.v_1
        self.P_Inv_Heat = abs(self.P_HV_BUS - self.P_BoP_pre) * (1 - self.Calib['Eff_E_M_Inv'])

class SoC_calc():
    def __init__(self, Calib):
        self.Calib = Calib
    
    def __call__(self, t_0, t_1, SoC_0, P_Bat):
        self.dE_Bat = P_Bat * (t_1 - t_0)
        self.SoC_1 = np.clip((self.Calib['Kap_Bat'] * SoC_0 - self.dE_Bat) / self.Calib['Kap_Bat'], 0, 1)

class Inverter_Cooling():
    def __init__(self, para, Nat, Calib):
        self.para = para
        self.Nat = Nat
        self.Calib = Calib
        self.Gas = Gas(para=self.para, Nat=self.Nat)

    def __call__(self, ptm_in, P_Inv_Heat):
        ptm_out = copy.deepcopy(ptm_in)
        ptm_out['temp'] = ptm_in['temp'] + P_Inv_Heat / self.Gas.C_p_Liquid() / ptm_in['m_dot']
        self.V_dot_norm = ptm_out['V_dot'] / self.para['V_dot_max_Ku_C']
        self.dpres = 0.1335533960400235 * np.exp(1.5683931800002318 * ((self.V_dot_norm + 1) / 2)) - 0.1335533960400235
        ptm_out['pres'] = ptm_in['pres'] - self.dpres
        return ptm_out
