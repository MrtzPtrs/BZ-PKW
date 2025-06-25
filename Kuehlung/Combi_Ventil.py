import copy
from Outsourced.Gasberechnungen import Gas
class Combi_Valve():
    def __init__(self, para, Nat, Calib):
        self.para = para
        self.Nat = Nat
        self.Calib = Calib

        self.Gas = Gas(para=self.para, Nat=self.Nat)
    def __call__(self, ptm_BZ, ptm_ZwK):
        ptm_out = copy.deepcopy(ptm_BZ)
        ptm_out['m_dot'] = ptm_BZ['m_dot'] + ptm_ZwK['m_dot']
        ptm_out['V_dot'] = ptm_out['m_dot'] / self.Gas.rho_liquid_calc()
        ptm_out['pres'] = min(ptm_BZ['pres'], ptm_ZwK['pres'])
        ptm_out['temp'] = (ptm_ZwK['temp'] * ptm_ZwK['m_dot'] + ptm_BZ['temp'] * ptm_BZ['m_dot']) / (ptm_out['m_dot'])
        return ptm_out