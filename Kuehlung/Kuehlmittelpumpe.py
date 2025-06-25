import copy
import numpy as np
from Outsourced.Gasberechnungen import Gas
class Kuehlmittelpumpe_Ka():
    def __init__(self, para, Nat, Calib):
        self.para = para
        self.Nat = Nat
        self.Calib = Calib
        self.Gas = Gas(para=self.para, Nat=self.Nat)

    def __call__(self, ptm_in, ptmx, pres_corr=0):
        ptm_out = copy.deepcopy(ptm_in)
        ptm_out['pres'] = self.pres_Co - pres_corr
        self.V_dot_norm = ptm_out['V_dot'] / self.para['V_dot_max_Ku_C']
        self.Eff_Pump = (40/3 * self.V_dot_norm ** 2 + 40/3 * self.V_dot_norm + 35) / 100
        self.P_Cooling = ptm_out['V_dot'] * 100 * (ptm_out['pres'] - (ptm_in['pres'] - pres_corr)) / self.Eff_Pump

        return ptm_out

class Kuehlmittelpumpe_BZ():
    def __init__(self, para, Nat, Calib):
        self.para = para
        self.Nat = Nat
        self.Calib = Calib
        self.Gas = Gas(para=self.para, Nat=self.Nat)

    def __call__(self, ptm_in, pres_corr=0):
        ptm_out = copy.deepcopy(ptm_in)
        ptm_out['pres'] = self.pres_Co - pres_corr
        self.V_dot_norm = np.clip(ptm_out['V_dot'] / self.para['V_dot_max_Ku_BZ'], 0, 1)
        self.Eff_Pump = (40/3 * self.V_dot_norm ** 2 + 40/3 * self.V_dot_norm + 35) / 100
        self.P_Cooling = ptm_out['V_dot'] * 100 * (ptm_out['pres'] - (ptm_in['pres'] - pres_corr)) / self.Eff_Pump

        return ptm_out


