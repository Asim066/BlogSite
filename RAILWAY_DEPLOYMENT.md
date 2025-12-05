# Railway Deployment Guide

This guide will help you deploy your Django Blog Platform to Railway.

## Prerequisites

1. **Railway Account**: Sign up at https://railway.app
2. **Railway CLI** (Optional but recommended): Install from https://docs.railway.app/develop/cli

## Step 1: Install Railway CLI (Optional)

**Windows (PowerShell):**
```powershell
iwr https://railway.app/install.ps1 | iex
```

**Or download from**: https://github.com/railwayapp/cli/releases

## Step 2: Login to Railway

```bash
railway login
```

This will open your browser to authenticate.

## Step 3: Initialize Railway Project

```bash
# Navigate to your project
cd BlogSite

# Initialize Railway project
railway init
```

This will:
- Create a new Railway project (or link to existing)
- Create a `railway.json` configuration file

## Step 4: Set Environment Variables

You need to set these environment variables in Railway:

### Required Variables:

```bash
# Django Secret Key (generate a new one for production)
railway variables set SECRET_KEY="your-secret-key-here"

# Debug Mode (set to False for production)
railway variables set DEBUG="False"

# Allowed Hosts (Railway will provide your domain)
railway variables set ALLOWED_HOSTS="your-app.railway.app,*.railway.app"

# Database URL (Railway provides this automatically when you add PostgreSQL)
# But you can also set it manually if needed
```

### Optional but Recommended:

```bash
# Email Configuration (if you want email notifications)
railway variables set EMAIL_HOST="smtp.gmail.com"
railway variables set EMAIL_PORT="587"
railway variables set EMAIL_USE_TLS="True"
railway variables set EMAIL_HOST_USER="your-email@gmail.com"
railway variables set EMAIL_HOST_PASSWORD="your-app-password"
railway variables set DEFAULT_FROM_EMAIL="your-email@gmail.com"
```

### Generate Secret Key:

```bash
# Generate a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and use it for `SECRET_KEY`.

## Step 5: Add PostgreSQL Database

Railway provides PostgreSQL databases:

```bash
# Add PostgreSQL service
railway add postgresql
```

This will automatically:
- Create a PostgreSQL database
- Set `DATABASE_URL` environment variable
- Your Django app will use it automatically

## Step 6: Update Settings for Production

The `settings.py` has been updated to:
- Use `DATABASE_URL` from environment
- Use `SECRET_KEY` from environment
- Serve static files with WhiteNoise
- Configure for Railway deployment

## Step 7: Deploy to Railway

### Option A: Using Railway CLI

```bash
# Deploy from current directory
railway up
```

### Option B: Using GitHub (Recommended)

1. **Push your code to GitHub** (already done ✅)
2. **Connect GitHub to Railway**:
   - Go to Railway dashboard
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository: `Asim066/BlogSite`
   - Railway will automatically deploy

## Step 8: Run Migrations & Setup Commands

After deployment, run these commands:

```bash
# Connect to Railway shell
railway run bash

# Or use Railway dashboard → Deployments → View Logs → Run Command
```

Then run:

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Setup groups
python manage.py setup_groups

# Populate categories and tags
python manage.py populate_categories_tags

# Collect static files (done automatically, but you can verify)
python manage.py collectstatic --noinput
```

## Step 9: Access Your Application

1. Railway will provide a URL like: `https://your-app.railway.app`
2. Access admin panel: `https://your-app.railway.app/admin/`
3. Login with your superuser credentials

## Step 10: Configure Custom Domain (Optional)

1. Go to Railway dashboard → Your Project → Settings
2. Click "Generate Domain" or add custom domain
3. Update `ALLOWED_HOSTS` with your domain

## Important Notes

### Static Files
- Static files are served using WhiteNoise
- `collectstatic` runs automatically on deploy
- No need for separate static file hosting

### Media Files
- For production, consider using:
  - **AWS S3** for media storage
  - **Cloudinary** for image hosting
  - **Railway Volumes** (persistent storage)

### Database
- Railway PostgreSQL is automatically managed
- Database backups are handled by Railway
- Connection string is in `DATABASE_URL`

### Environment Variables
Always set sensitive data as environment variables:
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- Database credentials (auto-set by Railway)

## Troubleshooting

### View Logs
```bash
railway logs
```

### Check Status
```bash
railway status
```

### Restart Service
```bash
railway restart
```

### Common Issues

1. **Static files not loading**:
   - Check `STATIC_ROOT` and `STATIC_URL` in settings
   - Verify `collectstatic` ran successfully

2. **Database connection errors**:
   - Verify PostgreSQL service is running
   - Check `DATABASE_URL` is set correctly

3. **500 errors**:
   - Check logs: `railway logs`
   - Verify all environment variables are set
   - Check `DEBUG=False` and proper error handling

## Quick Deploy Commands Summary

```bash
# 1. Login
railway login

# 2. Initialize
railway init

# 3. Add PostgreSQL
railway add postgresql

# 4. Set environment variables
railway variables set SECRET_KEY="your-key"
railway variables set DEBUG="False"
railway variables set ALLOWED_HOSTS="*.railway.app"

# 5. Deploy
railway up

# Or connect GitHub repo in Railway dashboard
```

## Cost

- Railway offers a **free tier** with:
  - $5 free credit monthly
  - 500 hours of usage
  - Perfect for small projects

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway

---

**Your app will be live at**: `https://your-app-name.railway.app`

