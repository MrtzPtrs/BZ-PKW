import copy
from Outsourced.Gasberechnungen import Gas

class Bypass():
    def __init__(self, para, Nat, Calib):
        self.para = para
        self.Nat = Nat
        self.Calib = Calib
        self.Gas = Gas(para=self.para, Nat=self.Nat)

    def __call__(self, ptmx_in, I_St):
        ptmx_out = copy.deepcopy(ptmx_in)
        ptmx_out['m_dot'] = min(self.Calib['NumCells'] * I_St * self.para['st_C'] / (self.Nat['el_O2'] * self.Nat['Faraday']) / ptmx_out['mx_O2'] * self.Nat['M_O2'], ptmx_in['m_dot'])
        ptmx_out['n_dot'] = ptmx_out['m_dot'] / self.Gas.M_Gasgemisch_mx_calc(ptmx_out)
        ptmx_out['V_dot'] = self.Gas.Volumen_calc(ptmx_out)
        self.m_dot_Bypass = ptmx_in['m_dot'] - ptmx_out['m_dot']
        return ptmx_out