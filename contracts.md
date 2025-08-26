# Backend Integration Contracts

## Overview
This document outlines the API contracts and integration strategy for Chindhamani's portfolio website, transitioning from mock data to a fully functional backend.

## Current Mock Data Structure

### Contact Form Mock (`mockContactSubmit`)
**Location**: `/app/frontend/src/mock.js`
**Current Implementation**: Simulates form submission with 1-second delay
**Mock Response**: 
```javascript
{
  success: true,
  message: "Thank you for your message! I'll get back to you soon."
}
```

### Portfolio Data Mock (`portfolioData`)
**Location**: `/app/frontend/src/mock.js`
**Static Data**: Contains all professional information extracted from resume
**Sections**: personal, experience, skills, certifications, courses, education, projects

## Backend Implementation Plan

### 1. Database Models

#### ContactMessage Model
```python
class ContactMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
    subject: str
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="unread")  # unread, read, replied
```

#### Portfolio Data Model (Optional - for future dynamic updates)
```python
class PortfolioConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    section: str  # personal, experience, skills, etc.
    data: dict  # JSON data for the section
    last_updated: datetime = Field(default_factory=datetime.utcnow)
```

### 2. API Endpoints

#### Contact Form API
- **POST** `/api/contact`
  - **Input**: ContactMessageCreate (name, email, subject, message)
  - **Output**: ContactMessage with success confirmation
  - **Validation**: Email format, required fields, message length
  - **Storage**: Save to MongoDB contacts collection

- **GET** `/api/contact/messages` (Admin only - future)
  - **Output**: List of contact messages
  - **Pagination**: Support for large message volumes

#### Portfolio Data API (Static for now)
- **GET** `/api/portfolio`
  - **Output**: Complete portfolio data structure
  - **Source**: Return same data as current mock but from backend
  - **Caching**: Consider response caching for performance

### 3. Frontend Integration Points

#### Contact Form (`/app/frontend/src/components/Portfolio.jsx`)
**Current Mock Call**:
```javascript
const result = await mockContactSubmit(formData);
```

**New Backend Call**:
```javascript
const response = await axios.post(`${API}/contact`, formData);
```

**Error Handling**:
- Network errors: Display user-friendly message
- Validation errors: Show field-specific errors
- Success: Show confirmation toast

#### Portfolio Data Loading (Future Enhancement)
**Current Implementation**: Direct import from mock.js
**Future Backend Integration**: 
```javascript
useEffect(() => {
  const fetchPortfolioData = async () => {
    const response = await axios.get(`${API}/portfolio`);
    setPortfolioData(response.data);
  };
  fetchPortfolioData();
}, []);
```

### 4. Validation & Error Handling

#### Backend Validation
- Email format validation
- Required field checks
- Message length limits (min: 10, max: 1000 characters)
- Rate limiting for contact form submissions

#### Frontend Error States
- Form validation before submission
- Loading states during API calls
- Success/error toast notifications
- Graceful fallback for API failures

### 5. Database Collections

#### contacts
```json
{
  "_id": "ObjectId",
  "id": "uuid",
  "name": "string",
  "email": "string",
  "subject": "string", 
  "message": "string",
  "created_at": "datetime",
  "status": "string"
}
```

#### portfolio_config (Future)
```json
{
  "_id": "ObjectId",
  "id": "uuid",
  "section": "string",
  "data": "object",
  "last_updated": "datetime"
}
```

### 6. Security Considerations
- Input sanitization for all contact form fields
- Rate limiting to prevent spam submissions
- CORS configuration for frontend domain
- Basic validation on all endpoints

### 7. Implementation Priority
1. **Phase 1**: Contact form backend (immediate)
2. **Phase 2**: Portfolio data API (optional enhancement)
3. **Phase 3**: Admin interface for managing messages (future)

## Integration Testing Plan
1. Test contact form submission with valid data
2. Test validation with invalid email formats
3. Test error handling for network failures
4. Verify toast notifications work correctly
5. Test form reset after successful submission

## Success Criteria
- Contact form submitting successfully to backend
- Messages stored in MongoDB
- Proper error handling and user feedback
- No breaking changes to existing UI/UX
- Form remains responsive and user-friendly