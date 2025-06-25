import copy
from Outsourced.Gasberechnungen import Gas

class Shutdown():
    def __init__(self, para, Nat):
        self.para = para
        self.Nat = Nat
        self.Gas = Gas(para=self.para, Nat=self.Nat)

    def __call__(self, ptmx_in, m_dot_Bypass):
        ptmx_out = copy.deepcopy(ptmx_in)
        ptmx_out['pres'] = self.para['pres_env']
        ptmx_out['m_dot'] = ptmx_in['m_dot'] + m_dot_Bypass
        ptmx_out['temp'] = (ptmx_in['temp'] * (ptmx_out['pres'] / ptmx_in['pres']) ** ((self.Gas.kappa_calc(ptmx_in) - 1) / self.Gas.kappa_calc(ptmx_in)) - ptmx_in['temp']) + ptmx_in['temp']
        ptmx_out['n_dot'] = ptmx_out['m_dot'] / self.Gas.M_Gasgemisch_mx_calc(ptmx_out)
        ptmx_out['V_dot'] = self.Gas.Volumen_calc(ptmx_out)
        ptmx_out['rH'] = ptmx_out['nx_H2O'] * ptmx_out['pres'] / self.Gas.p_sat_calc(ptmx_out['temp'])
        return ptmx_out