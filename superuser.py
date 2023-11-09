# create_superuser.py
from django.contrib.auth.models import User


def create_super_user():
    username = input("superuser")
    email = input("superuser@mail.com")
    password = input("s3*1416u")

    User.objects.create_superuser(username, email, password)
    print(f'Se ha creado el superusuario {username} exitosamente.')


if __name__ == "__main__":
    create_super_user()
