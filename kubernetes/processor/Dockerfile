FROM python:3.11-alpine

# Set up environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install Flask
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the processor code
COPY . .

# Expose the Flask port
EXPOSE 5000

# Run the Flask server
CMD ["python", "task.py"]