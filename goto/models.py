from django.db import models

# Create your models here.
class Linklib(models.Model):
	skey = models.CharField(max_length=6)
	link = models.TextField()
	click_count = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'linklib'
		ordering = ['-click_count']
