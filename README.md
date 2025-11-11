#  Mail Microservice (FastAPI)
[ Live Demo](https://mail-microservice-dy5x.onrender.com/)

A lightweight **Email API** built with **FastAPI**, supporting JWT authentication, rate limiting, background email sending, and PostgreSQL integration.

---

##  Features
-  Send emails via SMTP  
-  JWT-based authentication  
-  Rate limiting  
-  Logging support  

---

## Setup
```bash
git clone https://github.com/<your-username>/Mail_Microservice.git
cd Mail_Microservice
pip install -r requirements.txt
uvicorn app.main:app --reload

DATABASE_URL=your_database_connection_url
JWT_SECRET_KEY=your_jwt_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SMTP_EMAIL=youremail@gmail.com
SMTP_PASS=your_app_password
> Use a **Google App Password**, not your regular Gmail password.


##  API Endpoints

| GET -`/` | Health check |
| POST -`/auth/signup` | Register a new user |
| POST - `/auth/login` | Login & receive JWT token |
| POST -`/email/send-email` | Send email (requires JWT) |

