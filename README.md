MP4 to MP3 Microservices Converter
Welcome to the MP4 to MP3 Microservices Converter! This project provides a robust and scalable solution for converting video files (.mp4) into audio files (.mp3) using a microservices architecture orchestrated with Docker.

✨ Features
Microservices Architecture: Decoupled services for enhanced scalability, maintainability, and fault tolerance.

Dockerized: Easy deployment and consistent environments across development and production.

Asynchronous Processing: Utilizes a message queue for non-blocking conversions, improving user experience and system responsiveness.

Scalable: Easily scale individual services based on demand.

RESTful API: Simple API for submitting conversion requests and retrieving results.

🚀 Architecture Overview
This converter is built around a set of independent microservices that communicate via a message queue.

graph TD
    A[Client] --> B[API Gateway Service]
    B --> C[Message Queue (RabbitMQ)]
    C --> D[Conversion Worker Service]
    D --> E[Storage Service (e.g., Local Filesystem/S3)]
    E --> F[API Gateway Service]
    F --> G[Client]

    subgraph Services
        B
        D
        E
    end

API Gateway Service: (e.g., Flask/FastAPI)

Exposes RESTful endpoints for users to upload .mp4 files and check conversion status.

Puts conversion jobs onto the message queue.

Retrieves converted .mp3 files or status from storage/worker.

Message Queue (RabbitMQ):

Acts as a central communication hub between services.

Ensures reliable delivery of conversion tasks.

Conversion Worker Service: (e.g., Python with ffmpeg)

Pulls conversion jobs from the message queue.

Performs the actual mp4 to mp3 conversion using ffmpeg.

Stores the resulting .mp3 file in the Storage Service.

Storage Service: (e.g., Simple Flask app serving files, or integrate with cloud storage like AWS S3/Google Cloud Storage)

Manages the storage and retrieval of original .mp4 files and converted .mp3 files.

🛠️ Technologies Used
Docker: Containerization platform.

Docker Compose: Tool for defining and running multi-container Docker applications.

Python: Primary language for microservices (e.g., Flask, FastAPI).

RabbitMQ: Message broker for asynchronous communication.

FFmpeg: Command-line tool for handling multimedia data (used by the Conversion Worker).

🏁 Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
Before you begin, ensure you have the following installed:

Docker Desktop: Download Docker Desktop

This includes Docker Engine and Docker Compose.

Cloning the Repository
First, clone this repository to your local machine:

git clone https://github.com/your-username/mp4-to-mp3-converter.git
cd mp4-to-mp3-converter

Running the Application
To start all the microservices using Docker Compose, simply run:

docker-compose up --build

This command will:

Build the Docker images for each service (API Gateway, Worker, Storage).

Create and start the containers for RabbitMQ, API Gateway, Worker, and Storage.

You should see logs from all services in your terminal.

💡 Usage
Once all services are up and running, you can interact with the API Gateway.

The API Gateway service will typically be accessible at http://localhost:5000 (or whatever port is configured in docker-compose.yml).

1. Upload an MP4 File for Conversion
Send a POST request to the /convert endpoint with your .mp4 file.

Example using curl:

curl -X POST -F "file=@/path/to/your/video.mp4" http://localhost:5000/convert

Expected Response (JSON):

{
    "job_id": "unique-conversion-job-id",
    "status": "queued",
    "message": "Conversion job submitted successfully."
}

The job_id is crucial for checking the status and downloading the converted file.

2. Check Conversion Status
To check the status of a conversion job, send a GET request to the /status/<job_id> endpoint.

Example using curl:

curl http://localhost:5000/status/unique-conversion-job-id

Expected Responses:

If still processing:

{
    "job_id": "unique-conversion-job-id",
    "status": "processing",
    "message": "Conversion is in progress."
}

If completed:

{
    "job_id": "unique-conversion-job-id",
    "status": "completed",
    "message": "Conversion completed successfully.",
    "download_url": "http://localhost:5000/download/unique-conversion-job-id.mp3"
}

If failed:

{
    "job_id": "unique-conversion-job-id",
    "status": "failed",
    "message": "Conversion failed. Please check logs for details."
}

If job not found:

{
    "job_id": "unique-conversion-job-id",
    "status": "not_found",
    "message": "Conversion job not found."
}

3. Download the Converted MP3 File
Once the status is completed, you can download the .mp3 file using the download_url provided in the status response.

Example using curl:

curl -O http://localhost:5000/download/unique-conversion-job-id.mp3

This will download the unique-conversion-job-id.mp3 file to your current directory.

📁 Project Structure
.
├── api-gateway/
│   ├── app.py              # Flask/FastAPI application for API endpoints
│   ├── Dockerfile          # Dockerfile for API Gateway service
│   └── requirements.txt    # Python dependencies
├── conversion-worker/
│   ├── worker.py           # Python script for processing conversion jobs
│   ├── Dockerfile          # Dockerfile for Conversion Worker service
│   └── requirements.txt    # Python dependencies
├── storage-service/
│   ├── app.py              # Simple Flask app for file serving (or placeholder for S3 integration)
│   ├── Dockerfile          # Dockerfile for Storage Service
│   └── requirements.txt    # Python dependencies
├── docker-compose.yml      # Defines and links all services
└── README.md               # This file
