pipeline {
    agent any

    environment {
        // Define environment variables
        DOCKER_IMAGE = "sumedhkolupoti/mlops-lab-4"
        DOCKER_TAG = "${BUILD_NUMBER}"
        VENV_NAME = "venv"
        // Credentials binding
        DOCKER_CREDS = credentials('dockerhub-creds')
        // GIT_CREDS is automatically used by checkout scm if configured in the job
        // Best accuracy secret
        BEST_ACCURACY_CREDENTIAL = credentials('best-accuracy')
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the repository
                checkout scm
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                    # Create virtual environment if it doesn't exist
                    if [ ! -d "$VENV_NAME" ]; then
                        python3 -m venv $VENV_NAME
                    fi
                    
                    # Install dependencies
                    . $VENV_NAME/bin/activate
                    pip install --upgrade pip
                    if [ -f "requirements.txt" ]; then
                        pip install -r requirements.txt
                    else
                        echo "requirements.txt not found!"
                        exit 1
                    fi
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                    . $VENV_NAME/bin/activate
                    export PYTHONPATH=$PYTHONPATH:.
                    # Ensure artifacts directory exists
                    mkdir -p artifacts
                    # Run training script
                    python3 scripts/train.py
                '''
            }
        }

        stage('Read Accuracy') {
            steps {
                script {
                    def metricsFile = "artifacts/metrics.json"
                    if (fileExists(metricsFile)) {
                        // Read R2 score using python
                        def r2_score = sh(
                            script: """
                                . $VENV_NAME/bin/activate
                                python3 -c "import json; print(json.load(open('${metricsFile}'))['r2'])"
                            """,
                            returnStdout: true
                        ).trim()
                        
                        env.CURRENT_ACCURACY = r2_score
                        echo "Current Model Accuracy (R2): ${env.CURRENT_ACCURACY}"
                    } else {
                        error "metrics.json not found! Training might have failed."
                    }
                }
            }
        }

        stage('Compare Accuracy') {
            steps {
                script {
                    echo "Comparing Current Accuracy (${env.CURRENT_ACCURACY}) vs Best Accuracy (${env.BEST_ACCURACY_CREDENTIAL})"
                    
                    // Compare values using python
                    def isBetter = sh(
                        script: """
                            . $VENV_NAME/bin/activate
                            python3 -c "
import os
try:
    current = float(os.environ.get('CURRENT_ACCURACY', '0').strip())
    best_str = os.environ.get('BEST_ACCURACY_CREDENTIAL', '0').strip()
    if not best_str:
        best = -999.0
    else:
        best = float(best_str)
        
    if current > best:
        print('true')
    else:
        print('false')
except Exception as e:
    print('error')
"
                        """,
                        returnStdout: true
                    ).trim()

                    if (isBetter == 'true') {
                        echo "New model is better!"
                        env.NEW_MODEL_IS_BETTER = 'true'
                    } else {
                        echo "New model is NOT better than stored best."
                        env.NEW_MODEL_IS_BETTER = 'false'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            when {
                environment name: 'NEW_MODEL_IS_BETTER', value: 'true'
            }
            steps {
                script {
                    echo "Building Docker image since model improved."
                    
                    // Copy model to lab3 folder
                    sh 'cp artifacts/model.pkl lab3/model.pkl'
                    
                    dir('lab3') {
                        sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} -t ${DOCKER_IMAGE}:latest ."
                    }
                }
            }
        }

        stage('Push Docker Image') {
            when {
                environment name: 'NEW_MODEL_IS_BETTER', value: 'true'
            }
            steps {
                script {
                    sh "echo $DOCKER_CREDS_PSW | docker login -u $DOCKER_CREDS_USR --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    sh "docker push ${DOCKER_IMAGE}:latest"
                    sh "docker logout"
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'artifacts/**', allowEmptyArchive: true
            cleanWs()
        }
    }
}
