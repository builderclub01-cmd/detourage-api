from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove

app = FastAPI(title="Detourage API")

# --------------------
# CORS (obligatoire pour le frontend)
# --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # autorise tous les frontends (OK pour maintenant)
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# Routes
# --------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "API de détourage en ligne"}

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    try:
        # Lire l'image envoyée
        input_bytes = await file.read()

        # Détourage IA (rembg / U²-Net)
        output_bytes = remove(input_bytes)

        # Retourner l'image PNG détourée
        return Response(
            content=output_bytes,
            media_type="image/png"
        )

    except Exception as e:
        # Sécurité : éviter un crash silencieux
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
