## Product Management System Backend

<div align="center">
Fast & Reliable API<br>
<img src="https://img.shields.io/badge/FastAPI-0.104.0-green" alt="FastAPI"> 
<img src="https://img.shields.io/badge/Python-3.11%2B-blue" alt="Python"> 
<img src="https://img.shields.io/badge/PostgreSQL-15%2B-blue" alt="PostgreSQL"> 
<img src="https://img.shields.io/badge/SQLModel-0.0.8-orange" alt="SQLModel"> 
<img src="https://img.shields.io/badge/FastAPI--Users-13.0%2B-yellow" alt="FastAPI Users"> 
<img src="https://img.shields.io/badge/License-MIT-green" alt="License"> 
<img src="https://img.shields.io/badge/Auth-JWT%20%7C%20OAuth2-red" alt="Auth">
</div>

**Test Users & API Documentation:**  
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### in future this how i add auth + architucture file(MVC):
```
src/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── database.py
│   └── config.py
├── users/
│   ├── __init__.py
│   ├── models.py          
│   ├── schemas.py        
│   ├── service.py        
│   └── router.py         
├── auth/
│   ├── __init__.py
│   ├── config.py
│   ├── manager.py
│   └── router.py
└── products/
    ├── __init__.py
    ├── models.py
    ├── schemas.py
    ├── service.py
    └── router.py

```
