import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import os
from datetime import datetime

from Kathode.Kathode_main import Kathode
from Anode.Anode_main import Anode
from Kuehlung.Kuehlung_main import Kuehlung
from Fahrzeugmodell.Fahrzeugmodell import vehicle_modell
from Fahrzeugmodell.Fahrzeugmodell import SoC_calc
from Outsourced.Effizienzen import Eff
from Outsourced.Gasberechnungen import Gas
class main():
    def csv(self, SaveIt, Speichername, savefolder, Zeit, Soll_Geschwindigkeit, Ist_Geschwindigkeit, Soll_Beschleunigung, Ist_Beschleunigung,
                        Fahrzeug_Effizienz, BZ_System_Effizienz, BZ_Stapel_Effizienz,
                        Rad_Leistung, E_Motor_Soll_Leistung, E_Motor_Ist_Leistung, HV_Bus_Soll_Leistung, HV_Bus_Ist_Leistung,
                        BZ_Leistung, BoP_Leistungsaufnahme, Batterie_Leistung, mech_Bremsleistung,
                        Batterie_Ladestand, Zustand_Hybridsystemregelung,
                        BZ_Maximalleistung, Stapel_Strom, Stapel_Spannung, Zell_Spannung, ohmscheVerluste, Aktivierungsverluste, Konzentrationsverluste,
                        Kathoden_Massenstrom, Kathoden_Stapel_Massenstrom, Kompressor_Druckverhältnis, durchschn_BZ_Kathoden_Druck, durchschn_BZ_Kathodenkanal_Feuchte,
                        durchschn_BZ_Kathodenelektroden_Feuchte, BZ_Kathodenelektroden_Temperatur, BZ_Kathodenkanal_Temperatur,
                        Anoden_Massenstrom, H2_Injektor_Massenstrom, H2_Verbrauch, Rezirkulations_Druckverhältnis, durchschn_BZ_Anoden_Druck, durchschn_BZ_Anodenkanal_Feuchte,
                        durchschn_BZ_Anodenelektroden_Feuchte, BZ_Anoden_Temperatur,
                        H20_Stroffmengenstrom_durch_die_Membran, N2_Stroffmengenstrom_durch_die_Membran,
                        BZ_Stapel_Temperatur, Zustand_Temperaturregelung, therm_BZ_Leistung, Zwischenkühler_Wärmeübertrag, Wärmeübertrag_vom_Stapel_ins_Kühlmittel, HT_Massenstrom,
                        HT_Massenstrom_durch_den_Stapel, HT_Massenstrom_durch_den_Wärmetauscher, HT_Temperatur_niedrig, HT_Temperatur_hoch, HT_Druck,
                        Wechselrichter_Wärmeübertrag, Kompressor_Motor_Wärmebertrag, NT_Druck, NT_Temperatur_niedrig, NT_Temperatur_hoch):
        data = {
            'Zeit': Zeit,
            'Soll_Geschwindigkeit': Soll_Geschwindigkeit,
            'Ist_Geschwindigkeit': Ist_Geschwindigkeit,
            'Soll_Beschleunigung': Soll_Beschleunigung,
            'Ist_Beschleunigung': Ist_Beschleunigung,
            'Fahrzeug_Effizienz': Fahrzeug_Effizienz,
            'BZ_System_Effizienz': BZ_System_Effizienz,
            'BZ_Stapel_Effizienz': BZ_Stapel_Effizienz,
            'Rad_Leistung': Rad_Leistung,
            'E_Motor_Soll_Leistung': E_Motor_Soll_Leistung,
            'E_Motor_Ist_Leistung': E_Motor_Ist_Leistung,
            'HV_Bus_Soll_Leistung': HV_Bus_Soll_Leistung,
            'HV_Bus_Ist_Leistung': HV_Bus_Ist_Leistung,
            'BZ_Leistung': BZ_Leistung,
            'BoP_Leistungsaufnahme': BoP_Leistungsaufnahme,
            'Batterie_Leistung': Batterie_Leistung,
            'mech_Bremsleistung': mech_Bremsleistung,
            'Batterie_Ladestand': Batterie_Ladestand,
            'Zustand_Hybridsystemregelung': Zustand_Hybridsystemregelung,
            'BZ_Maximalleistung': BZ_Maximalleistung,
            'Stapel_Strom': Stapel_Strom,
            'Stapel_Spannung': Stapel_Spannung,
            'Zell_Spannung': Zell_Spannung,
            'ohmscheVerluste': ohmscheVerluste,
            'Aktivierungsverluste': Aktivierungsverluste,
            'Konzentrationsverluste': Konzentrationsverluste,
            'Kathoden_Massenstrom': Kathoden_Massenstrom,
            'Kathoden_Stapel_Massenstrom': Kathoden_Stapel_Massenstrom,
            'Kompressor_Druckverhältnis': Kompressor_Druckverhältnis,
            'durchschn_BZ_Kathoden_Druck': durchschn_BZ_Kathoden_Druck,
            'durchschn_BZ_Kathodenkanal_Feuchte': durchschn_BZ_Kathodenkanal_Feuchte,
            'durchschn_BZ_Kathodenelektroden_Feuchte': durchschn_BZ_Kathodenelektroden_Feuchte,
            'BZ_Kathodenelektroden_Temperatur': BZ_Kathodenelektroden_Temperatur,
            'BZ_Kathodenkanal_Temperatur': BZ_Kathodenkanal_Temperatur,
            'Anoden_Massenstrom': Anoden_Massenstrom,
            'H2_Injektor_Massenstrom': H2_Injektor_Massenstrom,
            'H2_Verbrauch': H2_Verbrauch,
            'Rezirkulations_Druckverhältnis': Rezirkulations_Druckverhältnis,
            'durchschn_BZ_Anoden_Druck': durchschn_BZ_Anoden_Druck,
            'durchschn_BZ_Anodenkanal_Feuchte': durchschn_BZ_Anodenkanal_Feuchte,
            'durchschn_BZ_Anodenelektroden_Feuchte': durchschn_BZ_Anodenelektroden_Feuchte,
            'BZ_Anoden_Temperatur': BZ_Anoden_Temperatur,
            'H20_Stroffmengenstrom_durch_die_Membran': H20_Stroffmengenstrom_durch_die_Membran,
            'N2_Stroffmengenstrom_durch_die_Membran': N2_Stroffmengenstrom_durch_die_Membran,
            'BZ_Stapel_Temperatur': BZ_Stapel_Temperatur,
            'Zustand_Temperaturregelung': Zustand_Temperaturregelung,
            'therm_BZ_Leistung': therm_BZ_Leistung,
            'Zwischenkühler_Wärmeübertrag': Zwischenkühler_Wärmeübertrag,
            'Wärmeübertrag_vom_Stapel_ins_Kühlmittel': Wärmeübertrag_vom_Stapel_ins_Kühlmittel,
            'HT_Massenstrom': HT_Massenstrom,
            'HT_Massenstrom_durch_den_Stapel': HT_Massenstrom_durch_den_Stapel,
            'HT_Massenstrom_durch_den_Wärmetauscher': HT_Massenstrom_durch_den_Wärmetauscher,
            'HT_Temperatur_niedrig': HT_Temperatur_niedrig,
            'HT_Temperatur_hoch': HT_Temperatur_hoch,
            'HT_Druck': HT_Druck,
            'Wechselrichter_Wärmeübertrag': Wechselrichter_Wärmeübertrag,
            'Kompressor_Motor_Wärmebertrag': Kompressor_Motor_Wärmebertrag,
            'NT_Druck': NT_Druck,
            'NT_Temperatur_niedrig': NT_Temperatur_niedrig,
            'NT_Temperatur_hoch': NT_Temperatur_hoch
        }
        df = pd.DataFrame(data)
        if SaveIt == True:
            os.makedirs(savefolder, exist_ok=True)
            df.to_csv(os.path.join(savefolder, 'csv_' + Speichername + '.csv'), index=False)
    def Plot_x_y(self, SaveIt, Speichername, x_indiv, y_indiv, y2_indiv, y3_indiv):
        axis = [x_indiv, y_indiv, y2_indiv, y3_indiv]
        for a in axis:
            if a in ['Zeit']:
                a_Einheit = 'Zeit [s]'
                a_label = 'Zeit'
                a_value = self.t
            elif a in ['Ist_Geschwindigkeit', 'Soll_Geschwindigkeit']:
                a_Einheit = 'Geschwindigkeit ['r'$\frac{m}{s}$]'
                if a == 'Ist_Geschwindigkeit':
                    a_label = 'Ist-Geschwindigkeit'
                    a_value = self.v_act
                elif a == 'Soll_Geschwindigkeit':
                    a_label = 'Soll-Geschwindigkeit'
                    a_value = list(self.parameter['FZ_geschw'])
            elif a in ['Ist_Beschleunigung', 'Soll_Beschleunigung']:
                a_Einheit = 'Beschleunigung ['r'$\frac{m}{s^{2}}$]'
                if a == 'Ist_Beschleunigung':
                    a_label = 'Ist-Beschleunigung'
                    a_value = self.a_act
                elif a == 'Soll_Beschleunigung':
                    a_label = 'Soll-Beschleunigung'
                    a_value = list(self.parameter['FZ_beschl'])
            elif a in ['BZ_Leistung', 'BoP_Leistungsaufnahme', 'Batterie_Leistung', 'mech._Bremsleistung', 'Rad_Leistung', 'E_Motor_Soll_Leistung', 'E_Motor_Ist_Leistung', 'HV_Bus_Soll_Leistung', 'HV_Bus_Ist_Leistung', 'BZ_Maximalleistung']:
                a_Einheit = 'Leistung [W]'
                if a == 'Rad_Leistung':
                    a_label = 'Radleistung'
                    a_value = self.P_Rad
                elif a == 'E_Motor_Soll_Leistung':
                    a_label = 'elek. E-Motor-Soll-Leistung'
                    a_value = self.P_E_M_soll
                elif a == 'E_Motor_Ist_Leistung':
                    a_label = 'elek. E-Motor-Ist_Leistung'
                    a_value = self.P_E_M
                elif a == 'BZ_Leistung':
                    a_label = 'BZ-Stapel-Leistung'
                    a_value = self.P_BZ
                elif a == 'BoP_Leistungsaufnahme':
                    a_label = 'BoP-Leistungsaufnahme'
                    a_value = self.P_BoP_act
                elif a == 'Batterie_Leistung':
                    a_label = 'Batterie-Leistung'
                    a_value = self.P_Bat
                elif a == 'mech._Bremsleistung':
                    a_label = 'mechanische Bremsleistung'
                    a_value = self.P_mB
                elif a == 'HV_Bus_Ist_Leistung':
                    a_label = 'HV-Bus-Ist-Leistung'
                    a_value = self.P_HV
                elif a == 'HV_Bus_Soll_Leistung':
                    a_label = 'HV-Bus-Soll-Leistung'
                    a_value = self.P_HV_soll
                elif a == 'BZ_Maximalleistung':
                    a_label = 'maximale BZ-Stapel-Leistung'
                    a_value = self.P_BZ_max
            elif a in ['Zustand_Hybridsystemregelung', 'Zustand_Temperaturregelung']:
                a_Einheit = 'Case [-]'
                if a == 'Zustand_Hybridsystemregelung':
                    a_label = 'SoC-Case'
                    a_value = self.SoC_Case
                elif a == 'Zustand_Temperaturregelung':
                    a_label = 'HT-Case'
                    a_value = self.case_HT
            elif a in ['Batterie_Ladestand']:
                a_Einheit = 'Ladestand [%]'
                a_label = 'Ladestand'
                a_value = self.SoC
            elif a in ['BZ_System_Effizienz', 'BZ_Stapel_Effizienz', 'Fahrzeug_Effizienz']:
                a_Einheit = 'Effizienz [%]'
                if a == 'BZ_Stapel_Effizienz':
                    a_label = 'Stapel-Effizienz'
                    a_value = self.Eff_BZ_Stack
                elif a == 'BZ_System_Effizienz':
                    a_label = 'BZ-System-Effizienz'
                    a_value = self.Eff_BZ_System
                elif a == 'Fahrzeug_Effizienz':
                    a_label = 'Fahrzeug-Effizienz'
                    a_value = self.Eff_Vehicle
            elif a in ['Kathoden_Massenstrom', 'Kathoden_Stapel_Massenstrom', 'Anoden_Massenstrom', 'HT_Massenstrom', 'HT_Massenstrom_durch_den_Stapel', 'HT_Massenstrom_durch_den_Wärmetauscher', 'NT_Massenstrom', 'H2_Injektor_Massenstrom']:
                a_Einheit = 'Massensstrom ['r'$\frac{g}{s}$]'
                if a == 'Kathoden_Massenstrom':
                    a_label = 'Kathoden-Massenstrom'
                    a_value = self.m_dot_C
                elif a == 'Kathoden_Stapel_Massenstrom':
                    a_label = 'Kathoden-Stapel-Massenstrom'
                    a_value = self.m_dot_C_BZ
                elif a == 'Anoden_Massenstrom':
                    a_label = 'Anoden-Stapel-Massenstrom'
                    a_value = self.m_dot_A_BZ_in
                elif a == 'HT_Massenstrom':
                    a_label = 'HT-Kühlmittelmassenstrom'
                    a_value = self.m_dot_Co_HT
                elif a == 'HT_Massenstrom_durch_den_Stapel':
                    a_label = 'Stapel-HT-Kühlmittelmassenstrom'
                    a_value = self.m_dot_Co_HT_BZ
                elif a == 'HT_Massenstrom_durch_den_Wärmetauscher':
                    a_label = 'Wärmetauscher-HT-Kühlmittelmassenstrom'
                    a_value = self.m_dot_Co_HT_WTau
                elif a == 'NT_Massenstrom':
                    a_label = 'NT-Kühlmittelmassenstrom'
                    a_value = self.m_dot_NT
                elif a == 'H2_Injektor_Massenstrom':
                    a_label = 'Wasserstoff-Einlassmassenstrom'
                    a_value = self.m_dot_H2_current
            elif a in ['H2_Verbrauch']:
                a_Einheit = 'Wasserstoffverbrauch [g]'
                a_label = 'Wasserstoffverbrauch'
                a_value = self.m_H2_total
            elif a in ['Kompressor_Druckverhältnis', 'Rezirkulations_Druckverhältnis']:
                a_Einheit = 'Druckverhältnis [-]'
                if a == 'Kompressor_Druckverhältnis':
                    a_label = 'Kompressordruckverhältnis'
                    a_value = self.p_rat_C_Comp
                elif a == 'Rezirkulations_Druckverhältnis':
                    a_label = 'Rezirkulationsdruckverhältnis'
                    a_value = self.p_rat_A_Rezi
            elif a in ['Kathoden_Druck_am_BZ_Eintritt', 'Kathoden_Druck_am_BZ_Austritt', 'Anoden_Druck_am_BZ_Eintritt', 'Anoden_Druck_am_BZ_Austritt', 'HT_Druck', 'NT_Druck']:
                a_Einheit = 'Druck [bara]'
                if a == 'Kathoden_Druck_am_BZ_Eintritt':
                    a_label = 'Kathodendruck am Stapeleintritt'
                    a_value = self.p_C_BZ_in
                elif a == 'Kathoden_Druck_am_BZ_Austritt':
                    a_label = 'Kathodendruck am Stapelaustritt'
                    a_value = self.p_C_BZ_out
                elif a == 'Anoden_Druck_am_BZ_Eintritt':
                    a_label = 'Anodendruck am Stapeleintritt'
                    a_value = self.p_A_BZ_in
                elif a == 'Anoden_Druck_am_BZ_Austritt':
                    a_label = 'Anodendruck am Stapelaustritt'
                    a_value = self.p_A_BZ_out
                elif a == 'HT_Druck':
                    a_label = 'Druck des HT-Kühlmittels'
                    a_value = self.p_Co_HT_Pump_out
                elif a == 'NT_Druck':
                    a_label = 'Druck des NT-Kühlmittels'
                    a_value = self.p_Pump_NT
            elif a in ['BZ_Stapel_Temperatur', 'BZ_Kathodenelektroden_Temperatur', 'BZ_Kathodenkanal_Temperatur', 'HT_Temperatur_hoch', 'HT_Temperatur_niedrig', 'BZ_Anodenkanal_Temperatur', 'NT_Temperatur_niedrig', 'NT_Temperatur_hoch']:
                a_Einheit = 'Temperatur [K]'
                if a == 'BZ_Stapel_Temperatur':
                    a_label = 'Stapel-Temperatur'
                    a_value = self.Temp_BZ
                elif a == 'BZ_Kathodenelektroden_Temperatur':
                    a_label = 'Temperatur der Kathodenelektrode'
                    a_value = self.Temp_KE
                elif a == 'BZ_Kathodenkanal_Temperatur':
                    a_label = 'Temperatur im Kathodenkanal'
                    a_value = self.Temp_KK
                elif a == 'HT_Temperatur_hoch':
                    a_label = 'Temperatur vor dem HT-Wärmetauscher'
                    a_value = self.Temp_Co_HT_WTau_in
                elif a == 'HT_Temperatur_niedrig':
                    a_label = 'Temperatur nach dem HT-Wärmetauscher'
                    a_value = self.Temp_Co_HT_WTau_out
                elif a == 'BZ_Anodenkanal_Temperatur':
                    a_label = 'Temperatur im Anodenkanal'
                    a_value = self.Temp_A_BZ
                elif a == 'NT_Temperatur_hoch':
                    a_label = 'Temperatur vor dem NT-Wärmetauscher'
                    a_value = self.Temp_Co_NT_WTau_out
                elif a == 'NT_Temperatur_niedrig':
                    a_label = 'Temperatur nach dem NT-Wärmetauscher'
                    a_value = self.Temp_Co_NT_WTau_out
            elif a in ['Kathoden_Feuchte_am_BZ_Austritt', 'Kathoden_Feuchte_am_BZ_Eintritt', 'durchschn_BZ_Kathodenkanal_Feuchte', 'durchschn_BZ_Kathodenelektroden_Feuchte', 'durchschn_BZ_Anodenkanal_Feuchte', 'durchschn_BZ_Anodenelektroden_Feuchte']:
                a_Einheit = 'relative Feuchte [-]'
                if a == 'Kathoden_Feuchte_am_BZ_Eintritt':
                    a_label = 'Kathodenfeuchte am Stapeleintritt'
                    a_value = self.rH_C_BZ_in
                elif a == 'Kathoden_Feuchte_am_BZ_Austritt':
                    a_label = 'Kathodenfeuchte am Stapelaustritt'
                    a_value = self.rH_C_BZ_out
                elif a == 'durchschn_BZ_Kathodenkanal_Feuchte':
                    a_label = 'durchschn. Feuchte im Kathodenkanal'
                    a_value = self.rH_KK
                elif a == 'durchschn_BZ_Kathodenelektroden_Feuchte':
                    a_label = 'durchschn. Feuchte in der Kathodenelektrode'
                    a_value = self.rH_KE
                elif a == 'durchschn_BZ_Anodenelektroden_Feuchte':
                    a_label = 'durchschn. Feuchte in der Anodenelektrode'
                    a_value = self.rH_AE
                elif a == 'durchschn_BZ_Anodenkanal_Feuchte':
                    a_label = 'durchschn. Feuchte im Andoenkanal'
                    a_value = self.rH_AK
            elif a in ['therm_BZ_Leistung']:
                a_Einheit = 'thermische Leistung [W]'
                a_label = 'thermische Stapel-Leistung'
                a_value = self.P_BZ_Heat
            elif a in ['Wärmeübertrag_vom_Stapel_ins_Kühlmittel', 'Zwischenkühler_Wärmeübertrag', 'Kompressor_Motor_Wärmeübertrag', 'Wechselrichter_Wärmeübertrag']:
                a_Einheit = 'Wärmestrom [W]'
                if a == 'Wärmeübertrag_vom_Stapel_ins_Kühlmittel':
                    a_label = 'Wärmeübertrag ins Kühlmittel im Stapel'
                    a_value = self.P_BZ_Cool
                elif a == 'Zwischenkühler_Wärmeübertrag':
                    a_label = 'Wärmestrom im Zwischenkühler'
                    a_value = self.P_ZwK_Heat
                elif a == 'Kompressor_Motor_Wärmeübertrag':
                    a_label = 'Wärmestrom im Kompressormotor'
                    a_value = self.P_Comp_Heat
                elif a == 'Wechselrichter_Wärmeübertrag':
                    a_label = 'Wärmestrom im Wechselrichter'
                    a_value = self.P_Inv_Heat
            elif a in ['H20_Stroffmengenstrom_durch_die_Membran', 'N2_Stroffmengenstrom_durch_die_Membran']:
                a_Einheit = 'Stoffmengenstrom ['r'$\frac{mol}{s}$]'
                if a == 'H20_Stroffmengenstrom_durch_die_Membran':
                    a_label = 'Wasserübertrag durch die Membran (Ka zu An)'
                    a_value = self.n_dot_H2O_cross
                if a == 'N2_Stroffmengenstrom_durch_die_Membran':
                    a_label = 'Stickstoffübertrag durch die Membran (Ka zu An)'
                    a_value = self.n_dot_N2_cross
            elif a in ['Stapel_Strom']:
                a_Einheit = 'Strom [A]'
                a_label = 'Stapelstrom'
                a_value = self.I_BZ
            elif a in ['Stapel_Spannung', 'Zell_Spannung', 'ohmsche Verluste', 'Aktivierungsverluste', 'Konzentrationsverluste']:
                a_Einheit = 'Spannung [V]'
                if a == 'Stapel_Spannung':
                    a_label = 'Stapelspannung'
                    a_value = self.U_BZ
                elif a == 'Aktivierungsverluste':
                    a_label = 'Aktivierungsverluste'
                    a_value = self.U_act
                elif a == 'ohmsche Verluste':
                    a_label = 'ohmsche Verluste'
                    a_value = self.U_ohm
                elif a == 'Konzentrationsverluste':
                    a_label = 'Konzentrationsverluste'
                    a_value = self.U_conc
                elif a == 'Zell_Spannung':
                    a_label = 'Zellspannung'
                    a_value = self.U_Zelle

            if a == x_indiv:
                x_Einheit = a_Einheit
                x_value = a_value
            elif a == y_indiv:
                y_Einheit = a_Einheit
                y_label = a_label
                y_value = a_value
            elif a == y2_indiv:
                try:
                    y2_Einheit = a_Einheit
                    y2_label = a_label
                    y2_value = a_value
                except:
                    None
            elif a == y3_indiv:
                try:
                    y3_Einheit = a_Einheit
                    y3_label = a_label
                    y3_value = a_value
                except:
                    None
        savefolder = 'D:/Projekte/Mirai/' + str(datetime.now().date())
        fig_size_x, fig_size_y = 20, 8
        fs_Title = 20
        fs_Lable = 14
        fig, ax1 = plt.subplots(figsize=(fig_size_x, fig_size_y))
        plt.title("variabler Plot während des " + Speichername + "-Lastprofils", fontsize=fs_Title)
        ax1.grid()
        ax1.set_xlabel(x_Einheit, fontsize=fs_Lable)

        ax1.set_ylabel(y_Einheit, fontsize=fs_Lable)
        lines =[]
        if x_indiv != 'Zeit':
            line1 = ax1.scatter(x_value, y_value, color='black', label=y_label)
        else:
            line1, = ax1.plot(x_value, y_value, color='black', label=y_label)
        lines += line1,

        if isinstance(y2_indiv, str):
            ax2 = ax1.twinx()
            ax2.set_ylabel(y2_Einheit, fontsize=fs_Lable)
            if x_indiv != 'Zeit':
                line2 = ax2.scatter(x_value, y2_value, color='blue', label=y2_label)
            else:
                line2, = ax2.plot(x_value, y2_value, color='blue', label=y2_label)
            lines += line2,

        if isinstance(y3_indiv, str):
            ax3 = ax1.twinx()
            ax3.set_ylabel(y3_Einheit, fontsize=fs_Lable)
            ax3.spines['right'].set_position(('outward', 50))
            if x_indiv != 'Zeit':
                line3 = ax3.scatter(x_value, y3_value, color='red', label=y3_label)
            else:
                line3, = ax3.plot(x_value, y3_value, color='red', label=y3_label)
            lines += line3,

        labels = [line.get_label() for line in lines]
        ax1.legend(lines, labels, loc=2)

        if SaveIt == True:
            os.makedirs(savefolder, exist_ok=True)
            plt.savefig(os.path.join(savefolder, 'variabler_Plot_' + Speichername + '_Lastprofil' + '.PNG'))
    def Plot_Leistungsverteilung(self, savefolder, SaveIt, Speichername, t, P_Rad, P_E_M, P_E_M_Soll, P_mB, P_Bat, P_BZ, P_BoP_act):
        fig_size_x, fig_size_y = 20, 8
        fs_Lable = 14
        fs_Title = 20
        fig, ax1 = plt.subplots(figsize=(fig_size_x, fig_size_y))
        plt.title("Lastverteilung während des " + Speichername + "-Lastprofils", fontsize=fs_Title)

        ax1.set_ylim(-300000, 300000)
        ax1.grid()

        ax1.set_xlabel('Zeit / s', fontsize=fs_Lable)
        ax1.set_ylabel('Leistung / W', fontsize=fs_Lable)

        ax1.plot(t, P_Rad, color='red', label='Rad-Leistung')
        ax1.plot(t, P_E_M, color='black', label='elek. E-M-Leistung')
        ax1.plot(t, P_E_M_Soll, color='black', linestyle='--', label='elek. Soll-E-M-Leistung')
        ax1.plot(t, P_BZ, color='blue', label='BZ-Leistung')
        ax1.plot(t, P_Bat, color='green', label='Bat-Leistung')
        ax1.plot(t, P_mB, color='darkgray', label='mechBremse-Leistung')
        ax1.plot(t, P_BoP_act, color='purple', label='tats. BoP-Leistung')

        ax1.legend(loc=2)
        if SaveIt == True:
            os.makedirs(savefolder, exist_ok=True)
            plt.savefig(os.path.join(savefolder, 'Leistungsverteilung_' + Speichername + '_Lastprofil' + '.PNG'))
            # Data = np.transpose(np.array([P_HV, P_HV_Soll, P_E_M, P_BZ, P_Bat, P_mB, P_BoP, SoC]))
            # dataF = pd.DataFrame(Data[0:], columns=["P_HV", "P_HV_soll", "P_E_M", "P_BZ", "P_Bat", "P_mB", "P_BoP", "SoC"])
            # dataF.to_csv(savefolder + '/Leistungsverteilung_' + Speichername + '_Lastprofil.csv')
    def Plot_Fahrzeug(self, savefolder, SaveIt, Speichername, t, P_E_M_Soll, P_E_M, v, v_Soll, a, a_Soll):
        fig_size_x, fig_size_y = 20, 8
        fs_Title = 20
        fs_Lable = 14
        fig, ax1 = plt.subplots(figsize=(fig_size_x, fig_size_y))
        ax2 = ax1.twinx()
        ax3 = ax1.twinx()

        ax1.set_ylim(0-5, 200)
        ax2.set_ylim(-10-0.4, 6)
        ax3.set_ylim(-300000-15000, 300000)
        ax1.set_yticks([0,25,50,75,100,125,150,175,200])
        ax2.set_yticks([-10,-8,-6,-4,-2,0,2,4])
        ax3.set_yticks([-300000,-225000,-150000,-75000,0,75000,150000,225000,300000])
        ax1.grid()
        plt.title("Geschwindigkeitsprofil während des " + Speichername + "-Lastprofils", fontsize=fs_Title)

        ax1.set_xlabel('Zeit [s]', fontsize=fs_Lable)
        ax1.set_ylabel('Geschwindigkeit / 'r'$\frac{m}{s}$', fontsize=fs_Lable)
        ax2.set_ylabel('Beschleunigung / 'r'$\frac{m}{s^{2}}$', fontsize=fs_Lable)
        ax2.spines['right'].set_position(('outward', -50))
        ax3.set_ylabel('Leistung / W', fontsize=fs_Lable)

        line1,=ax1.plot(t, v_Soll, color='black', label='Soll-Geschwindigkeit')
        line2,=ax1.plot(t, v, color='black', linestyle='--', label='Ist-Geschwindigkeit')
        line3,=ax2.plot(t, a_Soll, color='red', label='Soll-Beschleunigung')
        line4,=ax2.plot(t, a, color='red', linestyle='--', label='Ist-Beschleunigung')
        line5,=ax3.plot(t, P_E_M, color='blue', label='Soll-Leistung')
        line6,=ax3.plot(t, P_E_M_Soll, color='blue', linestyle='--', label='Ist-Leistung')

        lines = [line1, line2, line3, line4, line5, line6]
        labels = [line.get_label() for line in lines]

        ax1.legend(lines, labels, loc=2)

        if SaveIt == True:
            os.makedirs(savefolder, exist_ok=True)
            plt.savefig(os.path.join(savefolder, 'Fahrzeug_' + Speichername + '_Lastprofil' + '.PNG'))
    def Plot_Batterie(self, savefolder, SaveIt, Speichername, t, SoC_Case, SoC, P_Bat):
        fig_size_x, fig_size_y = 20, 8
        fs_Lable = 14
        fs_Title = 20
        fig, ax1 = plt.subplots(figsize=(fig_size_x, fig_size_y))
        plt.title("Batteriedaten während des " + Speichername + "-Lastprofils", fontsize=fs_Title)
        ax2 = ax1.twinx()
        ax3 = ax1.twinx()

        ax1.set_ylim(-60000-10000,40000+10000)
        ax2.set_ylim(0-0.1,1+0.1)
        ax3.set_ylim(0-0.3,3+0.3)
        ax1.set_yticks([-60000,-40000,-20000,0,20000,40000])
        ax2.set_yticks([0.0,0.2,0.4,0.6,0.8,1.0])
        ax3.set_yticks([0,1,2,3])
        ax1.grid()

        ax1.set_xlabel('Zeit / s', fontsize=fs_Lable)
        ax1.set_ylabel('Leistung / W', fontsize=fs_Lable)
        ax2.set_ylabel('Ladestand / -', fontsize=fs_Lable)
        ax3.set_ylabel('Case / -', fontsize=fs_Lable)
        ax3.spines['right'].set_position(('outward', -50))

        line1, = ax1.plot(t, P_Bat, color='black', label='Bat-Leistung')
        line2, = ax2.plot(t, SoC, color='red', label='SoC-Stand')
        line3, = ax3.plot(t, SoC_Case, color='orange', label='SoC-Case')

        lines = [line1, line2, line3]
        labels = [line.get_label() for line in lines]

        ax1.legend(lines, labels, loc=2)
        if SaveIt == True:
            os.makedirs(savefolder, exist_ok=True)
            plt.savefig(os.path.join(savefolder, 'Batterie_' + Speichername + '_Lastprofil' + '.PNG'))
    def Plot_BZ_Polk_t(self, savefolder, SaveIt, Speichername, t, I_St, U_Zelle, U_ohm, U_conc, U_act):
        fig_size_x, fig_size_y = 20, 8
        fs_Title = 20
        fs_Lable = 14
        fig, ax1 = plt.subplots(figsize=(fig_size_x, fig_size_y))
        ax2 = ax1.twinx()

        ax1.set_ylim(0-30, 600+30)
        ax2.set_ylim(0-0.06, 1.2+0.06)
        ax1.set_yticks([0,100,200,300,400,500,600])
        ax2.set_yticks([0.0,0.2,0.4,0.6,0.8,1.0,1.2])
        ax1.grid()
        plt.title("Ströme und Spannungen des Stapels während des " + Speichername + "-Lastprofils", fontsize=fs_Title)

        ax1.set_xlabel('Zeit / s', fontsize=fs_Lable)
        ax1.set_ylabel('Strom / A', fontsize=fs_Lable)
        ax2.set_ylabel('Spannung / V', fontsize=fs_Lable)

        line1, = ax1.plot(t, I_St, color='green', label='Stack-Stromstärke')
        line2, = ax2.plot(t, U_Zelle, color='black', label='Zell-Spannung')
        line3, = ax2.plot(t, U_conc, color='blue', linestyle='--', label='Konzentrationsverluste')
        line4, = ax2.plot(t, U_act, color='red', linestyle='--', label='Aktivierungsverluste')
        line5, = ax2.plot(t, U_ohm, color='green', linestyle='--', label='ohmsche Verluste')

        lines = [line1, line2, line3, line4, line5]
        labels = [line.get_label() for line in lines]

        ax1.legend(lines, labels, loc=2)

        if SaveIt == True:
            os.makedirs(savefolder, exist_ok=True)
            plt.savefig(os.path.join(savefolder, 'Stapel_über_t_' + Speichername + '_Lastprofil' + '.PNG'))
    def Plot_BZ_Polk_I_St(self, savefolder, SaveIt, Speichername, I_St, U_Zelle, U_ohm, U_conc, U_act):
        fig_size_x, fig_size_y = 20, 8
        fs_Title = 20
        fs_Lable = 14
        fig, ax1 = plt.subplots(figsize=(fig_size_x, fig_size_y))

        ax1.set_ylim(0-0.1, 1.3)
        ax1.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2])
        ax1.grid()
        plt.title("Polkurve während des " + Speichername + "-Lastprofils", fontsize=fs_Title)

        ax1.set_xlabel('Strom / A', fontsize=fs_Lable)
        ax1.set_ylabel('Spannung / V', fontsize=fs_Lable)

        ax1.scatter(I_St, U_Zelle, color='black', label='Zell-Spannung')
        ax1.scatter(I_St, U_conc, color='blue', label='Konzentrationsverluste')
        ax1.scatter(I_St, U_act, color='red', label='Aktivierungsverluste')
        ax1.scatter(I_St, U_ohm, color='green', label='ohmsche Verluste')

        ax1.legend(loc=2)

        if SaveIt == True:
            os.makedirs(savefolder, exist_ok=True)
            plt.savefig(os.path.join(savefolder, 'Stapel_Polkurve_' + Speichername + '_Lastprofil' + '.PNG'))
    def Plot_BZ_Bedingungen(self, savefolder, SaveIt, Speichername, t, Temp_BZ, rH_KE, rH_AE, p_KK, p_AK):
        fig_size_x, fig_size_y = 20, 8
        fs_Title = 20
        fs_Lable = 14
        fig, ax1 = plt.subplots(figsize=(fig_size_x, fig_size_y))
        ax2 = ax1.twinx()
        ax3 = ax1.twinx()

        ax1.set_ylim(285-8, 365)
        ax2.set_ylim(0-0.16, 1.6)
        ax3.set_ylim(1-0.2, 3)
        ax1.set_yticks([285,295,305,315,325,335,345,355])
        ax2.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6])
        ax3.set_yticks([1.0, 1.25,1.5, 1.75, 2.0, 2.25, 2.5, 2.75,3.0])
        ax1.grid()
        plt.title("Stapelbedingungen während des " + Speichername + "-Lastprofils", fontsize=fs_Title)

        ax1.set_xlabel('Zeit / s', fontsize=fs_Lable)
        ax1.set_ylabel('Temperatur / K', fontsize=fs_Lable)
        ax2.set_ylabel('relative Feuchte / -', fontsize=fs_Lable)
        ax3.set_ylabel('Druck / bara', fontsize=fs_Lable)
        ax3.spines['right'].set_position(('outward', 50))

        line1, = ax1.plot(t, Temp_BZ, color='red', label='Stapeltemperatur')
        line2, = ax2.plot(t, rH_KE, color='blue', label='Elektrodenfeuchte (Kathode)')
        line3, = ax2.plot(t, rH_AE, color='lightblue', label='Elektrodenfeuchte (Anode)')
        line4, = ax3.plot(t, p_KK, color='green', label='Druck (Kathode)')
        line5, = ax3.plot(t, p_AK, color='lime', label='Druck (Anode)')

        lines = [line1, line2, line3, line4, line5]
        labels = [line.get_label() for line in lines]

        ax1.legend(lines, labels, loc=2)
        if SaveIt == True:
            os.makedirs(savefolder, exist_ok=True)
            plt.savefig(os.path.join(savefolder, 'Stapel_Bedingungen_' + Speichername + '_Lastprofil' + '.PNG'))
    def Plot_Kathode(self, savefolder, SaveIt, Speichername, t, m_dot_C, m_dot_C_BZ, p_rat_C_Comp, rH_KE, rH_KK, Temp_KK, Temp_KE):
        fig_size_x, fig_size_y = 20, 8
        fs_Title = 20
        fs_Lable = 14
        fig, ax1 = plt.subplots(figsize=(fig_size_x, fig_size_y))
        ax2 = ax1.twinx()
        ax3 = ax1.twinx()
        ax4 = ax1.twinx()

        ax1.set_ylim(0-16,160)
        ax2.set_ylim(1-0.2,3)
        ax3.set_ylim(285-8,365)
        ax4.set_ylim(0-0.2,2)
        ax1.set_yticks([0,20,40,60,80,100,120,140,160])
        ax2.set_yticks([1.0, 1.25,1.5, 1.75, 2.0, 2.25, 2.5, 2.75,3.0])
        ax3.set_yticks([285,295,305,315,325,335,345,355])
        ax4.set_yticks([0.0,0.25,0.5,0.75,1.0,1.25,1.5,1.75,2.0])
        ax1.grid()
        plt.title("Kathoden-Gaseigenschaften während des " + Speichername + "-Lastprofils", fontsize=fs_Title)

        ax1.set_xlabel('Zeit / s', fontsize=fs_Lable)
        ax1.set_ylabel('Massenstrom / 'r'$\frac{g}{s}$', fontsize=fs_Lable)
        ax2.set_ylabel('Druckverhältnis / 'r'$\frac{bara}{bara}$', fontsize=fs_Lable)
        ax2.spines['right'].set_position(('outward', 50))
        ax3.set_ylabel('Temperatur / K', fontsize=fs_Lable)
        ax3.spines['right'].set_position(('outward', -50))
        ax4.set_ylabel('relative Feuchte / -', fontsize=fs_Lable)

        line1, = ax1.plot(t, m_dot_C, color='black', label='Massenstrom (Kathode)')
        line2, = ax1.plot(t, m_dot_C_BZ, color='gray', label='Massenstrom (BZ_C)')
        line3, = ax2.plot(t, p_rat_C_Comp, color='green', label='Kompressordruckverhältnis')
        line4, = ax3.plot(t, Temp_KK, color='red', label='Durchschnittskanaltemperatur')
        line5, = ax3.plot(t, Temp_KE, color='firebrick', label='Elektrodentemperatur')
        line6, = ax4.plot(t, rH_KE, color='blue', label='rel. Feuchte (Elektrode)')
        line7, = ax4.plot(t, rH_KK, color='lightblue', label='rel. Feuchte (Kanal)')

        lines = [line1, line2, line3, line4, line5, line6, line7]
        labels = [line.get_label() for line in lines]

        ax1.legend(lines, labels, loc=2)

        if SaveIt == True:
            os.makedirs(savefolder, exist_ok=True)
            plt.savefig(os.path.join(savefolder, 'Gaseigenschaften_Kathode_' + Speichername + '_Lastprofil' + '.PNG'))
    def Plot_Anode(self, savefolder, SaveIt, Speichername, t, m_dot_A_BZ_in, p_rat_A_Rezi, rH_AE, rH_AK, m_dot_H2_current, m_dot_H2_Purge):
        fig_size_x, fig_size_y = 20, 8
        fs_Title = 20
        fs_Lable = 14
        fig, ax1 = plt.subplots(figsize=(fig_size_x, fig_size_y))
        ax2 = ax1.twinx()
        ax3 = ax1.twinx()

        ax1.set_ylim(0-5,50)
        ax2.set_ylim(1-0.05, 1.5)
        ax3.set_ylim(0-0.1,1)
        ax1.set_yticks([0,10,20,30,40,50])
        ax2.set_yticks([1.0,1.1,1.2,1.3,1.4,1.5])
        ax3.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8])
        ax1.grid()
        plt.title("Anoden-Gaseigenschaften während des " + Speichername + "-Lastprofils", fontsize=fs_Title)

        ax1.set_xlabel('Zeit / s', fontsize=fs_Lable)
        ax1.set_ylabel('Massenstrom / 'r'$\frac{g}{s}$', fontsize=fs_Lable)
        ax2.set_ylabel('Druckverhältnis / 'r'$\frac{bara}{bara}$', fontsize=fs_Lable)
        ax3.set_ylabel('relative Feuchte -', fontsize=fs_Lable)
        ax3.spines['right'].set_position(('outward', -50))

        line1, = ax1.plot(t, m_dot_A_BZ_in, color='black', label='Massenstrom am Stapeleintritt')
        line2, = ax1.plot(t, m_dot_H2_current, color='red', label='H2-Injektor-Massenstrom')
        line3, = ax1.plot(t, m_dot_H2_Purge, color='firebrick', label='abgeblasener H2-Massenstrom')
        line4, = ax2.plot(t, p_rat_A_Rezi, color='green', label='Rezi-Druckverhältnis')
        line5, = ax3.plot(t, rH_AE, color='blue', label='Wassertransport durch die Membran')
        line6, = ax3.plot(t, rH_AK, color='lightblue', label='Wassertransport durch die Membran')

        lines = [line1, line2, line3, line4, line5, line6]
        labels = [line.get_label() for line in lines]

        ax1.legend(lines, labels, loc=2)

        if SaveIt == True:
            os.makedirs(savefolder, exist_ok=True)
            plt.savefig(os.path.join(savefolder, 'Gaseigenschaften_Anode_' + Speichername + '_Lastprofil' + '.PNG'))
    def Plot_HT_Kreisl(self, savefolder, SaveIt, Speichername, t, Case_HT, Temp_BZ, P_ZwK_Heat, P_BZ_Heat, P_BZ_Cool, m_dot_HT, m_dot_HT_WTau, m_dot_HT_BZ):
        fig_size_x, fig_size_y = 20, 8
        fs_Title = 20
        fs_Lable = 14
        fig, ax1 = plt.subplots(figsize=(fig_size_x, fig_size_y))
        ax2 = ax1.twinx()
        ax3 = ax1.twinx()
        ax4 = ax1.twinx()

        ax1.set_ylim(0-150,1500)
        ax2.set_ylim(0-15000,150000)
        ax3.set_ylim(285-8, 365)
        ax4.set_ylim(0-0.3,3)
        ax1.set_yticks([0,150,300,450,600,750,900,1050,1200,1350,1500])
        ax2.set_yticks([0,15000,30000,45000,60000,75000,90000,105000,120000,135000,150000])
        ax3.set_yticks([265,275,285,295,305,315,325,335,345,355,365])
        ax4.set_yticks([1,2])
        ax1.grid()
        plt.title("Kühlmitteleigenschaften im HT-Kreislauf während des " + Speichername + "-Lastprofils", fontsize=fs_Title)

        ax1.set_xlabel('Zeit / s', fontsize=fs_Lable)
        ax1.set_ylabel('Massenstrom / 'r'$\frac{g}{s}$', fontsize=fs_Lable)
        ax2.set_ylabel('Wärmeleistung / P', fontsize=fs_Lable)
        ax2.spines['right'].set_position(('outward', 50))
        ax3.set_ylabel('Temperatur / K', fontsize=fs_Lable)
        ax3.spines['right'].set_position(('outward', -50))
        ax4.set_ylabel('Case', fontsize=fs_Lable)

        line1, = ax1.plot(t, m_dot_HT_WTau, color='lightgray', label='Massenstrom durch den WTau')
        line2, = ax1.plot(t, m_dot_HT, color='black', label='Massenstrom')
        line3, = ax1.plot(t, m_dot_HT_BZ, color='gray', label='Massenstrom durch den Stapel')
        line4, = ax2.plot(t, P_BZ_Heat, color='blue', label='Stack-Wärmeleistung')
        line5, = ax2.plot(t, P_ZwK_Heat, color='lightblue', label='Zwischenkühler-Wärmeleistung')
        line6, = ax2.plot(t, P_BZ_Cool, color='darkblue', label='tats. Kühlleistung')
        line7, = ax3.plot(t, Temp_BZ, color='red', label='Stapel-Temperatur')
        line8, = ax4.plot(t, Case_HT, color='red', linestyle='--', label='HT-Case')

        lines = [line1, line2, line3, line4, line5, line6, line7, line8]
        labels = [line.get_label() for line in lines]

        ax1.legend(lines, labels, loc=2)

        if SaveIt == True:
            os.makedirs(savefolder, exist_ok=True)
            plt.savefig(os.path.join(savefolder, 'Eigenschaften_HT_Kreislauf_' + Speichername + '_Lastprofil' + '.PNG'))
    def Plot_NT_Kreisl(self, savefolder, SaveIt, Speichername, t, P_Inv_Heat, P_Comp_Heat, p_NT, m_dot_NT):
        fig_size_x, fig_size_y = 20, 8
        fs_Title = 20
        fs_Lable = 14
        fig, ax1 = plt.subplots(figsize=(fig_size_x, fig_size_y))
        ax2 = ax1.twinx()
        ax3 = ax1.twinx()

        ax1.set_ylim(0-25,250)
        ax2.set_ylim(1-0.025,1.25)
        ax3.set_ylim(0-1000, 10000)
        ax1.set_yticks([0,25,50,75,100,125,150,175,200,225,250])
        ax2.set_yticks([1.0,1.05,1.1,1.15,1.2,1.25])
        ax3.set_yticks([0,2000,4000,6000,8000,10000])
        ax1.grid()
        plt.title("Kühlmitteleigenschaften im NT-Kreislauf während des " + Speichername + "-Lastprofils", fontsize=fs_Title)

        ax1.set_xlabel('Zeit / s', fontsize=fs_Lable)
        ax1.set_ylabel('Massenstrom / 'r'$\frac{g}{s}$', fontsize=fs_Lable)
        ax2.set_ylabel('Druck / bara', fontsize=fs_Lable)
        ax3.set_ylabel('Wärmeleistung / W', fontsize=fs_Lable)
        ax3.spines['right'].set_position(('outward', 50))

        line1, = ax1.plot(t, m_dot_NT, color='black', label='Kühlmittelfluss')
        line2, = ax2.plot(t, p_NT, color='green', label='Ausgangsdruck nach der Pumpe')
        line3, = ax3.plot(t, P_Inv_Heat, color='firebrick', label='Wechselrichter-Wärmestrom')
        line4, = ax3.plot(t, P_Comp_Heat, color='red', label='Kompressormotor-Wärmestrom')

        lines = [line1, line2, line3, line4]
        labels = [line.get_label() for line in lines]

        ax1.legend(lines, labels, loc=2)

        if SaveIt == True:
            os.makedirs(savefolder, exist_ok=True)
            plt.savefig(os.path.join(savefolder, 'Eigenschaften_NT-Kreislauf_' + Speichername + '_Lastprofil' + '.PNG'))
    def Plot_Effizienzen(self, savefolder, SaveIt, Speichername, t, Eff_BZ_Sys, Eff_BZ, Eff_Veh, SoC, m_H2):
        fig_size_x, fig_size_y = 20, 8
        fs_Lable = 14
        fs_Title = 20
        fig, ax1 = plt.subplots(figsize=(fig_size_x, fig_size_y))
        plt.title("Effizenzen während des " + Speichername + "-Lastprofils", fontsize=fs_Title)
        ax2 = ax1.twinx()
        ax3 = ax1.twinx()

        ax1.set_ylim(0-0.1, 1+0.1)
        ax2.set_ylim(0-0.1, 1+0.1)
        ax3.set_ylim(0-150, 1500+150)
        ax1.set_yticks([0.0,0.2,0.4,0.6,0.8,1.0])
        ax2.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax3.set_yticks([0,300,600,900,1200,1500])
        ax1.grid()

        ax1.set_xlabel('Zeit / s', fontsize=fs_Lable)
        ax1.set_ylabel('Effizienz / -', fontsize=fs_Lable)
        ax2.set_ylabel('Ladestand / -', fontsize=fs_Lable)
        ax3.set_ylabel('Masse / g', fontsize=fs_Lable)
        ax3.spines['right'].set_position(('outward', -50))

        line1, = ax1.plot(t, Eff_BZ_Sys, color='blue', label='BZ-System-Effizienz')
        line2, = ax1.plot(t, Eff_BZ, color='lightblue', label='Stapel-Effizienz')
        line3, = ax1.plot(t, Eff_Veh, color='black', label='Fahrzeug-Effizienz')
        line4, = ax2.plot(t, SoC, color='yellow', label='SoC-Stand')
        line5, = ax3.plot(t, m_H2, color='red', label='H2-Verbauch')

        lines = [line1, line2, line3, line4, line5]
        labels = [line.get_label() for line in lines]

        ax1.legend(lines, labels, loc=2)
        if SaveIt == True:
            os.makedirs(savefolder, exist_ok=True)
            plt.savefig(os.path.join(savefolder, 'Effizenzen_' + Speichername + '_Lastprofil' + '.PNG'))
    def Plot_BoP(self, savefolder, SaveIt, Speichername, t, P_BoP, P_Comp, P_Rezi, P_Pump_NT, P_Pump_HT):
        fig_size_x, fig_size_y = 20, 8
        fs_Lable = 14
        fs_Title = 20
        fig, ax1 = plt.subplots(figsize=(fig_size_x, fig_size_y))
        plt.title("BoP-Leistungsverteilung während des " + Speichername + "-Lastprofils", fontsize=fs_Title)

        ax1.set_ylim(0-2000, 20000)
        ax1.grid()

        ax1.set_xlabel('Zeit / s', fontsize=fs_Lable)
        ax1.set_ylabel('Leistungsaufnahme / W', fontsize=fs_Lable)

        line1, = ax1.plot(t, P_BoP, color='black', label='BoP-Leistung')
        line2, = ax1.plot(t, P_Comp, color='blue', label='Kompressor-Leistung')
        line3, = ax1.plot(t, P_Rezi, color='green', label='Rezi-Leistung')
        line4, = ax1.plot(t, P_Pump_NT, color='red', label='NT-Pumpe-Leistung')
        line5, = ax1.plot(t, P_Pump_HT, color='firebrick', label='HT-Pumpe-Leistung')

        lines = [line1, line2, line3, line4, line5]
        labels = [line.get_label() for line in lines]

        ax1.legend(lines, labels, loc=2)
        if SaveIt == True:
            os.makedirs(savefolder, exist_ok=True)
            plt.savefig(os.path.join(savefolder, 'BoP_Leistungsverteilung_' + Speichername + '_Lastprofil' + '.PNG'))

    def __init__(self, Lastprofil = 'WLTC', Umgebung = 'standard', Steigung = '0%', Zuladung= '100kg', SoC = '55%', st_C='1.5', presrat_Komp='2.0', Temp_ZwK='60°C', t_Komp_Dynamik= "1.5s", opres_A='0.4bar', st_A='2.0', mean_H2='85% vol', dtemp_C_Co="15K", dtemp_FC='15K', x_glyk='30% vol', Temp_BZ_Init='kalt'):
        self.Naturkonstanten = {
            "Faraday": 96485.3399, "Avogadro": 6.02214E+23, "Boltzmann": 1.38064852E-23,
            "mx_O2": 0.2314, "mx_N2": 0.7686, "mx_H2": 0,
            "el_H2": 2, "el_O2": 4, "EN_H": 2.2, "EN_O": 3.37, #"EN_O":3.43
            "M_H2": 1.00784 * 2, "M_O2": 15.999 * 2, "M_H2O": 18.01528, "M_N2": 28.0134,
            "Hi_H2": 119972,
            "f_O2": 5, "f_N2": 5, "f_H2": 5, "f_H2O": 3,#Freiheitsgrade
            "c_p_H2": 14.3, "c_p_H2O": 4.19, "c_p_Glykol": 2.5,
            "rho_H2O": 0.997, "rho_Glykol": 1.11,
            "NormVol": 22.414, "NormTemp": 273.15, "NormPres": 1.01325,
            "eps": 1E-15, # Wert wird als == 0 angenommen

            "rho_air_0": 1.225, "pres_air_0": 1.01325,
            "earth_accelaration": 9.81,
        }
        self.Eingabe = {
            #Umgebung
            "Umgebung": {"standard": {"temp_U": 293.15, "humidity_U": 0.7, 'height': 0},
                            "heiß": {"temp_U": 313.15, "humidity_U": 0.6, 'height': 0},
                            "kalt": {"temp_U": 253.15, "humidity_U": 0.8, 'height': 0},
                            "Höhe": {"temp_U": 293.15, "humidity_U": 0.7, 'height': 2000},
                            "trocken": {"temp_U": 293.15, "humidity_U": 0, 'height': 0},
                            },
            "Steigung": {"20%": 20, "15%": 15, "10%": 10, "5%": 5, "0%": 0, "-5%": -5, "-10%": -10, "-15%": -15, "-20%": -2},

            #Fahrzeug
            "Zuladung": {"0kg": 0, "50kg": 50, "100kg": 100, "200kg": 200, "500kg": 500},
            #Batterie
            "SoC": {"0%": 0, "20%": 0.2, "40%": 0.4, "50%": 0.5, "55%": 0.55, "60%": 0.6, "80%": 0.8, "100%": 1},

            #BZ-System
            #Kathode
            "st_C": {"1.4": 1.4, "1.5": 1.5, "1.6": 1.6, "1.8": 1.8, "2.0": 2, "2.2": 2.2, "2.4": 2.4, "2.6": 2.6, "2.8": 2.8},
            "presrat_Komp": {"1.25": 1.25, "1.5": 1.5, "1.75": 1.75, "2.0": 2, "2.25": 2.25, "2.5": 2.5},
            "Temp_ZwK": {"50°C": 323.15, "60°C": 333.15, "70°C": 343.15, "80°C": 353.15},
            #Anode
            "st_A": {"1.2": 1.2, "1.5": 1.5, "1.8": 1.8, "2.0": 2, "2.5": 2.5, "3.0": 3, "4.0": 4, "5.0": 5},
            "opres_A": {"0.1bar": 0.1, "0.2bar": 0.2, "0.3bar": 0.3, "0.4bar": 0.4, "0.5bar": 0.5},
            "mean_H2": {"75% vol": 0.75, "85% vol": 0.85, "95% vol": 0.95},
            #Kühlung
            "dtemp_C_Co": {"5K": 5, "10K": 10, "15K": 15, "20K": 20, "25K": 25},
            "dtemp_FC": {"5K": 5, "10K": 10, "15K": 15, "20K": 20, "25K": 25},
            "x_glyk": {"0% vol": 0.0, "10% vol": 0.1, "20% vol": 0.2, "30% vol": 0.3, "40% vol": 0.4, "50% vol": 0.5},
            "Temp_BZ_Init": {"kalt": 273.15+50, "Soll": 273.15+65, "heiß": 273.15+80},
            #Dynamik
            "t_Komp_Dynamik": {"0.5s": 0.5, "1s": 1, "1.5s": 1.5, "3s": 3, "5s": 5, "10s": 10, "20s": 20},
        }
        Data = pd.read_excel("Lastprofile/" + Lastprofil + ".xlsx", usecols=['time in s', 'speed in m/s', 'a in m/s^2'])
        self.Lastprofil=Lastprofil
        self.parameter = {
            #Fahrprofil
            "Time": np.array(Data['time in s']),
            "FZ_geschw": np.array(Data['speed in m/s']),
            "FZ_beschl": np.array(Data['a in m/s^2']),

            # Umgebung
            "Steigung": self.Eingabe['Steigung'][Steigung],
            "height": self.Eingabe['Umgebung'][Umgebung]['height'],
            "temp_env": self.Eingabe['Umgebung'][Umgebung]['temp_U'],
            "rH_env": self.Eingabe['Umgebung'][Umgebung]['humidity_U'],

            # Batterie
            "SoC": self.Eingabe['SoC'][SoC],

            #BZ-System
            #Kathode
            "st_C": self.Eingabe['st_C'][st_C],
            "presrat_comp": self.Eingabe['presrat_Komp'][presrat_Komp],
            "temp_interc": self.Eingabe['Temp_ZwK'][Temp_ZwK],

            #Anode
            "temp_TV": 303.15,
            "opres_A": self.Eingabe['opres_A'][opres_A],
            "st_A": self.Eingabe['st_A'][st_A],
            "mean_H2": self.Eingabe['mean_H2'][mean_H2],

            #Kühlung
            "dtemp_FC": self.Eingabe['dtemp_FC'][dtemp_FC],
            "temp_max_C_Co": self.Eingabe['Temp_ZwK'][Temp_ZwK] + self.Eingabe['dtemp_C_Co'][dtemp_C_Co],
            "w_glyk": self.Eingabe['x_glyk'][x_glyk] * self.Naturkonstanten['rho_Glykol'] / (self.Eingabe['x_glyk'][x_glyk] * self.Naturkonstanten['rho_Glykol'] + (1 - self.Eingabe['x_glyk'][x_glyk]) * self.Naturkonstanten['rho_H2O']),

            #Dynamik
            "t_Komp_Dynamik": self.Eingabe['t_Komp_Dynamik'][t_Komp_Dynamik],

            #Übergangslösungen
            "deltatemp_BZ_C": self.Eingabe['dtemp_FC'][dtemp_FC],
            "V_dot_max_C": 100,
            "m_dot_max_C": 115,
            "V_dot_max_A": 45,
            "m_dot_max_A": 30,
            "V_dot_max_Ku_C": 1.5,
            "m_dot_max_Ku_C": 1600,
            "V_dot_max_Ku_BZ": 5,
            "m_dot_max_Ku_BZ": 5000,
        }
        if Temp_BZ_Init == "Umgebung":
            self.parameter |= {"Temp_BZ_Init": self.Eingabe['Umgebung'][Umgebung]['temp_U']}
        else:
            self.parameter |= {"Temp_BZ_Init": self.Eingabe['Temp_BZ_Init'][Temp_BZ_Init]}
        self.Calib = {
            #Fahrzeug
            "FZ_masse": 1925 + self.Eingabe['Zuladung'][Zuladung], "Stirnfläche": 2.55, "c_W-Wert": 0.29, "c_R-Wert": 0.008,
            #Antriebsstrang
            "Eff_E_M": 1, "Eff_mech": 0.95,
            "Eff_E_M_Inv": 0.98,
            "P_max_E_M": 134000, "P_max_Rekup_E_M": -56800,
            #Batterie
            "Kap_Bat": 4464000,
            "P_max_Bat": 31500,
            "P_max_Rekup_Bat": -40000,
            "SoC_min": 0.22, "SoC_Soll_U": 0.53, "SoC_Soll": 0.545, "SoC_Soll_O": 0.56, "SoC_Konst_Antr": 20, "SoC_Hysterese": 0.02,
            "Eff_Bat": 0.95,
            #Brennstoffzelle
            "Eff_BZ_Konv": 1,"activeArea": 0.028, "NumCells": 330, "P_max_BZ": 130000, "I_max_BZ": 600,
            "P_BoP_min": 85.9 + 2.6 + 10,
            "Masse_BZ_therm": 22.77 * 1000,
            'BoP_st_C_Korrektur': 2.1,
            #Polkurve
            "i_cross": 0.18, "A": 0.105, "C_i0": 4.522385348226745, "C_m": 0.0035821310521886404, "C_n": 6111, "C_ohm": 10565, "C_Tempcorr": 2.3,
            #MEA
            "Membran_Thickness": 15E-6, "M_Membran_dry": 1.1, "rho_Membran_dry": 1.98E+6, "N2_Diff_Koeff": 2E-7, "H2O_Diff_Koeff": 0.063E-4 * 1E-6, "Osmose_Korrektur": 1,
            "D_lit": 0.0063, "K_D": 0.5, "p_D_lit": 1.013, "T_D_lit": 25 + 273.15,
            "Wärmeüb_GDL": 0.85,
            #Kathode
            "K_v_Filter": 0.024,
            "Eff_C_CompEng": 0.95, "m_dot_min_Comp": 5, "m_dot_max_Comp": 151,
            #HT-Kühlung
            "P_max_Heat_Control": 80000, "P_Max_WTau": 50000, "K_Temp_Regelung": 2500, "HT_Hysterese": 2.5,
            "Temp_BZ_Soll": 273.15+70, "Temp_BZ_min": 273.15+65, "Temp_BZ_max": 273.15+75,
            "V_dot_max_HT": 1.75, "V_dot_min_HT": 1.75 * 0.005,
            "V_Coolant_HT": 16.4,
            "mx_ZwK": 0.1
        }

        self.SoC_calc = SoC_calc(Calib=self.Calib)
        self.Eff = Eff(para=self.parameter, Nat=self.Naturkonstanten)
        self.Gas = Gas(para=self.parameter, Nat=self.Naturkonstanten)

        self.parameter |= {'pres_env': self.Gas.pres_air_calc()}
        self.Fahrzeugmodell = vehicle_modell(Nat=self.Naturkonstanten, para=self.parameter, Calib=self.Calib)
        self.Kathode = Kathode(para=self.parameter, Nat=self.Naturkonstanten, Calib=self.Calib)
        self.Anode = Anode(para=self.parameter, Nat=self.Naturkonstanten, Kathode=self.Kathode, Calib=self.Calib)
        self.Kuehlung = Kuehlung(Eingabe=self.Eingabe, para=self.parameter, Nat=self.Naturkonstanten, Calib=self.Calib, Kathode=self.Kathode, Anode=self.Anode, Fahrzeugmodell=self.Fahrzeugmodell)

        if "Datenerfassung":

            self.a_Soll = [0]
            self.v_Soll = [0]
            #Fahrzeugmodell Plotting
            self.t = [0]
            self.v_act = [0]
            self.a_act = [0]
            self.P_Rad = [0]
            self.P_E_M_soll = [0]
            self.P_E_M = [0]
            self.P_BZ = [0]
            self.P_BoP_act = [0]
            self.P_Bat = [0]
            self.P_mB = [0]
            self.P_HV = [0]
            self.P_HV_soll = [0]
            self.SoC = [self.parameter['SoC']]
            self.SoC_Case = [0]
            self.Eff_Vehicle = [1]

            #Brennstoffzellen Plotting
            self.P_BZ_max = [0]
            self.Eff_BZ_System = [1]
            self.Eff_BZ_Stack = [1]

            self.m_dot_C = [0]
            self.m_dot_C_BZ = [0]
            self.p_rat_C_Comp = [1]
            self.p_C_BZ_in = [1]
            self.p_C_BZ_out = [1]
            self.rH_C_BZ_in = [0]
            self.rH_C_BZ_out = [0]
            self.Temp_KK = [self.parameter['temp_env']]
            self.Temp_KE = [self.parameter['temp_env']]
            self.rH_KK = [0]
            self.rH_KE = [0]
            self.p_KK = [1]
            self.P_Comp = [0]

            self.m_dot_A_BZ_in = [0]
            self.p_rat_A_Rezi = [1]
            self.p_A_BZ_in = [1]
            self.p_A_BZ_out = [1]
            self.rH_AK = [0]
            self.rH_AE = [0]
            self.Temp_A_BZ = [self.parameter['Temp_BZ_Init']]
            self.m_dot_H2_current = [0]
            self.m_H2_total = [0]
            self.n_dot_H2O_cross = [0]
            self.n_dot_N2_cross = [0]
            self.p_AK = [1]
            self.P_Rezi = [0]
            self.m_dot_H2_Purge = [0]

            self.P_BZ_Heat = [0]
            self.P_ZwK_Heat = [0]
            self.P_BZ_Cool = [0]
            self.Temp_BZ = [self.parameter['Temp_BZ_Init']]
            self.m_dot_Co_HT = [0]
            self.m_dot_Co_HT_BZ = [0]
            self.m_dot_Co_HT_ZwK = [0]
            self.m_dot_Co_HT_WTau = [0]
            self.Temp_Co_HT_WTau_in = [40 + 273.15]
            self.Temp_Co_HT_WTau_out = [40 + 273.15]
            self.p_Co_HT_Pump_out = [1]
            self.case_HT = [0]
            self.P_Pump_HT = [0]

            self.P_Inv_Heat = [0]
            self.P_Comp_Heat = [0]
            self.m_dot_NT = [0]
            self.p_Pump_NT = [1]
            self.Temp_Co_NT_WTau_in = [self.parameter['temp_env']]
            self.Temp_Co_NT_WTau_out = [self.parameter['temp_env']]
            self.P_Pump_NT = [0]

            self.I_BZ = [0]
            self.U_BZ = [1]
            self.U_Zelle = [1.2]
            self.U_ohm = [0]
            self.U_act = [0]
            self.U_conc = [0]

            self.P_BoP_pre = [0]
            self.diff_P_BZ = [0]
            self.P_BoP_pre_AVL = [0]

    def __call__(self, SaveIt=False, savefolder='D:/Projekte/Mirai/' + str(datetime.now().date()), csv=False, Plots_vorg=False, Plot_indiv=False, Plot_Live=False, Plots_alt=False, x_indiv=0, y1_indiv=0, y2_indiv=0, y3_indiv=0, y1_live=0, y2_live=0, y3_live=0):
        if 'Initialisierungen':
            if Plot_Live == True:
                import socket
                TCP_IP = '127.0.0.1'
                TCP_PORT = 7800
                sender = []
                os.startfile("Liveplot\\LiveMonitor.exe")
                i=0
                for y in [y1_live, y2_live, y3_live]:
                    if isinstance(y, str):
                        if 'Zuordnung':
                            if y == 'Zeit':
                                a = self.t
                                b = ' / s'
                            elif y == 'Ist_Geschwindigkeit':
                                a = self.v_act
                                b = ' / m/s'
                            elif y == 'Soll_Geschwindigkeit':
                                a = self.v_Soll
                                b = ' / m/s'
                            elif y == 'Ist_Beschleunigung':
                                a = self.a_act
                                b = ' / m/s^2'
                            elif y == 'Soll_Beschleunigung':
                                a = self.a_Soll
                                b = ' / m/s^2'
                            elif y == 'Rad_Leistung':
                                a = self.P_Rad
                                b = ' / W'
                            elif y == 'E_Motor_Soll_Leistung':
                                a = self.P_E_M_soll
                                b = ' / W'
                            elif y == 'E_Motor_Ist_Leistung':
                                a = self.P_E_M
                                b = ' / W'
                            elif y == 'BZ_Leistung':
                                a = self.P_BZ
                                b = ' / W'
                            elif y == 'BoP_Leistungsaufnahme':
                                a = self.P_BoP_act
                                b = ' / W'
                            elif y == 'Batterie_Leistung':
                                a = self.P_Bat
                                b = ' / W'
                            elif y == 'mech._Bremsleistung':
                                a = self.P_mB
                                b = ' / W'
                            elif y == 'HV_Bus_Ist_Leistung':
                                a = self.P_HV
                                b = ' / W'
                            elif y == 'HV_Bus_Soll_Leistung':
                                a = self.P_HV_soll
                                b = ' / W'
                            elif y == 'BZ_Maximalleistung':
                                a = self.P_BZ_max
                                b = ' / W'
                            elif y == 'Zustand_Hybridsystemregelung':
                                a = self.SoC_Case
                                b = ' / -'
                            elif y == 'Zustand_Temperaturregelung':
                                a = self.case_HT
                                b = ' / -'
                            elif y == 'Batterie_Ladestand':
                                a = self.SoC
                                b = ' / -'
                            elif y == 'BZ_Stapel_Effizienz':
                                a = self.Eff_BZ_Stack
                                b = ' / -'
                            elif y == 'BZ_System_Effizienz':
                                a = self.Eff_BZ_System
                                b = ' / -'
                            elif y == 'Fahrzeug_Effizienz':
                                a = self.Eff_Vehicle
                                b = ' / -'
                            elif y == 'Kathoden_Massenstrom':
                                a = self.m_dot_C
                                b = ' / g/s'
                            elif y == 'Kathoden_Stapel_Massenstrom':
                                a = self.m_dot_C_BZ
                                b = ' / g/s'
                            elif y == 'Anoden_Massenstrom':
                                a = self.m_dot_A_BZ_in
                                b = ' / g/s'
                            elif y == 'HT_Massenstrom':
                                a = self.m_dot_Co_HT
                                b = ' / g/s'
                            elif y == 'HT_Massenstrom_durch_den_Stapel':
                                a = self.m_dot_Co_HT_BZ
                                b = ' / g/s'
                            elif y == 'HT_Massenstrom_durch_den_Wärmetauscher':
                                a = self.m_dot_Co_HT_WTau
                                b = ' / g/s'
                            elif y == 'NT_Massenstrom':
                                a = self.m_dot_NT
                                b = ' / g/s'
                            elif y == 'H2_Injektor_Massenstrom':
                                a = self.m_dot_H2_current
                                b = ' / g/s'
                            elif y == 'H2_Verbrauch':
                                a = self.m_H2_total
                                b = ' / g'
                            elif y == 'Kompressor_Druckverhältnis':
                                a = self.p_rat_C_Comp
                                b = ' / bara/bara'
                            elif y == 'Rezirkulations_Druckverhältnis':
                                a = self.p_rat_A_Rezi
                                b = ' / bara/bara'
                            elif y == 'Kathoden_Druck_am_BZ_Eintritt':
                                a = self.p_C_BZ_in
                                b = ' / bara'
                            elif y == 'Kathoden_Druck_am_BZ_Austritt':
                                a = self.p_C_BZ_out
                                b = ' / bara'
                            elif y == 'Anoden_Druck_am_BZ_Eintritt':
                                a = self.p_A_BZ_in
                                b = ' / bara'
                            elif y == 'Anoden_Druck_am_BZ_Austritt':
                                a = self.p_A_BZ_out
                                b = ' / bara'
                            elif y == 'HT_Druck':
                                a = self.p_Co_HT_Pump_out
                                b = ' / bara'
                            elif y == 'NT_Druck':
                                a = self.p_Pump_NT
                                b = ' / bara'
                            elif y == 'BZ_Stapel_Temperatur':
                                a = self.Temp_BZ
                                b = ' / K'
                            elif y == 'BZ_Kathodenelektroden_Temperatur':
                                a = self.Temp_KE
                                b = ' / K'
                            elif y == 'BZ_Kathodenkanal_Temperatur':
                                a = self.Temp_KK
                                b = ' / K'
                            elif y == 'HT_Temperatur_hoch':
                                a = self.Temp_Co_HT_WTau_in
                                b = ' / K'
                            elif y == 'HT_Temperatur_niedrig':
                                a = self.Temp_Co_HT_WTau_out
                                b = ' / K'
                            elif y == 'BZ_Anodenkanal_Temperatur':
                                a = self.Temp_A_BZ
                                b = ' / K'
                            elif y == 'NT_Temperatur_hoch':
                                a = self.Temp_Co_NT_WTau_out
                                b = ' / K'
                            elif y == 'NT_Temperatur_niedrig':
                                a = self.Temp_Co_NT_WTau_out
                                b = ' / K'
                            elif y == 'Kathoden_Feuchte_am_BZ_Eintritt':
                                a = self.rH_C_BZ_in
                                b = ' / -'
                            elif y == 'Kathoden_Feuchte_am_BZ_Austritt':
                                a = self.rH_C_BZ_out
                                b = ' / -'
                            elif y == 'durchschn_BZ_Kathodenkanal_Feuchte':
                                a = self.rH_KK
                                b = ' / -'
                            elif y == 'durchschn_BZ_Kathodenelektroden_Feuchte':
                                a = self.rH_KE
                                b = ' / -'
                            elif y == 'durchschn_BZ_Anodenelektroden_Feuchte':
                                a = self.rH_AE
                                b = ' / -'
                            elif y == 'durchschn_BZ_Anodenkanal_Feuchte':
                                a = self.rH_AK
                                b = ' / -'
                            elif y == 'therm_BZ_Leistung':
                                a = self.P_BZ_Heat
                                b = ' / W'
                            elif y == 'Wärmeübertrag_vom_Stapel_ins_Kühlmittel':
                                a = self.P_BZ_Cool
                                b = ' / W'
                            elif y == 'Zwischenkühler_Wärmeübertrag':
                                a = self.P_ZwK_Heat
                                b = ' / W'
                            elif y == 'Kompressor_Motor_Wärmeübertrag':
                                a = self.P_Comp_Heat
                                b = ' / W'
                            elif y == 'Wechselrichter_Wärmeübertrag':
                                a = self.P_Inv_Heat
                                b = ' / W'
                            elif y == 'H20_Stroffmengenstrom_durch_die_Membran':
                                a = self.n_dot_H2O_cross
                                b = ' / mol/s'
                            elif y == 'N2_Stroffmengenstrom_durch_die_Membran':
                                a = self.n_dot_N2_cross
                                b = ' / mol/s'
                            elif y == 'Stapel_Strom':
                                a = self.I_BZ
                                b = ' / A'
                            elif y == 'Stapel_Spannung':
                                a = self.U_BZ
                                b = ' / V'
                            elif y == 'Aktivierungsverluste':
                                a = self.U_act
                                b = ' / v'
                            elif y == 'ohmsche Verluste':
                                a = self.U_ohm
                                b = ' / v'
                            elif y == 'Konzentrationsverluste':
                                a = self.U_conc
                                b = ' / V'
                            elif y == 'Zell_Spannung':
                                a = self.U_Zelle
                                b = ' / V'

                            if y == y1_live:
                                y1_value = a
                            elif y == y2_live:
                                y2_value = a
                            elif y == y3_live:
                                y3_value = a
                        sender += socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                        sender[i].connect((TCP_IP, TCP_PORT))
                        FirstMessage = y+b+'\n'
                        sender[i].send(bytes(FirstMessage, encoding='utf8'))
                        i+=1

            Temp_BZ = self.parameter['Temp_BZ_Init']
            Temp_Coolant_HT = self.parameter['Temp_BZ_Init']
            SoC_0 = self.parameter['SoC']
            self.I_Stack = 0
            self.I_min_BZ = 0
            F_Run_Time = True

        for t in range(len(self.parameter['Time'])-1):
            t_0 = self.parameter['Time'][t]
            t_1 = self.parameter['Time'][t+1]

            if 'Maximalwert-BZ':
                #Wärmenotlaufmodus
                if self.Kuehlung.case_HT == 2:
                    self.P_max_BZ = self.Calib['P_max_Heat_Control']
                else:
                    self.P_max_BZ = self.Calib['P_max_BZ']

                I_BZ_max = []
                P_brut_max = []

                if F_Run_Time == True:
                    I_St_max = min(self.Calib['I_max_BZ'], self.Calib['m_dot_max_Comp'] * self.Naturkonstanten['el_O2'] * self.Naturkonstanten['Faraday'] / (self.Calib['NumCells'] * self.parameter['st_C']) * self.Gas.mx_n_start(mx_old=self.Naturkonstanten['mx_O2'], rH=self.parameter['rH_env']) / self.Naturkonstanten['M_O2'])
                    I_min = 0
                    I_max = math.ceil(I_St_max * (t_1 - t_0) / self.parameter['t_Komp_Dynamik'])
                else:
                    I_min = math.floor(max(0, self.I_Stack - self.Calib['I_max_BZ'] * (t_1 - t_0) / self.parameter['t_Komp_Dynamik']))
                    I_max = math.ceil(min(I_St_max, self.I_Stack + self.Calib['I_max_BZ'] * (t_1 - t_0) / self.parameter['t_Komp_Dynamik']))

                i_grob = np.linspace(I_min,I_max,11)
                F_Run_P_max = True
                for self.I_Stack in i_grob:
                    self.Kuehlung.Cooling_Pump_BZ.pres_Co = 5
                    self.Kuehlung.Cooling_Pump_Ka.pres_Co = 5
                    self.Anode.BZ_A.n_dot_Diffu_N2 = 0
                    self.Anode.BZ_A.m_dot_cross_H2O = 0
                    self.Anode.rH_FC_in = 0.6
                    self.Kuehlung.P_BZ_Heat = 0

                    x=0
                    while x<2:
                        self.Kathode(I_St=self.I_Stack, I_St_min=I_min, n_dot_Diffu_N2=self.Anode.BZ_A.n_dot_Diffu_N2, m_dot_cross_H2O=self.Anode.BZ_A.m_dot_cross_H2O, rH_An=self.Anode.rH_FC_in, Temp_BZ=Temp_BZ, P_Heat_BZ=self.Kuehlung.P_BZ_Heat)
                        self.Anode(I_St=self.I_Stack, Temp_BZ=Temp_BZ)
                        self.Kuehlung(I_St=self.I_Stack, Temp_BZ=Temp_BZ, Temp_Coolant_HT=Temp_Coolant_HT, dt=t_1-t_0)
                        x += 1

                    I_BZ_max += self.I_Stack,
                    P_brut_max += self.Kathode.BZ_C.P_Stack,

                    if F_Run_P_max == False and P_brut_max[-1] < P_brut_max[-2]:
                        try:
                            I_BZ_max_1 = math.floor(I_BZ_max[-3])
                        except:
                            I_BZ_max_1 = math.floor(I_BZ_max[-2])
                        for self.I_Stack in range(I_BZ_max_1,math.ceil(I_BZ_max[-1])):
                            self.Kuehlung.Cooling_Pump_BZ.pres_Co = 5
                            self.Kuehlung.Cooling_Pump_Ka.pres_Co = 5
                            self.Anode.BZ_A.n_dot_Diffu_N2 = 0
                            self.Anode.BZ_A.m_dot_cross_H2O = 0
                            self.Anode.rH_FC_in = 0.6
                            self.Kuehlung.P_BZ_Heat = 0

                            x = 0
                            while x <= 1:
                                self.Kathode(I_St=self.I_Stack, I_St_min=I_min, n_dot_Diffu_N2=self.Anode.BZ_A.n_dot_Diffu_N2, m_dot_cross_H2O=self.Anode.BZ_A.m_dot_cross_H2O,
                                             rH_An=self.Anode.rH_FC_in, Temp_BZ=Temp_BZ, P_Heat_BZ=self.Kuehlung.P_BZ_Heat)
                                self.Anode(I_St=self.I_Stack, Temp_BZ=Temp_BZ)
                                self.Kuehlung(I_St=self.I_Stack, Temp_BZ=Temp_BZ, Temp_Coolant_HT=Temp_Coolant_HT, dt=t_1 - t_0)
                                x += 1

                            I_BZ_max += self.I_Stack,
                            P_brut_max += self.Kathode.BZ_C.P_Stack,
                            if P_brut_max[-1] < P_brut_max[-2]:
                                break
                    if F_Run_P_max == False and P_brut_max[-1] > self.P_max_BZ:
                        break
                    F_Run_P_max = False
                self.P_max_BZ = min(max(P_brut_max), self.P_max_BZ)
                self.I_max_BZ = I_BZ_max[P_brut_max.index(max(P_brut_max))]
                self.P_min_BZ = max(min(P_brut_max), 0)
                self.I_min_BZ = I_BZ_max[P_brut_max.index(min(P_brut_max))]

            #Fahrzeugmodell
            self.Fahrzeugmodell(t=t, t_0=t_0, t_1=t_1, SoC_0=SoC_0, P_max_BZ=self.P_max_BZ)

            if 'Brennstoffzelle':
                if self.Fahrzeugmodell.P_BZ == 0 or F_Run_Time == True:
                    self.I_Stack = 0
                    I_Stack_old = self.Naturkonstanten['eps']
                elif self.Fahrzeugmodell.Warn_zu_wenig_Leistung == True:
                    self.I_Stack = self.I_max_BZ
                else:
                    self.I_Stack = I_Stack_old

                self.Anode.BZ_A.n_dot_Diffu_N2 = 0
                self.Anode.BZ_A.m_dot_cross_H2O = 0
                self.Anode.rH_FC_in = 0.6
                self.Kathode.BZ_C.P_Stack = self.Naturkonstanten['eps']
                self.Kuehlung.Cooling_Pump_BZ.pres_Co = 5
                self.Kuehlung.Cooling_Pump_Ka.pres_Co = 5
                self.Kuehlung.P_BZ_Heat = 0

                if self.Fahrzeugmodell.P_BZ < 1000:
                    accuracy = 0.01
                elif self.Fahrzeugmodell.P_BZ < 10000:
                    accuracy = 0.001
                else:
                    accuracy = 0.0001
                i = 0
                i_border = 50
                UR_Faktor = 1
                increment = 0.75
                VZ_old = 0
                VZ_new = 0
                F_Run_BZ = True
                while (self.Kathode.BZ_C.P_Stack < self.Fahrzeugmodell.P_BZ * (1 - accuracy) or self.Kathode.BZ_C.P_Stack > self.Fahrzeugmodell.P_BZ * (1 + accuracy) or i <= 1) and i <= i_border:
                    self.Kathode(I_St=self.I_Stack, I_St_min=self.I_min_BZ, n_dot_Diffu_N2=self.Anode.BZ_A.n_dot_Diffu_N2, m_dot_cross_H2O=self.Anode.BZ_A.m_dot_cross_H2O, rH_An=self.Anode.rH_FC_in, Temp_BZ=Temp_BZ, P_Heat_BZ=self.Kuehlung.P_BZ_Heat)
                    self.Anode(I_St=self.I_Stack, Temp_BZ=Temp_BZ)
                    self.Kuehlung(I_St=self.I_Stack, Temp_BZ=Temp_BZ, Temp_Coolant_HT=Temp_Coolant_HT, dt=t_1-t_0)

                    if self.Fahrzeugmodell.P_BZ * (1 - accuracy) > self.Kathode.BZ_C.P_Stack or self.Kathode.BZ_C.P_Stack > self.Fahrzeugmodell.P_BZ * (1 + accuracy):
                        self.I_Stack = min(self.I_Stack + (self.Fahrzeugmodell.P_BZ - self.Kathode.BZ_C.P_Stack) / self.Kathode.BZ_C.U_Stack * UR_Faktor, I_max)
                    if self.Fahrzeugmodell.P_BZ - self.Kathode.BZ_C.P_Stack < 0:
                        VZ_new = 0
                    if self.Fahrzeugmodell.P_BZ - self.Kathode.BZ_C.P_Stack > 0:
                        VZ_new = 1
                    if VZ_new != VZ_old and F_Run_BZ == False:
                        UR_Faktor = UR_Faktor * increment
                    VZ_old = VZ_new
                    if UR_Faktor < 1e-4 or (F_Run_BZ == False and I_Stack_old == self.I_Stack):
                        break
                    F_Run_BZ = False
                    i += 1
                self.sys_eff = self.Eff.Eff_calc(m_O2_in=self.Kathode.ptmx['BZ_in']['mx_O2'] * self.Kathode.ptmx['BZ_in']['m_dot'],
                                                 m_O2_out=self.Kathode.ptmx['BZ_out']['mx_O2'] * self.Kathode.ptmx['BZ_out']['m_dot'],
                                                 P_Brutto=self.Kathode.BZ_C.P_Stack, P_CompEng=self.Kathode.Comp.P_Comp_Engine,
                                                 P_Anode=self.Anode.Rezi.P_Rezi, P_Cooling=self.Kuehlung.Cooling_Pump_BZ.P_Cooling + self.Kuehlung.Cooling_Pump_Ka.P_Cooling)

            if 'Korrektur_und_SoC':
                #SoC-Berechnung
                self.Fahrzeugmodell.P_Bat += self.P_BoP_act[-1] - self.Fahrzeugmodell.P_BoP_pre
                self.SoC_calc(t_0=t_0, t_1=t_1, SoC_0=SoC_0, P_Bat=self.Fahrzeugmodell.P_Bat)
                SoC_0 = self.SoC_calc.SoC_1

                #BZ-Temperatur-Berechnung
                Temp_BZ = self.Kuehlung.Temp_BZ
                Temp_Coolant_HT = self.Kuehlung.Temp_Coolant_HT
                I_Stack_old=self.I_Stack
                F_Run_Time = False

            if 'Datenerfassung':
                    self.v_Soll += self.parameter['FZ_geschw'][t_1],
                    self.a_Soll += self.parameter['FZ_beschl'][t_1],

                    #Fahrzeugmodell Plotting
                    self.t += t_1,
                    self.v_act += self.Fahrzeugmodell.v_1,
                    self.a_act += self.Fahrzeugmodell.a,
                    self.P_Rad += self.Fahrzeugmodell.P_Rad,
                    self.P_E_M_soll += self.Fahrzeugmodell.P_E_M_soll,
                    self.P_E_M += self.Fahrzeugmodell.P_E_M,
                    self.P_BZ += self.Fahrzeugmodell.P_BZ,
                    self.P_Bat += self.Fahrzeugmodell.P_Bat,
                    self.P_mB += self.Fahrzeugmodell.P_mB,
                    self.P_HV_soll += self.Fahrzeugmodell.P_HV_BUS_soll,
                    self.P_HV += self.Fahrzeugmodell.P_HV_BUS,
                    self.P_BoP_act += self.Kathode.Comp.P_Comp_Engine + self.Anode.Rezi.P_Rezi + self.Kuehlung.Cooling_Pump_BZ.P_Cooling + self.Kuehlung.Cooling_Pump_Ka.P_Cooling,
                    self.SoC += self.SoC_calc.SoC_1,
                    self.SoC_Case += self.Fahrzeugmodell.case_SoC,

                    self.Eff_Vehicle += np.clip(self.Fahrzeugmodell.P_Rad / (self.Anode.ptmx['Tankv_out']['m_dot'] * self.Naturkonstanten['Hi_H2'] + self.P_Bat[-1]),0,1),

                    #Brennstoffzellen Plotting
                    self.P_BZ_max += self.P_max_BZ,
                    self.Eff_BZ_System += max(self.sys_eff, 0),
                    self.Eff_BZ_Stack += max(self.Kathode.BZ_C.Stack_Eff,0),

                    self.m_dot_C += self.Kathode.ptmx['Sys_in']['m_dot'],
                    self.m_dot_C_BZ += self.Kathode.ptmx['BZ_in']['m_dot'],
                    self.p_rat_C_Comp += self.Kathode.Comp.p_rat,
                    self.p_C_BZ_in += self.Kathode.ptmx['BZ_in']['pres'],
                    self.p_C_BZ_out += self.Kathode.ptmx['BZ_out']['pres'],
                    self.rH_C_BZ_in += self.Kathode.ptmx['BZ_in']['rH'],
                    self.rH_C_BZ_out += self.Kathode.ptmx['BZ_out']['rH'],
                    self.Temp_KK += (self.Kathode.ptmx['BZ_in']['temp'] + self.Kathode.ptmx['BZ_out']['temp']) / 2,
                    self.Temp_KE += self.Kathode.BZ_C.Temp_KE,
                    self.rH_KE += self.Kathode.BZ_C.rH_KE,
                    self.rH_KK += (self.Kathode.ptmx['BZ_out']['rH'] + self.Kathode.ptmx['BZ_in']['rH']) / 2,
                    self.p_KK += (self.Kathode.ptmx['BZ_out']['pres'] + self.Kathode.ptmx['BZ_in']['pres']) / 2,
                    self.P_Comp += self.Kathode.Comp.P_Comp_Engine,

                    self.m_dot_A_BZ_in += self.Anode.ptmx['BZ_in']['m_dot'],
                    self.p_rat_A_Rezi += self.Anode.Rezi.presrat_Rezi,
                    self.p_A_BZ_in += self.Anode.ptmx['BZ_in']['pres'],
                    self.p_A_BZ_out += self.Anode.ptmx['BZ_out']['pres'],
                    self.Temp_A_BZ += (self.Anode.ptmx['BZ_out']['temp'] + self.Anode.ptmx['BZ_in']['temp']) / 2,
                    self.rH_AE += self.Anode.BZ_A.rH_AE,
                    self.rH_AK += self.Anode.BZ_A.rH_AK,
                    self.m_dot_H2_current += self.Anode.ptmx['Tankv_out']['m_dot'],
                    self.m_H2_total += self.m_H2_total[-1] + self.Anode.ptmx['Tankv_out']['m_dot'] * (t_1-t_0),
                    self.p_AK += (self.Anode.ptmx['BZ_out']['pres'] + self.Anode.ptmx['BZ_in']['pres']) / 2,
                    self.P_Rezi += self.Anode.Rezi.P_Rezi,
                    self.m_dot_H2_Purge += self.Anode.Purge_Valve.m_dot_H2_purge,

                    self.P_BZ_Heat += self.Kuehlung.P_BZ_Heat,
                    self.P_ZwK_Heat += self.Kathode.Intercooler.P_ZwK_Heat,
                    self.P_BZ_Cool += self.Kuehlung.P_BZ_Heat_Cool,
                    self.Temp_BZ += self.Kuehlung.Temp_BZ,
                    self.m_dot_Co_HT += self.Kuehlung.ptm_BZ['Pump_in']['m_dot'],
                    self.m_dot_Co_HT_BZ += self.Kuehlung.ptm_BZ['BZ_in']['m_dot'],
                    self.m_dot_Co_HT_ZwK += self.Kuehlung.ptm_BZ['ZwK_in']['m_dot'],
                    self.m_dot_Co_HT_WTau += self.Kuehlung.Heat_Ex_BZ.m_dot_WTau,
                    self.Temp_Co_HT_WTau_in += self.Kuehlung.ptm_BZ['Wtau_in']['temp'],
                    self.Temp_Co_HT_WTau_out += self.Kuehlung.ptm_BZ['Wtau_out']['temp'],
                    self.p_Co_HT_Pump_out += self.Kuehlung.ptm_BZ['Pump_out']['pres'],
                    self.case_HT += self.Kuehlung.case_HT,
                    self.P_Pump_HT += self.Kuehlung.Cooling_Pump_BZ.P_Cooling,

                    self.P_Inv_Heat += self.Fahrzeugmodell.P_Inv_Heat,
                    self.P_Comp_Heat += self.Kathode.Comp.P_Comp_Heat,
                    self.m_dot_NT += self.Kuehlung.ptm_Ka['Pump_in']['m_dot'],
                    self.p_Pump_NT += self.Kuehlung.ptm_Ka['Pump_out']['pres'],
                    self.Temp_Co_NT_WTau_in += self.Kuehlung.ptm_Ka['Wtau_in']['temp'],
                    self.Temp_Co_NT_WTau_out += self.Kuehlung.ptm_Ka['Wtau_out']['temp'],
                    self.P_Pump_NT += self.Kuehlung.Cooling_Pump_Ka.P_Cooling,

                    self.I_BZ += self.I_Stack,
                    self.U_BZ += self.Kathode.BZ_C.U_Stack,
                    self.U_Zelle += self.Kathode.BZ_C.Zellspannung.U_Cell,
                    self.U_act += self.Kathode.BZ_C.Zellspannung.U_act,
                    self.U_ohm += self.Kathode.BZ_C.Zellspannung.U_ohm,
                    self.U_conc += self.Kathode.BZ_C.Zellspannung.U_conc,
                    self.n_dot_H2O_cross += self.Anode.BZ_A.m_dot_cross_H2O / self.Naturkonstanten['M_H2O'],
                    self.n_dot_N2_cross += self.Anode.BZ_A.n_dot_Diffu_N2,

                    #Genauigkeitsprüfungen
                    self.P_BoP_pre += self.Fahrzeugmodell.P_BoP_pre,
                    self.diff_P_BZ += self.Fahrzeugmodell.P_BZ - self.Kathode.BZ_C.P_Stack,
                    self.P_BoP_pre_AVL += self.Fahrzeugmodell.P_BoP_pre_AVL(P_BZ=self.Kathode.BZ_C.P_Stack),

            if Plot_Live == True:
                i = 0
                for y in [y1_live, y2_live, y3_live]:
                    if isinstance(y, str):
                        if y == y1_live:
                            y = y1_value[-1]
                        elif y == y2_live:
                            y = y2_value[-1]
                        elif y == y3_live:
                            y = y3_value[-1]
                        MESSAGE = '{x}\n{y}\n'.format(x=t_1, y=y)
                        sender[i].send(bytes(MESSAGE, encoding='utf8'))
                        i+=1

        if 'Plotbefehle':
            if Plots_vorg == True:
                self.Plot_Leistungsverteilung(savefolder=savefolder, SaveIt=SaveIt, Speichername=self.Lastprofil, t=self.t, P_Rad=self.P_Rad, P_E_M=self.P_E_M, P_E_M_Soll=self.P_E_M_soll, P_mB=self.P_mB, P_Bat=self.P_Bat, P_BZ=self.P_BZ, P_BoP_act=self.P_BoP_act)
                self.Plot_Fahrzeug(savefolder=savefolder, SaveIt=SaveIt, Speichername=self.Lastprofil, t=self.t, P_E_M_Soll=self.P_E_M_soll, P_E_M=self.P_E_M, v=self.v_act, v_Soll=self.v_Soll, a=self.a_act, a_Soll=self.a_Soll)
                self.Plot_Batterie(savefolder=savefolder, SaveIt=SaveIt, Speichername=self.Lastprofil, t=self.t, SoC_Case=self.SoC_Case, SoC=self.SoC, P_Bat=self.P_Bat)
                self.Plot_BZ_Polk_t(savefolder=savefolder, SaveIt=SaveIt, Speichername=self.Lastprofil, t=self.t, I_St=self.I_BZ, U_Zelle=self.U_Zelle, U_ohm=self.U_ohm, U_conc=self.U_conc, U_act=self.U_act)
                self.Plot_BZ_Polk_I_St(savefolder=savefolder, SaveIt=SaveIt, Speichername=self.Lastprofil, I_St=self.I_BZ, U_Zelle=self.U_Zelle, U_ohm=self.U_ohm, U_conc=self.U_conc, U_act=self.U_act)
                self.Plot_BZ_Bedingungen(savefolder=savefolder, SaveIt=SaveIt, Speichername=self.Lastprofil, t=self.t, Temp_BZ=self.Temp_BZ, rH_KE=self.rH_KE, rH_AE=self.rH_AE, p_KK=self.p_KK, p_AK=self.p_AK)
                self.Plot_Kathode(savefolder=savefolder, SaveIt=SaveIt, Speichername=self.Lastprofil, t=self.t, m_dot_C=self.m_dot_C, m_dot_C_BZ=self.m_dot_C_BZ, p_rat_C_Comp=self.p_rat_C_Comp, rH_KE=self.rH_KE, rH_KK=self.rH_KK, Temp_KK=self.Temp_KK, Temp_KE=self.Temp_KE)
                self.Plot_Anode(savefolder=savefolder, SaveIt=SaveIt, Speichername=self.Lastprofil, t=self.t, m_dot_A_BZ_in=self.m_dot_A_BZ_in, p_rat_A_Rezi=self.p_rat_A_Rezi, rH_AE=self.rH_AE, rH_AK=self.rH_AK, m_dot_H2_current=self.m_dot_H2_current, m_dot_H2_Purge=self.m_dot_H2_Purge)
                self.Plot_HT_Kreisl(savefolder=savefolder, SaveIt=SaveIt, Speichername=self.Lastprofil, t=self.t, Case_HT=self.case_HT, Temp_BZ=self.Temp_BZ, P_ZwK_Heat=self.P_ZwK_Heat, P_BZ_Heat=self.P_BZ_Heat, P_BZ_Cool=self.P_BZ_Cool, m_dot_HT=self.m_dot_Co_HT, m_dot_HT_WTau=self.m_dot_Co_HT_WTau, m_dot_HT_BZ=self.m_dot_Co_HT_BZ)
                self.Plot_NT_Kreisl(savefolder=savefolder, SaveIt=SaveIt, Speichername=self.Lastprofil, t=self.t, P_Inv_Heat=self.P_Inv_Heat, P_Comp_Heat=self.P_Comp_Heat, p_NT=self.p_Pump_NT, m_dot_NT=self.m_dot_NT)
                self.Plot_Effizienzen(savefolder=savefolder, SaveIt=SaveIt, Speichername=self.Lastprofil, t=self.t, Eff_BZ_Sys=self.Eff_BZ_System, Eff_BZ=self.Eff_BZ_Stack, Eff_Veh=self.Eff_Vehicle, SoC=self.SoC, m_H2=self.m_H2_total)
                self.Plot_BoP(savefolder=savefolder, SaveIt=SaveIt, Speichername=self.Lastprofil, t=self.t, P_BoP=self.P_BoP_act, P_Comp=self.P_Comp, P_Rezi=self.P_Rezi, P_Pump_NT=self.P_Pump_NT, P_Pump_HT=self.P_Pump_HT)
            if Plot_indiv == True:
                self.Plot_x_y(Speichername=self.Lastprofil, SaveIt=SaveIt, x_indiv=x_indiv, y_indiv=y1_indiv, y2_indiv=y2_indiv, y3_indiv=y3_indiv)
            if csv == True:
                self.csv(SaveIt=SaveIt, savefolder=savefolder, Speichername='WLTC', Zeit=self.t, Soll_Geschwindigkeit=self.v_Soll, Ist_Geschwindigkeit=self.v_act, Soll_Beschleunigung=self.a_Soll,
                        Ist_Beschleunigung=self.a_act,
                        Fahrzeug_Effizienz=self.Eff_Vehicle, BZ_System_Effizienz=self.Eff_BZ_System, BZ_Stapel_Effizienz=self.Eff_BZ_Stack,
                        Rad_Leistung=self.P_Rad, E_Motor_Soll_Leistung=self.P_E_M_soll, E_Motor_Ist_Leistung=self.P_E_M, HV_Bus_Soll_Leistung=self.P_HV_soll, HV_Bus_Ist_Leistung=self.P_HV,
                        BZ_Leistung=self.P_BZ, BoP_Leistungsaufnahme=self.P_BoP_act, Batterie_Leistung=self.P_Bat, mech_Bremsleistung=self.P_mB,
                        Batterie_Ladestand=self.SoC, Zustand_Hybridsystemregelung=self.SoC_Case,
                        BZ_Maximalleistung=self.P_BZ_max, Stapel_Strom=self.I_BZ, Stapel_Spannung=self.U_BZ, Zell_Spannung=self.U_Zelle, ohmscheVerluste=self.U_ohm, Aktivierungsverluste=self.U_act,
                        Konzentrationsverluste=self.U_conc,
                        Kathoden_Massenstrom=self.m_dot_C, Kathoden_Stapel_Massenstrom=self.m_dot_C_BZ, Kompressor_Druckverhältnis=self.p_rat_C_Comp, durchschn_BZ_Kathoden_Druck=self.p_KK,
                        durchschn_BZ_Kathodenkanal_Feuchte=self.rH_KK,
                        durchschn_BZ_Kathodenelektroden_Feuchte=self.rH_KE, BZ_Kathodenelektroden_Temperatur=self.Temp_KK, BZ_Kathodenkanal_Temperatur=self.Temp_KE,
                        Anoden_Massenstrom=self.m_dot_A_BZ_in, H2_Injektor_Massenstrom=self.m_dot_H2_current, H2_Verbrauch=self.m_H2_total, Rezirkulations_Druckverhältnis=self.p_rat_A_Rezi,
                        durchschn_BZ_Anoden_Druck=self.p_AK, durchschn_BZ_Anodenkanal_Feuchte=self.rH_AK,
                        durchschn_BZ_Anodenelektroden_Feuchte=self.rH_AE, BZ_Anoden_Temperatur=self.Temp_A_BZ,
                        H20_Stroffmengenstrom_durch_die_Membran=self.n_dot_H2O_cross, N2_Stroffmengenstrom_durch_die_Membran=self.n_dot_N2_cross,
                        BZ_Stapel_Temperatur=self.Temp_BZ, Zustand_Temperaturregelung=self.case_HT, therm_BZ_Leistung=self.P_BZ_Heat, Zwischenkühler_Wärmeübertrag=self.P_ZwK_Heat,
                        Wärmeübertrag_vom_Stapel_ins_Kühlmittel=self.P_BZ_Cool, HT_Massenstrom=self.m_dot_Co_HT,
                        HT_Massenstrom_durch_den_Stapel=self.m_dot_Co_HT_BZ, HT_Massenstrom_durch_den_Wärmetauscher=self.m_dot_Co_HT_WTau, HT_Temperatur_niedrig=self.Temp_Co_HT_WTau_out,
                        HT_Temperatur_hoch=self.Temp_Co_HT_WTau_in, HT_Druck=self.p_Co_HT_Pump_out,
                        Wechselrichter_Wärmeübertrag=self.P_Inv_Heat, Kompressor_Motor_Wärmebertrag=self.P_Comp_Heat, NT_Druck=self.p_Pump_NT, NT_Temperatur_niedrig=self.Temp_Co_NT_WTau_out,
                        NT_Temperatur_hoch=self.Temp_Co_NT_WTau_in)
