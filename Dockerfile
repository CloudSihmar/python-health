# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the Python application files to the container
COPY . .


# Install Flask
RUN pip install flask requests

# Expose the port the Flask app will listen on
EXPOSE 8080

# Command to run the Flask application
CMD ["python", "app.py"]

