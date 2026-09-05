import os
import io
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from fastapi.concurrency import run_in_threadpool
from google import genai
from pypdf import PdfReader

from src.rule_engine import analyze_lease

# Load environment variables
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_summary_sync(lease_text: str, report: dict) -> str:
    prompt = f"""
    You are an expert legal review assistant.
    Provide a concise 3 to 4 bullet-point plain-language summary for a non-lawyer signer based on:
    Findings: {report}
    Lease Text: {lease_text}

    IMPORTANT INSTRUCTIONS:
    - Do NOT approve, reject, or advise signing.
    - Do NOT use phrases like "safe to sign" or "safe to proceed".
    - Always explicitly state that final approval must be performed by a human legal reviewer.
    """
    try:
        # Corrected: Valid Gemini Flash model name
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Summary generation failed: {str(e)}"

# Home Page GET Route
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# Diagnostic Test Route
@app.get("/test")
def test():
    return {"message": "working"}

# File Upload and Analysis POST Route
@app.post("/analyze")
async def analyze(request: Request, file: UploadFile = File(...)):
    filename = file.filename.lower()
    
    # 1. Server-side File Extension Check
    if not filename.endswith((".txt", ".pdf")):
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": "Invalid file type. Please upload a .txt or .pdf file."}
        )
        
    content = await file.read()
    
    # 2. Extract Text from PDF or TXT File
    if filename.endswith(".pdf"):
        try:
            pdf_reader = PdfReader(io.BytesIO(content))
            lease_text = ""
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    lease_text += text + "\n"
        except Exception:
            lease_text = ""
    else:
        lease_text = content.decode("utf-8", errors="ignore")
    
    # 3. Rule Engine Analysis
    report = analyze_lease(lease_text)
    
    # 4. Compliance Score Calculation
    prohibited_count = len(report.get("prohibited", []))
    deviations_count = len(report.get("deviations", []))
    missing_count = len(report.get("missing", []))
    score = 100 - (prohibited_count * 20) - (deviations_count * 15) - (missing_count * 10)
    report["score"] = max(0, score)

    # 5. Gemini AI Summary Call
    summary = await run_in_threadpool(generate_summary_sync, lease_text, report)
    report["ai_summary"] = summary

    return templates.TemplateResponse(
        request=request, 
        name="report.html", 
        context={"report": report}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)