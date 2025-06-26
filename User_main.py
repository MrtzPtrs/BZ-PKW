from PKW_main import main
from datetime import datetime
import matplotlib.pyplot as plt

if 'Eingabeparameter':
    Lastprofil = ["30km_h", "50km_h", "70km_h", "100km_h", "130km_h", "170km_h", "170km_h_1s", "WLTC", "Testlast", "RDE_Sport", "RDE_Normal", "NEDC"] #variiert das Lastprofil
    Umgebung = ['standard', 'heiß', 'kalt', 'Höhe', 'trocken'] #variiert die Zustandsgrößen der Umgenungsluft
    Steigung = ['-20%', '-10%', '0%', '10%', '20%'] #variiert die Steigung der befahrenen Straße
    Zuladung = ['0kg', '50kg', '100kg', '200kg', '500kg'] #variiert das Fahrzeuggewicht
    SoC = ['0%', '20%', '40%', '50%', '55%', '60%', '80%', '100%'] #variiert den initialen Ladestand der Batterie
    
    st_C = ['1.4', '1.5', '1.6', '1.8', '2.0', '2.2', '2.4', '2.6', '2.8'] #variiert die Stöchiometrie der Luftzufuhr (Die Stöchiometrie beschreibt das Verhältnis zwischen umgesetzem Sauerstoff und zugeführtem Sauerstoff)
    presrat_Komp = ['1.25', '1.5', '1.75', '2.0', '2.25', '2.5'] #variiert die maximale Druckaufladung des Kompressors (Die Druckaufladung hält sich dennoch an ein Kompressorkennfeld)
    t_Komp_Dynamik = ['0.5s', '1s', '1.5s', '3s', '5s', '10s', '20s'] #variiert die Hochfahrgeschwindigkeit des Kompressors, und somit das des BRennstoffzellensystems; Die wählbare Zeit beschreibt die notwendige Zeit den Kompressor von Minimal- auf Maximaldrehzahl zu drehen
    Temp_ZwK = ['50°C', '60°C', '70°C', '80°C'] #variiert die Solltemperatur des Zwischenkühlers; Dies ist gleichbedeutend mit der kathodenseitigen Stackeinlasstemperatur
    
    st_A = ['1.2', '1.5', '1.8', '2.0', '2.5', '3.0', '4.0', '5.0'] #variiert die Stöchiometrie der Anode (Die Stöchiometrie beschreibt das Verhältnis zwischen der Brennstoffzelle zugeführtem Wasserstoff und dem umgesetzten Wasserstoff)
    opres_A = ['0.1', '0.2', '0.3', '0.4', '0.5'] #variiert den Überdruck der Anode über das Kathodendruckniveau
    mean_H2 = ['75% vol', '85% vol', '95% vol'] #variiert den durchschnittlichen H2-Volumenanteil im Trockengas der Anode
    
    Temp_BZ_Init = ['kalt', 'Soll', 'heiß'] #variiert die initiale Temperatur der Brennstoffzelle
    dTemp_NT = ['5K', '10K', '15K', '20K', '25K'] #variiert den Temperaturunterschied im Niedertemperaturkreislauf
    dTemp_FC = ['5K', '10K', '15K', '20K', '25K'] #variiert den Temperaturunterschied im Hochtemperaturkreislauf
    x_Glykol = ['0% vol', '10% vol', '20% vol', '30% vol', '40% vol', '50% vol'] #variiert den Glykol-Volumenanteil der Kühlmittelsysteme

