# 🎓 LearnVishwa

LearnVishwa is a Django-based student project repository platform where students can upload and showcase their academic projects. Users can explore projects, watch videos, like projects, and filter them by branch, class, and domain.

## Features

- User Authentication
- Project Upload
- Video Repository
- Project Search & Filters
- Like System
- Password Reset
- Responsive UI

---

# 📁 Project Structure

```
projectlib/
│
├── media/
├── projectlib/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── static/
│   ├── css/
│   ├── fonts/
│   ├── img/
│   └── js/
│
├── students/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

### Move into the Project Directory

```bash
cd YOUR_REPOSITORY
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Database Migrations

```bash
python manage.py migrate
```

### Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```
