#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py shell <<EOF
from django.contrib.auth.models import User

# Verificar si el usuario ya existe
if not User.objects.filter(username='admin').exists():
    # Crear un nuevo superusuario
    User.objects.create_superuser('superuser', 'superuser@mail.com', 's3*1416u')
EOF
