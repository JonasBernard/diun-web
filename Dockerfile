# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY diun_web.py .
COPY diun_notify.py .
COPY templates/ templates/

# Create a volume directory for the JSON data
RUN mkdir -p /app/data
ENV DATA_FILE=/app/data/notifications.json

# Expose the web server port
EXPOSE 8080

# Serve the app using Gunicorn (WSGI)
# -w 4 = 4 worker processes
# -b 0.0.0.0:8080 = bind to all interfaces on port 8080
# app:app = look for the 'app' object in 'app.py'
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "diun_web:app"]
