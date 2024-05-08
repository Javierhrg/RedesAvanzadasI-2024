import requests
import urllib.parse

ruta_url = "https://graphhopper.com/api/1/route?"
clave = "8d02a856-921f-43b9-b68a-053035085b3b"

traducciones = {
    "arrive": "llegar",
    "at": "en",
    "destination": "destino",
    "turn": "gira",
    "left": "izquierda",
    "right": "derecha",
    "keep": "mantente",
    "onto": "en",
}

def geocodificacion(ubicacion, clave):
    while not ubicacion:
        ubicacion = input("Ingrese la ubicación nuevamente: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": ubicacion, "limit": "1", "key": clave})
    datos_respuesta = requests.get(url)
    json_datos = datos_respuesta.json()
    json_estado = datos_respuesta.status_code

    if json_estado == 200 and json_datos.get("hits"):
        hit = json_datos["hits"][0]
        lat = hit["point"]["lat"]
        lng = hit["point"]["lng"]
        nombre = hit["name"]
        valor = hit["osm_value"]
        pais = hit.get("country", "")
        estado = hit.get("state", "")
        nueva_ubicacion = f"{nombre}, {estado}, {pais}" if estado and pais else f"{nombre}, {pais}" if estado else nombre
    else:
        lat = lng = "null"
        nueva_ubicacion = ubicacion
        if json_estado != 200:
            print(f"Estado de la API de Geocodificación: {json_estado}\nMensaje de error: {json_datos.get('message', '')}")
    return json_estado, lat, lng, nueva_ubicacion

while True:
    print("\n\n===================================================")
    print("EVA 2, ITEM 2.2 | Javier Riquelme - Bastian Martorell".center(50))
    print("===================================================")
    print("Perfiles de vehículos disponibles en Graphhopper:")
    print("===================================================")
    print("car, bike, foot".center(50))
    print("===================================================")
    perfil = ["car", "bike", "foot"]
    vehiculo = input("\n-Ingrese un perfil de vehículo de la lista anterior (escriba 's' para salir): ").lower()
    if vehiculo in perfil:
        pass
    elif vehiculo == "s" or vehiculo == "salir":
        break
    else:
        vehiculo = "car"
        print("-No se ingresó un perfil de vehículo válido. Usando el perfil de carro.")

    for i in range(2):
        loc = input("-Ingrese la ubicación de partida (o escriba 's' para salir): " if i == 0 else "-Ingrese el destino (o escriba 's' para salir): ")
        if loc.lower() == "s" or loc.lower() == "salir":
            break
        resultado = geocodificacion(loc, clave)
        if i == 0:
            orig = resultado
        else:
            dest = resultado

    if all(result[0] == 200 for result in [orig, dest]):
        op = f"&point={orig[1]}%2C{orig[2]}"
        dp = f"&point={dest[1]}%2C{dest[2]}"
        paths_url = ruta_url + urllib.parse.urlencode({"key": clave, "vehicle": vehiculo}) + op + dp
        paths_estado = requests.get(paths_url).status_code
        paths_datos = requests.get(paths_url).json()
        print("\n===================================================")
        print(f"\n-Estado de la API de Enrutamiento: {paths_estado}\n-URL de la API de Enrutamiento:\n{paths_url}")
        print("\n===================================================")
        print(f"\nDirecciones desde {orig[3]} hasta {dest[3]} en {vehiculo}")
        print("\n===================================================\n")

        if paths_estado == 200:
            path = paths_datos["paths"][0]
            millas = round(path["distance"] / 1000 / 1.61, 1)
            km = round(path["distance"] / 1000, 1)
            sec = int(path["time"] / 1000 % 60)
            min = int(path["time"] / 1000 / 60 % 60)
            hr = int(path["time"] / 1000 / 60 / 60)
            print(f"-Distancia Recorrida: {millas:.1f} millas / {km:.1f} km")
            print(f"-Duración del Viaje: {hr:02d} horas, {min:02d} minutos, {sec:02d} segundos")
            print("\n===================================================\n")
            print("Ruta a seguir:\n")
            for instruccion in path["instructions"]:
                instruccion_texto = instruccion["text"]
                for ingles, espanol in traducciones.items():
                    instruccion_texto = instruccion_texto.replace(ingles, espanol)
                distancia = round(instruccion["distance"] / 1000, 1)
                print(f"{instruccion_texto} ({distancia:.1f} km)")
            print("\n===============================================")
            print("TERMINO DEL PROCESO".center(50))
            print("===============================================\n\n")

        else:
            print(f"Mensaje de error: {paths_datos.get('message', '')}")
            print("*******")
