# README.md

## Overview

This Flask-based web service to deploy a monitoring solution on an Amazon EKS cluster using Kubernetes and Helm. The service generates a Kubernetes configuration file based on the provided AWS credentials and EKS cluster details, and then deploys Grafana using Helm.

## Prerequisites

- Python 3.x
- Flask
- Boto3
- PyYAML
- AWS CLI
- Kubernetes CLI (kubectl)
- Helm

## Setup

1. **Clone the Repository**

    ```bash
    git clone https://github.com/your-repo/your-project.git
    cd your-project
    ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set Environment Variables**

    Update the environment variables for AWS access keys in the `monitoring_deployment` function:

    ```python
    os.environ['AWS_ACCESS_KEY_ID'] = 'your-access-key'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'your-secret-key'
    ```

## Running the Service

1. **Start the Flask Server**

    ```bash
    python app.py
    ```

2. **Create Monitoring**

    Send a POST request to `http://localhost:4004/create_monitoring` with a JSON payload containing the following keys:
    
    - `access_key`: Your AWS access key.
    - `secret_key`: Your AWS secret key.
    - `cluster_name`: The name of your EKS cluster.
    - `region_name`: The AWS region where your EKS cluster is located.

    Example payload:
    
    ```json
    {
        "access_key": "your-access-key",
        "secret_key": "your-secret-key",
        "cluster_name": "your-cluster-name",
        "region_name": "your-region-name"
    }
    ```

    You can use `curl` or any API client to send the request:

    ```bash
    curl -X POST http://localhost:4004/create_monitoring -H "Content-Type: application/json" -d '{
        "access_key": "your-access-key",
        "secret_key": "your-secret-key",
        "cluster_name": "your-cluster-name",
        "region_name": "your-region-name"
    }'
    ```
