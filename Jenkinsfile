pipeline {
    agent any
    tools {
        maven 'Maven'
        jdk 'JDK17'
    }

    environment {
        PROFILE = "${params.BRANCH == "master" ? "prod" : "test"}"
        PROJECT_NAME = 'akamuinsaner'
        EXPOSE_PORT = "8000"
        OPEN_PORT = "${params.BRANCH == "master" ? "8001" : "8000"}"
    }

    stages {
        stage('Git Clone') {
            steps {
                checkout scm
            }
        }

    //     stage('Test') {
    //         steps {
    //             sh """
    //                 mvn test
    //             """
    //         }
    //     }

    //    stage('Mvn package') {
    //        steps {
    //            sh "mvn clean package -DskipTests -P${env.PROFILE}"
    //        }
    //    }

        stage('Docker build') {
            steps {
                sh """
                    docker build --build-arg PORT=${env.EXPOSE_PORT} --build-arg ENV=${env.PROFILE} -t ${env.PROJECT_NAME}/${env.JOB_NAME}-${env.PROFILE}:${env.BUILD_ID} .
                """
            }
        }

        stage('Docker push') {
            when {
                expression { params.BRANCH == 'master' }
            }
            steps {
                withCredentials([string(credentialsId: 'hub.docker', passwordVariable: 'password', usernameVariable: 'username')]) {
                    sh """
                        docker login --username ${username} --password ${password}
                        docker push ${env.PROJECT_NAME}/${env.JOB_NAME}-${env.PROFILE}:${env.BUILD_ID}
                    """
                }

            }
        }

        stage ('Deploy') {

            steps {
                script {
                    def CONTAINER_ID = sh(script: "docker ps -a | grep -0e ${env.PROJECT_NAME}/${env.JOB_NAME}-${env.PROFILE} | cut -c1-10", returnStdout: true).trim();
                    sh """
                        docker run -d -p ${env.OPEN_PORT}:${env.EXPOSE_PORT} ${env.PROJECT_NAME}/${env.JOB_NAME}-${env.PROFILE}:${env.BUILD_ID}
                    """
                }
            }
        }
    }
}