#!/bin/bash
# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Build Jenkins image if it doesn't exist
echo "Building Jenkins image..."
docker build -t custom-jenkins -f lab5/Dockerfile.jenkins lab5/

# Start Jenkins container
echo "Starting Jenkins container..."
docker run -d --name jenkins-lab -p 8080:8080 -p 50000:50000 -v /var/run/docker.sock:/var/run/docker.sock custom-jenkins

echo "Jenkins starting at http://localhost:8080"
