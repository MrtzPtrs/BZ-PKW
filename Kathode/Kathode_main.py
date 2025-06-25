from Kathode.Luftfilter import Luftfilter
from Kathode.Verdichter import Verdichter
from Kathode.Zwischenkuehler import Zwischenkuehler_Kathode
from Kathode.Bypass_Ventil import Bypass
from Kathode.Brennstoffzelle import BZ_C
from Kathode.Shutdown_Ventil import Shutdown

from Outsourced.Effizienzen import Eff
from Outsourced.Gasberechnungen import Gas

class Kathode():

    def __init__(self, para, Nat, Calib):

        self.para = para
        self.Nat = Nat
        self.Calib = Calib

        self.Luftfilter = Luftfilter(para=self.para, Nat=self.Nat, Calib=self.Calib)
        self.Comp = Verdichter(para=self.para, Nat=self.Nat, Calib=self.Calib)
        self.Intercooler = Zwischenkuehler_Kathode(para=self.para, Nat=self.Nat, Calib=self.Calib)
        self.Bypass = Bypass(para=self.para, Nat=self.Nat, Calib=self.Calib)
        self.BZ_C = BZ_C(para=self.para, Nat=self.Nat, Calib=self.Calib)
        self.Shutvalve = Shutdown(para=self.para, Nat=self.Nat)
        self.Eff = Eff(para=self.para, Nat=self.Nat)
        self.Gas = Gas(para=self.para, Nat=self.Nat)

    def __call__(self, I_St, I_St_min, n_dot_Diffu_N2, m_dot_cross_H2O, rH_An, Temp_BZ, P_Heat_BZ):
        self.ptmx = {
            "Sys_in": {"temp": self.para['temp_env'], "pres": self.para['pres_env'],"rH": self.para['rH_env']}}
        self.ptmx['Sys_in'] |= {"mx_H2O": self.Gas.mx_H2O_start(rH=self.ptmx['Sys_in']['rH']),
                                "mx_H2": self.Gas.mx_n_start(mx_old=self.Nat['mx_H2'], rH=self.ptmx['Sys_in']['rH']),
                                "mx_O2": self.Gas.mx_n_start(mx_old=self.Nat['mx_O2'], rH=self.ptmx['Sys_in']['rH']),
                                "mx_N2": self.Gas.mx_n_start(mx_old=self.Nat['mx_N2'], rH=self.ptmx['Sys_in']['rH']),
                                "nx_H2O": self.Gas.nx_n_start(mx_n=self.Gas.mx_H2O_start(rH=self.ptmx['Sys_in']['rH'])                       , M_n=self.Nat['M_H2O'], rH=self.ptmx['Sys_in']['rH']),
                                "nx_H2": self.Gas.nx_n_start(mx_n=self.Gas.mx_n_start(mx_old=self.Nat['mx_H2'], rH=self.ptmx['Sys_in']['rH']), M_n=self.Nat['M_H2'], rH=self.ptmx['Sys_in']['rH']),
                                "nx_O2": self.Gas.nx_n_start(mx_n=self.Gas.mx_n_start(mx_old=self.Nat['mx_O2'], rH=self.ptmx['Sys_in']['rH']), M_n=self.Nat['M_O2'], rH=self.ptmx['Sys_in']['rH']),
                                "nx_N2": self.Gas.nx_n_start(mx_n=self.Gas.mx_n_start(mx_old=self.Nat['mx_N2'], rH=self.ptmx['Sys_in']['rH']), M_n=self.Nat['M_N2'], rH=self.ptmx['Sys_in']['rH'])}
        self.ptmx['Sys_in'] |= {"m_dot": max(self.Calib['NumCells'] * max(I_St, I_St_min) * self.para['st_C'] / (self.Nat['el_O2'] * self.Nat['Faraday']) / self.ptmx['Sys_in']['mx_O2'] * self.Nat['M_O2'], self.Calib['m_dot_min_Comp'])}
        self.ptmx['Sys_in'] |= {"n_dot": self.ptmx['Sys_in']['m_dot'] * self.ptmx['Sys_in']['mx_O2'] / self.Nat['M_O2'] / self.ptmx['Sys_in']['nx_O2']}
        self.ptmx['Sys_in'] |= {"V_dot": self.Gas.Volumen_calc(self.ptmx['Sys_in'])
                                }
        self.ptmx |= {'Fil_in': self.ptmx['Sys_in']}
        self.ptmx |= {'Fil_out': self.Luftfilter(self.ptmx['Fil_in'])}
        self.ptmx |= {'Comp_in': self.ptmx['Fil_out']}
        self.ptmx |= {'Comp_out': self.Comp(self.ptmx['Comp_in'])}
        self.ptmx |= {'Zwkuehl_in': self.ptmx['Comp_out']}
        self.ptmx |= {'Zwkuehl_out': self.Intercooler(self.ptmx['Zwkuehl_in'],
                                                       I_St=I_St)}
        self.ptmx |= {'Bypass_in': self.ptmx['Zwkuehl_out']}
        self.ptmx |= {'Bypass_out': self.Bypass(self.ptmx['Bypass_in'],
                                                       I_St=I_St)}
        self.ptmx |= {'BZ_in': self.ptmx['Bypass_out']}
        self.ptmx |= {'BZ_out': self.BZ_C(self.ptmx['BZ_in'],
                                                       I_St=I_St,
                                                       m_dot_Diffu_N2=n_dot_Diffu_N2 * self.Nat['M_N2'],
                                                       m_dot_cross_H2O=m_dot_cross_H2O,
                                                       rH_An=rH_An,
                                                       Temp_BZ=Temp_BZ,
                                                       P_Heat=P_Heat_BZ)}
        self.ptmx |= {'Shutvalve_in': self.ptmx['BZ_out']}
        self.ptmx |= {'Shutvalve_out': self.Shutvalve(self.ptmx['Shutvalve_in'],
                                                       m_dot_Bypass=self.Bypass.m_dot_Bypass)}
        self.ptmx |= {'Sys_out': self.ptmx['Shutvalve_out']}