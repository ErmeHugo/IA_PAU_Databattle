FROM python:3.8.10-slim

# Set the working directory
WORKDIR /app

# Install necessary build dependencies for compiling packages
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code into the container
COPY . /app

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download fr_core_news_md

# Expose the appropriate port (change as per your app's requirement)
EXPOSE 5000

# Command to run the application (adjust this for your app's entry point)
CMD ["python", "Camembert.py"]




