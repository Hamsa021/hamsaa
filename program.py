pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'devops-automation-app'
        REGISTRY_URL = 'ibm_container_registry_url'
        CLUSTER_NAME = 'Photo'
    }
    stages {
        stage('Checkout Code') {
            steps {
                git ‘https://github.com/Hamsa021/pro.git’
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $REGISTRY_URL/$DOCKER_IMAGE .'
                }
            }
        }
        stage('Push Docker Image to Registry') {
            steps {
                script {
                    sh 'docker push $REGISTRY_URL/$DOCKER_IMAGE'
                }
            }
        }
        stage('Deploy to Kubernetes Cluster') {
            steps {
                script {
                    sh '''
                    ibmcloud login --apikey <API_KEY> -r <REGION> -g <RESOURCE_GROUP>
                    ibmcloud ks cluster config --cluster $CLUSTER_NAME
                    kubectl apply -f k8s/deployment.yaml
                    '''
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline executed successfully. Automation tracking complete.'
        }
        failure {
            echo 'Pipeline failed. Please review logs for details.'
        }
    }
}
