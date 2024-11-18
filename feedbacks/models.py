from django.db import models

class feedback(models.Model):
	content = models.TextField(default="Good downloader")

	def __str__(self):
		return self.content
