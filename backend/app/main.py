from fastapi import FastAPI, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uuid
from pipeline import process_image

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

OUTPUT_DIR = Path("./outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

@app.post("/api/process")
async def process(file: UploadFile = File(...)):
    img_bytes = await file.read()
    input_path = OUTPUT_DIR / f"input_{uuid.uuid4().hex}.png"
    input_path.write_bytes(img_bytes)

    final_path = process_image(str(input_path))
    return Response(content=final_path.read_bytes(), media_type="image/png")
