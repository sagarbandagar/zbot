# Zbot Kubernetes Deployment Guide

## 🚀 Quick Start (Automated Setup)

### Option 1: Automated Ubuntu Setup
```bash
# Download and run the complete setup script
wget https://raw.githubusercontent.com/your-repo/zbot/main/k8s/ubuntu-setup.sh
chmod +x ubuntu-setup.sh
./ubuntu-setup.sh
```

### Option 2: Manual Setup on Ubuntu Machine

#### 1. System Update
```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. Install Docker
```bash
# Install Docker
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (logout and login after this)
sudo usermod -aG docker $USER
```

#### 3. Install kubectl
```bash
# Download kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Install kubectl
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Verify installation
kubectl version --client
```

#### 4. Install Minikube (for local development)
```bash
# Download minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

# Install minikube
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start minikube with proper configuration
minikube start --driver=docker --memory=4096 --cpus=2

# Enable addons
minikube addons enable ingress
minikube addons enable dashboard

# Verify minikube
kubectl cluster-info
```

## Deployment Steps

### 1. Prepare the Secret
First, you need to encode your OpenAI API key:
```bash
echo -n "your-actual-openai-api-key" | base64
```

Edit `k8s/secrets.yaml` and replace the empty `openai-api-key` value with the base64 encoded key.

### 2. Make Scripts Executable
```bash
chmod +x k8s/*.sh
```

### 3. Deploy the Application
```bash
cd k8s

# For standard deployment (LoadBalancer/ClusterIP)
./deploy.sh

# For NodePort deployment (internet accessible)
kubectl create namespace zbot --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f secrets.yaml -n zbot
kubectl apply -f nodeport-deployment.yaml -n zbot

# Setup internet access
./setup-internet-access.sh
```

### 4. Access the Application

#### 🌐 Internet Access Options

**Method 1: NodePort (Recommended for local access)**
```bash
# Deploy with NodePort configuration
kubectl apply -f nodeport-deployment.yaml -n zbot

# Get Minikube IP
minikube ip

# Access via:
# Frontend: http://<minikube-ip>:30080
# Backend API: http://<minikube-ip>:30800
```

**Method 2: Port Forwarding (Localhost access)**
```bash
# Automated setup
./setup-internet-access.sh

# Manual setup
kubectl port-forward svc/zbot-frontend-service 8080:80 -n zbot &
kubectl port-forward svc/zbot-backend-service 8000:8000 -n zbot &

# Access via:
# Frontend: http://localhost:8080
# Backend API: http://localhost:8000
```

**Method 3: Ingress (Domain-like access)**
```bash
# Apply ingress configuration
kubectl apply -f ingress.yaml -n zbot

# Start tunnel (run in separate terminal)
minikube tunnel

# Access via: http://localhost
# API via: http://localhost/api
```

**Method 4: External Access (Real Internet)**
For real internet access, you need:
1. Public IP address
2. Port forwarding on your router
3. Or deploy to cloud providers (AWS EKS, GKE, AKS)

## Useful Commands

### Check Deployment Status
```bash
kubectl get pods -n zbot
kubectl get services -n zbot
kubectl get deployments -n zbot
```

### View Logs
```bash
# Backend logs
kubectl logs -l app=zbot-backend -n zbot -f

# Frontend logs
kubectl logs -l app=zbot-frontend -n zbot -f
```

### Debug Issues
```bash
# Describe pods
kubectl describe pods -n zbot

# Get events
kubectl get events -n zbot --sort-by='.lastTimestamp'

# Shell into backend pod
kubectl exec -it deployment/zbot-backend -n zbot -- /bin/bash

# Shell into frontend pod
kubectl exec -it deployment/zbot-frontend -n zbot -- /bin/sh
```

### Scale Deployments
```bash
# Scale backend
kubectl scale deployment zbot-backend --replicas=3 -n zbot

# Scale frontend
kubectl scale deployment zbot-frontend --replicas=2 -n zbot
```

## Cleanup
To remove the entire deployment:
```bash
./cleanup.sh
```

## Troubleshooting

### Common Issues:

1. **ImagePullBackOff**: Make sure your Docker images are accessible
   ```bash
   kubectl describe pod <pod-name> -n zbot
   ```

2. **CrashLoopBackOff**: Check application logs
   ```bash
   kubectl logs <pod-name> -n zbot
   ```

3. **Service not accessible**: Check service endpoints
   ```bash
   kubectl get endpoints -n zbot
   ```

### Health Checks
Add these to your deployments for better reliability:
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

## Production Considerations

1. **Use persistent volumes for data**
2. **Implement proper resource limits**
3. **Set up monitoring with Prometheus/Grafana**
4. **Configure ingress for better traffic management**
5. **Use ConfigMaps for configuration**
6. **Implement backup strategies**