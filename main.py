from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
from PIL import Image
import io

app = FastAPI(title="Detourage API")

# CORS (OK pour tests frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "API de détourage en ligne"}

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    try:
        # Lire le fichier uploadé
        input_bytes = await file.read()

        # Charger l'image avec Pillow
        image = Image.open(io.BytesIO(input_bytes)).convert("RGBA")

        # Supprimer l’arrière-plan (IMPORTANT : Image PIL)
        result_image = remove(image)

        # Convertir en PNG
        output_buffer = io.BytesIO()
        result_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return Response(
            content=output_buffer.read(),
            media_type="image/png"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
