from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from PIL import Image
from rembg import remove
import io

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    # Lire l'image envoyée
    input_bytes = await file.read()

    # Détourage avec rembg (U²-Net)
    output_bytes = remove(input_bytes)

    # Retourner l'image PNG détourée
    return Response(
        content=output_bytes,
        media_type="image/png"
    )
