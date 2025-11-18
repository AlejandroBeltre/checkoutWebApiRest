#!/bin/bash

# Exit on error
set -e

echo "Starting entrypoint script..."

# Wait for database to be ready (if using external DB in future)
echo "Checking database connectivity..."

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist (optional, for admin access)
echo "Creating superuser if needed..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: username=admin, password=admin123')
else:
    print('Superuser already exists')
EOF

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Database setup completed successfully!"

# Execute the main command (passed as arguments to this script)
exec "$@"
