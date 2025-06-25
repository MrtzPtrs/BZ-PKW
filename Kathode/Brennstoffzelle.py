import copy
import numpy as np
from Outsourced.Zellspannung import Zellspannung
from Outsourced.Gasberechnungen import Gas

class BZ_C:
    def __init__(self, para, Nat, Calib):
        self.para = para
        self.Nat = Nat
        self.Calib = Calib
        self.Gas = Gas(para=self.para, Nat=self.Nat)
        self.Zellspannung = Zellspannung(Calib=self.Calib, Nat=self.Nat)

    def __call__(self, ptmx_in, I_St, m_dot_Diffu_N2, m_dot_cross_H2O, rH_An, Temp_BZ, P_Heat):
        ptmx_out = copy.deepcopy(ptmx_in)
        if ptmx_in['m_dot'] > 0:
            self.V_norm_BZ_C = np.clip(ptmx_in['V_dot'] / self.para['V_dot_max_C'],0,1)
            self.deltapres_BZ_C = -539.9004430207449 * self.V_norm_BZ_C - 24.52754403323702 * self.V_norm_BZ_C**2 + 6241.093103010336 * np.exp(0.08666158697511717 * self.V_norm_BZ_C) - 6241.093103010336 #Ballard_MCmoveXD
            ptmx_out['pres'] = ptmx_in['pres'] - self.deltapres_BZ_C
            ptmx_out['temp'] = ptmx_in['temp'] + self.para['deltatemp_BZ_C']
            m_dot_N2 = max(0, ptmx_in['mx_N2'] * ptmx_in['m_dot'] - m_dot_Diffu_N2)
            m_dot_H2 = ptmx_in['mx_H2'] * ptmx_in['m_dot']
            m_dot_O2 = ptmx_in['m_dot'] * ptmx_in['mx_O2'] * (1 - 1 / self.para['st_C'])
            self.m_dot_H2O_Prod = (ptmx_in['m_dot'] * ptmx_in['mx_O2'] - m_dot_O2) / self.Nat['M_O2'] * 2 * self.Nat['M_H2O']
            m_dot_H2O = max(0, self.m_dot_H2O_Prod + ptmx_in['m_dot'] * ptmx_in['mx_H2O'] - m_dot_cross_H2O)
            ptmx_out['m_dot'] = m_dot_N2 + m_dot_O2 + m_dot_H2O + m_dot_H2
            ptmx_out['mx_O2'] = m_dot_O2 / ptmx_out['m_dot']
            ptmx_out['mx_N2'] = m_dot_N2 / ptmx_out['m_dot']
            ptmx_out['mx_H2'] = m_dot_H2 / ptmx_out['m_dot']
            ptmx_out['mx_H2O'] = m_dot_H2O / ptmx_out['m_dot']
            ptmx_out['n_dot'] = ptmx_out['m_dot'] / self.Gas.M_Gasgemisch_mx_calc(ptmx_out)
            ptmx_out['V_dot'] = self.Gas.Volumen_calc(ptmx_out)
            ptmx_out['nx_O2'] = m_dot_O2 / self.Nat['M_O2'] / ptmx_out['n_dot']
            ptmx_out['nx_N2'] = m_dot_N2 / self.Nat['M_N2'] / ptmx_out['n_dot']
            ptmx_out['nx_H2O'] = m_dot_H2O / self.Nat['M_H2O'] / ptmx_out['n_dot']
            ptmx_out['rH'] = ptmx_out['nx_H2O'] * ptmx_out['pres'] / self.Gas.p_sat_calc(ptmx_out['temp'])

            self.H2Oliquid_m_dot_C_5 = max(0, m_dot_H2O - ((ptmx_out['n_dot'] - m_dot_H2O / self.Nat['M_H2O']) * self.Nat['M_H2O'] * self.Gas.p_sat_calc(ptmx_out['temp']) / (ptmx_out['pres'] - self.Gas.p_sat_calc(ptmx_out['temp']))))

            self.i = I_St / self.Calib['activeArea'] / 10000
        else:
            ptmx_out['V_dot'] = 0
            ptmx_out['n_dot'] = 0
            self.m_dot_H2O_Prod = 0

        # Elektrodenberechnung Quelle: Diss Sönke S.41f.
        dT_KE_KK = P_Heat * self.Calib['Membran_Thickness'] / self.Calib['Wärmeüb_GDL'] * 0.55
        self.Temp_KE = (ptmx_out['temp'] + ptmx_in['temp']) / 2 + dT_KE_KK
        D = self.Calib['D_lit'] / self.Calib['K_D'] * self.Calib['p_D_lit'] / ((ptmx_out['pres'] + ptmx_in['pres']) / 2) * ((ptmx_out['temp'] + ptmx_in['temp']) / (2 * self.Calib['T_D_lit'])) ** (3 / 2)
        nx_H2O_KE = (ptmx_in['nx_H2O'] + ptmx_out['nx_H2O']) / 2 + (self.m_dot_H2O_Prod - m_dot_cross_H2O) / self.Nat['M_H2O'] * self.Calib['Membran_Thickness'] / self.Calib['activeArea'] / D
        self.rH_KE = nx_H2O_KE * (ptmx_out['pres'] + ptmx_in['pres']) / 2 / self.Gas.p_sat_calc(self.Temp_KE)

        #Spannungs- und Leistungs- und Effizienzberechnung
        self.U_Cell = self.Zellspannung.U_Cell_calc(ptmx_in, ptmx_out, I_St, rH_An, Temp_BZ, rH_KE=self.rH_KE)
        self.U_Stack = self.U_Cell * self.Calib['NumCells']
        self.P_Stack = I_St * self.U_Stack
        self.P_Heat_Gas = ptmx_out['m_dot'] * self.Gas.C_p_Gas(ptmx_out) * (ptmx_out['temp'] - ptmx_in['temp'])
        self.Stack_Eff = self.U_Cell / self.Zellspannung.U_Ideal
        return ptmx_out

