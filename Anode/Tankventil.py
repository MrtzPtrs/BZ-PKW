import copy
from Outsourced.Gasberechnungen import Gas
class Tankventil():
    def __init__(self, para, Nat, Kathode):
        self.Kathode = Kathode
        self.para = para
        self.Nat = Nat
        self.Gas = Gas(para=self.para, Nat=self.Nat)

    def __call__(self, ptmx_in, m_H2_need, m_H2_purge):
        ptmx_out = copy.deepcopy(ptmx_in)
        ptmx_out['mx_H2'] = 1
        ptmx_out['mx_H2O'] = 0
        ptmx_out['mx_O2'] = 0
        ptmx_out['mx_N2'] = 0
        ptmx_out['nx_H2'] = 1
        ptmx_out['nx_H2O'] = 0
        ptmx_out['nx_O2'] = 0
        ptmx_out['nx_N2'] = 0
        ptmx_out['rH'] = 0
        ptmx_out['temp'] = self.para["temp_TV"]
        ptmx_out['pres'] = self.para["opres_A"] + self.Kathode.ptmx['BZ_in']['pres']
        ptmx_out['m_dot'] = m_H2_need + m_H2_purge
        ptmx_out['n_dot'] = ptmx_out['mx_H2'] / self.Nat['M_H2'] * ptmx_out['m_dot']
        ptmx_out['V_dot'] = self.Gas.Volumen_calc(ptmx_out)

        return ptmx_out
