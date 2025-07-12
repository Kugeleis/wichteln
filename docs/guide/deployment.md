# Deployment Guide

Deploy the Secret Santa application to production.

## Production Checklist

- [ ] Set `FLASK_DEBUG=False`
- [ ] Use a strong `SECRET_KEY`
- [ ] Configure proper email settings
- [ ] Set up reCAPTCHA
- [ ] Configure logging
- [ ] Set up monitoring

## Deployment Options

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv sync --frozen

EXPOSE 5000
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

Build and run:

```bash
docker build -t secret-santa .
docker run -p 5000:5000 --env-file .env secret-santa
```

### Heroku Deployment

1. Create a `Procfile`:
   ```
   web: uv run gunicorn app:app
   ```

2. Deploy:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### VPS Deployment

1. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   pip3 install uv
   ```

2. **Setup Application**
   ```bash
   git clone https://github.com/Kugeleis/wichteln.git
   cd wichteln
   uv sync
   ```

3. **Configure Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

4. **Setup Systemd Service**
   ```ini
   [Unit]
   Description=Secret Santa App
   After=network.target

   [Service]
   User=your-user
   WorkingDirectory=/path/to/wichteln
   ExecStart=/path/to/uv run gunicorn app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

## Monitoring

### Logging

Configure structured logging for production:

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
```

### Health Checks

Add a health check endpoint:

```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'version': '1.0.0'}
```

## Security Considerations

- Use HTTPS in production
- Set proper CORS headers
- Implement rate limiting
- Regular security updates
- Monitor for suspicious activity
