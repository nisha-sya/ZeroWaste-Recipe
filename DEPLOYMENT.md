# Deployment Guide

This guide explains how to deploy the Recipe App to production.

## Prerequisites

- Python 3.8+
- PostgreSQL (recommended) or MySQL
- Redis (for caching)
- Nginx (web server)
- Gunicorn (WSGI server)

## Environment Setup

1. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Configure environment variables:**
   ```bash
   # Django Settings
   DJANGO_SECRET_KEY=your-super-secret-key-here
   DEBUG=False
   DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   
   # Database Settings
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=recipeapp_db
   DB_USER=recipeapp_user
   DB_PASSWORD=secure_password
   DB_HOST=localhost
   DB_PORT=5432
   
   # Email Settings
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   
   # Security Settings
   SECURE_SSL_REDIRECT=True
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   ```

## Database Setup

1. **Install PostgreSQL:**
   ```bash
   sudo apt-get install postgresql postgresql-contrib
   ```

2. **Create database and user:**
   ```sql
   CREATE DATABASE recipeapp_db;
   CREATE USER recipeapp_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE recipeapp_db TO recipeapp_user;
   ```

## Application Deployment

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate --settings=ReceipeApp.production
   ```

3. **Collect static files:**
   ```bash
   python manage.py collectstatic --settings=ReceipeApp.production
   ```

4. **Create superuser:**
   ```bash
   python manage.py createsuperuser --settings=ReceipeApp.production
   ```

## Web Server Configuration

### Nginx Configuration

Create `/etc/nginx/sites-available/recipeapp`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/your/project;
    }
    
    location /media/ {
        root /path/to/your/project;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

### Gunicorn Configuration

Create `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
RuntimeDirectory=gunicorn
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock ReceipeApp.wsgi:application

[Install]
WantedBy=multi-user.target
```

## Security Checklist

- [ ] DEBUG = False
- [ ] SECRET_KEY is secure and unique
- [ ] ALLOWED_HOSTS is properly configured
- [ ] SSL/HTTPS is enabled
- [ ] Database credentials are secure
- [ ] Static files are served by web server
- [ ] Media files are properly secured
- [ ] Logs are configured and monitored
- [ ] Regular backups are scheduled

## Monitoring

1. **Set up logging:**
   - Application logs: `/var/log/recipeapp/`
   - Nginx logs: `/var/log/nginx/`
   - System logs: `journalctl -u gunicorn`

2. **Health checks:**
   - Monitor application response time
   - Check database connectivity
   - Monitor disk space and memory usage

## Backup Strategy

1. **Database backups:**
   ```bash
   pg_dump recipeapp_db > backup_$(date +%Y%m%d_%H%M%S).sql
   ```

2. **Media files backup:**
   ```bash
   tar -czf media_backup_$(date +%Y%m%d_%H%M%S).tar.gz media/
   ```

## Performance Optimization

1. **Enable caching:**
   - Redis for session and cache storage
   - CDN for static files

2. **Database optimization:**
   - Regular VACUUM and ANALYZE
   - Proper indexing
   - Connection pooling

3. **Static files:**
   - Use ManifestStaticFilesStorage
   - Enable compression
   - Set proper cache headers 