#!/usr/bin/env python3
"""
Simple HTTP server for ZBot frontend development
Serves the frontend and provides backend connection status
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

# Configuration
PORT = 3000
BACKEND_URL = "http://localhost:8000"

class ZBotHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)
    
    def end_headers(self):
        # Add CORS headers for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Serve index.html for root path
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # Simple status check (you could enhance this)
            self.wfile.write(b'{"status": "frontend_running", "backend": "check_docker"}')
            return
        
        super().do_GET()

def main():
    # Change to frontend directory
    frontend_dir = Path(__file__).parent
    os.chdir(frontend_dir)
    
    print("🤖 Starting ZBot Frontend Development Server")
    print("=" * 50)
    print(f"📁 Serving files from: {frontend_dir}")
    print(f"🌐 Frontend URL: http://localhost:{PORT}")
    print(f"🔌 Backend URL: {BACKEND_URL}")
    print("📡 WebSocket: ws://localhost:8000/ws")
    print("=" * 50)
    print("\n✅ Make sure your Docker backend is running:")
    print("   docker-compose up -d backend")
    print("\n🚀 Access your ZBot at: http://localhost:3000")
    print("\n💡 Press Ctrl+C to stop the server\n")
    
    try:
        with socketserver.TCPServer(("", PORT), ZBotHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Shutting down ZBot frontend server...")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {PORT} is already in use!")
            print("💡 Try closing other applications using this port or use a different port")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()