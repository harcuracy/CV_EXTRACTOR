from fastapi import FastAPI, UploadFile, File, HTTPException
from io import BytesIO
import uvicorn
import anyio

from main import main  

app = FastAPI(title="CV LLM API")

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.post("/CV_LLM")
async def cv_llm(file: UploadFile = File(...)):
    # Validate file extension
    if not file.filename.lower().endswith((".pdf", ".docx", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF, DOCX, TXT files are allowed")

    # Read file into memory
    file_content = await file.read()
    if len(file_content) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="File too large (max 10 MB)")

    file_like = BytesIO(file_content)
    file_like.name = file.filename  # Needed for extension detection

    # Run main() in a thread to avoid blocking
    try:
        data_dict = await anyio.to_thread.run_sync(lambda: main(file_like))
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return data_dict

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)