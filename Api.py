import requests
import urllib.parse

clave = "8d02a856-921f-43b9-b68a-053035085b3b"  # Reemplazar con tu clave de API

def geolocalizacion(ubicacion, clave):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": ubicacion, "limit": "1", "key": clave})
    datos_respuesta = requests.get(url)
    json_datos = datos_respuesta.json()
    json_estado = datos_respuesta.status_code
    if json_estado == 200 and len(json_datos["hits"]) != 0:
        lat = json_datos["hits"][0]["point"]["lat"]
        lng = json_datos["hits"][0]["point"]["lng"]
        ciudad = json_datos["hits"][0].get("city", ubicacion)  # Si no hay ciudad, usar la ubicación ingresada
        region = json_datos["hits"][0].get("state", None)
        pais = json_datos["hits"][0].get("country", None)
    else:
        lat, lng, ciudad, region, pais = None, None, ubicacion, None, None  # Usar la ubicación ingresada como ciudad
    return lat, lng, ciudad, region, pais

while True:
    print("\n\n===================================================")
    print("EVA 2, ITEM 2.1 | Javier Riquelme - Bastian Martorell".center(50))
    print("===================================================\n\n")
    loc1 = input("Ingrese la ubicación de partida (o escriba 's' para salir): ")
    if loc1.lower() == "s" or loc1.lower() == "salir":
        break
    orig_lat, orig_lng, orig_ciudad, orig_region, orig_pais = geolocalizacion(loc1, clave)
    if orig_lat is not None:
        print("\n-Latitud:", orig_lat)
        print("-Longitud:", orig_lng)
        print("-Ciudad:", orig_ciudad)
        print("-Región:", orig_region)
        print("-País:", orig_pais)
        print("\n===================================================")
    else:
        print("No se pudo obtener la geolocalización para la ubicación de partida.")

    loc2 = input("\nIngrese el destino (o escriba 's' para salir): ")
    if loc2.lower() == "s" or loc2.lower() == "salir":
        break
    dest_lat, dest_lng, dest_ciudad, dest_region, dest_pais = geolocalizacion(loc2, clave)
    if dest_lat is not None:
        print("\n-Latitud:", dest_lat)
        print("-Longitud:", dest_lng)
        print("-Ciudad:", dest_ciudad)
        print("-Región:", dest_region)
        print("-País:", dest_pais)
        print("\n===============================================")
        print("TERMINO DEL PROCESO".center(50))
        print("===============================================\n")

    else:
        print("No se pudo obtener la geolocalización para el destino.")
