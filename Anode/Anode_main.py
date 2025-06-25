from Anode.Tankventil import Tankventil
from Kathode.Brennstoffzelle import BZ_A
from Anode.Drainventil import Wasserabscheider
from Anode.Purgeventil import Purge
from Anode.Rezirkulationsgeblaese import Rezirkulationsgeblaese
from Outsourced.Effizienzen import Eff
from Outsourced.Gasberechnungen import Gas

class Anode():
    def __init__(self, para, Nat, Kathode, Calib):
        self.Kathode = Kathode
        self.para = para
        self.Nat = Nat
        self.Calib = Calib

        self.Tank_Valve = Tankventil(para=self.para, Nat=self.Nat, Kathode=self.Kathode)
        self.BZ_A = BZ_A(para=self.para, Nat=self.Nat, Kathode=self.Kathode, Calib=self.Calib)
        self.Drain_Valve = Wasserabscheider(para=self.para, Nat=self.Nat)
        self.Rezi = Rezirkulationsgeblaese(para=self.para, Nat=self.Nat, Calib=self.Calib)
        self.Purge_Valve = Purge(para=self.para, Nat=self.Nat)

        self.Eff = Eff(para=self.para, Nat=self.Nat)
        self.Gas = Gas(para=self.para, Nat=self.Nat)

    def __call__(self, I_St, Temp_BZ):
        self.ptmx = {"Init": {"temp": self.Kathode.ptmx['BZ_in']['temp'], "pres": self.Kathode.ptmx['BZ_in']['pres'] + self.para['opres_A'], "nx_H2O": min(self.rH_FC_in,1) * self.Gas.p_sat_calc(self.Kathode.ptmx['BZ_in']['temp']) / (self.Kathode.ptmx['BZ_in']['pres'] + self.para['opres_A'])}}
        self.ptmx['Init'] |= {"nx_O2": 0, "nx_H2": (1 - self.ptmx['Init']['nx_H2O']) * self.para['mean_H2'], "nx_N2": (1 - self.para['mean_H2']) * (1 - self.ptmx['Init']['nx_H2O'])}
        self.ptmx['Init'] |= {"n_dot": self.Eff.H2_Need(m_O2_in=self.Kathode.ptmx['BZ_in']['mx_O2'] * self.Kathode.ptmx['BZ_in']['m_dot'],
                                                        m_O2_out=self.Kathode.ptmx['BZ_out']['mx_O2'] * self.Kathode.ptmx['BZ_out']['m_dot']) * self.para['st_A'] / self.ptmx['Init']['nx_H2'] / self.Nat['M_H2']}
        self.ptmx['Init'] |= {"m_dot": self.ptmx['Init']['n_dot'] * self.Gas.M_Gasgemisch_nx_calc(self.ptmx['Init'])}
        self.ptmx['Init'] |= {"V_dot": self.Gas.Volumen_calc(self.ptmx['Init']),
                              "mx_H2O": self.ptmx['Init']['nx_H2O'] * self.Nat['M_H2O'] / self.Gas.M_Gasgemisch_nx_calc(self.ptmx['Init']),
                              "mx_H2": self.ptmx['Init']['nx_H2'] * self.Nat['M_H2'] / self.Gas.M_Gasgemisch_nx_calc(self.ptmx['Init']),
                              "mx_O2": self.ptmx['Init']['nx_O2'] * self.Nat['M_O2'] / self.Gas.M_Gasgemisch_nx_calc(self.ptmx['Init']),
                              "mx_N2": self.ptmx['Init']['nx_N2'] * self.Nat['M_N2'] / self.Gas.M_Gasgemisch_nx_calc(self.ptmx['Init']),
                              "rH":  min(self.rH_FC_in,1)
                              }
        self.ptmx |= {'BZ_in': self.ptmx['Init']}

        i = 0
        accuracy = 0.0001
        self.Last_mx_H2O = 1
        while (self.ptmx['BZ_in']['mx_H2O'] * (1 - accuracy) > self.Last_mx_H2O or self.Last_mx_H2O > self.ptmx['BZ_in']['mx_H2O'] * (1 + accuracy)) and i <= 100:
            self.Last_mx_H2O = self.ptmx['BZ_in']['mx_H2O']
            self.ptmx |= {'BZ_out': self.BZ_A(self.ptmx['BZ_in'],
                                                           I_St=I_St,
                                                           ptmx_Ka=self.Kathode.ptmx['BZ_out'],
                                                           Temp_BZ=Temp_BZ)}
            self.ptmx |= {'Wasserabsch_in': self.ptmx['BZ_out']}
            self.ptmx |= {'Wasserabsch_out': self.Drain_Valve(self.ptmx['Wasserabsch_in'], self.BZ_A.H2Oliquid_m_dot_A_2)}
            self.ptmx |= {'Purgev_in': self.ptmx['Wasserabsch_out']}
            self.ptmx |= {'Purgev_out': self.Purge_Valve(self.ptmx['Purgev_in'], n_dot_Diffu_N2=self.BZ_A.n_dot_Diffu_N2)}
            self.ptmx |= {'Rezi_in_1': self.ptmx['Purgev_out']}
            self.ptmx |= {'Tankv_out': self.Tank_Valve(self.ptmx["Init"],
                                                            m_H2_need=self.Eff.m_H2_Need,
                                                            m_H2_purge=self.Purge_Valve.m_dot_H2_purge)}
            self.ptmx |= {'Rezi_in_2': self.ptmx['Tankv_out']}
            self.ptmx |= {'Rezi_out': self.Rezi(ptmx_Pu=self.ptmx['Rezi_in_1'],
                                                ptmx_TV=self.ptmx['Rezi_in_2'])}
            self.ptmx |= {'BZ_in': self.ptmx['Rezi_out']}

            i += 1
        self.rH_FC_in = self.BZ_A.rH_AE