import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myportfolio.settings')
print("USERNAME = ",os.environ.get('USERNAME'))
print("PASSWORD = ",os.environ.get('PASSWORD'))
django.setup()

from django.contrib.auth.models import User
from django.core.management import call_command


email = 'hamabarhamou@gmail.com'  # Remplacez par l'adresse e-mail souhaitée
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

# Vérifier si le superutilisateur existe déjà
if not User.objects.filter(username=username).exists():
    call_command('createsuperuser', username=username, email=email, interactive=False)
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print('Superutilisateur créé avec succès.')
else:
    print('Le superutilisateur existe déjà.')