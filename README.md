# CampusMarket

University campus marketplace built with Django. A platform for students to buy, sell, and trade items within their campus community.

## Features

- **User Accounts** — Registration, login, and profile management with a custom user model
- **Listings** — Create, browse, edit, and delete marketplace listings with image uploads
- **Messaging** — Direct messaging between buyers and sellers
- **Search & Filter** — Find items quickly across the marketplace
- **Responsive Design** — Mobile-friendly interface powered by Bootstrap 5

## Tech Stack

- **Backend:** Django 5.x (Python)
- **Database:** SQLite (development)
- **Frontend:** Django Templates + Bootstrap 5
- **Forms:** django-crispy-forms with crispy-bootstrap5
- **Image Handling:** Pillow

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd CampusMarket
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run database migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to view the application.

## Project Structure

```
CampusMarket/
├── campus_market/      # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/           # User authentication & profiles
├── listings/           # Marketplace listings
├── messaging/          # User-to-user messaging
├── templates/          # Global templates
├── static/             # Static assets (CSS, JS, images)
├── media/              # User-uploaded files
├── manage.py
└── requirements.txt
```

## License

This project is for educational purposes.
