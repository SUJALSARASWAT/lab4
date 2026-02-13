pipeline {
    agent any

    environment {
        IMAGE_NAME = "sujal0307/wine-quality-predictor"
        BEST_ACCURACY = credentials('best-accuracy')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                . venv/bin/activate
                python scripts/train.py
                '''
            }
        }

        stage('Read Accuracy') {
            steps {
                script {
                    def metrics = readJSON file: 'output/metrics.json'
                    env.CURRENT_R2 = metrics.r2.toString()
                    echo "Current R2: ${env.CURRENT_R2}"
                }
            }
        }

        stage('Compare Accuracy') {
            steps {
                script {
                    if (env.CURRENT_R2.toFloat() > BEST_ACCURACY.toFloat()) {
                        env.BUILD_DOCKER = "true"
                        echo "Model improved!"
                    } else {
                        env.BUILD_DOCKER = "false"
                        echo "Model did not improve."
                    }
                }
            }
        }

        stage('Build Docker Image') {
            when {
                expression { env.BUILD_DOCKER == "true" }
            }
            steps {
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
            }
        }

        stage('Push Docker Image') {
            when {
                expression { env.BUILD_DOCKER == "true" }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh '''
                    echo $PASS | docker login -u $USER --password-stdin
                    docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                    docker push ${IMAGE_NAME}:latest
                    '''
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'output/**', allowEmptyArchive: true
        }
    }
}
