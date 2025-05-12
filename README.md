
# 🎓 Student Registration API — GDPR-Compliant Flask Web Service

This project is a secure RESTful web API built using **Flask** and **MongoDB**. It allows students to register, log in, and manage personal information — including sensitive data like disabilities — with **GDPR compliance** via encryption and hashing. No frontend whatsoever!

---

## 🔐 Features

- 📥 Register with encrypted personal data 
- 🔐 Passwords hashed with PBKDF2 + salt
- 🔑 Token-based login authentication (UUID-based)
- 🔒 AES-GCM encryption using `cryptography` for sensitive fields
- 🧪 Full unit test suite using `unittest`
- 🐙 CI pipeline with GitHub Actions (linting, testing)
---

## 📦 Tech Stack

- **Python 3.12**
- **Flask**
- **MongoDB**
- **PyMongo**
- **cryptography**
- **unittest**
- **GitHub Actions**
- **Docker / Docker Compose**

---

## 🚀 Setup Instructions

### 🧰 1. Clone the Repository

```bash
cd encrypt-rest-api
```

### 🐍 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 📦 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the App

### MongoDB in Docker

```bash
docker run --rm -d -p 27017:27017 --name flask-mongo mongo
```

### Flask(requires Mongo running on host)

```bash
python app.py
```