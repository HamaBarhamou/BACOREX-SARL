from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to="avatars/")
    fonction = models.CharField(max_length=50)

    def __str__(self):
        return "Profil de {0}".format(self.user.username)