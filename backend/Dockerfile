FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the current directory to the container's working directory
COPY . .

# Install dependencies from the requirements file without using cache to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Start the application using Gunicorn with 4 worker processes
# - `-w 4`: uses 4 worker processes
# - `-b 0.0.0.0:7860`: binds the server to port 7860 on all network interfaces
# - `app:superkart_api`: the Flask instance `superkart_api` inside app.py
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:superkart_api"]
