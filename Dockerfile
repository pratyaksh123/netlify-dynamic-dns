# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install pipenv
RUN pip install pipenv

# Install dependencies from Pipfile
RUN pipenv install

# Run the script when the container launches
CMD ["pipenv", "run", "python", "main.py"]