Ausgabeparameter = ['Zeit', 'Soll_Geschwindigkeit', 'Ist_Geschwindigkeit', 'Soll_Beschleunigung', 'Ist_Beschleunigung', #Fahrzeug
                    'Fahrzeug_Effizienz', 'BZ_System_Effizienz', 'BZ_Stapel_Effizienz', #Effizienzen
                    'Rad_Leistung', 'E_Motor_Soll_Leistung', 'E_Motor_Ist_Leistung', 'HV_Bus_Soll_Leistung', 'HV_Bus_Ist_Leistung', #Leistungenaufnahmen
                    'BZ_Leistung', 'BoP_Leistungsaufnahme', 'Batterie_Leistung', 'mech._Bremsleistung', #Leistungsabgaben
                    'Batterie_Ladestand', 'Zustand_Hybridsystemregelung', #Reglungszustände
                    'BZ_Maximalleistung', 'Stapel_Strom', 'Stapel_Spannung', 'Zell_Spannung', 'ohmsche Verluste', 'Aktivierungsverluste', 'Konzentrationsverluste', #Brennstoffzelle
                    'Kathoden_Massenstrom', 'Kathoden_Stapel_Massenstrom', 'Kompressor_Druckverhältnis', 'Kathoden_Druck_am_BZ_Eintritt', 'Kathoden_Druck_am_BZ_Austritt', 'Kathoden_Feuchte_am_BZ_Austritt', 'Kathoden_Feuchte_am_BZ_Eintritt', 'durchschn_BZ_Kathodenkanal_Feuchte', 'durchschn_BZ_Kathodenelektroden_Feuchte', 'BZ_Kathodenelektroden_Temperatur', 'BZ_Kathodenkanal_Temperatur', #Kathode
                    'Anoden_Massenstrom', 'H2_Injektor_Massenstrom', 'H2_Verbrauch', 'Rezirkulations_Druckverhältnis', 'Anoden_Druck_am_BZ_Eintritt', 'Anoden_Druck_am_BZ_Austritt', 'durchschn_BZ_Anodenkanal_Feuchte', 'durchschn_BZ_Anodenelektroden_Feuchte', 'BZ_Anodenkanal_Temperatur', #Anode
                    'H20_Stroffmengenstrom_durch_die_Membran', 'N2_Stroffmengenstrom_durch_die_Membran', #Diffusionseffekte
                    'BZ_Stapel_Temperatur', 'Zustand_Temperaturregelung', 'therm_BZ_Leistung', 'Zwischenkühler_Wärmeübertrag', 'Wärmeübertrag_vom_Stapel_ins_Kühlmittel', 'HT_Massenstrom', 'HT_Massenstrom_durch_den_Stapel', 'HT_Massenstrom_durch_den_Wärmetauscher', 'HT_Temperatur_niedrig', 'HT_Temperatur_hoch', 'HT_Druck', #HT-Kühlkreislauf
                    'NT_Massenstrom', 'Wechselrichter_Wärmeübertrag', 'Kompressor_Motor_Wärmeübertrag', 'NT_Druck', 'NT_Temperatur_niedrig', 'NT_Temperatur_hoch' #NT-Kühlkreislauf
                    ]

if __name__ == '__main__':
    SaveIt = True #Sollen die Plots gespeichert werden?
    savefolder = './Plots/' + str(datetime.now().date()) #Legen Sie den Speicherort fest.

    csv = False #Das Erstellen einer CSV-Datei zur Datenverarbeitung kann hier ausgeschaltet werden.

    Plots_vorgefertigt = True #Das Anzeigen aller vorgefertigeten Plots kann hier ausgeschaltet werden.

    LivePlot = False #Das Anzeigen des Live-Plots kann hier ausgeschaltet werden. (benötigt https://github.com/RadioNCN/LiveMonitor/releases/tag/v0.4.0)
    y1_live = 'Ist_Geschwindigkeit' #Hier können bis zu 3 Größen, aus der Tabelle Ausgabeparameter, ausgewählt werden, die während der Simulation in einem Plot dargestellt werden sollen. Eine gültige Eingabe für y1 ist notwendig. Die Variablen werden auf einer Skala angezeigt
    y2_live = 'Batterie_Ladestand'
    y3_live = 'BZ_Stapel_Temperatur'

    Plot_individuell = True #Das Erstellen eines individuellen Plots kann hier ausgeschaltet werden
    x_indiv = 'Stapel_Strom' #Hier können Variablen, aus der Tabelle AUsgabeparameter, ausgewählt werden, die übereinander geplottet werden sollen. Gültige Eingaben für x_indiv und y1_indiv sind notwendig.
    y1_indiv = 'Stapel_Spannung'
    y2_indiv = 'Kompressor_Druckverhältnis'
    y3_indiv = 'durchschn_BZ_Kathodenelektroden_Feuchte'

    Sim = main(Lastprofil='WLTC', Zuladung='500kg', Temp_BZ_Init='Umgebung', SoC='55%') #Initialisierung (mit Beispielvariation)
    Sim(SaveIt=SaveIt, csv=csv, Plots_vorg=Plots_vorgefertigt, Plot_indiv=Plot_individuell, Plot_Live=LivePlot, x_indiv=x_indiv, y1_indiv=y1_indiv, y2_indiv=y2_indiv, y3_indiv=y3_indiv, y1_live=y1_live, y2_live=y2_live, y3_live=y3_live) #Berechnung
    plt.show()