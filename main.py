from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
from PIL import Image
import io

app = FastAPI(title="Detourage API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ⚠️ SESSION REMBG CRÉÉE UNE SEULE FOIS
session = new_session("u2net")

@app.get("/")
def root():
    return {"status": "ok", "message": "API de détourage en ligne"}

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    try:
        input_bytes = await file.read()

        image = Image.open(io.BytesIO(input_bytes)).convert("RGBA")

        # 👇 utilisation de la session
        result = remove(image, session=session)

        output = io.BytesIO()
        result.save(output, format="PNG")
        output.seek(0)

        return Response(
            content=output.read(),
            media_type="image/png"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
