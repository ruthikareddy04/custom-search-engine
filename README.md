# 🔍 Custom Search Engine

A full-stack **Custom Search Engine** built using **Django** and **FastAPI**. The project crawls websites, indexes their content, and provides relevant search results through a modern web interface.

---

## 🚀 Features

- 🔎 Search indexed websites
- 🌐 Website crawling and indexing
- ⚡ FastAPI-powered Search API
- 🎯 Relevance-based search results
- 📊 Analytics Dashboard
- 📱 Responsive UI
- ☁️ Railway Deployment
- 🗄️ SQLite Database

---

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3
- Django Templates

### Backend
- Django
- FastAPI
- Python

### Database
- SQLite

### Libraries
- BeautifulSoup4
- Requests
- Uvicorn
- Pydantic

### Deployment
- Railway

### Version Control
- Git & GitHub

---

## 📂 Project Structure

```
Custom Search Engine/
│
├── custom_search_engine/
├── searchapp/
├── fastapi_backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── search.py
│   └── __init__.py
│
├── staticfiles/
├── db.sqlite3
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/ruthikareddy04/custom-search-engine.git
cd custom-search-engine
```

### Create Virtual Environment

```bash
python -m venv env
```

### Activate Virtual Environment

Windows

```bash
env\Scripts\activate
```

Linux / macOS

```bash
source env/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Django

```bash
python manage.py runserver
```

Runs at

```
http://127.0.0.1:8000
```

---

## ⚡ Run FastAPI

```bash
cd fastapi_backend
uvicorn main:app --reload --port 8001
```

Runs at

```
http://127.0.0.1:8001
```

API Documentation

```
http://127.0.0.1:8001/docs
```

---

## 🔍 Search Workflow

1. Crawl websites
2. Extract webpage content
3. Store indexed data
4. Process user query
5. FastAPI retrieves matching documents
6. Django displays ranked search results

---

## 🌐 Deployment

**Frontend:** Railway (Django)

**Backend API:** FastAPI

---

## 📸 Project Screens

- Home Page
- Search Results
- Website Indexing
- Analytics Dashboard
- FastAPI API Docs

---

## 👩‍💻 Developer

**Ruthika Pyreddy**

GitHub:
https://github.com/ruthikareddy04

---

⭐ Developed by **Ruthika Pyreddy**