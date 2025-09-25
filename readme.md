# 🤖 ZBot - AI Chatbot with Kubernetes# 🤖 ZBot - AI Chatbot with Kubernetes# 🤖 ZBot - AI Chatbot with Kubernetes# 🤖 ZBot - AI Chatbot with Kubernetes



A full-stack AI chatbot application with FastAPI backend, HTML/JS frontend, and Kubernetes deployment.



## 🏗️ ArchitectureA full-stack AI chatbot application with FastAPI backend, HTML/JS frontend, and Kubernetes deployment.



```

Frontend (HTML/JS) → nginx → WebSocket → Backend (FastAPI) → OpenAI API

```**Latest Update**: Simplified CI/CD pipeline - builds Docker images automatically! 🚀A full-stack AI chatbot application with FastAPI backend, HTML/JS frontend, and Kubernetes deployment.A full-stack AI chatbot application with FastAPI backend, HTML/JS frontend, and Kubernetes deployment.



## 🚀 Features



- ✨ **Real-time chat** with WebSocket## 🏗️ Architecture

- 🤖 **OpenAI GPT integration** 

- 🐳 **Docker containerization**

- ☸️ **Kubernetes deployment**

- 🔄 **Automated CI/CD** with GitHub Actions```**Latest Update**: Simplified CI/CD pipeline - builds Docker images automatically! 🚀**Latest Update**: Docker Hub secrets added, testing full CI/CD pipeline! 🚀✅

- 🌐 **Internet ready** via ngrok

Frontend (HTML/JS) → nginx → WebSocket → Backend (FastAPI) → OpenAI API

## 📁 Project Structure

```

```

zbot/

├── front-end/              # HTML/CSS/JS frontend

│   ├── Dockerfile## 🚀 Features## 🏗️ Architecture## 🏗️ Architecture

│   ├── index.html

│   ├── script.js

│   ├── style.css

│   └── nginx.conf- ✨ Real-time chat with WebSocket

├── back-end/               # Python FastAPI backend

│   ├── Dockerfile- 🤖 OpenAI GPT integration  

│   ├── requirement.txt

│   ├── app/- 🐳 Docker containerization``````

│   │   ├── main.py

│   │   ├── models.py- ☸️ Kubernetes deployment

│   │   └── ws_handler.py

│   └── services/- 🔄 Automated CI/CD with GitHub ActionsFrontend (HTML/JS) → nginx → WebSocket → Backend (FastAPI) → OpenAI APIFrontend (HTML/JS) → nginx → WebSocket → Backend (FastAPI) → OpenAI API

│       └── openai_services.py

├── k8s/                    # Kubernetes manifests- 🌐 Ready for internet access

│   ├── secrets.yaml

│   ├── backend.yaml``````

│   ├── frontend.yaml

│   └── complete-deployment.yaml## 📁 Project Structure

├── .github/workflows/      # CI/CD pipeline

│   └── ci-cd.yml

└── deploy-manual.sh        # Manual deployment script

``````



## 🔄 CI/CD Pipelinezbot/## 🚀 Features## 🚀 Features



**Automated on every push to main:**├── front-end/              # HTML/CSS/JS frontend



1. 🔨 **Build Docker Images**│   ├── Dockerfile

   - Frontend: `sagarbandagar/zbot-frontend:latest`

   - Backend: `sagarbandagar/zbot-backend:latest`│   ├── index.html



2. 📤 **Push to Docker Hub**│   ├── script.js- ✨ Real-time chat with WebSocket- Real-time chat with WebSocket

   - Images available publicly

│   ├── style.css

3. 📋 **Ready for Deployment**

   - Use manual deployment script on your Kubernetes cluster│   └── nginx.conf- 🤖 OpenAI GPT integration- OpenAI GPT integration



## 🚀 Quick Start├── back-end/               # Python FastAPI backend  



### Prerequisites│   ├── Dockerfile- 🐳 Docker containerization- Docker containerization

- Docker & Docker Hub account

- Kubernetes (minikube)│   ├── requirement.txt

- OpenAI API key

│   ├── app/- ☸️ Kubernetes deployment- Kubernetes deployment

### Setup & Deploy

│   └── services/

1. **Clone repository**

   ```bash├── k8s/                    # Kubernetes manifests- 🔄 Automated CI/CD with GitHub Actions- Automated CI/CD with GitHub Actions

   git clone https://github.com/sagarbandagar/zbot.git

   cd zbot├── .github/workflows/      # CI/CD pipeline

   ```

└── deploy-manual.sh        # Manual deployment script- 🌐 Internet access via ngrok- Internet access via ngrok

2. **Set OpenAI API key**

   ```bash```

   echo "OPENAI_API_KEY=your-api-key-here" > back-end/.env

   ```



