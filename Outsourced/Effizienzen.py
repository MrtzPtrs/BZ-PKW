class Eff():
    def __init__(self, para, Nat):
        self.para = para
        self.Nat = Nat
        self.P_Netto = 0
    def H2_Need(self, m_O2_in, m_O2_out):
        self.m_H2_Need = (m_O2_in - m_O2_out) * 2 * self.Nat['M_H2'] / self.Nat['M_O2']
        return self.m_H2_Need

    def P_Netto_calc(self, P_Brutto, P_CompEng, P_Anode=0, P_Cooling=0):
        self.P_Netto = P_Brutto - P_CompEng - P_Anode - P_Cooling
        return self.P_Netto

    def Eff_calc(self, m_O2_in, m_O2_out, P_Brutto, P_CompEng, P_Anode, m_H2_purge=0, P_Cooling=0):
        if P_Brutto == 0:
            self.Eff = 0
        else:
            self.Eff = Eff.P_Netto_calc(self, P_Brutto, P_CompEng, P_Anode, P_Cooling) / ((Eff.H2_Need(self, m_O2_in, m_O2_out) + m_H2_purge) * self.Nat['Hi_H2'])
        return self.Eff