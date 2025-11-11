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

SECRET_KEY=your_secret_key
ALGORITHM=HS256
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=youremail@gmail.com
SENDER_PASSWORD=your_app_password
> Use a **Google App Password**, not your regular Gmail password.


##  API Endpoints

| GET -`/` | Health check |
| POST -`/auth/signup` | Register a new user |
| POST - `/auth/login` | Login & receive JWT token |
| POST -`/email/send-email` | Send email (requires JWT) |

