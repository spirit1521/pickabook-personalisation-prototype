from fastapi import FastAPI, UploadFile, File, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uuid

# Try importing process_image safely
try:
    from pipeline import process_image
except ImportError:
    process_image = None
    print("Warning: pipeline.py or process_image not found. Endpoint will not work until fixed.")

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Output directory
OUTPUT_DIR = Path("./outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

@app.get("/")
def read_root():
    return {"status": "Server is running"}

@app.post("/api/process")
async def process(file: UploadFile = File(...)):
    if process_image is None:
        raise HTTPException(status_code=500, detail="process_image function not available")

    try:
        # Save uploaded file
        img_bytes = await file.read()
        input_path = OUTPUT_DIR / f"input_{uuid.uuid4().hex}.png"
        input_path.write_bytes(img_bytes)

        # Process image
        final_path = process_image(str(input_path))

        # Return processed image
        return Response(content=final_path.read_bytes(), media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")
