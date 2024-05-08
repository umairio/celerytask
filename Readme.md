
---

# Django User Management and Subscription System

This project showcases a Django-based system with an extended user model that uses email as the default identifier. It integrates a profile model with subscription start and end date-time fields, providing API endpoints for user login and subscription management. The system also employs Celery tasks to generate test data and update subscription dates hourly. Docker Compose is used for a simplified setup, and Redis is included to support Celery tasks.

## Project Structure
- **User Model**: Extends the Django user model to use email as the default identifier.
- **Profile Model**: Associates a one-to-one relationship with the User model, including subscription start and end date-times.
- **User Login**: Provides an API endpoint for user authentication.
- **Subscription Management**: Includes an API endpoint for updating subscription date and time with validation against past dates.
- **Celery Tasks**:
  - Populates both the User and Profile models with test data (50,000 records).
  - A task that updates subscription times to the current time for users whose subscriptions are at least one hour old.
- **Docker Compose**: Manages the Django application, Redis, and additional services for Celery tasks.

## Prerequisites
Ensure you have the following installed:
- Git
- Docker
- Docker Compose

## Setup and Installation
### Create a .env File
To store environment-specific settings, create a `.env` file in the root directory of your project with the following content:

```env
DEBUG=True
SECRET_KEY=GENERATE_YOUR_OWN_SECRET_KEY
CELERY_BROKER=redis://redis:6379/0
CELERY_BACKEND=redis://redis:6379/0
```

- **DEBUG**: Set to `True` for development. Change to `False` for production.
- **SECRET_KEY**: This must be a secure, unique, random string. Use a Django tool or an online generator to create a secret key.
- **CELERY_BROKER** and **CELERY_BACKEND**: Both point to the Redis service in Docker.

**To generate a secure `SECRET_KEY` for Django**, you can run the following command in a Django shell:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
Replace `GENERATE_YOUR_OWN_SECRET_KEY` with the output from this command.

### Clone the Repository
```bash
git clone https://github.com/umairio/celerytask.git
cd celerytask
```

### Start the Application with Docker Compose
```bash
docker-compose up
```

This command will build the Django application and start Redis, along with any other required services.

### Migrate the Database
```bash
docker-compose run web python manage.py migrate
```

### Create a Superuser
To create a Django superuser for accessing the admin interface, run the following command:

```bash
docker-compose run web python manage.py createsuperuser
```

This will prompt you to enter a username, email address, and password for the superuser. Once completed, you can log into the Django admin interface to manage users and other admin-related tasks.

### Stop the Application
```bash
docker-compose down
```

This command stops all containers and removes them.

## Troubleshooting
If you encounter issues, try the following:
- Ensure Docker and Docker Compose are installed and running.
- Check that you've provided the correct environment variables in `.env`.
- Use `docker-compose logs` to review logs from the running containers.

## Contributing
Contributions are welcome. Here's how you can contribute:
- Fork the repository and create a new branch for your feature or bug fix.
- Commit and push your changes.
- Open a pull request for review.

## Acknowledgements
Thank you to the Django and Docker communities for providing the tools and resources to create this project, and to the Celery project for its powerful task queue capabilities.

---
