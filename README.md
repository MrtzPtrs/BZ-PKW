Dies ist ein dynamisches PEM-Brennstoffzellen-Hybridfahrzeug-Modell.

## Anforderungen um das Modell zu starten:
```
Python-Version: 3.10 (getestet) 
installierte Pakete: datetime v5.5, matplotlib.pyplot v3.10.3, pandas v1.5.3, numpy v1.23.5
```

## Struktur

Strukturiert ist das Modell in ein Maskenskript (User_main.py) und ein Hauptskript (Mirai_main.py), in dem der Programmablauf programmiert ist. Die Ordner (Fahrzeugmodell, Kathode, Anode, Kuehlung) enthalten Skripts die von Hauptskript abgerufen werden. Der Ordner (Lastprofile) enthält Exceltabellen, in denen abzufahrende Geschwindigkeitsprofile hinterlegt sind. Für einen funktionierenden Programmablauf darf die Ordnerstruktur nicht verändert werden.

## Bedienung

Um das Modell zu starten öffnen Sie das Datei: User_main.py. 

### Auswahl des Ausgabeformats

Das sich öffnende Skript zeigt eine Schaltzentrale die beim Ausführen des Programms das Modell startet.
In dem Maskenskript ist es möglich beliebige graphische und tabellarische Ausgaben sich ausgeben zu lassen. Das Ein- und Ausschalten dieser ist durch die Wertzuweisung folgender Variablen mit = True oder = False möglich:

| Beschreibung | Variable |
|--|--|
| vorgefertigte Graphen: | Plots_vorgefertigt |
| individuelle Graphen:	| Plots_individuell |
| echtzeitfähige Graphen: | LivePlot |
| tabellarische Auswertung: | csv |


In den individuellen und echtzeitfähigen Auswertungen können Sie selber die Ausgabeparameter festlegen, die angezeigt werden sollen. Die Eingabe dessen erfolgt in den Variablen:
```
y1_live, y2_live, y3_live
x_indiv, y1_indiv, y2_indiv, y3_indiv
```
Es sind nur Zuweisungen auf diese Variablen zulässig, die ein Element in der Liste Ausgabeparameter (Zeile 26-37) sind. Die Zugewiesenen Variablen müssen daher als String formuliert sein. Es können bis zu 3 Ausgaben in Echtzeit dargestellt werden, sowie bis zu 3 Ausgaben über eine andere Ausgabe in den individuellen Darstellungen dargestellt werden. Wenn weniger Ausgaben in diesen gezeigt werden sollen belegen Sie die Variablen mit einem None.

### Speichern der Ausgaben

Sollen die Auswertungen gespeichert werden muss die Variable SaveIt den Inhalt True enthalten. Die Bilder und Tabellen werden dann unter dem in savefolder einstellbaren Ordnerpfad gespeichert.

### Variation der Betriebsbedingungen

Im Modell können Betriebsbedingungen des Fahrzeugs und der Brennstoffzelle variiert werden. Die Eingabe erfolgt in der Initialisierung der Klasse main (Zeile 59) per Keyword Argument. Die Keyword Arguments entsprechen den Listennamen der Eingabeparameter (Zeile 5-24) und die zuzuweisende Variable muss ein Element aus der jeweiligen Liste sein. Diese müssen als String eingegeben werden.

### Autor

Moritz Peters, ZBT GmbH
