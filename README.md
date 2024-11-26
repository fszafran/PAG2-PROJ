# Projekt: Implementacja i wizualizacja działania algorytmu A*
Algorytm A* zaimplementowany został w języku Python z wykorzystaniem struktur danych optymalizujących czas wykonywania: [algorithm.py](https://github.com/fszafran/PAG2-PROJ/blob/main/algorithm.py). Nasza implementacja zakłada parametryzację, pozwalającą na wybór rodzaju trasy: 
- trasa najszybsza
- trasa najkrótsza
- trasa specjalna - trasa przebiegająca przy największej liczbie atrakcji (przyjęty promień 25m wokół drogi)

Projekt zakładał także stworzenie grafu, na podstawie sieci drogowej w formie pliku .shp. Graf został wygenerowany zgodnie z podejściem obiektowym [HelperClasses.py](https://github.com/fszafran/PAG2-PROJ/blob/main/HelperClasses.py) i jest reprezentowany i używany w formie pliku .json [graph.json](https://raw.githubusercontent.com/fszafran/PAG2-PROJ/refs/heads/main/graph.json). W zaimplementowanej wersji graf został wygenerowany dla sieci drogowej miasta Toruń, pobranej z bazy danych przestrzennych BDOT10k.

Wizualizacja wykonana została przy pomocy frameworka [pyscript](https://pyscript.net/) oraz biblioteki JavaScript [Leaflet](https://leafletjs.com/)
<div align="center">
  <img src="https://github.com/user-attachments/assets/cc279d88-36de-48bc-933d-9b8133aa21fb">
</div>



