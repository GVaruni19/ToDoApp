from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ToDo(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	task = models.CharField(max_length=200)
	complete = models.BooleanField(default=False)
	date = models.DateTimeField()

	def __str__(self):
		return self.task
	
	class Meta:
		ordering = ['complete']
	