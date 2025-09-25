class ZBotChat {
    constructor() {
        this.ws = null;
        this.isConnected = false;
        this.messageHistory = [];
        
        // DOM elements
        this.messagesContainer = document.getElementById('messages');
        this.promptInput = document.getElementById('promptInput');
        this.sendButton = document.getElementById('sendButton');
        this.charCount = document.getElementById('charCount');
        this.status = document.getElementById('status');
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.connectWebSocket();
        this.updateCharCount();
    }
    
    setupEventListeners() {
        // Send button click
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Enter key to send (Shift+Enter for new line)
        this.promptInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-resize textarea
        this.promptInput.addEventListener('input', () => {
            this.updateCharCount();
            this.autoResizeTextarea();
        });
        
        // Paste handling
        this.promptInput.addEventListener('paste', (e) => {
            setTimeout(() => {
                this.updateCharCount();
                this.autoResizeTextarea();
            }, 10);
        });
    }
    
    getWebSocketUrl() {
        const hostname = window.location.hostname;
        const port = window.location.port;
        const protocol = window.location.protocol;
        
        console.log('Current location:', { hostname, port, protocol });
        
        // For local development with Docker backend
        if (hostname === 'localhost' || hostname === '127.0.0.1' || protocol === 'file:') {
            return 'ws://localhost:8000/ws';
        }
        
        // For local development (frontend on port 3000, backend on 8000)
        if (port === '3000') {
            return 'ws://localhost:8000/ws';
        }
        
        // For ngrok deployment - use nginx proxy
        if (hostname.includes('ngrok')) {
            const wsProtocol = protocol === 'https:' ? 'wss:' : 'ws:';
            return `${wsProtocol}//${hostname}/ws`;
        }
        
        // For Kubernetes NodePort access (direct IP access)
        if (hostname.match(/^\d+\.\d+\.\d+\.\d+$/)) {
            // If accessing via IP, try to connect to backend NodePort
            const wsProtocol = protocol === 'https:' ? 'wss:' : 'ws:';
            if (port === '30080') {
                // Frontend is on 30080, backend is on 30800
                return `${wsProtocol}//${hostname}:30800/ws`;
            }
        }
        
        // For containerized deployment (standard ports) - use nginx proxy
        if (port === '' || port === '80' || port === '443') {
            const wsProtocol = protocol === 'https:' ? 'wss:' : 'ws:';
            return `${wsProtocol}//${hostname}/ws`;
        }
        
        // Fallback - try nginx proxy
        const wsProtocol = protocol === 'https:' ? 'wss:' : 'ws:';
        return `${wsProtocol}//${hostname}/ws`;
    }
    
    connectWebSocket() {
        this.updateStatus('Connecting...', 'connecting');
        
        try {
            // WebSocket URL for local development (Docker backend)
            const wsUrl = this.getWebSocketUrl();
            console.log('Connecting to:', wsUrl);
            this.ws = new WebSocket(wsUrl);
            
            this.ws.onopen = () => {
                this.isConnected = true;
                this.updateStatus('Connected', 'connected');
                console.log('Connected to ZBot server');
            };
            
            this.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleResponse(data);
                } catch (error) {
                    console.error('Error parsing message:', error);
                    this.addMessage('Error parsing server response', 'bot');
                }
            };
            
            this.ws.onclose = () => {
                this.isConnected = false;
                this.updateStatus('Disconnected', 'error');
                console.log('Disconnected from ZBot server');
                
                // Attempt to reconnect after 3 seconds
                setTimeout(() => {
                    if (!this.isConnected) {
                        this.connectWebSocket();
                    }
                }, 3000);
            };
            
            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.updateStatus('Connection Error', 'error');
                this.addMessage('Connection error. Please check if the server is running.', 'bot');
            };
            
        } catch (error) {
            console.error('Failed to create WebSocket connection:', error);
            this.updateStatus('Failed to Connect', 'error');
            this.addMessage('Failed to connect to server. Using demo mode.', 'bot');
        }
    }
    
    sendMessage() {
        const message = this.promptInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input
        this.promptInput.value = '';
        this.updateCharCount();
        this.autoResizeTextarea();
        
        // Send to server if connected
        if (this.isConnected && this.ws && this.ws.readyState === WebSocket.OPEN) {
            try {
                this.ws.send(JSON.stringify({
                    message: message,
                    timestamp: new Date().toISOString()
                }));
                
                // Show loading indicator
                this.showLoadingMessage();
                
            } catch (error) {
                console.error('Error sending message:', error);
                this.addMessage('Error sending message. Please try again.', 'bot');
            }
        } else {
            // Demo mode - simulate response
            this.simulateResponse(message);
        }
    }
    
    handleResponse(data) {
        // Remove loading message if present
        this.removeLoadingMessage();
        
        if (data.response) {
            this.addMessage(data.response, 'bot');
        } else if (data.error) {
            this.addMessage(`Error: ${data.error}`, 'bot');
        } else {
            this.addMessage('Received unknown response format', 'bot');
        }
    }
    
    simulateResponse(userMessage) {
        // Remove loading message if present
        this.removeLoadingMessage();
        
        // Show loading
        this.showLoadingMessage();
        
        // Simulate thinking time
        setTimeout(() => {
            this.removeLoadingMessage();
            
            // Simple demo responses
            const responses = [
                "I understand you said: \"" + userMessage + "\". This is a demo response since the server isn't connected.",
                "Thanks for your message! I'm currently in demo mode. Please check your backend connection.",
                "Interesting question! Unfortunately, I can't provide a real AI response without the backend server running.",
                "I received your message, but I'm running in offline mode. Please start the ZBot backend to get AI responses."
            ];
            
            const randomResponse = responses[Math.floor(Math.random() * responses.length)];
            this.addMessage(randomResponse, 'bot');
        }, 1500);
    }
    
    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const icon = sender === 'bot' ? '🤖' : '👤';
        
        messageDiv.innerHTML = `
            <div class="message-icon">${icon}</div>
            <div class="message-content">
                <p>${this.escapeHtml(content)}</p>
            </div>
        `;
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Store in history
        this.messageHistory.push({ content, sender, timestamp: new Date() });
    }
    
    showLoadingMessage() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message bot-message loading-message';
        loadingDiv.innerHTML = `
            <div class="message-icon">🤖</div>
            <div class="message-content">
                <p><span class="loading"></span> Thinking...</p>
            </div>
        `;
        
        this.messagesContainer.appendChild(loadingDiv);
        this.scrollToBottom();
    }
    
    removeLoadingMessage() {
        const loadingMessage = this.messagesContainer.querySelector('.loading-message');
        if (loadingMessage) {
            loadingMessage.remove();
        }
    }
    
    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    updateCharCount() {
        const count = this.promptInput.value.length;
        this.charCount.textContent = `${count}/2000`;
        
        if (count > 1800) {
            this.charCount.style.color = '#dc3545';
        } else if (count > 1500) {
            this.charCount.style.color = '#ffc107';
        } else {
            this.charCount.style.color = '#6c757d';
        }
    }
    
    autoResizeTextarea() {
        this.promptInput.style.height = 'auto';
        this.promptInput.style.height = Math.min(this.promptInput.scrollHeight, 120) + 'px';
    }
    
    updateStatus(text, className = '') {
        this.status.textContent = text;
        this.status.className = `status ${className}`;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the chat when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new ZBotChat();
});

// Add some utility functions for potential future features
function formatTime(date) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        console.log('Text copied to clipboard');
    }).catch(err => {
        console.error('Failed to copy text: ', err);
    });
}