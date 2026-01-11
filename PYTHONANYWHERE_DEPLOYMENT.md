# PythonAnywhere Deployment Guide

## Complete Step-by-Step Instructions for Beginners

### **Prerequisites**
- Your Django project (this one!)
- A GitHub account (optional, but recommended)
- A PythonAnywhere account (free)

---

## **Step 1: Prepare Your Project**

### A. Update ALLOWED_HOSTS
In `patent_project/settings.py`, you'll need to add your PythonAnywhere URL later.
For now, we've prepared the project for deployment.

### B. Push to GitHub (Recommended Method)

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Ready for deployment"
   ```

2. **Create a new repository on GitHub:**
   - Go to https://github.com/new
   - Name it: `Patent-Management-System`
   - Don't add README, .gitignore, or license
   - Click "Create repository"

3. **Push your code:**
   ```bash
   git remote add origin https://github.com/YOUR-USERNAME/Patent-Management-System.git
   git branch -M main
   git push -u origin main
   ```

---

## **Step 2: Sign Up for PythonAnywhere**

1. Go to https://www.pythonanywhere.com
2. Click **"Pricing & signup"**
3. Choose **"Create a Beginner account"** (FREE)
4. Complete the registration
5. Verify your email

---

## **Step 3: Clone Your Project on PythonAnywhere**

1. **Open a Bash Console:**
   - From your PythonAnywhere Dashboard
   - Click **"Consoles"** → **"Bash"**

2. **Clone your repository:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/Patent-Management-System.git
   cd Patent-Management-System
   ```

   **Alternative (if not using GitHub):**
   - Upload files using the **"Files"** tab
   - Or use `wget` to download a ZIP file

---

## **Step 4: Set Up Virtual Environment**

In the Bash console:

```bash
# Create virtual environment with Python 3.10
mkvirtualenv --python=/usr/bin/python3.10 patent_env

# Activate it (should auto-activate after creation)
workon patent_env

# Install dependencies
pip install -r requirements.txt
```

**Note:** We're using Python 3.10 because PythonAnywhere doesn't support Python 3.12 yet. The project has been updated to use Django 5.1 which is fully compatible.

---

## **Step 5: Configure the Web App**

1. **Go to Web Tab:**
   - Click **"Web"** in the top menu
   - Click **"Add a new web app"**

2. **Follow the wizard:**
   - Click **"Next"** (accept default domain)
   - Select **"Manual configuration"**
   - Choose **"Python 3.10"**
   - Click **"Next"**

3. **Configure Virtual Environment:**
   - In the **"Virtualenv"** section
   - Enter: `/home/YOUR-USERNAME/.virtualenvs/patent_env`
   - (Replace YOUR-USERNAME with your actual username)

4. **Configure WSGI File:**
   - In the **"Code"** section
   - Click on the WSGI configuration file link (e.g., `/var/www/youruser_pythonanywhere_com_wsgi.py`)
   - **Delete all contents** and replace with:

   ```python
   import os
   import sys

   # Add your project directory to the sys.path
   path = '/home/YOUR-USERNAME/Patent-Management-System'
   if path not in sys.path:
       sys.path.insert(0, path)

   # Set environment variable for Django settings
   os.environ['DJANGO_SETTINGS_MODULE'] = 'patent_project.settings'

   # Import Django WSGI application
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
   - Replace `YOUR-USERNAME` with your PythonAnywhere username
   - Click **"Save"**

5. **Configure Static Files:**
   - Scroll to **"Static files"** section
   - Add two entries:

   | URL          | Directory                                                    |
   |--------------|--------------------------------------------------------------|
   | /static/     | /home/YOUR-USERNAME/Patent-Management-System/staticfiles    |
   | /static/     | /home/YOUR-USERNAME/Patent-Management-System/patents/static |

---

## **Step 6: Collect Static Files**

Go back to your Bash console:

```bash
cd ~/Patent-Management-System
workon patent_env
python manage.py collectstatic --noinput
```

---

## **Step 7: Set Up Database**

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Import your CSV data (if needed)
python manage.py import_csv
```

---

## **Step 8: Update ALLOWED_HOSTS**

1. **In the Bash console, edit settings.py:**
   ```bash
   nano patent_project/settings.py
   ```

2. **Find the ALLOWED_HOSTS line and update it:**
   ```python
   ALLOWED_HOSTS = ['YOUR-USERNAME.pythonanywhere.com', 'localhost', '127.0.0.1']
   ```
   - Replace `YOUR-USERNAME` with your actual username

3. **Save the file:**
   - Press `Ctrl + O` (save)
   - Press `Enter`
   - Press `Ctrl + X` (exit)

**OR** Use the Files tab and edit `patent_project/settings.py` in the web editor.

---

## **Step 9: Reload Your Web App**

1. Go back to the **"Web"** tab
2. Scroll to the top
3. Click the big green **"Reload"** button
4. Wait for it to reload (takes a few seconds)

---

## **Step 10: Visit Your Website!**

Your website should now be live at:
```
https://YOUR-USERNAME.pythonanywhere.com
```

🎉 **Congratulations! Your Django app is deployed!**

---

## **Troubleshooting**

### **Error: Site doesn't load**
1. Check the **"Error log"** in the Web tab
2. Common issues:
   - Wrong path in WSGI file
   - Virtual environment path incorrect
   - ALLOWED_HOSTS not updated

### **Error: Static files not loading**
1. Make sure you ran `collectstatic`
2. Check static files paths in Web tab
3. Hard refresh browser (Ctrl + Shift + R)

### **Error: Database errors**
1. Make sure migrations ran successfully
2. Check file permissions on `db.sqlite3`

### **Can't see changes after updating code**
1. Always click **"Reload"** in the Web tab after changes
2. Clear browser cache

---

## **Updating Your Deployed Site**

When you make changes to your code:

```bash
# In PythonAnywhere Bash console
cd ~/Patent-Management-System
git pull  # If using GitHub

# If you changed models
python manage.py makemigrations
python manage.py migrate

# If you changed static files
python manage.py collectstatic --noinput

# Then reload web app from Web tab
```

---

## **Important Notes**

✅ **Free tier limitations:**
- One web app
- Your site sleeps after inactivity (wakes up when visited)
- Limited CPU/bandwidth (sufficient for small projects)

✅ **Your data:**
- Your SQLite database persists across reloads
- Backup your `db.sqlite3` file regularly

✅ **Domain:**
- Free tier: `yourname.pythonanywhere.com`
- Paid: Can use custom domain

---

## **Need Help?**

- PythonAnywhere Forums: https://www.pythonanywhere.com/forums/
- PythonAnywhere Help: https://help.pythonanywhere.com/
- Django Documentation: https://docs.djangoproject.com/

---

## **Quick Reference Commands**

```bash
# Access bash console
# Use the Consoles tab

# Activate virtual environment
workon patent_env

# Navigate to project
cd ~/Patent-Management-System

# Run Django commands
python manage.py [command]

# View logs
tail -f /var/log/youruser.pythonanywhere.com.error.log
```
