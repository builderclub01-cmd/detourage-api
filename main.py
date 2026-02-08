from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from PIL import Image
import io

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    # Lire l'image envoyée
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")

    # (pour l'instant) on ne fait rien sur l'image
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return Response(
        content=buffer.getvalue(),
        media_type="image/png"
    )
