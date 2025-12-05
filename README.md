# Advanced Blog Platform

A premium, full-featured Django blog platform with modern UI/UX design, user authentication, role-based permissions, rich text editing, and comprehensive content management.

## 🚀 Features

- **User Authentication & Roles**: Admin, Author, and Reader roles with different access levels
- **Rich Text Editor**: CKEditor integration for beautiful content creation
- **Categories & Tags**: Organize posts with categories and tags
- **Comments System**: Comment moderation and spam prevention
- **Search & Filter**: Search posts and filter by category/tag
- **Responsive Design**: Modern, premium UI that works on all devices
- **Image Upload**: Featured images for posts with Pillow support
- **SEO-Friendly**: Auto-generated slugs for better URLs
- **Dashboard**: Author dashboard for managing posts
- **Pagination**: Efficient post listing with pagination

## 📋 Prerequisites

- Python 3.11 or higher (Python 3.12 recommended)
- pip (Python package manager)
- Virtual environment (recommended)

## 🛠️ Installation & Setup

### 1. Clone or Navigate to Project

```bash
cd BlogSite
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
```

### 5. Setup User Groups & Permissions

```bash
# Create default user groups (Admin, Author, Reader)
python manage.py setup_groups
```

### 6. Populate Categories & Tags

```bash
# Add default categories and tags
python manage.py populate_categories_tags
```

### 7. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## 🏃 Running the Application

### Start Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

### Access Admin Panel

Navigate to: **http://127.0.0.1:8000/admin/**

Login with your superuser credentials.

## 📁 Project Structure

