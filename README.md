# Personal Blog Project
# Personal Blog with Flask

[![Deployed on Render](https://img.shields.io/badge/Render-Deployed-brightgreen)](https://personal-blog-tue5.onrender.com/)

A full-featured personal blog with admin panel, built with Python Flask. Deployed on Render with persistent storage.

## Features ✨

- **Guest View**:
  - Read published articles
  - Clean, responsive design

- **Admin Panel**:
  - Secure login (username/password)
  - Create/edit/delete articles
  - Manage publishing dates

- **Tech Stack**:
  - Python Flask (Backend)
  - HTML/CSS (Frontend)
  - Render (Hosting)
  - File-based/MongoDB storage

## Live Demo 🌐
Access the live site:  
https://your-render-url.onrender.com

**Admin Credentials**:  
👤 Username: 
🔑 Password: 

## Installation 💻
1. Clone repo:
   ```bash
   git clone https://github.com/your-username/personal_blog.git
   cd personal_blog


Create virtual environment:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


Install dependencies:
bash
pip install -r requirements.txt

Run locally:
bash
python app.py

Deployment :
This project is configured for easy deployment on:
Render.com
PythonAnywhere
Railway.app


Project structure:
personal_blog/
├── app.py                # Main application
├── requirements.txt      # Dependencies
├── runtime.txt           # Python version
├── articles/             # Article storage (or DB)
├── templates/            # HTML templates
│   ├── admin/            # Admin panel templates
│   ├── guest/            # Public pages
│   └── base.html         # Base template
└── static/               # CSS/JS/assets
