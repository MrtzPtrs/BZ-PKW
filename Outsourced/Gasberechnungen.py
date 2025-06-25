import numpy as np
class Gas():
    def __init__(self, para, Nat):
        self.para = para
        self.Nat = Nat

    def p_sat_calc(self, temp_act):
        # Hyland, R.W.und A.Wexler: Formulations for the thermodynamic properties of the saturated phase of H2O from 173.15 to 473.15 K, 1983
        A = -5800.2206
        B = 1.3914993
        C = -0.048640239
        D = 0.000041764768
        E = -0.000000014452093
        F = 6.545973
        p_sat = np.exp(A / temp_act + B + C * temp_act + D * pow(temp_act, 2) + E * pow(temp_act, 3) + F * np.log(temp_act)) / 100000
        return p_sat #bar

    def rH_to_TP(self, rH, temp_act):
        if rH != 0:
            temp_act=temp_act-273.15 #M.Bahr
            a=7.5
            b=237.3
            SDD=6.1078*pow(10,((a*temp_act)/(b+temp_act)))
            DD=rH*SDD
            v=np.log10(DD/6.1078)
            TP=b*v/(a-v)
            TP=273.15+TP
        else:
            TP = 0.1
        return TP

    def mx_H2O_start(self, rH):
        M_dry = self.Nat['M_O2'] * self.Nat['mx_O2'] + self.Nat['M_N2'] * self.Nat['mx_N2'] + self.Nat['M_H2'] * self.Nat['mx_H2']
        TP = self.rH_to_TP(rH=rH, temp_act=self.para['temp_env'])
        p_dry = self.para['pres_env'] - self.p_sat_calc(temp_act=TP)
        mx_H2O = self.Nat['M_H2O'] * self.p_sat_calc(temp_act=TP)/(M_dry*p_dry * (1 + self.Nat['M_H2O'] * self.p_sat_calc(temp_act=TP)/(M_dry * p_dry)))
        return mx_H2O

    def mx_n_start(self, mx_old, rH):
        mx_new = mx_old * (1 - self.mx_H2O_start(rH=rH))
        return mx_new

    def nx_n_start(self, mx_n, M_n, rH):
        nx_n = mx_n / (M_n * (self.mx_H2O_start(rH=rH) / self.Nat['M_H2O'] + self.mx_n_start(self.Nat['mx_O2'], rH=rH) / self.Nat['M_O2'] + self.mx_n_start(self.Nat['mx_N2'], rH=rH) / self.Nat['M_N2'] + self.mx_n_start(self.Nat['mx_H2'], rH=rH) / self.Nat['M_H2']))
        return nx_n

    def M_Gasgemisch_nx_calc(self, ptmx):
        return ptmx['nx_O2'] * self.Nat['M_O2'] + ptmx['nx_H2'] * self.Nat['M_H2'] + ptmx['nx_N2'] * self.Nat['M_N2'] + ptmx['nx_H2O'] * self.Nat['M_H2O']

    def M_Gasgemisch_mx_calc(self, ptmx):
        return 1 / (ptmx['mx_O2'] / self.Nat['M_O2'] + ptmx['mx_H2'] / self.Nat['M_H2'] + ptmx['mx_N2'] / self.Nat['M_N2'] + ptmx['mx_H2O'] / self.Nat['M_H2O'])

    def Volumen_calc(self, ptmx):
        return ptmx['n_dot'] * self.Nat['NormVol'] * ptmx['temp'] / self.Nat['NormTemp'] * self.Nat['NormPres'] / ptmx['pres']

    def kappa_calc(self, ptmx):
        R_s = self.Nat['Avogadro'] * self.Nat['Boltzmann'] / self.M_Gasgemisch_nx_calc(ptmx)
        kappa = self.C_p_Gas(ptmx) / (self.C_p_Gas(ptmx) - R_s)
        return kappa

    def C_p_Gas(self, ptmx): #Annahme: c_p-Werte sind temperaturkonstant
        R_s = self.Nat['Avogadro'] * self.Nat['Boltzmann'] / self.M_Gasgemisch_nx_calc(ptmx)
        f = self.Nat['f_O2'] * ptmx['nx_O2'] + self.Nat['f_H2'] * ptmx['nx_H2'] + self.Nat['f_N2'] * ptmx['nx_N2'] + self.Nat['f_H2O'] * ptmx['nx_H2O']
        C_p = R_s * (f / 2 + 1)  # Näherung
        return C_p

    def C_p_Liquid(self): #Annahme: c_p-Werte sind temperaturkonstant
        return self.Nat['c_p_H2O'] * (1 - self.para['w_glyk']) + self.Nat['c_p_Glykol'] * self.para['w_glyk']

    def rho_gas_calc(self, ptmx):
        return ptmx['pres'] * self.M_Gasgemisch_nx_calc(ptmx) / (self.Nat['Avogadro'] * self.Nat['Boltzmann'] * ptmx['temp'])

    def rho_liquid_calc(self):
        return 1/((1 - self.para['w_glyk'])/self.Nat['rho_H2O'] + self.para['w_glyk']/self.Nat['rho_Glykol']) * 1000

    def rho_air_calc(self):
        return self.Nat['rho_air_0'] * (1 - self.para['height'] / 44300) ** 4.256 #abgeleitet aus idealem Gasgesetz und barometrischer Höhenformel

    def pres_air_calc(self):
        return self.Nat['pres_air_0'] * (1 - self.para['height'] / 44300) ** 5.256 #barometrische Höhenformel