# 🤖 ZBot - AI Chatbot with Kubernetes

A full-stack AI chatbot application with FastAPI backend, HTML/JS frontend, and Kubernetes deployment.

**Latest Update**: Testing CI/CD pipeline with secrets configured! 🚀✅

## 🏗️ Architecture

```
Frontend (HTML/JS) → nginx → WebSocket → Backend (FastAPI) → OpenAI API
```

## 🚀 Features

- Real-time chat with WebSocket
- OpenAI GPT integration
- Docker containerization
- Kubernetes deployment
- Automated CI/CD with GitHub Actions
- Internet access via ngrok

## 📁 Project Structure

```
zbot/
├── front-end/              # HTML/CSS/JS frontend
│   ├── Dockerfile
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── nginx.conf
├── back-end/               # Python FastAPI backend
│   ├── Dockerfile
│   ├── requirement.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   └── ws_handler.py
│   └── services/
│       └── openai_services.py
├── k8s/                    # Kubernetes manifests
│   ├── secrets.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   └── frontend-service.yaml
└── .github/workflows/      # CI/CD pipeline
    └── ci-cd.yml
```

## 🔧 Local Development

### Prerequisites
- Python 3.9+
- Docker
- Kubernetes (minikube)
- OpenAI API key

### Setup
1. Clone repository
2. Set OpenAI API key in `.env`
3. Build Docker images
4. Deploy to Kubernetes

## 🌐 Deployment

The application automatically deploys on push to main branch via GitHub Actions.

### Manual Deployment
```bash
# Build and push images
docker build -t sagarbandagar/zbot:frontend ./front-end
docker build -t sagarbandagar/zbot:backend ./back-end
docker push sagarbandagar/zbot:frontend
docker push sagarbandagar/zbot:backend

# Deploy to Kubernetes
kubectl apply -f k8s/
```

## 🔄 CI/CD

Automated deployment pipeline:
1. Build Docker images
2. Push to Docker Hub
3. Deploy to Kubernetes
4. Verify deployment

## 📝 Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: GPT model (default: gpt-3.5-turbo)

## 🚀 Live Demo

Access the live application via ngrok URL (provided in deployment logs).

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

MIT License