from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
from PIL import Image
import io

app = FastAPI(title="Detourage API")

# -------------------------------------------------
# Préchargement du modèle (CRUCIAL pour Render)
# -------------------------------------------------
session = new_session("u2net")

# -------------------------------------------------
# CORS (OK large pour tests)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Routes
# -------------------------------------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "API de détourage en ligne"}

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    try:
        # Lire le fichier uploadé
        input_bytes = await file.read()

        # Convertir en image PIL
        input_image = Image.open(io.BytesIO(input_bytes)).convert("RGBA")

        # Détourage avec session préchargée
        output_image = remove(input_image, session=session)

        # Reconvertir en PNG bytes
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format="PNG")
        output_bytes = output_buffer.getvalue()

        return Response(
            content=output_bytes,
            media_type="image/png"
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