3. **Start Minikube & Deploy**## 🔄 CI/CD Pipeline

   ```bash

   minikube start## 📁 Project Structure## 📁 Project Structure

   kubectl apply -f k8s/

   ```**Automated on every push to main:**



4. **Access Application**

   ```bash

   minikube service list -n zbot1. 🔨 **Build Docker Images**

   ```

   - Frontend: `sagarbandagar/zbot-frontend:latest```````

## 🔧 Manual Deployment

   - Backend: `sagarbandagar/zbot-backend:latest`

After CI/CD builds new images:

zbot/zbot/

```bash

# On your Kubernetes machine2. 📤 **Push to Docker Hub**

./deploy-manual.sh

   - Images available publicly├── front-end/              # HTML/CSS/JS frontend├── front-end/              # HTML/CSS/JS frontend

# Or manually:

kubectl apply -f k8s/

kubectl set image deployment/zbot-frontend frontend=sagarbandagar/zbot-frontend:latest -n zbot

kubectl set image deployment/zbot-backend backend=sagarbandagar/zbot-backend:latest -n zbot3. 📋 **Ready for Deployment**│   ├── Dockerfile│   ├── Dockerfile

```

   - Use manual deployment script

## 📝 Environment Variables

│   ├── index.html│   ├── index.html

| Variable | Description | Default |

|----------|-------------|---------|### Manual Deployment

| `OPENAI_API_KEY` | Your OpenAI API key | **Required** |

| `OPENAI_MODEL` | GPT model to use | `gpt-3.5-turbo` |│   ├── script.js│   ├── script.js

| `HOST` | Server host | `0.0.0.0` |

| `PORT` | Server port | `8000` |```bash



## 💡 Development# On your Kubernetes machine│   ├── style.css│   ├── style.css



```bash./deploy-manual.sh

# Backend development

cd back-end│   └── nginx.conf│   └── nginx.conf

pip install -r requirement.txt

python -m app.main# Or manually:



# Frontend development  kubectl apply -f k8s/├── back-end/               # Python FastAPI backend├── back-end/               # Python FastAPI backend

cd front-end

python -m http.server 3000kubectl set image deployment/zbot-frontend frontend=sagarbandagar/zbot-frontend:latest -n zbot

```

kubectl set image deployment/zbot-backend backend=sagarbandagar/zbot-backend:latest -n zbot│   ├── Dockerfile│   ├── Dockerfile

## 🤝 Contributing

```

1. Fork the repository

2. Create feature branch (`git checkout -b feature/amazing-feature`)│   ├── requirement.txt│   ├── requirement.txt

3. Commit changes (`git commit -m 'Add amazing feature'`)

4. Push to branch (`git push origin feature/amazing-feature`)## 🚀 Quick Start

5. Open Pull Request

│   ├── app/│   ├── app/

## 📄 License

1. **Clone and setup**

MIT License

   ```bash│   │   ├── main.py│   │   ├── main.py

---

   git clone https://github.com/sagarbandagar/zbot.git

**🚀 Happy Chatting with ZBot!**

   cd zbot│   │   ├── models.py│   │   ├── models.py

*Built with ❤️ using FastAPI, WebSocket, and OpenAI*
   ```

│   │   └── ws_handler.py│   │   └── ws_handler.py

2. **Add OpenAI API key**

   ```bash│   └── services/│   └── services/

   echo "OPENAI_API_KEY=your-key" > back-end/.env

   ```│       └── openai_services.py│       └── openai_services.py