class BZ_A():
    def __init__(self, para, Nat, Kathode, Calib):
        self.Ka = Kathode
        self.para = para
        self.Nat = Nat
        self.Calib = Calib
        self.Gas = Gas(para=self.para, Nat=self.Nat)
        self.Zellspannung = Zellspannung(Calib=self.Calib, Nat=self.Nat)

    def __call__(self, ptmx_in, I_St, ptmx_Ka, Temp_BZ):
        ptmx_out = copy.deepcopy(ptmx_in)
        self.V_norm_BZ_A = np.clip(ptmx_in['V_dot'] / self.para['V_dot_max_A'],0,1)
        self.deltapres_BZ_A = (-1094.7738027971584 * self.V_norm_BZ_A - 47.43333462896918 * self.V_norm_BZ_A**2 + 13190.7 * np.exp(0.08307688315771287 * self.V_norm_BZ_A) - 13190.7) * 0.8 #Ballard_MCmoveXD (Personal Fit wegen Plateau)
        ptmx_out['pres'] = self.Ka.ptmx['BZ_in']['pres'] + self.para['opres_A'] - self.deltapres_BZ_A
        ptmx_out['temp'] = Temp_BZ

        if ptmx_in['m_dot'] > 0:
            i = 0

            accuracy_rH = 0.001
            increment_rH = 0.5
            VZ_rH_old = 0
            VZ_rH_new = 1
            rH_out = 0.8

            accuracy_N2 = 0.0001
            increment_N2 = 0.5
            VZ_N2_old = 0
            VZ_N2_new = 1
            nx_N2_out = 0.1
            while (ptmx_out['rH'] * (1 - accuracy_rH) > rH_out or rH_out > ptmx_out['rH'] * (1 + accuracy_rH) or ptmx_out['nx_N2'] * (1 - accuracy_N2) > nx_N2_out or nx_N2_out > ptmx_out['nx_N2'] * (1 + accuracy_N2)) and i <= 100:
                d_pres_N2 = ((self.Ka.ptmx['BZ_out']['nx_N2'] + self.Ka.ptmx['BZ_in']['nx_N2']) * (self.Ka.ptmx['BZ_in']['pres'] + self.Ka.ptmx['BZ_out']['pres']) - (nx_N2_out + ptmx_in['nx_N2']) * (ptmx_out['pres'] + ptmx_in['pres'])) / 4 * 100000 #Kathode zu Anode
                self.n_dot_Diffu_N2 = self.Calib['N2_Diff_Koeff'] * d_pres_N2 / (self.Nat['Avogadro'] * self.Nat['Boltzmann']) / Temp_BZ / self.Calib['Membran_Thickness'] * self.Calib['activeArea']
                m_dot_N2 = self.n_dot_Diffu_N2 * self.Nat['M_N2'] + ptmx_in['mx_N2'] * ptmx_in['m_dot']

                d_Lambda = -1 * (self.Zellspannung.Lambda_calc(min(1, (rH_out + ptmx_in['rH']) / 2)) - self.Zellspannung.Lambda_calc((min(1, self.Ka.ptmx['BZ_in']['rH'] + self.Ka.ptmx['BZ_out']['rH']) / 2))) #Kathode zu Anode
                self.n_dot_Diffu_H2O = self.Calib['H2O_Diff_Koeff'] * self.Calib['rho_Membran_dry'] * d_Lambda * self.Calib['activeArea'] / (self.Calib['M_Membran_dry'] * self.Calib['Membran_Thickness'])
                osm_Koeff = 2.5 * self.Zellspannung.Lambda_Mem_calc(rH_An=(min(1, rH_out) + min(ptmx_in['rH'], 1)) / 2, rH_Ka=(self.Ka.ptmx['BZ_in']['rH'] + self.Ka.ptmx['BZ_out']['rH']) / 2) / 22
                self.n_dot_Osm_H2O = -1 * osm_Koeff * I_St / self.Nat['Faraday'] * self.Calib['Osmose_Korrektur'] #Kathode zu Anode
                self.m_dot_cross_H2O = np.clip((self.n_dot_Osm_H2O + self.n_dot_Diffu_H2O) * self.Nat['M_H2O'], -ptmx_in['mx_H2O'] * ptmx_in['m_dot'], ptmx_Ka['m_dot'] * ptmx_Ka['mx_H2O'] * 0.8)
                m_dot_H2O = self.m_dot_cross_H2O + ptmx_in['mx_H2O'] * ptmx_in['m_dot']

                m_dot_H2 = ptmx_in['mx_H2'] * ptmx_in['m_dot'] * (1 - 1 / self.para['st_A'])
                ptmx_out['m_dot'] = m_dot_H2 + m_dot_N2 + m_dot_H2O
                ptmx_out['mx_N2'] = m_dot_N2 / ptmx_out['m_dot']
                ptmx_out['mx_H2'] = m_dot_H2 / ptmx_out['m_dot']
                ptmx_out['mx_H2O'] = m_dot_H2O / ptmx_out['m_dot']
                ptmx_out['n_dot'] = ptmx_out['m_dot'] / self.Gas.M_Gasgemisch_mx_calc(ptmx_out)
                ptmx_out['nx_N2'] = m_dot_N2 / (self.Nat['M_N2'] * ptmx_out['n_dot'])
                ptmx_out['nx_H2'] = m_dot_H2 / (self.Nat['M_H2'] * ptmx_out['n_dot'])
                ptmx_out['nx_H2O'] = m_dot_H2O / (self.Nat['M_H2O'] * ptmx_out['n_dot'])
                ptmx_out['V_dot'] = self.Gas.Volumen_calc(ptmx_out)
                ptmx_out['rH'] = ptmx_out['nx_H2O'] * ptmx_out['pres'] / self.Gas.p_sat_calc(ptmx_out['temp'])

                if ptmx_out['rH'] * (1 - accuracy_rH) < rH_out:
                    rH_out = rH_out * (1 - increment_rH)
                    VZ_rH_new = 0
                elif rH_out < ptmx_out['rH'] * (1 + accuracy_rH):
                    rH_out = rH_out * (1 + increment_rH)
                    VZ_rH_new = 1
                if VZ_rH_old != VZ_rH_new:
                    increment_rH = increment_rH / 2
                VZ_rH_old = VZ_rH_new

                if ptmx_out['nx_N2'] * (1 - accuracy_N2) < nx_N2_out:
                    nx_N2_out = nx_N2_out * (1 - increment_N2)
                    VZ_N2_new = 0
                elif nx_N2_out < ptmx_out['nx_N2'] * (1 + accuracy_N2):
                    nx_N2_out = nx_N2_out * (1 + increment_N2)
                    VZ_N2_new = 1
                if VZ_N2_old != VZ_N2_new:
                    increment_N2 = increment_N2 / 2
                VZ_N2_old = VZ_N2_new

                i += 1
            self.P_Heat_Gas = ptmx_out['m_dot'] * self.Gas.C_p_Gas(ptmx_out) * (ptmx_out['temp'] - ptmx_in['temp'])
            self.H2Oliquid_m_dot_A_2 = max(0, m_dot_H2O - ((ptmx_out['n_dot'] - m_dot_H2O / self.Nat['M_H2O']) * self.Nat['M_H2O'] * self.Gas.p_sat_calc(ptmx_out['temp']) / (ptmx_out['pres'] - self.Gas.p_sat_calc(ptmx_out['temp']))))
        else:
            ptmx_out['V_dot'] = self.Gas.Volumen_calc(ptmx_out)
            ptmx_out['rH'] = ptmx_out['nx_H2O'] * ptmx_out['pres'] / self.Gas.p_sat_calc(ptmx_out['temp'])
            self.P_Heat_Gas = 0
            self.H2Oliquid_m_dot_A_2 = 0
            self.m_dot_cross_H2O = 0
            self.n_dot_Diffu_N2 = 0
            self.n_dot_Diffu_H2O = 0
            self.n_dot_Osm_H2O = 0

        self.rH_AK = (ptmx_in['nx_H2O'] + ptmx_out['nx_H2O']) / 2 * (ptmx_out['pres'] + ptmx_in['pres']) / 2 / self.Gas.p_sat_calc((ptmx_out['temp'] + ptmx_in['temp']) / 2)
        #Elektrodenberechnungen Quelle: Diss Sönke S.43
        D = self.Calib['D_lit'] / self.Calib['K_D'] * self.Calib['p_D_lit'] / ((ptmx_out['pres'] + ptmx_in['pres']) / 2) * ((ptmx_out['temp'] + ptmx_in['temp']) / (2 * self.Calib['T_D_lit'])) ** (3 / 2)
        nx_H2O_AE = (ptmx_in['nx_H2O'] + ptmx_out['nx_H2O']) / 2 + self.m_dot_cross_H2O / self.Nat['M_H2O'] * self.Calib['Membran_Thickness'] / self.Calib['activeArea'] / D
        self.rH_AE = nx_H2O_AE * (ptmx_out['pres'] + ptmx_in['pres']) / 2 / self.Gas.p_sat_calc((ptmx_out['temp'] + ptmx_in['temp']) / 2)
        return ptmx_out

