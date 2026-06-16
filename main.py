from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import uvicorn
import sylvia_processor

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    
    # Вызов логики из sylvia_processor
    reply = sylvia_processor.get_ai_response(user_message)
    
    return {"reply": reply}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
