# Use an official Python runtime as a base image
FROM python:3-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Define the command to run your application
CMD ["python", "app.py"]

