from django.db import models

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=40)
	pwd = models.CharField(max_length=40)

	def __str__(self):
		return self.name


class Followers(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	another_user = models.ManyToManyField(User, related_name='another_user')

	def __str__(self):
		return self.user.name
	
    