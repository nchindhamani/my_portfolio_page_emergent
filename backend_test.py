#!/usr/bin/env python3
"""
Backend Testing Suite for Chindhamani's Portfolio Website
Tests all backend APIs, database operations, and validation logic
"""

import asyncio
import aiohttp
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, List
import uuid

# Add backend directory to path for imports
sys.path.append('/app/backend')

class PortfolioBackendTester:
    def __init__(self):
        # Get backend URL from frontend .env file
        self.base_url = self._get_backend_url()
        self.session = None
        self.test_results = []
        
    def _get_backend_url(self) -> str:
        """Get backend URL from frontend .env file"""
        try:
            with open('/app/frontend/.env', 'r') as f:
                for line in f:
                    if line.startswith('REACT_APP_BACKEND_URL='):
                        return line.split('=', 1)[1].strip()
        except Exception as e:
            print(f"Warning: Could not read frontend .env file: {e}")
        
        # Fallback to default
        return "https://portfolio-revival.preview.emergentagent.com"
    
    async def setup(self):
        """Initialize test session"""
        self.session = aiohttp.ClientSession()
        print(f"🚀 Starting backend tests for: {self.base_url}")
        print("=" * 60)
    
    async def teardown(self):
        """Clean up test session"""
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name: str, status: str, details: str = "", response_data: Any = None):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_emoji} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
        if response_data and status == "FAIL":
            print(f"   Response: {response_data}")
        print()
    
    async def test_api_health(self):
        """Test API root endpoint health"""
        try:
            async with self.session.get(f"{self.base_url}/api/") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("message") == "Portfolio API is running" and data.get("status") == "active":
                        self.log_test("API Health Check", "PASS", "API is running and responsive")
                    else:
                        self.log_test("API Health Check", "FAIL", f"Unexpected response format", data)
                else:
                    self.log_test("API Health Check", "FAIL", f"HTTP {response.status}", await response.text())
        except Exception as e:
            self.log_test("API Health Check", "FAIL", f"Connection error: {str(e)}")
    
    async def test_portfolio_data_api(self):
        """Test portfolio data endpoints"""
        # Test complete portfolio data
        try:
            async with self.session.get(f"{self.base_url}/api/portfolio") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success") and "data" in data:
                        portfolio_data = data["data"]
                        required_sections = ["personal", "experience", "skills", "certifications", "education", "projects"]
                        missing_sections = [section for section in required_sections if section not in portfolio_data]
                        
                        if not missing_sections:
                            self.log_test("Portfolio Data API - Complete", "PASS", 
                                        f"All {len(required_sections)} sections present")
                        else:
                            self.log_test("Portfolio Data API - Complete", "FAIL", 
                                        f"Missing sections: {missing_sections}")
                    else:
                        self.log_test("Portfolio Data API - Complete", "FAIL", "Invalid response format", data)
                else:
                    self.log_test("Portfolio Data API - Complete", "FAIL", 
                                f"HTTP {response.status}", await response.text())
        except Exception as e:
            self.log_test("Portfolio Data API - Complete", "FAIL", f"Request error: {str(e)}")
        
        # Test individual sections
        sections_to_test = ["personal", "experience", "skills", "invalid_section"]
        for section in sections_to_test:
            try:
                async with self.session.get(f"{self.base_url}/api/portfolio/{section}") as response:
                    if section == "invalid_section":
                        # Should return 404 for invalid section
                        if response.status == 404:
                            self.log_test(f"Portfolio Section API - {section}", "PASS", 
                                        "Correctly returns 404 for invalid section")
                        else:
                            self.log_test(f"Portfolio Section API - {section}", "FAIL", 
                                        f"Expected 404, got {response.status}")
                    else:
                        # Should return 200 for valid sections
                        if response.status == 200:
                            data = await response.json()
                            if data.get("success") and data.get("section") == section and "data" in data:
                                self.log_test(f"Portfolio Section API - {section}", "PASS", 
                                            "Section data retrieved successfully")
                            else:
                                self.log_test(f"Portfolio Section API - {section}", "FAIL", 
                                            "Invalid response format", data)
                        else:
                            self.log_test(f"Portfolio Section API - {section}", "FAIL", 
                                        f"HTTP {response.status}", await response.text())
            except Exception as e:
                self.log_test(f"Portfolio Section API - {section}", "FAIL", f"Request error: {str(e)}")
    
    async def test_contact_form_api(self):
        """Test contact form API with various scenarios"""
        
        # Test 1: Valid contact form submission
        valid_contact_data = {
            "name": "Chindhamani Test User",
            "email": "test@example.com",
            "subject": "Test message from automated testing",
            "message": "This is a test message to verify the contact form functionality is working properly."
        }
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/contact",
                json=valid_contact_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success") and "contact_id" in data:
                        self.log_test("Contact Form - Valid Submission", "PASS", 
                                    f"Message submitted successfully with ID: {data.get('contact_id')}")
                        # Store contact_id for later tests
                        self.test_contact_id = data.get('contact_id')
                    else:
                        self.log_test("Contact Form - Valid Submission", "FAIL", 
                                    "Invalid response format", data)
                else:
                    self.log_test("Contact Form - Valid Submission", "FAIL", 
                                f"HTTP {response.status}", await response.text())
        except Exception as e:
            self.log_test("Contact Form - Valid Submission", "FAIL", f"Request error: {str(e)}")
        
        # Test 2: Invalid email format
        invalid_email_data = {
            "name": "Test User",
            "email": "invalid-email-format",
            "subject": "Test subject",
            "message": "This should fail due to invalid email format."
        }
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/contact",
                json=invalid_email_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 422:  # Validation error
                    self.log_test("Contact Form - Invalid Email", "PASS", 
                                "Correctly rejected invalid email format")
                else:
                    data = await response.text()
                    self.log_test("Contact Form - Invalid Email", "FAIL", 
                                f"Expected 422, got {response.status}", data)
        except Exception as e:
            self.log_test("Contact Form - Invalid Email", "FAIL", f"Request error: {str(e)}")
        
        # Test 3: Missing required fields
        missing_fields_data = {
            "name": "Test User",
            "email": "test@example.com"
            # Missing subject and message
        }
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/contact",
                json=missing_fields_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 422:  # Validation error
                    self.log_test("Contact Form - Missing Fields", "PASS", 
                                "Correctly rejected missing required fields")
                else:
                    data = await response.text()
                    self.log_test("Contact Form - Missing Fields", "FAIL", 
                                f"Expected 422, got {response.status}", data)
        except Exception as e:
            self.log_test("Contact Form - Missing Fields", "FAIL", f"Request error: {str(e)}")
        
        # Test 4: Message too short
        short_message_data = {
            "name": "Test User",
            "email": "test@example.com",
            "subject": "Short message test",
            "message": "Short"  # Less than 10 characters
        }
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/contact",
                json=short_message_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 422:  # Validation error
                    self.log_test("Contact Form - Message Too Short", "PASS", 
                                "Correctly rejected message under 10 characters")
                else:
                    data = await response.text()
                    self.log_test("Contact Form - Message Too Short", "FAIL", 
                                f"Expected 422, got {response.status}", data)
        except Exception as e:
            self.log_test("Contact Form - Message Too Short", "FAIL", f"Request error: {str(e)}")
        
        # Test 5: Message too long
        long_message_data = {
            "name": "Test User",
            "email": "test@example.com",
            "subject": "Long message test",
            "message": "A" * 1001  # More than 1000 characters
        }
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/contact",
                json=long_message_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 422:  # Validation error
                    self.log_test("Contact Form - Message Too Long", "PASS", 
                                "Correctly rejected message over 1000 characters")
                else:
                    data = await response.text()
                    self.log_test("Contact Form - Message Too Long", "FAIL", 
                                f"Expected 422, got {response.status}", data)
        except Exception as e:
            self.log_test("Contact Form - Message Too Long", "FAIL", f"Request error: {str(e)}")
    
    async def test_contact_message_retrieval(self):
        """Test contact message retrieval endpoints"""
        
        # Test getting all messages
        try:
            async with self.session.get(f"{self.base_url}/api/contact/messages") as response:
                if response.status == 200:
                    data = await response.json()
                    if isinstance(data, list):
                        self.log_test("Contact Messages - Get All", "PASS", 
                                    f"Retrieved {len(data)} messages")
                    else:
                        self.log_test("Contact Messages - Get All", "FAIL", 
                                    "Expected list response", data)
                else:
                    self.log_test("Contact Messages - Get All", "FAIL", 
                                f"HTTP {response.status}", await response.text())
        except Exception as e:
            self.log_test("Contact Messages - Get All", "FAIL", f"Request error: {str(e)}")
        
        # Test getting specific message (if we have a test contact ID)
        if hasattr(self, 'test_contact_id'):
            try:
                async with self.session.get(
                    f"{self.base_url}/api/contact/messages/{self.test_contact_id}"
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("id") == self.test_contact_id:
                            self.log_test("Contact Messages - Get Specific", "PASS", 
                                        "Retrieved specific message successfully")
                        else:
                            self.log_test("Contact Messages - Get Specific", "FAIL", 
                                        "Message ID mismatch", data)
                    else:
                        self.log_test("Contact Messages - Get Specific", "FAIL", 
                                    f"HTTP {response.status}", await response.text())
            except Exception as e:
                self.log_test("Contact Messages - Get Specific", "FAIL", f"Request error: {str(e)}")
        
        # Test getting non-existent message
        fake_id = str(uuid.uuid4())
        try:
            async with self.session.get(
                f"{self.base_url}/api/contact/messages/{fake_id}"
            ) as response:
                if response.status == 404:
                    self.log_test("Contact Messages - Non-existent", "PASS", 
                                "Correctly returns 404 for non-existent message")
                else:
                    self.log_test("Contact Messages - Non-existent", "FAIL", 
                                f"Expected 404, got {response.status}")
        except Exception as e:
            self.log_test("Contact Messages - Non-existent", "FAIL", f"Request error: {str(e)}")
    
    async def test_message_status_update(self):
        """Test message status update functionality"""
        
        if not hasattr(self, 'test_contact_id'):
            self.log_test("Message Status Update", "SKIP", "No test contact ID available")
            return
        
        # Test valid status update
        valid_statuses = ["read", "replied"]
        for status in valid_statuses:
            try:
                async with self.session.patch(
                    f"{self.base_url}/api/contact/messages/{self.test_contact_id}/status",
                    params={"status": status}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("success"):
                            self.log_test(f"Message Status Update - {status}", "PASS", 
                                        f"Status updated to {status}")
                        else:
                            self.log_test(f"Message Status Update - {status}", "FAIL", 
                                        "Update failed", data)
                    else:
                        self.log_test(f"Message Status Update - {status}", "FAIL", 
                                    f"HTTP {response.status}", await response.text())
            except Exception as e:
                self.log_test(f"Message Status Update - {status}", "FAIL", f"Request error: {str(e)}")
        
        # Test invalid status
        try:
            async with self.session.patch(
                f"{self.base_url}/api/contact/messages/{self.test_contact_id}/status",
                params={"status": "invalid_status"}
            ) as response:
                if response.status == 400:
                    self.log_test("Message Status Update - Invalid", "PASS", 
                                "Correctly rejected invalid status")
                else:
                    self.log_test("Message Status Update - Invalid", "FAIL", 
                                f"Expected 400, got {response.status}")
        except Exception as e:
            self.log_test("Message Status Update - Invalid", "FAIL", f"Request error: {str(e)}")
    
    async def test_cors_headers(self):
        """Test CORS headers are properly set"""
        try:
            async with self.session.options(f"{self.base_url}/api/") as response:
                headers = response.headers
                cors_headers = {
                    'Access-Control-Allow-Origin': headers.get('Access-Control-Allow-Origin'),
                    'Access-Control-Allow-Methods': headers.get('Access-Control-Allow-Methods'),
                    'Access-Control-Allow-Headers': headers.get('Access-Control-Allow-Headers')
                }
                
                if any(cors_headers.values()):
                    self.log_test("CORS Headers", "PASS", 
                                f"CORS headers present: {cors_headers}")
                else:
                    self.log_test("CORS Headers", "WARN", 
                                "No CORS headers found in OPTIONS response")
        except Exception as e:
            self.log_test("CORS Headers", "FAIL", f"Request error: {str(e)}")
    
    def print_summary(self):
        """Print test summary"""
        print("=" * 60)
        print("🏁 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        skipped_tests = len([r for r in self.test_results if r["status"] == "SKIP"])
        warning_tests = len([r for r in self.test_results if r["status"] == "WARN"])
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️  Warnings: {warning_tests}")
        print(f"⏭️  Skipped: {skipped_tests}")
        print()
        
        if failed_tests > 0:
            print("❌ FAILED TESTS:")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"  - {result['test']}: {result['details']}")
            print()
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 Excellent! Backend is working well.")
        elif success_rate >= 70:
            print("👍 Good! Minor issues to address.")
        else:
            print("⚠️  Needs attention! Several critical issues found.")
    
    async def run_all_tests(self):
        """Run all backend tests"""
        await self.setup()
        
        try:
            # Core API tests
            await self.test_api_health()
            await self.test_portfolio_data_api()
            
            # Contact form tests
            await self.test_contact_form_api()
            await self.test_contact_message_retrieval()
            await self.test_message_status_update()
            
            # Additional tests
            await self.test_cors_headers()
            
        finally:
            await self.teardown()
        
        self.print_summary()
        return self.test_results

async def main():
    """Main test runner"""
    print("🧪 Portfolio Backend Test Suite")
    print("Testing Chindhamani's Portfolio Website Backend")
    print("=" * 60)
    
    tester = PortfolioBackendTester()
    results = await tester.run_all_tests()
    
    # Return exit code based on test results
    failed_tests = len([r for r in results if r["status"] == "FAIL"])
    return 0 if failed_tests == 0 else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)