My Voice AI + Fish Audio backend

महत्वपूर्ण:
- API key को HTML/JavaScript में कभी न डालें।
- यह backend Fish Audio के आधिकारिक POST https://api.fish.audio/v1/tts endpoint को कॉल करता है।
- मॉडल default: s2.1-pro-free. अगर यह मॉडल आपके account/voice ID के साथ उपलब्ध न हो, Render में FISH_MODEL को Fish Audio dashboard/docs में उपलब्ध मॉडल के अनुसार बदलें।
- API usage/limits आपके Fish Audio account की शर्तों पर निर्भर हैं; पूरी तरह मुफ्त होने की गारंटी नहीं है।

Render setup:
1. GitHub repository में इस ZIP की सभी फाइलें upload करें; index.html मुख्य UI है।
2. Render > New > Web Service > GitHub repository चुनें।
3. Build Command: pip install -r requirements.txt
4. Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT
5. Environment Variables में:
   FISH_API_KEY = आपकी Fish Audio API key
   FISH_VOICE_ID = आपकी cloned voice ID
   FISH_MODEL = s2.1-pro-free
6. Deploy करें। फिर साइट पर हिंदी text डालकर Generate दबाएँ।

Health check: https://YOUR-SERVICE.onrender.com/health
यह JSON में बताएगा कि key और voice ID configure हैं या नहीं; secrets नहीं दिखाएगा।
