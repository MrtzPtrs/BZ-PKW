import copy
import numpy as np
from Outsourced.Gasberechnungen import Gas
class Luftfilter:

    def __init__(self, para, Nat, Calib):
        self.para = para
        self.Nat = Nat
        self.Calib = Calib
        self.Gas = Gas(para=self.para, Nat=self.Nat)

    def __call__ (self, ptmx_in):
        ptmx_out = copy.deepcopy(ptmx_in)
        self.V_dot_norm = np.clip(ptmx_in['V_dot'] / self.para['V_dot_max_C'], 0, 1)
        self.dpres = np.square(self.V_dot_norm / (514 * self.Calib['K_v_Filter'])) * self.Gas.rho_gas_calc(ptmx_in) * ptmx_in['temp'] / ptmx_in['pres']
        ptmx_out['pres'] = ptmx_in['pres'] - self.dpres
        ptmx_out['V_dot'] = self.Gas.Volumen_calc(ptmx_out)
        ptmx_out['rH'] = ptmx_out['nx_H2O'] * ptmx_out['pres'] / self.Gas.p_sat_calc(ptmx_out['temp'])
        return ptmx_out
