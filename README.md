# EventHub — Backend API

Django REST API for **EventHub**, a full-stack event booking platform.

**🔗 Frontend Repo:** [eventhub-frontend](https://github.com/NARESHRAJESH/eventhub-frontend)
**🔗 Live Demo:** [https://eventhub-frontend-beryl.vercel.app](https://eventhub-frontend-beryl.vercel.app)

---

## 🛠 Tech Stack

- **Django 6.1** + **Django REST Framework**
- **Token Authentication** (DRF)
- **PostgreSQL** on Render (production)
- **Mysql** for local development
- **Cloudinary** for image hosting
- **WhiteNoise** for serving static files
- **Gunicorn** as the production WSGI server
- Deployed on **Render**

---

## 🚀 Features

### Authentication
- Token-based authentication
- User / Organizer registration with role selection
- Email domain validation
- Password strength validation

### Events API
- List all events (public)
- Create event (organizer only)
- Update / delete event (owner only)
- **Multi-tenant isolation** — organizers can only manage their own events

### Bookings API
- Create booking (authenticated users)
- Automatic seat availability check
- Booking history per user

### Organizer Dashboard
- Real-time statistics: total events, bookings, customers, revenue

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.12+
- PostgreSQL (optional — SQLite works for local development)

### Installation

```bash
git clone https://github.com/NARESHRAJESH/eventhub-backend.git
cd eventhub-backend

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt

# Create a .env file (see .env.example)

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## 🔐 Environment Variables (`.env`)

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=postgresql://user:password@host:port/dbname

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=your_password
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/register/` | User / Organizer registration | Public |
| POST | `/api/login/` | Login (returns token) | Public |
| GET | `/api/events/` | List all events | Public |
| POST | `/api/events/` | Create event | Organizer |
| GET | `/api/events/<id>/` | Event details | Public |
| PUT | `/api/events/<id>/` | Update event | Owner |
| DELETE | `/api/events/<id>/` | Delete event | Owner |
| POST | `/api/bookings/` | Create booking | Authenticated |
| GET | `/api/my-bookings/` | Current user's bookings | Authenticated |
| GET | `/api/organizer/dashboard/` | Organizer statistics | Organizer |

---

## 🧪 Testing the API

You can test the API endpoints using:
- **Django REST Framework's browsable API** (visit endpoints in browser)
- **Postman** or **Insomnia**
- **curl** from the command line

For authenticated endpoints, include the token in the header:

```
Authorization: Token <your_token_here>
```

---

## 🔒 Security

- Token-based authentication (DRF)
- Password hashing (Django default)
- CSRF protection
- CORS configured for production origins
- Object-level permissions (organizers can modify only their own events)
- Environment variables for all secrets
- `.env` ignored in `.gitignore`

---

## 📦 Deployment

This backend is deployed on **Render** with the following configuration:

- **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- **Start Command:** `gunicorn config.wsgi:application`
- **Database:** PostgreSQL (Render add-on)
- **Media Storage:** Cloudinary

---

## 👨‍💻 Author

**Naresh Rajesh**
- GitHub: [@NARESHRAJESH](https://github.com/NARESHRAJESH)
- Live Demo: [EventHub](https://eventhub-frontend-beryl.vercel.app)

---

⭐ **If you like this project, please give it a star!**
