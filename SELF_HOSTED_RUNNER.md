# Self-Hosted GitHub Actions Runner Setup

## 🏃‍♂️ **Setup Self-Hosted Runner on Ubuntu**

Since your Ubuntu machine (`10.233.49.30`) is on a private network that GitHub Actions can't reach, we'll run the CI/CD directly on your Ubuntu machine.

### **Step 1: Install GitHub Actions Runner**

On your Ubuntu machine (`zebra@el114d1u22-593`), run:

```bash
# Create a folder for the runner
mkdir ~/actions-runner && cd ~/actions-runner

# Download the latest runner package
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz

# Optional: Validate the hash
echo "29fc8cf2dab4c195bb147384e7e2c94cfd4d4022c793b346a6175435265aa278  actions-runner-linux-x64-2.311.0.tar.gz" | shasum -a 256 -c

# Extract the installer
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz
```

### **Step 2: Configure the Runner**

1. Go to your GitHub repository: `https://github.com/sagarbandagar/zbot`
2. Go to **Settings** → **Actions** → **Runners**
3. Click **"New self-hosted runner"**
4. Select **Linux** and **x64**
5. Copy the configuration command and run it on your Ubuntu machine

It will look like:
```bash
./config.sh --url https://github.com/sagarbandagar/zbot --token AXXXXXXXXXXXXXXXXXXXXX
```

### **Step 3: Install Dependencies**

Install required tools on your Ubuntu machine:

```bash
# Install Docker (if not already installed)
sudo apt update
sudo apt install -y docker.io
sudo usermod -aG docker $USER
sudo systemctl start docker
sudo systemctl enable docker

# Logout and login again for docker group changes
```

### **Step 4: Start the Runner**

```bash
cd ~/actions-runner
./run.sh
```

Or run as a service:
```bash
sudo ./svc.sh install
sudo ./svc.sh start
```

### **Step 5: Update GitHub Secrets**

You can now remove these SSH-related secrets (no longer needed):
- ❌ `SSH_PRIVATE_KEY` 
- ❌ `SSH_USER`
- ❌ `REMOTE_HOST`

Keep these:
- ✅ `DOCKER_HUB_USERNAME`
- ✅ `DOCKER_HUB_TOKEN`

## 🚀 **How It Works Now:**

1. **Push code** → GitHub triggers workflow
2. **Build images** → Runs on GitHub's servers  
3. **Push to Docker Hub** → Images uploaded
4. **Deploy** → Runs on YOUR Ubuntu machine (self-hosted runner)
5. **Update Kubernetes** → Direct access to your Minikube

## ✅ **Benefits:**

- ✅ No network connectivity issues
- ✅ Direct access to your Minikube cluster
- ✅ Faster deployment (no SSH overhead)
- ✅ More secure (no SSH keys needed)

## 🔧 **Alternative: Manual Deployment**

If you don't want to set up a self-hosted runner, you can:

1. Let GitHub Actions build and push Docker images
2. Manually run deployment script on your Ubuntu machine:

```bash
cd ~/zbot-deploy
kubectl apply -f k8s/
kubectl set image deployment/zbot-frontend frontend=sagarbandagar/zbot-frontend:latest -n zbot
kubectl set image deployment/zbot-backend backend=sagarbandagar/zbot-backend:latest -n zbot
```