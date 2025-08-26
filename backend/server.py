from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from typing import List
from models import ContactMessage, ContactMessageCreate, ContactMessageResponse
from database import database
from portfolio_data import PORTFOLIO_DATA

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app without a prefix
app = FastAPI(
    title="Chindhamani's Portfolio API",
    description="Backend API for portfolio website with contact form and data management",
    version="1.0.0"
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Portfolio Routes
@api_router.get("/")
async def root():
    return {"message": "Portfolio API is running", "status": "active"}

@api_router.get("/portfolio")
async def get_portfolio_data():
    """Get complete portfolio data"""
    return {
        "success": True,
        "data": PORTFOLIO_DATA
    }

@api_router.get("/portfolio/{section}")
async def get_portfolio_section(section: str):
    """Get specific portfolio section data"""
    if section not in PORTFOLIO_DATA:
        raise HTTPException(status_code=404, detail=f"Section '{section}' not found")
    
    return {
        "success": True,
        "section": section,
        "data": PORTFOLIO_DATA[section]
    }

# Contact Form Routes
@api_router.post("/contact", response_model=ContactMessageResponse)
async def create_contact_message(message_data: ContactMessageCreate):
    """Submit a new contact form message"""
    try:
        # Create contact message in database
        contact_message = await database.create_contact_message(message_data)
        
        return ContactMessageResponse(
            success=True,
            message="Thank you for your message! I'll get back to you soon.",
            contact_id=contact_message.id
        )
        
    except Exception as e:
        logging.error(f"Error creating contact message: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to send message. Please try again later."
        )

@api_router.get("/contact/messages", response_model=List[ContactMessage])
async def get_contact_messages(limit: int = 50, skip: int = 0):
    """Get all contact messages (admin endpoint)"""
    try:
        messages = await database.get_contact_messages(limit=limit, skip=skip)
        return messages
    except Exception as e:
        logging.error(f"Error retrieving contact messages: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve messages"
        )

@api_router.get("/contact/messages/{message_id}", response_model=ContactMessage)
async def get_contact_message(message_id: str):
    """Get a specific contact message"""
    try:
        message = await database.get_contact_message_by_id(message_id)
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        return message
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving contact message: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve message"
        )

@api_router.patch("/contact/messages/{message_id}/status")
async def update_message_status(message_id: str, status: str):
    """Update message status (read/unread/replied)"""
    try:
        valid_statuses = ["unread", "read", "replied"]
        if status not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Must be one of: {valid_statuses}"
            )
        
        success = await database.update_message_status(message_id, status)
        if not success:
            raise HTTPException(status_code=404, detail="Message not found")
        
        return {"success": True, "message": f"Status updated to {status}"}
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating message status: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to update message status"
        )

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


