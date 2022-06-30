from django.db import models
from django.conf import settings # authetification user model
from mod_helpers.hlp_paths import PathsHelpers

def path_photo_user(instance, filename):
	"""
	Path photo d'identité
	"""
	return PathsHelpers.path_and_rename(instance, filename, PathsHelpers.PHOTO_USER_FOLDER)

class UserProfile(models.Model):
	"""
	Model : USer Profile
	"""
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	tel = models.CharField(max_length=20, blank=True, null=True)
	email = models.CharField(max_length=70, blank=True, null=True)
	fonction = models.CharField(max_length=255, blank=True, null=True)
	avatar = models.ImageField(upload_to=path_photo_user, max_length=255, null=True, blank=True)