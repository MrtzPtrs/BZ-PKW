import copy
from Outsourced.Gasberechnungen import Gas

class Purge():
    def __init__(self, para, Nat):
        self.para = para
        self.Nat = Nat
        self.Gas = Gas(para=self.para, Nat=self.Nat)

    def __call__(self, ptmx_in, n_dot_Diffu_N2):
        ptmx_out = copy.deepcopy(ptmx_in)
        if ptmx_out['m_dot'] > 0:
            self.n_dot_purge = n_dot_Diffu_N2 / ptmx_in['nx_N2']
            self.m_dot_purge = self.n_dot_purge * self.Gas.M_Gasgemisch_nx_calc(ptmx_out)
            ptmx_out['n_dot'] = ptmx_in['n_dot'] - self.n_dot_purge
            self.n_dot_H2_purge = self.n_dot_purge * ptmx_out['nx_H2']
            self.m_dot_H2_purge = self.n_dot_H2_purge * self.Nat['M_H2']
            ptmx_out['m_dot'] = ptmx_in['m_dot'] * ptmx_out['n_dot'] / ptmx_in['n_dot']
            ptmx_out['V_dot'] = self.Gas.Volumen_calc(ptmx_out)
        else:
            self.n_dot_purge = 0
            self.m_dot_purge = 0
            self.n_dot_H2_purge = 0
            self.m_dot_H2_purge = 0

        return ptmx_out