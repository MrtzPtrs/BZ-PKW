import copy
import numpy as np
from Outsourced.Gasberechnungen import Gas

class Zwischenkuehler_Kathode:
    def __init__(self, para, Nat, Calib):
        self.para = para
        self.Nat = Nat
        self.Calib = Calib
        self.Gas = Gas(para=self.para, Nat=self.Nat)

    def __call__(self, ptmx_in, I_St):
        ptmx_out = copy.deepcopy(ptmx_in)
        if I_St > 0:
            ptmx_out['temp'] = min(self.para['temp_interc'], ptmx_in['temp'])
            self.V_dot_norm = np.clip(ptmx_in['V_dot'] / self.para['V_dot_max_C'], 0, 1)
            ptmx_out['pres'] = ptmx_out['pres'] - (0.1 / (np.e - 1) * np.exp(self.V_dot_norm) - 0.1 / (np.e - 1))
            ptmx_out['V_dot'] = self.Gas.Volumen_calc(ptmx_out)
            ptmx_out['rH'] = ptmx_out['nx_H2O'] * ptmx_out['pres'] / self.Gas.p_sat_calc(ptmx_out['temp'])

            self.P_ZwK_Heat = ptmx_out['m_dot'] * self.Gas.C_p_Gas(ptmx_in) * (ptmx_in['temp'] - ptmx_out['temp'])
            self.deltatemp_Interc = ptmx_in['temp'] - ptmx_out['temp']
        else:
            self.P_ZwK_Heat = 0
            self.deltatemp_Interc = 0
        return ptmx_out

class Zwischenkuehler_Cooling:
    def __init__(self, para, Nat, Calib):
        self.para = para
        self.Nat = Nat
        self.Calib = Calib
        self.Gas = Gas(para=self.para, Nat=self.Nat)

    def __call__(self, ptm_in, ptmx, P_ZwK_Heat):
        ptm_out = copy.deepcopy(ptm_in)
        ptm_out['m_dot'] = ptm_in['m_dot'] * self.Calib['mx_ZwK']
        ptm_out['V_dot'] = ptm_in['V_dot'] * self.Calib['mx_ZwK']
        ptm_out['temp'] = ptm_in['temp'] + P_ZwK_Heat / (ptm_out['m_dot'] * self.Gas.rho_liquid_calc())
        self.V_dot_norm = ptm_out['V_dot'] / self.para['V_dot_max_Ku_C']
        #self.dpres = min(0.3, self.Calib['C_dpres_Co'] * (0.3 / (np.e - 1 + 0.02) * np.exp(self.V_dot_norm) - 0.3 / (np.e - 1 + 0.02)))
        self.dpres = (0.03 / (np.e - 1 + 0.005) * np.exp((self.V_dot_norm + 1) / 2) - 0.03 / (np.e - 1 + 0.005))
        ptm_out['pres'] = ptm_in['pres'] - self.dpres
        return ptm_out
