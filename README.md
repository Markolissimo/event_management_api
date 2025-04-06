# Event Management API

A Django REST API for managing events, user registrations, and email notifications

## Features

- **User Management**
  - JWT-based authentication
  - Custom user model with email authentication
  - User registration and profile management

- **Event Management**
  - Create, read, update, and delete events
  - Event registration system
  - Advanced filtering and search capabilities
  - Capacity management

- **Notifications**
  - Automated email notifications for event registrations
  - Asynchronous processing using Celery
  - Customizable email templates

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- PostgreSQL
- Redis (for Celery)

## Tech Stack

- Django 5.2
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- JWT Authentication
- Docker

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd event-management
```

### 2. Environment Setup

Create a `.env` file in the project root:

```env
# Django
DEBUG=1
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgres://postgres:postgres@db:5432/event_management

# Redis
REDIS_URL=redis://redis:6379/0

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your.email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
JWT_SECRET_KEY=your-jwt-secret-key
```

### 3. Start the Application

Using Docker Compose:
```bash
docker-compose up --build
```

### 4. Initialize the Database

```bash
docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py createsuperuser
```

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT tokens
- `POST /api/token/refresh/` - Refresh JWT token

### Users
- `POST /api/users/` - Register new user
- `GET /api/users/me/` - Get current user profile

### Events
- `GET /api/events/` - List all events
- `POST /api/events/` - Create new event
- `GET /api/events/{id}/` - Get event details
- `PUT/PATCH /api/events/{id}/` - Update event
- `DELETE /api/events/{id}/` - Delete event
- `POST /api/events/{id}/register/` - Register for event

### Event Filtering
The following filters are available for the events endpoint:
- `title` - Search by title (contains)
- `location` - Search by location
- `min_date` & `max_date` - Filter by date range
- `min_price` & `max_price` - Filter by price range
- `is_active` - Filter active events
- `has_available_seats` - Filter events with available capacity
- `upcoming` - Filter upcoming events

Example:
```
GET /api/events/?upcoming=true&has_available_seats=true&location=center
```

## Email Configuration

For email notifications to work:

1. If using Gmail:
   - Enable 2-Step Verification
   - Generate App Password
   - Use App Password in `.env` file

2. For development/testing:
   - Set `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` in settings.py
   - Emails will be printed to console

## Development

### Running Tests
```bash
docker-compose exec web python manage.py test
```

### Code Style
```bash
docker-compose exec web flake8
```

### API Documentation
Access the API documentation at:
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`

## Deployment

For production deployment:

1. Update `.env` file with production settings:
   - Set `DEBUG=0`
   - Update `ALLOWED_HOSTS`
   - Use secure passwords/keys
   - Configure production email settings

2. Build and run:
```bash
docker-compose -f docker-compose.prod.yml up --build
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
