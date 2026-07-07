# 1. Use a lightweight base image with Python 3.12 pre-installed
FROM python:3.12-slim

# 2. Set the working directory inside the container's virtual filesystem
WORKDIR /app

# 3. Copy requirements first to leverage Docker's layer caching mechanism
COPY requirements.txt .

# 4. Install python dependencies without saving caching index files to save space
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application files (filtered automatically by .dockerignore)
COPY . .

# 6. Expose the port Gunicorn will bind to inside the container
EXPOSE 5000

# 7. Start the application in production mode using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
