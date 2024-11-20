from fastapi import FastAPI, Form, UploadFile, File
import os
import uuid
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/fotos")
async def guarda_foto(
    nombre: str = Form(...),
    direccion: str = Form(...),
    vip: bool = Form(False),
    fotografia: UploadFile = File(...)
):
    print("Nombre:", nombre)
    print("Dirección:", direccion)
    print("VIP:", vip)

    home_usuario = os.path.expanduser("~")  # Home del usuario
    carpeta_vip = os.path.join(home_usuario, "fotos-usuarios-vip")
    carpeta_no_vip = os.path.join(home_usuario, "fotos-usuarios")
    carpeta_destino = carpeta_vip if vip else carpeta_no_vip

    os.makedirs(carpeta_destino, exist_ok=True)

    # Generar un nombre único para la foto
    nombre_archivo = uuid.uuid4()  # Nombre en formato hexadecimal
    extension_foto = os.path.splitext(fotografia.filename)[1]
    ruta_imagen = os.path.join(carpeta_destino, f"{nombre_archivo}{extension_foto}")

    print("Guardando la foto en", ruta_imagen)

    with open(ruta_imagen, "wb") as imagen:
        contenido = await fotografia.read()
        imagen.write(contenido)

    # Respuesta al cliente
    respuesta = {
        "Nombre": nombre,
        "Dirección": direccion,
        "VIP": vip,
        "Ruta": ruta_imagen
    }

    return JSONResponse(content=respuesta)

