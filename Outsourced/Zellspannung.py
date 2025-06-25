"""Kathode (C) [ -0-> Luftfilter (I) -1-> Kompressor (II) -2-> Zwischenkühler (III) -3-> Befeuchter A (IV) -4-> BZ (V) -5-> Befeuchter B (VI) -6-> Expander (VII) -7-> ]"""
import numpy as np
import math

class Zellspannung():
    def __init__(self, Calib, Nat):
        self.Calib = Calib
        self.Nat = Nat
    def Lambda_calc(self, rH):
        # Kulikovsky, Andrei A.: Chapter 1 - Fuel cell basics. In: Kulikovsky, Andrei A. (Herausgeber): Analytical Modelling of Fuel Cells, Seiten 1 – 38. Elsevier, Amsterdam, 2010
        Lambda = 0.3 + 6 * rH * (1 - math.tanh(rH - 0.5)) + 3.9 * rH ** 0.5 * (1 + math.tanh((rH - 0.89) / 0.23))
        return Lambda
    def Lambda_Mem_calc(self, rH_An, rH_Ka):
        Lambda_Mem = (self.Lambda_calc(rH_An) + self.Lambda_calc(rH_Ka)) / 2
        return Lambda_Mem

    def Membranleitwert(self, rH_Ka, rH_An):
        if self.Lambda_Mem_calc(rH_An, rH_Ka) < 1.253:
            Leitwert = 0
        else:
            Leitwert = (0.005738 * self.Lambda_Mem_calc(rH_An, rH_Ka) - 0.007192) * 100

        Leitwert = max(Leitwert, 0.2)
        return Leitwert
    def U_Cell_calc(self, ptmx_in, ptmx_out, I_St, rH_An, Temp_BZ, rH_KE):
        # James Larminie Oxford Brookes University UK, Andrew Dicks University of Queensland Australia(Former Principal Scientist, BG Technology, UK)
        p_O2_ref = ptmx_in['pres'] * ptmx_in['nx_O2']
        p_O2 = (ptmx_in['pres'] + ptmx_out['pres']) / 2 * (ptmx_in['nx_O2'] + ptmx_out['nx_O2']) / 2

        i = I_St / (self.Calib['activeArea'] * 10000)

        self.U_Ideal = self.Nat['EN_O'] - self.Nat['EN_H']

        if ptmx_in['m_dot'] != 0:
            #self.U_ohm = (i + self.Calib['i_cross']) * self.Calib['Membran_Thickness'] / self.Membranleitwert(rH_Ka=(ptmx_in['rH'] + ptmx_out['rH'])/2, rH_An=rH_An) * self.Calib['C_ohm']
            self.U_ohm = (i + self.Calib['i_cross']) * self.Calib['Membran_Thickness'] / self.Membranleitwert(rH_Ka=rH_KE, rH_An=rH_An) * self.Calib['C_ohm']

            self.U_act = max(0, self.Calib['A'] * np.log((i + self.Calib['i_cross']) / (self.Calib['C_i0'] * p_O2_ref * 2E-2)))   # - 0.0015 2E-7 * 1E+5 wegen bar/ Pa
            self.U_act = self.U_act * (self.Calib['Temp_BZ_Soll'] / Temp_BZ) ** self.Calib['C_Tempcorr']

            self.n_emp = self.Calib['C_n'] * (0.0001340428 * np.log(p_O2_ref / p_O2) + 0.000062629589) * (1.6574 - p_O2_ref)
            self.U_conc = self.Calib['C_m'] * np.exp(self.n_emp * (i + self.Calib['i_cross']))
        else:
            self.U_ohm = 0
            self.U_conc = 0
            self.U_act = 0

        self.U_Cell = max(self.Nat['eps'], self.U_Ideal - (self.U_act + self.U_ohm + self.U_conc))

        return self.U_Cell

