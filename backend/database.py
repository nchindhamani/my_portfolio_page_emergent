from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
import os
from models import ContactMessage, ContactMessageCreate, PortfolioConfig
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        """Initialize database connection"""
        try:
            mongo_url = os.environ.get('MONGO_URL')
            if not mongo_url:
                raise ValueError("MONGO_URL environment variable not set")
            
            self.client = AsyncIOMotorClient(mongo_url)
            self.db = self.client[os.environ.get('DB_NAME', 'portfolio_db')]
            
            # Test connection
            await self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    async def disconnect(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")

    # Contact Message Operations
    async def create_contact_message(self, message_data: ContactMessageCreate) -> ContactMessage:
        """Create a new contact message"""
        try:
            contact_message = ContactMessage(**message_data.dict())
            message_dict = contact_message.dict()
            
            result = await self.db.contacts.insert_one(message_dict)
            
            if result.inserted_id:
                logger.info(f"Contact message created with ID: {contact_message.id}")
                return contact_message
            else:
                raise Exception("Failed to insert contact message")
                
        except Exception as e:
            logger.error(f"Error creating contact message: {e}")
            raise

    async def get_contact_messages(self, limit: int = 50, skip: int = 0) -> List[ContactMessage]:
        """Retrieve contact messages with pagination"""
        try:
            cursor = self.db.contacts.find().sort("created_at", -1).skip(skip).limit(limit)
            messages = await cursor.to_list(length=limit)
            
            return [ContactMessage(**message) for message in messages]
            
        except Exception as e:
            logger.error(f"Error retrieving contact messages: {e}")
            raise

    async def get_contact_message_by_id(self, message_id: str) -> Optional[ContactMessage]:
        """Get a specific contact message by ID"""
        try:
            message = await self.db.contacts.find_one({"id": message_id})
            return ContactMessage(**message) if message else None
            
        except Exception as e:
            logger.error(f"Error retrieving contact message {message_id}: {e}")
            raise

    async def update_message_status(self, message_id: str, status: str) -> bool:
        """Update the status of a contact message"""
        try:
            result = await self.db.contacts.update_one(
                {"id": message_id},
                {"$set": {"status": status}}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error updating message status: {e}")
            raise

    # Portfolio Configuration Operations (Future use)
    async def get_portfolio_section(self, section: str) -> Optional[PortfolioConfig]:
        """Get portfolio configuration for a specific section"""
        try:
            config = await self.db.portfolio_config.find_one({"section": section})
            return PortfolioConfig(**config) if config else None
            
        except Exception as e:
            logger.error(f"Error retrieving portfolio section {section}: {e}")
            raise

    async def update_portfolio_section(self, section: str, data: dict) -> PortfolioConfig:
        """Update or create portfolio configuration for a section"""
        try:
            config = PortfolioConfig(section=section, data=data)
            config_dict = config.dict()
            
            result = await self.db.portfolio_config.update_one(
                {"section": section},
                {"$set": config_dict},
                upsert=True
            )
            
            logger.info(f"Portfolio section {section} updated")
            return config
            
        except Exception as e:
            logger.error(f"Error updating portfolio section {section}: {e}")
            raise

# Global database instance
database = Database()