# Use nginx to serve static files
FROM nginx:alpine

# Copy the frontend files to nginx html directory
COPY index.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/
COPY script.js /usr/share/nginx/html/
COPY server.html /usr/share/nginx/html/

# Create a custom nginx configuration for our frontend
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]