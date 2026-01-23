from fastapi import FastAPI ,Request
from app.routes.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="AI Chatbot",
    description="AI-power chatbot API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(chat_router)


templates =Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def chat_ui(request:Request):
    return templates.TemplateResponse("chat.html",{"request":request})
