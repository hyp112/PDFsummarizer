# app/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pdf_utils import extract_text_from_pdf
from model import summarize_text

app = FastAPI()

# CORS設定（ローカルやStreamlitからのリクエストを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番では限定するのが望ましい
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/summarize")
async def summarize_pdf(file: UploadFile = File(...)):
    try:
        # PDFからテキストを抽出
        text = extract_text_from_pdf(file)

        if len(text.strip()) == 0:
            raise HTTPException(status_code=400, detail="PDFにテキストが含まれていません")

        # LLMで要約
        summary = summarize_text(text)

        return {"summary": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"処理中にエラーが発生しました: {str(e)}")
