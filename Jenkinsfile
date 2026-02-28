pipeline {
    agent any

    environment {
        // Define environment variables
        DOCKER_IMAGE = "2022bcs0169sumedhkolupoti/mlops-lab-4"
        DOCKER_TAG = "latest"
        CONTAINER_NAME = "wine-api-validation-${BUILD_NUMBER}"
        API_PORT = "8000"
        
        // Credentials binding (from previous labs)
        DOCKER_CREDS = credentials('dockerhub-creds')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Pull Image') {
            steps {
                script {
                    echo "Pulling Docker image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    sh "docker pull ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    echo "Starting container: ${CONTAINER_NAME}"
                    // Run container in background, mapping port 8000
                    sh "docker run -d --name ${CONTAINER_NAME} -p ${API_PORT}:8000 ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }

        stage('Wait for Service Readiness') {
            steps {
                script {
                    echo "Waiting for API to be ready at http://localhost:${API_PORT}/"
                    timeout(time: 2, unit: 'MINUTES') {
                        waitUntil {
                            def response = sh(
                                script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:${API_PORT}/ || echo '000'",
                                returnStdout: true
                            ).trim()
                            echo "Health check response: ${response}"
                            return (response == "200")
                        }
                    }
                }
            }
        }

        stage('Send Valid Inference Request') {
            steps {
                script {
                    echo "Sending valid inference request..."
                    def response = sh(
                        script: "curl -s -X POST http://localhost:${API_PORT}/predict -H 'Content-Type: application/json' -d @valid_input.json",
                        returnStdout: true
                    ).trim()
                    echo "API Response: ${response}"
                    
                    // Validation: HTTP status is handled by curl (explicit check if needed, but here we check content)
                    // We'll use a python snippet for easy JSON validation
                    sh """
                        python3 -c "
import json
import sys
data = json.loads('''${response}''')
print(f'Validating response: {data}')
if 'wine_quality' not in data:
    print('Error: wine_quality field missing')
    sys.exit(1)
if not isinstance(data['wine_quality'], (int, float)):
    print(f'Error: wine_quality is not numeric: {type(data[\"wine_quality\"])}')
    sys.exit(1)
print('Validation Passed: Prediction value is numeric.')
"
                    """
                }
            }
        }

        stage('Send Invalid Request') {
            steps {
                script {
                    echo "Sending invalid (malformed) inference request..."
                    // FastAPI returns 422 Unprocessable Entity for schema validation errors
                    def httpCode = sh(
                        script: "curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost:${API_PORT}/predict -H 'Content-Type: application/json' -d @invalid_input.json",
                        returnStdout: true
                    ).trim()
                    
                    echo "HTTP Status Code for invalid request: ${httpCode}"
                    
                    if (httpCode == "422") {
                        echo "Validation Success: API blocked the invalid request as expected."
                    } else {
                        error "Validation Failed: Expected status 422 for invalid request, but got ${httpCode}."
                    }
                }
            }
        }

        stage('Stop Container') {
            steps {
                script {
                    echo "Stopping and removing container: ${CONTAINER_NAME}"
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rm ${CONTAINER_NAME} || true"
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning up..."
            sh "docker stop ${CONTAINER_NAME} || true"
            sh "docker rm ${CONTAINER_NAME} || true"
            cleanWs()
        }
    }
}