3. **Deploy**├── k8s/                    # Kubernetes manifests├── k8s/                    # Kubernetes manifests

   ```bash

   kubectl apply -f k8s/│   ├── secrets.yaml│   ├── secrets.yaml

   ```

│   ├── backend.yaml│   ├── backend-deployment.yaml

## 📄 License

│   ├── frontend.yaml│   ├── backend-service.yaml

MIT License

│   └── complete-deployment.yaml│   ├── frontend-deployment.yaml

---

├── .github/workflows/      # CI/CD pipeline│   └── frontend-service.yaml

**🚀 Happy Chatting with ZBot!**
│   └── ci-cd.yml└── .github/workflows/      # CI/CD pipeline

└── deploy-manual.sh        # Manual deployment script    └── ci-cd.yml

``````



## 🔧 Quick Start## 🔧 Local Development



### Prerequisites### Prerequisites

- Python 3.9+- Python 3.9+

- Docker & Docker Hub account- Docker

- Kubernetes (minikube)- Kubernetes (minikube)

- OpenAI API key- OpenAI API key



### Setup### Setup

1. **Clone repository**1. Clone repository

   ```bash2. Set OpenAI API key in `.env`

   git clone https://github.com/sagarbandagar/zbot.git3. Build Docker images

   cd zbot4. Deploy to Kubernetes

   ```

## 🌐 Deployment

2. **Set OpenAI API key**

   ```bashThe application automatically deploys on push to main branch via GitHub Actions.

   # Create .env file in back-end directory

   echo "OPENAI_API_KEY=your-api-key-here" > back-end/.env### Manual Deployment

   ``````bash

# Build and push images

3. **Start Minikube**docker build -t sagarbandagar/zbot:frontend ./front-end

   ```bashdocker build -t sagarbandagar/zbot:backend ./back-end

   minikube startdocker push sagarbandagar/zbot:frontend

   ```docker push sagarbandagar/zbot:backend



4. **Deploy to Kubernetes**# Deploy to Kubernetes

   ```bashkubectl apply -f k8s/

   kubectl apply -f k8s/```

   ```

## 🔄 CI/CD

## 🔄 CI/CD Pipeline

Automated deployment pipeline:

**Automated on every push to main:**1. Build Docker images

2. Push to Docker Hub

1. 🔨 **Build Docker Images**3. Deploy to Kubernetes

   - Frontend: `sagarbandagar/zbot-frontend:latest`4. Verify deployment

   - Backend: `sagarbandagar/zbot-backend:latest`

## 📝 Environment Variables

2. 📤 **Push to Docker Hub**

   - Images available publicly- `OPENAI_API_KEY`: Your OpenAI API key

- `OPENAI_MODEL`: GPT model (default: gpt-3.5-turbo)

3. 📋 **Ready for Deployment**

   - Use manual deployment script on your Kubernetes cluster## 🚀 Live Demo



### Manual DeploymentAccess the live application via ngrok URL (provided in deployment logs).

After CI/CD builds new images:

## 🤝 Contributing

```bash

# On your Ubuntu/Kubernetes machine1. Fork the repository

./deploy-manual.sh2. Create feature branch

3. Commit changes

# Or manually:4. Push to branch

kubectl apply -f k8s/5. Create Pull Request

kubectl set image deployment/zbot-frontend frontend=sagarbandagar/zbot-frontend:latest -n zbot

kubectl set image deployment/zbot-backend backend=sagarbandagar/zbot-backend:latest -n zbot## 📄 License

```

MIT License

## 🌐 Access Your Application #   C I / C D   P i p e l i n e   T e s t   -   2 0 2 5 - 0 9 - 2 5   1 5 : 3 0 

 

```bash 
# Get application URLs
minikube service list -n zbot

# Or use port forwarding
kubectl port-forward svc/zbot-frontend 8080:80 -n zbot
```

Then open: `http://localhost:8080`

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `OPENAI_MODEL` | GPT model to use | `gpt-3.5-turbo` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - feel free to use this project for learning and development!

---

**🚀 Happy Chatting with ZBot!** 

*Last Updated: September 25, 2025*