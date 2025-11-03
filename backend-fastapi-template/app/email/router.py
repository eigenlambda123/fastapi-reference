from fastapi import APIRouter, BackgroundTasks, HTTPException
from .utils import send_email

router = APIRouter(prefix="/email", tags=["email"])

@router.post("/send-test")
async def send_test_email(background_tasks: BackgroundTasks, recipient: str):
    """
    Send a test email asynchronously.
    """
    subject = "Hackathon Boilerplate Test Email"
    body = """
    <h2>Hackathon Boilerplate Email Test</h2>
    <p>Dabalyu!</p>
    """
    background_tasks.add_task(send_email, subject, [recipient], body)
    return {"message": f"Email to {recipient} is being sent in background."}
