import folium
from pyproj import CRS, Transformer
import arcpy.conversion
from algorithm import algorithm
from graphGenerator import generate_graph

arcpy.env.workspace = r"C:\Users\mikol\Desktop\PAG\MyProject1\MyProject1.gdb"
arcpy.env.overwriteOutput = True
atrakcje_shp = r"C:\Users\mikol\Desktop\PAG\PAG2-PROJ\atrakcjeTorun\attr.shp"
skjz_shp = r"C:\Users\mikol\Desktop\PAG\bdot_torun\L4_1_BDOT10k__OT_SKJZ_L.shp"
# arcpy.conversion.FeatureClassToGeodatabase(atrakcje_shp, arcpy.env.workspace)
# arcpy.conversion.FeatureClassToGeodatabase(skjz_shp, arcpy.env.workspace)

atrakcjeLayer = arcpy.ListFeatureClasses("attr*")[0]
drogi_torun = arcpy.ListFeatureClasses("L4*")[0]

# kopia_drogi_torun = arcpy.management.CopyFeatures(drogi_torun, "kopia_drogi_torun")
# kopia_drogi_torun = prepare_data(kopia_drogi_torun, atrakcjeLayer)
#kopia_drogi_torun.save("kopia")
kopia_drogi_torun = arcpy.ListFeatureClasses("*torun")[0]
graph = generate_graph(kopia_drogi_torun)
path_string = algorithm(graph, [476023, 573797], [479470, 573184], 0)
path = [(int(coord.split("_")[0]), int(coord.split("_")[1])) for coord in path_string]

# Tworzenie obiektów CRS
crs_2180 = CRS.from_epsg(2180)  # EPSG:2180
crs_4326 = CRS.from_epsg(4326)  # EPSG:4326 (WGS84)

# Tworzenie transformera
transformer = Transformer.from_crs(crs_2180, crs_4326)

# Konwersja współrzędnych
path_wgs84 = [transformer.transform(y, x) for x, y in path]

# Tworzenie mapy, używając pierwszego punktu jako centrum mapy
m = folium.Map(location=path_wgs84[0], zoom_start=13)

# Dodanie trasy na mapie
folium.PolyLine(path_wgs84, color="blue", weight=5, opacity=0.7).add_to(m)

# Wyświetlenie mapy
m.show_in_browser()