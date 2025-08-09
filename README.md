# 🐍 Django Project

[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Made with ❤️ by Kaiser-iDusk](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red.svg)]()

A Django project configured for **India Standard Time (IST)**, ensuring time-sensitive features like scheduling respect your local timezone and prevent users from selecting a time earlier than the current time.

---

## 📦 Features
- 🌏 **Timezone set to Asia/Kolkata**
- ⏱ Prevents scheduling times earlier than the current time (with a 1-minute buffer)
- 🔐 Secure Django setup
- 📊 Scalable project structure

---

## 🚀 Getting Started

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Kaiser-iDusk/e_commerce.git
cd e_commerce
```

### 2️⃣ Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  
```

On Windows: 
```powershell
venv\Scripts\activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Timezone in settings.py
```python
# settings.py
TIME_ZONE = 'Asia/Kolkata'
USE_TZ = True
```

⏱ Time Validation Example
In your form or model clean method:

```python
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

def clean_preferred_time(self):
    preferred_time = self.cleaned_data['preferred_time']
    now = timezone.localtime(timezone.now()) + timedelta(minutes=1)  # 1 min buffer
    if preferred_time < now:
        raise ValidationError("Please choose a time at least 1 minute from now.")
    return preferred_time
```

### ▶ Run the project
```bash
python manage.py migrate
python manage.py runserver
```

### 🛠 Tech Stack
Backend: Django

Database: SQLite / PostgreSQL

Frontend: HTML, CSS, JS, jQUery