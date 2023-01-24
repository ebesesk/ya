from fastapi import(
    APIRouter, Request, 
    WebSocket, WebSocketDisconnect,
    Form,
    )
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette import status
from fastapi.templating import Jinja2Templates
from datetime import datetime

from apis.utils.chat import ConnectionManager, generate_chat_id


router = APIRouter()
templates = Jinja2Templates(directory='templates')
router.mount("/static", StaticFiles(directory="static"), name="static")


manager = ConnectionManager()


@router.websocket('/{chat_id}')
async def messages(websocket: WebSocket, chat_id: str):
    await manager.connect(chat_id, websocket)
    try:
        while True:
            message = await websocket.receive_text()
            data = {
                'message': message,
                'created_at': datetime.now().strftime('%H:%M:%S'),
            }
            await manager.broadcast(chat_id, data)
    except WebSocketDisconnect:
        manager.disconnect(chat_id, websocket)



@router.get('/')
def home(request: Request):
    return templates.TemplateResponse('chat2/home.html', {'request': request})


@router.get('/new')
def create_chat():
    chat_id = generate_chat_id()
    url = f'/chats/{chat_id}'
    return RedirectResponse(url)


@router.post('/connect')
def connect_to_chat(chat_id: str = Form(...)):
    url = f'/chats/{chat_id}'
    return RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)


@router.get('/{chat_id}')
def chat(request: Request, chat_id: str):
    context = {'request': request, 'chat_id': chat_id}
    return templates.TemplateResponse('chat2/chat.html', context)

