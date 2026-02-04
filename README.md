# News Application

## Overview
This is a Django-based News Application that models a simple news platform. Journalists submit articles, editors approve them, and readers subscribe to publishers or journalists to receive published content.

---

# STEP 1 – Install Required Software

### 1.1 Install Python

1. Open your web browser
2. Go to https://www.python.org/downloads/
3. Download **Python 3.10 or newer**
4. During installation:
   - Tick **“Add Python to PATH”**
   - Click **Install**
5. Finish installation

Verify Python is installed:

1. Open **Command Prompt / Terminal**
2. Type:

```bash
python --version
```
---

### 1.2 Install MySQL Server

    1. Open your web browser
    2. Go to https://dev.mysql.com/downloads/mysql/
    3. Download MySQL Community Server
    4. Run the installer
    5. Choose Developer Default
    6. When asked to create a password:
        - Write it down
        - You will need it later
    7. Finish installation

Verify MySQL is installed:

1. Open **Command Prompt / Terminal**
2. Type:

```bash
mysql --version
```

---

### 1.3 Install Git
    1. Open your web browser
    2. Go to https://git-scm.com/downloads
    3. Download Git for Windows
    4. Run the installer
    5. Finish installation

Verify Git is installed:

1. Open **Command Prompt / Terminal**
2. Type:

```bash
git --version
```

---

# STEP 2 – Clone the Repository

```bash
git clone https://github.com/Roodtf7/News-Application.git
cd News-Application
```

# STEP 3. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

# STEP 4. Install dependencies
```bash
pip install -r requirements.txt
```

# STEP 5. Open MySQL and Log in
5.1 Open Terminal
5.2 Type:
```sql
mysql -u root -p
```
5.3 Type your password
5.4 
```sql
CREATE DATABASE newsapp_db;
```
5.5 Confirm database was created:
```sql
SHOW DATABASES;
```
5.6 Exit MySQL:
```sql
exit;
```

### 6. Create a MySQL User for the Project
6.1 Log back into MySQL:
```bash
mysql -u root -p
```

6.2 Enter your MySQL password again. Then run each command one at a time:
```sql
CREATE USER 'newsuser'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON newsapp_db.* TO 'newsuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```
Save these credentials:

Username: newsuser
Password: password123

### 7. Update Django Database Settings
7.1 Open the project folder in a code editor
7.2 Open the news_project/settings.py file
7.3 Update the DATABASES setting:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'newsapp_db',
        'USER': 'newsuser',
        'PASSWORD': 'password123',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 8. Apply database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 9. Create a superuser
```bash
python manage.py createsuperuser
```
Enter a username
Enter a password

### 10. Run the development server
```bash
python manage.py runserver
```

### 11. Access the application
Open your web browser and navigate to http://localhost:8000 to access the application.


---

## User Roles

- **Reader** – Subscribes to publishers or journalists to receive published articles.
- **Journalist** – Creates articles and submits them for approval.
- **Editor** – Reviews and approves submitted articles before publication.

Roles are selected during user registration.

---

## Application Structure

The project is organised into modular Django applications:

- **users** – Custom user model and role-based authentication
- **publishers** – Publisher entities and editor associations
- **articles** – Article and newsletter creation and approval
- **subscriptions** – Reader subscriptions to journalists or publishers
- **notifications** – Notification handling on article approval
- **api** – Read-only REST API for retrieving published articles

Each application contains its own templates to maintain proper separation of concerns.

---

## Notes

- Editorial actions can be performed via the web interface or Django Admin.
- Email notifications use Django’s console email backend for development.
- The REST API is read-only and requires authentication.
- Project folder names use underscores instead of spaces for portability.

---

## Technology Stack

- Python
- Django
- Django REST Framework
- MySQL / MariaDB
