
# Use an official Python runtime as a parent image

FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /app

# Copy only requirements file first for leveraging Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port your FastAPI app runs on (default is 8000)
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
