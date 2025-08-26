# Static portfolio data - extracted from resume
# This will serve as the backend data source until dynamic updates are needed

PORTFOLIO_DATA = {
    "personal": {
        "name": "Chindhamani Nachiappan",
        "title": "Backend Developer",
        "location": "Sunnyvale, CA",
        "email": "nchindhamani@gmail.com",
        "linkedin": "https://www.linkedin.com/in/chindhamani-nachiappan-59a979bb/",
        "photo": "https://customer-assets.emergentagent.com/job_portfolio-revival/artifacts/xq8t7kke_my_passport_size_photo.jpg",
        "tagline": "Experienced developer ready to return to tech after focused career development",
        "summary": "7+ years of professional software development experience with strong backend expertise in Python, Oracle PL/SQL, and MySQL. Recently certified in Python programming and actively upskilling to return to the tech industry with enhanced capabilities."
    },
    
    "experience": [
        {
            "id": 1,
            "company": "Tata Consultancy Services (TCS)",
            "role": "IT Analyst",
            "duration": "Nov 2010 – Sep 2017",
            "location": "India & USA",
            "projects": [
                {
                    "client": "Cisco",
                    "role": "Developer",
                    "duration": "Apr 2015 – Sep 2017",
                    "location": "Bangalore, India",
                    "achievements": [
                        "Designed and optimized backend logic for web-based team calendar",
                        "Improved response time from 9s to 0.2s",
                        "Developed 10 triggers, 8 procedures, and 2 functions in MySQL",
                        "Used Flask and Python for frontend/backend logic"
                    ],
                    "techStack": ["Python", "Flask", "MySQL", "PyCharm", "MySQL Workbench"]
                },
                {
                    "client": "Huntington Bank",
                    "role": "Developer", 
                    "duration": "Oct 2016 – Mar 2017",
                    "location": "Bangalore, India",
                    "achievements": [
                        "Developed optimized PL/SQL code and implemented business logic",
                        "Resolved defects and participated in Agile stand-ups",
                        "Maintained client communication and sync meetings"
                    ],
                    "techStack": ["Oracle PL/SQL", "Python", "Excel"]
                },
                {
                    "client": "Vodafone UK",
                    "role": "Team Lead",
                    "duration": "Sep 2015 – Sep 2016", 
                    "location": "Chennai, India",
                    "achievements": [
                        "Led data migration project with team of 7 members",
                        "Wrote and reviewed PL/SQL ETL scripts",
                        "Interfaced with clients for data collection and validation",
                        "Addressed SIT/UAT defects and enhanced reconciliation processes"
                    ],
                    "techStack": ["Oracle PL/SQL", "Unix"]
                },
                {
                    "client": "CenturyLink Inc.",
                    "role": "Developer",
                    "duration": "Apr 2011 – Jul 2015",
                    "location": "Chennai, India & Dublin, Ohio",
                    "achievements": [
                        "Developed and maintained enterprise provisioning tools",
                        "Analyzed and resolved tickets with root cause analysis",
                        "Delivered client documentation including HLDs, LLDs, and test reports"
                    ],
                    "techStack": ["PowerBuilder", "Oracle PL/SQL"]
                }
            ]
        }
    ],

    "skills": {
        "languages": ["Python", "Oracle PL/SQL", "MySQL", "Unix"],
        "frameworks": ["Flask", "FastAPI", "Pandas", "NumPy", "Pytest"],
        "databases": ["Oracle 9i – 12c", "MySQL"],
        "tools": ["JIRA", "Confluence", "GitHub", "RabbitMQ", "SQL Developer", "PowerBuilder", "PyCharm", "Jupyter", "PGAdmin"],
        "cloud": ["AWS S3", "AWS EC2", "AWS IAM", "AWS Lambda"],
        "others": ["Tableau", "Excel (VLOOKUP, Pivot, Macros)", "Unix"]
    },

    "certifications": [
        {
            "title": "PCAP – Certified Associate in Python Programming",
            "year": "2023",
            "issuer": "Python Institute"
        },
        {
            "title": "Oracle Advanced PL/SQL Developer Certified Professional", 
            "year": "2016",
            "issuer": "Oracle"
        }
    ],

    "courses": [
        {
            "title": "Data Warehouse – The Ultimate Guide",
            "platform": "Udemy"
        },
        {
            "title": "RabbitMQ with Python",
            "platform": "Udemy"
        }
    ],

    "education": {
        "degree": "B.Tech in Information Technology",
        "university": "Anna University, India",
        "duration": "2006–2010",
        "cgpa": "8.25 / 10.0"
    },

    "projects": [
        {
            "title": "Team Calendar Optimization",
            "client": "Cisco",
            "description": "Backend optimization project that improved response time from 9 seconds to 0.2 seconds",
            "techStack": ["Python", "Flask", "MySQL"],
            "achievements": ["90% performance improvement", "Full-stack development", "Database optimization"]
        },
        {
            "title": "Data Migration System",
            "client": "Vodafone UK", 
            "description": "Led end-to-end data migration project with team management and client interface",
            "techStack": ["Oracle PL/SQL", "Unix"],
            "achievements": ["Team leadership", "ETL development", "Client management"]
        },
        {
            "title": "Enterprise Provisioning Tools",
            "client": "CenturyLink Inc.",
            "description": "Developed and maintained enterprise-level provisioning applications",
            "techStack": ["PowerBuilder", "Oracle PL/SQL"],
            "achievements": ["Enterprise software", "Documentation", "Support & maintenance"]
        }
    ]
}