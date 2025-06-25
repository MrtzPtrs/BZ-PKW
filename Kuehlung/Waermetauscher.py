import copy
import numpy as np
from Outsourced.Gasberechnungen import Gas

class Waermetauscher_Ka():
    def __init__(self, para, Nat, Calib):
        self.para = para
        self.Nat = Nat
        self.Calib = Calib

    def __call__(self, ptm_in, ptmx, P_Ka):
        ptm_out = copy.deepcopy(ptm_in)
        ptm_out['temp'] = self.para['temp_interc']
        self.dpres_WTau = 0.0024637799584740065 * np.exp(0.00765884974194413 * ptm_in['m_dot'] / 1000 * 60) - 0.0024637799584740065
        self.pres_WTau_out = ptm_in['pres'] - self.dpres_WTau
        return ptm_out


class Waermetauscher_BZ():
    def __init__(self, para, Nat, Calib):
        self.para = para
        self.Nat = Nat
        self.Calib = Calib
        self.Gas = Gas(para=self.para, Nat=self.Nat)

    def __call__(self, ptm_in, P_BZ_Heat_Cool, Temp_Coolant_HT, P_Max_WTau):
        ptm_out = copy.deepcopy(ptm_in)
        if ptm_in['m_dot'] > 0:
            self.m_dot_WTau = min(P_BZ_Heat_Cool / P_Max_WTau * ptm_in['m_dot'], ptm_in['m_dot'])
            self.m_dot_Bypass = ptm_in['m_dot'] - self.m_dot_WTau
            self.V_dot_WTau = ptm_in['V_dot'] * self.m_dot_WTau / ptm_in['m_dot']
            self.V_dot_Bypass = ptm_in['V_dot'] * self.m_dot_Bypass / ptm_in['m_dot']
            ptm_out['temp'] = Temp_Coolant_HT - self.para['dtemp_FC'] / 2
            self.dpres_WTau = 0.0024637799584740065 * np.exp(0.00765884974194413 * self.m_dot_WTau / 1000 * 60) - 0.0024637799584740065
            ptm_out['pres'] = ptm_in['pres'] - self.dpres_WTau
        return ptm_out

        #Berechnung der kalten Seite
        # self.T_Wtau_out = (ptm_in['m_dot'] * self.para['dtemp_FC'] + self.m_dot_WTau * ptm_in['temp']) / self.m_dot_WTau
        # dT_min = self.T_Wtau_out - self.para['temp_env']
        # dT_max = 2 * dT_min
        # dT_mlog = P_BZ_Heat / (self.Calib['k_WTau'] * self.Calib['actA_WTau'])
        # Null = self.Calib['C_WTau'] * (dT_max - dT_min) - dT_mlog * np.log(dT_max / dT_min)
        #
        # i = 0
        # accuracy = 1E-5
        # VZ_old = 1
        # VZ_new = 0
        # increment = 0.5
        # while (Null > 0 + accuracy or Null < 0 - accuracy) and i <= 100:
        #     Null = self.Calib['C_WTau'] * (dT_max - dT_min) - dT_mlog * np.log(dT_max / dT_min)
        #     if Null > 0 + accuracy:
        #         dT_min = dT_min * (1 - increment)
        #         VZ_new = 1
        #     if Null < 0 - accuracy:
        #         dT_min = dT_min * (1 + increment)
        #         VZ_new = 0
        #     if VZ_old != VZ_new:
        #         increment = increment / 2
        #     VZ_old = VZ_new
        #     i += 1
        # self.temp_air_out = ptm_in['temp'] - dT_max
        #
        # self.m_dot_air = P_BZ_Heat / (self.Gas.C_p_Gas(ptmx_air) * (self.temp_air_out - self.para['temp_env']))
        # self.V_dot_air = self.m_dot_air / self.Gas.rho_gas_calc(ptmx_air)
        # self.v_dot_air = self.V_dot_air / self.Calib['A_WTau']
        # self.P_fan = max(0, 0.5 * self.m_dot_air * (self.v_dot_air ** 2 - self.para['vehicle_speed']) ** 2) / self.Calib['Eff_Fan']
