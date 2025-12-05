# GitHub Setup Guide

## Step 1: Install Git

If Git is not installed on your system:

**Windows:**
1. Download Git from: https://git-scm.com/download/win
2. Run the installer
3. Restart your terminal/PowerShell

**Verify Installation:**
```bash
git --version
```

## Step 2: Configure Git (First Time Only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 3: Initialize Git Repository

```bash
# Navigate to your project directory
cd BlogSite

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Advanced Blog Platform"
```

## Step 4: Create GitHub Repository

1. Go to https://github.com
2. Click the **"+"** icon in the top right
3. Select **"New repository"**
4. Repository name: `advanced-blog` (or your preferred name)
5. Description: "Premium Django Blog Platform"
6. Choose **Public** or **Private**
7. **DO NOT** initialize with README, .gitignore, or license (we already have these)
8. Click **"Create repository"**

## Step 5: Connect and Push to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/advanced-blog.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Alternative: Using SSH

If you have SSH keys set up:

```bash
git remote add origin git@github.com:YOUR_USERNAME/advanced-blog.git
git branch -M main
git push -u origin main
```

## Important Notes

⚠️ **Before pushing, make sure:**
- ✅ `.gitignore` is in place (already created)
- ✅ `DEBUG = False` in production (or use environment variables)
- ✅ `SECRET_KEY` should be in environment variables for production
- ✅ Database file (`db.sqlite3`) is in `.gitignore` (already included)

## Future Updates

After making changes:

```bash
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Description of changes"

# Push
git push
```

## Branching (Optional)

```bash
# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main

# Merge branch
git merge feature-name
```

---

**Need Help?**
- Git Documentation: https://git-scm.com/doc
- GitHub Guides: https://guides.github.com

