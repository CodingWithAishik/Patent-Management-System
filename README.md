# IIEST Shibpur Patent & Copyright Management System

A comprehensive Django-based GUI application for managing patents (filed & granted) and copyrights for IIEST, Shibpur.

## Features

✅ **Dashboard with Statistics**
- Total counts for Copyrights, Patents Filed, and Patents Granted
- Quick navigation to all sections
- Recent entries display

✅ **Full CRUD Operations**
- Create, Read, Update, Delete for all three data types
- Separate interfaces for Copyrights, Filed Patents, and Granted Patents

✅ **Advanced Search Functionality**
- Multi-parameter dynamic search
- Select one or more search fields
- Partial matching (case-insensitive)
- Separate search for each data type

✅ **Professional UI**
- Light and Dark theme support with toggle
- Professional blue color scheme
- Responsive design
- Clean and intuitive interface

✅ **No Authentication Required**
- Open access for all users
- Simplified workflow

## Technology Stack

- **Backend**: Django 6.0
- **Database**: SQLite (default)
- **Frontend**: HTML5, CSS3, JavaScript
- **Python**: 3.12.6

## Project Structure

```
Patent_GUI/
├── venv/                           # Virtual environment
├── db.sqlite3                      # SQLite database
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
├── patent_project/                 # Main project folder
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── patents/                        # Main application
│   ├── models.py                   # Copyright, PatentFiled, PatentGranted models
│   ├── views.py                    # All CRUD and search views
│   ├── urls.py                     # URL routing
│   ├── management/
│   │   └── commands/
│   │       └── import_csv.py       # CSV import command
│   ├── templates/
│   │   └── patents/
│   │       ├── base.html           # Base template with navigation
│   │       ├── home.html           # Dashboard
│   │       ├── copyright_*.html    # Copyright templates
│   │       ├── filed_*.html        # Filed patent templates
│   │       └── granted_*.html      # Granted patent templates
│   └── static/
│       └── patents/
│           ├── css/
│           │   └── styles.css      # Professional blue theme CSS
│           └── js/
│               └── main.js         # Theme toggle & dynamic search JS
└── CSV Files (3 files)             # Original data sources
```

## Installation & Setup

### 1. Prerequisites
- Python 3.12.6 installed
- Git installed

### 2. Initial Setup

```powershell
# Navigate to project directory
cd "C:\Users\Aishik Banerjee\Patent_GUI"

# Virtual environment is already created
# Activate it:
.\venv\Scripts\activate

# Install dependencies (if needed on fresh setup)
pip install -r requirements.txt
```

### 3. Database Setup

Database is already set up with migrations applied and CSV data imported:
- 6 Copyright records
- 27 Filed Patent records
- 51 Granted Patent records

**To re-import CSV data (if needed):**
```powershell
python manage.py import_csv
```

### 4. Run Development Server

```powershell
python manage.py runserver
```

Access the application at: **http://127.0.0.1:8000/**

## Usage Guide

### Homepage Dashboard
- View total counts for all three data types
- Quick access buttons to view all, search, or add new records
- Recent entries displayed for each category

### Navigation
- **Home**: Dashboard with statistics
- **Copyrights**: Manage copyright records
- **Patents Filed**: Manage filed patent applications
- **Patents Granted**: Manage granted patents
- **Theme Toggle**: Switch between light and dark themes (🌙/☀️)

### Search Functionality

1. Click "Search" button from any list page
2. Select one or more search parameters using checkboxes
3. Input fields appear dynamically based on selection
4. Enter search values and press "Search"
5. Results display matching records with partial matching

**Available Search Parameters:**

**Copyrights:**
- Year
- Faculty/Students
- Title
- Inventors

**Patents Filed:**
- Date of Filing
- Inventors
- Title
- Application Number
- Applicant Name

**Patents Granted:**
- Patent Number
- Date of Grant
- Inventors
- Title
- Filing Institute

### CRUD Operations

**Create:**
- Click "Add New" button
- Fill in form fields
- Click "Save"

**Read/View:**
- Click on data type from navigation
- View all records in table format

**Update:**
- Click "Edit" button on any record
- Modify fields
- Click "Save"

**Delete:**
- Click "Delete" button on any record
- Confirm deletion
- Click "Yes, Delete"

## Data Model

### Copyright
- Serial Number
- Year
- Name of Faculty/Students
- Title of Copy rights
- Filing Informations
- Inventor(s)

### Patent Filed
- Serial Number
- Date of Filing
- Inventor(s)/Faculty/Student
- Title of Patent
- Application Number
- Date of Publication
- Abstract
- Applicant Name

### Patent Granted
- Serial Number
- Granted Patent No.
- Date of Grant
- Inventor(s)/Faculty/Student
- Title of Patent
- Application Number
- Date of Publication
- Patent Filing Institute/Individual(s)
- Abstract

## Theme Support

The application supports two themes:

**Light Theme** (Default):
- Professional blue color scheme
- Clean white backgrounds
- High contrast for readability

**Dark Theme**:
- Dark blue backgrounds
- Reduced eye strain in low-light
- Maintains professional appearance

Toggle theme using the button in the navigation bar. Theme preference is saved in browser's localStorage.

## Git Repository

Initialized with proper .gitignore to exclude:
- Virtual environment (venv/)
- Database file (db.sqlite3)
- Python cache files (__pycache__/, *.pyc)
- IDE files

## Troubleshooting

**Issue: Static files not loading**
```powershell
python manage.py collectstatic
```

**Issue: Database needs reset**
```powershell
# Delete db.sqlite3
# Run migrations again
python manage.py migrate
python manage.py import_csv
```

**Issue: Port 8000 already in use**
```powershell
python manage.py runserver 8080
```

## Future Enhancements (Optional)

- Export search results to CSV/Excel
- Advanced filtering and sorting
- Bulk import/export functionality
- Data visualization (charts/graphs)
- Print-friendly views
- Backup/restore functionality

## Developer Information

**Institution**: Indian Institute of Engineering Science and Technology (IIEST), Shibpur
**Purpose**: Intellectual Property Management System
**Framework**: Django 6.0
**Database**: SQLite

## Deployment

### Deploy to PythonAnywhere (Recommended for Beginners)

This project is ready to deploy on PythonAnywhere with SQLite database.

**📖 Complete Step-by-Step Guide**: See [PYTHONANYWHERE_DEPLOYMENT.md](PYTHONANYWHERE_DEPLOYMENT.md)

**Quick Summary:**
1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com) (FREE)
2. Clone this repository or upload files
3. Create virtual environment & install dependencies
4. Configure web app through their Web tab
5. Your site is live at `yourname.pythonanywhere.com`

**Why PythonAnywhere?**
- ✅ Works with SQLite (no database migration needed)
- ✅ Free tier available
- ✅ Beginner-friendly web interface
- ✅ Django-native platform

### Alternative: Vercel Deployment

Files included for Vercel deployment:
- `vercel.json` - Vercel configuration
- `build.sh` - Build script
- `.env.example` - Environment variables template

**Note**: Vercel requires PostgreSQL (not SQLite). See deployment guide for details.

## License

This is an internal management system for IIEST, Shibpur.

---

**Server Status**: ✅ Running at http://127.0.0.1:8000/

**Data Imported**: 
- ✅ 6 Copyrights
- ✅ 27 Patents Filed
- ✅ 51 Patents Granted

**All Features**: ✅ Fully Functional
