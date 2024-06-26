import subprocess
import boto3
import yaml
import os
from flask import Flask, request

app = Flask(__name__)

def get_config(data):
    access_key_secret = data["access_key"]
    secret_access_key_secret = data["secret_key"]
    cluster_name = data["cluster_name"]
    region_name = data["region_name"]
    s = boto3.Session(region_name=region_name)
    eks = s.client("eks",aws_access_key_id=access_key_secret, aws_secret_access_key=secret_access_key_secret)

    # get cluster details
    cluster = eks.describe_cluster(name=cluster_name)
    cluster_cert = cluster["cluster"]["certificateAuthority"]["data"]
    cluster_ep = cluster["cluster"]["endpoint"]
    cluster_name = cluster["cluster"]["arn"]
    cluster_short_name = cluster["cluster"]["name"]

    # build the cluster config hash
    cluster_config = {
            "apiVersion": "v1",
            "kind": "Config",
            "clusters": [
                {
                    "cluster": {
                        "server": str(cluster_ep),
                        "certificate-authority-data": str(cluster_cert)
                    },
                    "name": str(cluster_name)
                }
            ],
            "contexts": [
                {
                    "context": {
                        "cluster": str(cluster_name),
                        "user": str(cluster_name)
                    },
                    "name": str(cluster_name)
                }
            ],
            "current-context": str(cluster_name),
            "preferences": {},
            "users": [
                {
                    "name": str(cluster_name),
                    "user": {
                        "exec": {
                            "apiVersion": "client.authentication.k8s.io/v1beta1",
                            "command": "aws",
                            "args": [
                                "--region", region_name, "eks" , "get-token","--cluster-name",cluster_short_name,"--output","json"
                            ]
                        }
                    }
                }
            ]
        }

    # Write in YAML.
    config_text=yaml.dump(cluster_config, default_flow_style=False)
    open("my_kubeconfig.json", "w").write(config_text)
    return config_text

def monitoring_deployment():

    try:
        os.environ['AWS_ACCESS_KEY_ID'] = 'your-access-key'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'your-secret-key'
        subprocess.run(["kubectl", "--kubeconfig", "my_kubeconfig.json", "get", "pods"], text=True)
        subprocess.run(["helm", "install", "grafana", "./grafana/"])
    except subprocess.CalledProcessError as e:
        print(f"Error during backup: {e}")
    
@app.route('/create_monitoring',methods=['POST'])
def create_monitoring():
    data = request.get_json()
    print(data)
    get_config(data)
    monitoring_deployment()

if __name__ == '__main__':
    app.run('0.0.0.0',4004,debug=True)