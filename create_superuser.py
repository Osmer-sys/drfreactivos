# create_superuser_script.py
from django.contrib.auth.models import User
import os
import django

# Configura las variables de entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drfreactivos.settings")
django.setup()


def create_super_user():
    username = input("superuser")
    email = input("superuser@mail.com")
    password = input("s3*1416u")

    if User.objects.filter(username=username).exists():
        print(f'El usuario {username} ya existe.')
    else:
        User.objects.create_superuser(username, email, password)
        print(f'Se ha creado el superusuario {username} exitosamente.')


if __name__ == "__main__":
    create_super_user()