class BZ_Cooling():
    def __init__(self, para, Nat, Calib):
        self.para = para
        self.Nat = Nat
        self.Calib = Calib
    def __call__(self, ptm_in):
        ptm_out = copy.deepcopy(ptm_in)
        ptm_out['m_dot'] = ptm_in['m_dot'] * (1 - self.Calib['mx_ZwK'])
        ptm_out['V_dot'] = ptm_in['V_dot'] * (1 - self.Calib['mx_ZwK'])
        self.V_dot_norm = np.clip(ptm_out['V_dot'] / self.para['V_dot_max_Ku_BZ'], 0, 1)
        ptm_out['temp'] = ptm_in['temp'] + self.para['dtemp_FC']
        #self.dpres = self.Calib['C_dpres_Co'] * (0.001 * self.Calib['C_dpres_BZ_Co'] * (3831.488409573302 * np.exp(1.323312587042635 * self.V_dot_norm) - 3796.5002968674007)) #Ballard_MCmoveXD
        self.dpres = 0.00001 * (3831.488409573302 * np.exp(1.323312587042635 * (self.V_dot_norm + 1) / 2) - 3796.5002968674007) #Ballard_MCmoveXD
        ptm_out['pres'] = ptm_in['pres'] - self.dpres

        return ptm_out
