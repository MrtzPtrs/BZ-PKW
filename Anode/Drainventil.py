import copy
from Outsourced.Gasberechnungen import Gas

class Wasserabscheider():
    def __init__(self, para, Nat):
        self.para = para
        self.Nat = Nat
        self.Gas = Gas(para=self.para, Nat=self.Nat)

    def __call__(self, ptmx_in, m_H2O_liquid):
        ptmx_out = copy.deepcopy(ptmx_in)
        if ptmx_in['m_dot'] > 0:
            ptmx_out['m_dot'] = ptmx_in['m_dot'] - m_H2O_liquid
            m_dot_H2O = ptmx_in['mx_H2O'] * ptmx_in['m_dot'] - m_H2O_liquid
            m_dot_N2 = ptmx_in['mx_N2'] * ptmx_in['m_dot']
            m_dot_H2 = ptmx_in['mx_H2'] * ptmx_in['m_dot']
            ptmx_out['mx_N2'] = m_dot_N2 / ptmx_out['m_dot']
            ptmx_out['mx_H2'] = m_dot_H2 / ptmx_out['m_dot']
            ptmx_out['mx_H2O'] = m_dot_H2O / ptmx_out['m_dot']
            n_H2O_liquid = m_H2O_liquid / self.Nat['M_H2O']
            ptmx_out['n_dot'] = ptmx_in['n_dot'] - n_H2O_liquid
            ptmx_out['V_dot'] = self.Gas.Volumen_calc(ptmx_out)
            ptmx_out['nx_N2'] = m_dot_N2 / (self.Nat['M_N2'] * ptmx_out['n_dot'])
            ptmx_out['nx_H2'] = m_dot_H2 / (self.Nat['M_H2'] * ptmx_out['n_dot'])
            ptmx_out['nx_H2O'] = m_dot_H2O / (self.Nat['M_H2O'] * ptmx_out['n_dot'])
            ptmx_out['rH'] = ptmx_out['nx_H2O'] * ptmx_out['pres'] / self.Gas.p_sat_calc(ptmx_out['temp'])
        return ptmx_out