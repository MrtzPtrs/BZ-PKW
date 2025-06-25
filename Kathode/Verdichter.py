import copy
import numpy as np
from Outsourced.Gasberechnungen import Gas

class Verdichter():
    def __init__(self, para, Nat, Calib):
        self.para = para
        self.Nat = Nat
        self.Calib = Calib
        self.Gas = Gas(para=self.para, Nat=self.Nat)

    def __call__(self, ptmx_in):
        self.m_dot_norm = np.clip(ptmx_in['m_dot'] / self.para['m_dot_max_C'],0,1)
        #Funktionsschar auf Basis des Rotrex
        self.Eff_Comp = np.clip((0.66107306 * self.para['presrat_comp']**4 - 6.38872182 * self.para['presrat_comp']**3 + 22.58738023 * self.para['presrat_comp']**2 - 34.00381123 * self.para['presrat_comp'] + 16.86762954) * self.m_dot_norm**2 + (-0.70664882 * self.para['presrat_comp']**4 + 6.79141544 * self.para['presrat_comp']**3 - 24.10032979 * self.para['presrat_comp']**2 + 36.98175407 * self.para['presrat_comp'] - 19.26757402) * self.m_dot_norm + (-0.03638384 * self.para['presrat_comp'] + 0.49209596),0.1,0.99)

        p_rat_max = 0.010196950904586943 * ptmx_in['m_dot'] - 0.0022654748123404366 * np.exp(0.08663492403812725*(ptmx_in['m_dot']-82.82017567323848)) +1.0560025993378848 #kombinierte Surgeline und Chokeline
        self.p_rat = min(p_rat_max, self.para['presrat_comp'])
        ptmx_out = copy.deepcopy(ptmx_in)
        ptmx_out['pres'] = self.p_rat * ptmx_in['pres']
        ptmx_out['temp'] = (ptmx_in['temp'] * (ptmx_out['pres'] / ptmx_in['pres']) ** ((self.Gas.kappa_calc(ptmx_in) - 1) / self.Gas.kappa_calc(ptmx_in)) - ptmx_in['temp']) / self.Eff_Comp + ptmx_in['temp']
        ptmx_out['V_dot'] = ptmx_in['V_dot'] * ptmx_out['temp'] / ptmx_in['temp'] * ptmx_in['pres'] / ptmx_out['pres']
        ptmx_out['rH'] = ptmx_out['nx_H2O'] * ptmx_out['pres'] / self.Gas.p_sat_calc(ptmx_out['temp'])
        self.P_Comp = ptmx_in['m_dot'] * self.Gas.C_p_Gas(ptmx_in) * ptmx_in['temp'] * ((ptmx_out['pres'] / ptmx_in['pres']) ** ((self.Gas.kappa_calc(ptmx_in) - 1) / self.Gas.kappa_calc(ptmx_in)) - 1) / self.Eff_Comp
        self.P_Comp_Engine = self.P_Comp / self.Calib['Eff_C_CompEng']
        self.P_Comp_Heat = self.P_Comp_Engine - self.P_Comp
        return ptmx_out

class Engine_Cooling():
    def __init__(self, para, Nat, Calib):
        self.para = para
        self.Nat = Nat
        self.Calib = Calib
        self.Gas = Gas(para=self.para, Nat=self.Nat)

    def __call__(self, ptm_in, ptmx, P_Comp_Heat):
        ptm_out = copy.deepcopy(ptm_in)
        ptm_out['temp'] = ptm_in['temp'] + P_Comp_Heat / self.Gas.C_p_Liquid() / ptm_in['m_dot']
        self.V_dot_norm = ptm_out['V_dot'] / self.para['V_dot_max_Ku_C']
        #self.dpres = min(0.3, self.Calib['C_dpres_Co'] * (0.1335533960400235 * np.exp(1.5683931800002318 * self.V_dot_norm) - 0.1335533960400235))
        self.dpres = 0.1335533960400235 * np.exp(1.5683931800002318 * ((self.V_dot_norm + 1) / 2)) - 0.1335533960400235
        ptm_out['pres'] = ptm_in['pres'] - self.dpres
        return ptm_out