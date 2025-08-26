from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime
from enum import Enum

class MessageStatus(str, Enum):
    UNREAD = "unread"
    READ = "read"
    REPLIED = "replied"

class ContactMessageCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Contact's full name")
    email: EmailStr = Field(..., description="Valid email address")
    subject: str = Field(..., min_length=5, max_length=200, description="Message subject")
    message: str = Field(..., min_length=10, max_length=1000, description="Message content")

class ContactMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    subject: str
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: MessageStatus = Field(default=MessageStatus.UNREAD)

    class Config:
        use_enum_values = True

class ContactMessageResponse(BaseModel):
    success: bool
    message: str
    contact_id: Optional[str] = None

class PortfolioSection(str, Enum):
    PERSONAL = "personal"
    EXPERIENCE = "experience"
    SKILLS = "skills"
    CERTIFICATIONS = "certifications"
    EDUCATION = "education"
    PROJECTS = "projects"

class PortfolioConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    section: PortfolioSection
    data: dict
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True