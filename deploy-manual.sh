#!/bin/bash

# Manual Deployment Script for ZBot
# Run this on your Ubuntu machine after GitHub Actions builds the images

echo "🚀 Deploying ZBot to Minikube..."

# Check if Minikube is running
if ! minikube status | grep -q "Running"; then
    echo "❌ Minikube is not running. Please start it first:"
    echo "   minikube start"
    exit 1
fi

# Apply Kubernetes manifests
echo "📦 Applying Kubernetes manifests..."
kubectl apply -f k8s/

# Update to latest images
echo "🔄 Updating to latest Docker images..."
kubectl set image deployment/zbot-frontend frontend=sagarbandagar/zbot-frontend:latest -n zbot
kubectl set image deployment/zbot-backend backend=sagarbandagar/zbot-backend:latest -n zbot

# Wait for rollout
echo "⏳ Waiting for deployment rollout..."
kubectl rollout status deployment/zbot-frontend -n zbot --timeout=300s
kubectl rollout status deployment/zbot-backend -n zbot --timeout=300s

# Show status
echo "📊 Deployment status:"
kubectl get pods -n zbot
kubectl get svc -n zbot

echo "✅ Deployment complete!"
echo ""
echo "🌐 To access your application:"
echo "Frontend: http://$(minikube ip):$(kubectl get svc zbot-frontend -n zbot -o jsonpath='{.spec.ports[0].nodePort}')"
echo "Backend: http://$(minikube ip):$(kubectl get svc zbot-backend -n zbot -o jsonpath='{.spec.ports[0].nodePort}')"