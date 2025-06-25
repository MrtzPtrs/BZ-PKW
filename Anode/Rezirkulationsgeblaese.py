import copy
import numpy as np

from Outsourced.Gasberechnungen import Gas

class Rezirkulationsgeblaese():
    def __init__(self, para, Nat, Calib):
        self.para = para
        self.Nat = Nat
        self.Calib = Calib
        self.Gas = Gas(para=self.para, Nat=self.Nat)

    def __call__(self, ptmx_TV, ptmx_Pu):
        self.m_dot_norm = np.clip(ptmx_Pu['m_dot'] / self.para["m_dot_max_A"],0,1)
        self.presrat_Rezi = ptmx_TV['pres'] / ptmx_Pu['pres']
        self.Eff_Rezi = (133.31202792 * self.presrat_Rezi**4 - 687.98840844 * self.presrat_Rezi**3 + 1330.04133171 * self.presrat_Rezi**2 - 1142.93521501 * self.presrat_Rezi + 367.28944631) * self.m_dot_norm**2 + (-105.88385704 * self.presrat_Rezi**4 + 554.12732821 * self.presrat_Rezi**3 - 1091.5098634 * self.presrat_Rezi**2 + 961.20966678 * self.presrat_Rezi - 318.14917149) * self.m_dot_norm + (2.15836998 * self.presrat_Rezi**2 -6.41103957 * self.presrat_Rezi + 4.89893857)
        ptmx_out = copy.deepcopy(ptmx_TV)
        ptmx_out['pres'] = ptmx_TV['pres']
        self.temp_Rezi_out = (ptmx_Pu['temp'] * (ptmx_out['pres'] / ptmx_Pu['pres']) ** ((self.Gas.kappa_calc(ptmx_Pu) - 1) / self.Gas.kappa_calc(ptmx_Pu)) - ptmx_Pu['temp']) / self.Eff_Rezi + ptmx_Pu['temp']
        ptmx_out['m_dot'] = ptmx_TV['m_dot'] + ptmx_Pu['m_dot']
        ptmx_out['n_dot'] = ptmx_Pu['n_dot'] + ptmx_TV['n_dot']
        if ptmx_out['m_dot'] > 0:
            ptmx_out['temp'] = (ptmx_TV['m_dot'] * ptmx_TV['temp'] * self.Gas.C_p_Gas(ptmx_TV) + ptmx_Pu['m_dot'] * self.temp_Rezi_out * self.Gas.C_p_Gas(ptmx_Pu)) / (ptmx_TV['m_dot'] * self.Gas.C_p_Gas(ptmx_TV) + ptmx_Pu['m_dot'] * self.Gas.C_p_Gas(ptmx_Pu))
            ptmx_out['mx_H2'] = (ptmx_TV['mx_H2'] * ptmx_TV['m_dot'] + ptmx_Pu['mx_H2'] * ptmx_Pu['m_dot']) / ptmx_out['m_dot']
            ptmx_out['mx_N2'] = ptmx_Pu['mx_N2'] * ptmx_Pu['m_dot'] / ptmx_out['m_dot']
            ptmx_out['mx_O2'] = ptmx_Pu['mx_O2'] * ptmx_Pu['m_dot'] / ptmx_out['m_dot']
            ptmx_out['mx_H2O'] = ptmx_Pu['mx_H2O'] * ptmx_Pu['m_dot'] / ptmx_out['m_dot']
            ptmx_out['nx_H2'] = (ptmx_TV['nx_H2'] * ptmx_TV['n_dot'] + ptmx_Pu['nx_H2'] * ptmx_Pu['n_dot']) / ptmx_out['n_dot']
            ptmx_out['nx_O2'] = ptmx_Pu['nx_O2'] * ptmx_Pu['n_dot'] / ptmx_out['n_dot']
            ptmx_out['nx_N2'] = ptmx_Pu['nx_N2'] * ptmx_Pu['n_dot'] / ptmx_out['n_dot']
            ptmx_out['nx_H2O'] = 1 - (ptmx_out['nx_O2'] + ptmx_out['nx_N2'] + ptmx_out['nx_H2'])
        ptmx_out['V_dot'] = self.Gas.Volumen_calc(ptmx_out)
        ptmx_out['rH'] = max(self.Nat['eps'], ptmx_out['nx_H2O'] * ptmx_out['pres'] / self.Gas.p_sat_calc(ptmx_out['temp']))

        self.rH_Rezi_out = ptmx_Pu['nx_H2O'] * ptmx_out['pres'] / self.Gas.p_sat_calc(self.temp_Rezi_out)
        self.P_Rezi = ptmx_Pu['m_dot'] * self.Gas.C_p_Gas(ptmx_Pu) * self.temp_Rezi_out * ((ptmx_out['pres'] / ptmx_Pu['pres']) ** ((self.Gas.kappa_calc(ptmx_Pu) - 1) / self.Gas.kappa_calc(ptmx_Pu)) - 1) / 0.7
        return ptmx_out