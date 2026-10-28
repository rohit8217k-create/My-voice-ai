import os
from pathlib import Path
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
FISH_API_KEY = os.getenv("FISH_API_KEY", "").strip()
FISH_VOICE_ID = os.getenv("FISH_VOICE_ID", "").strip()
FISH_MODEL = os.getenv("FISH_MODEL", "s2.1-pro-free").strip()

app = FastAPI(title="My Voice AI")

class TTSRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)

@app.get("/")
def home():
    return FileResponse(BASE_DIR / "index.html")

@app.get("/health")
def health():
    return {"ok": True, "api_key_configured": bool(FISH_API_KEY), "voice_id_configured": bool(FISH_VOICE_ID)}

@app.post("/api/tts")
async def tts(body: TTSRequest):
    if not FISH_API_KEY:
        raise HTTPException(status_code=503, detail="Render Environment Variables में FISH_API_KEY सेट करें।")
    if not FISH_VOICE_ID:
        raise HTTPException(status_code=503, detail="Render Environment Variables में FISH_VOICE_ID सेट करें।")
    payload = {"text": body.text.strip(), "reference_id": FISH_VOICE_ID, "format": "mp3"}
    headers = {
        "Authorization": f"Bearer {FISH_API_KEY}",
        "Content-Type": "application/json",
        "model": FISH_MODEL,
    }
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            upstream = await client.post("https://api.fish.audio/v1/tts", headers=headers, json=payload)
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Fish Audio API तक कनेक्शन नहीं हो पाया।")
    if upstream.status_code >= 400:
        # Avoid exposing API key or raw sensitive request headers.
        try:
            data = upstream.json()
            message = data.get("message") or data.get("detail") or "Fish Audio ने अनुरोध स्वीकार नहीं किया।"
        except Exception:
            message = "Fish Audio ने अनुरोध स्वीकार नहीं किया। API key, Voice ID, मॉडल और quota जाँचें।"
        raise HTTPException(status_code=upstream.status_code, detail=str(message)[:500])
    return Response(content=upstream.content, media_type=upstream.headers.get("content-type", "audio/mpeg"), headers={"Content-Disposition": 'inline; filename="my-voice.mp3"', "Cache-Control": "no-store"})