```
BlogSite/
│
├── advanced_blog/              # Main Django project settings
│   ├── __init__.py
│   ├── settings.py            # Project configuration
│   ├── urls.py                # Main URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── blog/                      # Blog application
│   ├── __init__.py
│   ├── models.py              # Post, Category, Tag, Comment models
│   ├── views.py               # View logic
│   ├── urls.py                # Blog URL patterns
│   ├── forms.py               # Form definitions
│   ├── admin.py               # Admin customization
│   ├── signals.py             # Django signals
│   ├── apps.py
│   │
│   ├── management/
│   │   └── commands/
│   │       ├── setup_groups.py              # Create user groups
│   │       └── populate_categories_tags.py  # Populate categories/tags
│   │
│   └── migrations/           # Database migrations
│
├── accounts/                   # User authentication app
│   ├── __init__.py
│   ├── models.py
│   ├── views.py               # Registration, login, profile
│   ├── forms.py               # User registration form
│   ├── urls.py                # Auth URL patterns
│   ├── middleware.py          # Custom middleware
│   ├── permissions.py         # Permission helpers
│   └── admin.py
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── navbar.html            # Navigation bar
│   ├── footer.html            # Footer
│   │
│   ├── accounts/
│   │   ├── register.html      # Registration page
│   │   ├── login.html         # Login page
│   │   └── profile.html       # User profile
│   │
│   └── blog/
│       ├── home.html          # Homepage/blog list
│       ├── post_detail.html   # Post detail page
│       ├── dashboard.html     # Author dashboard
│       ├── post_form.html     # Create/Edit post form
│       └── comment_moderation.html  # Comment moderation
│
├── static/                     # Static files (CSS, JS, images)
│   ├── css/
│   │   ├── global.css         # Global styles & variables
│   │   ├── custom.css         # Additional custom styles
│   │   │
│   │   ├── components/
│   │   │   ├── navbar.css     # Navigation styles
│   │   │   └── footer.css     # Footer styles
│   │   │
│   │   └── pages/
│   │       ├── home.css       # Homepage styles
│   │       ├── dashboard.css  # Dashboard styles
│   │       └── post_form.css # Form styles
│   │
│   ├── js/
│   │   └── main.js            # Main JavaScript
│   │
│   └── images/                # Image uploads
│
├── media/                      # User-uploaded media files
│   └── posts/                  # Post images
│
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 👥 User Roles & Permissions

### Admin
- Full access to all features
- Can manage all posts, comments, categories, tags
- Access to admin panel
- Can moderate comments

### Author
- Can create, edit, and delete own posts
- Can moderate comments on own posts
- Access to author dashboard
- Can publish/draft posts

### Reader
- Can view published posts
- Can add comments
- Can search and filter posts
- No content creation access

## 🎯 How to Use

### 1. Registration & Login

**Register a New User:**
1. Go to homepage
2. Click "Sign Up" in navbar
3. Fill in details (Username, Email, Password)
4. Select role: **User/Reader** or **Author**
5. Click "Register"

**Login:**
1. Click "Login" in navbar
2. Enter username and password
3. Click "Login"

### 2. Creating Posts (Authors/Admins)

1. **Login** as Author or Admin
2. Go to **Dashboard** (from navbar)
3. Click **"Create New Post"** button
4. Fill in the form:
   - **Title**: Post title
   - **Content**: Use rich text editor
   - **Category**: Select from dropdown (30+ categories available)
   - **Tags**: Select multiple tags (100+ tags available)
   - **Status**: Draft or Published
   - **Featured Image**: Upload image (optional)
5. Click **"Create Post"**

### 3. Managing Posts

**View All Posts:**
- Go to **Dashboard** to see all your posts

**Edit Post:**
- Click **Edit** button (pencil icon) next to post in dashboard
- Make changes and click **"Update Post"**

**Delete Post:**
- Click **Delete** button (trash icon) next to post
- Confirm deletion

### 4. Commenting (All Users)

1. Navigate to any published post
2. Scroll to **Comments** section
3. Write your comment
4. Click **"Post Comment"**
5. Comment will be pending approval (if moderation enabled)

### 5. Comment Moderation (Authors/Admins)

1. Go to **"Moderate"** in navbar (Admin only)
2. Or click **"Moderate Comments"** on post detail page
3. Approve or delete comments

### 6. Searching & Filtering

**Search:**
- Use search bar in navbar
- Enter keywords and press Enter

**Filter by Category:**
- Click category name in sidebar or filter buttons
- Or click category link on any post

**Filter by Tag:**
- Click tag on any post
- Or use tag links in sidebar

## 🎨 Design System

The platform uses a modern, premium design system:

- **Colors**: Indigo primary (#4F46E5), Teal secondary (#00ADB5)
- **Typography**: Poppins (headings), Inter (body)
- **Components**: Cards, buttons, forms with smooth animations
- **Responsive**: Mobile-first design, works on all screen sizes

## 📝 Management Commands

### Setup User Groups
```bash
python manage.py setup_groups
```
Creates Admin, Author, and Reader groups with appropriate permissions.

### Populate Categories & Tags
```bash
python manage.py populate_categories_tags
```
Adds 30+ default categories and 100+ tags to the database.

## 🔧 Configuration

### Settings File
Edit `advanced_blog/settings.py` for:
- Database configuration
- Email settings (for notifications)
- Static/Media file paths
- Installed apps

### Email Configuration (Optional)
Uncomment and configure email settings in `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

## 🐛 Troubleshooting

### Admin Panel Issues
If you encounter errors in admin panel (Python 3.14.1 compatibility):
- Use Python 3.12 instead (recommended)
- Or use management commands instead of admin panel

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Database Issues
```bash
python manage.py makemigrations
python manage.py migrate
```

### Missing Categories/Tags
```bash
python manage.py populate_categories_tags
```

## 📦 Dependencies

Key packages:
- Django 4.2.27
- django-ckeditor (Rich text editor)
- django-taggit (Tagging system)
- Pillow (Image processing)

See `requirements.txt` for complete list.

## 🔐 Security Notes

- Never commit `settings.py` with sensitive data
- Use environment variables for secrets
- Keep `DEBUG = False` in production
- Use strong passwords for admin accounts

## 📄 License

This project is open source and available for personal and commercial use.

## 🤝 Support

For issues or questions:
1. Check this README
2. Review Django documentation
3. Check project structure and settings

## 🎉 Getting Started Checklist

- [ ] Install Python 3.11+
- [ ] Create virtual environment
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Run migrations (`python manage.py migrate`)
- [ ] Create superuser (`python manage.py createsuperuser`)
- [ ] Setup groups (`python manage.py setup_groups`)
- [ ] Populate categories/tags (`python manage.py populate_categories_tags`)
- [ ] Run server (`python manage.py runserver`)
- [ ] Access homepage at http://127.0.0.1:8000/
- [ ] Login and start creating posts!

---

**Built with ❤️ using Django**
