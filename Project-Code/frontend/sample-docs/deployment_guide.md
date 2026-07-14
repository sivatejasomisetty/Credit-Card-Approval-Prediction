# System Deployment & Configuration Guide

This document provides step-by-step instructions for configuring, running, and deploying the Credit Card Approval Prediction application.

---

## 1. Local Environment Configuration

### 1.1 Prerequisites
- Python 3.9 or higher installed.
- Git installed.

### 1.2 Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd credit-card-approval-prediction
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```
3. **Activate the virtual environment:**
   - On Windows:
     ```powershell
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
4. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 1.3 Running the Development Server
Start the Flask application:
```bash
python main.py
```
By default, the server runs in debug mode on `http://127.0.0.1:5000`.

---

## 2. Docker Containerization

To simplify deployment, a configuration file is included in the project root:

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_ENV=production

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

### Build and Run with Docker
1. **Build the Docker image:**
   ```bash
   docker build -t credit-card-predictor .
   ```
2. **Run the container:**
   ```bash
   docker run -d -p 5000:5000 --name credit-app credit-card-predictor
   ```
3. **Access the application:** Open `http://localhost:5000` in your web browser.

---

## 3. Production Cloud Deployment (Render)

Render is the recommended hosting platform for this application.

### Deployment Steps
1. Push your latest code changes to a GitHub repository.
2. Sign in to [Render](https://render.com) and create a new **Web Service**.
3. Connect your GitHub repository.
4. Configure the runtime settings:
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn main:app`
5. Select a free or paid tier and click **Create Web Service**.
