from ubuntu:22.04

RUN apt update && \
  apt install -y python3.11 && \
  ln -s /usr/bin/python3.11 /usr/bin/python3 && \
  apt install -y curl && \ 
  apt install -y zip

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && ./aws/install && rm awscliv2.zip
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
RUN curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 && chmod 700 get_helm.sh && ./get_helm.sh && rm get_helm.sh
WORKDIR app
COPY . /app
RUN apt install -y python3-pip
RUN pip install -r requirement.txt
CMD ["python3","app.py"]