from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save



class Post(models.Model):
	title = models.CharField(max_length=50)
	content = models.TextField()
	image = models.ImageField(upload_to='images', null=True, blank=True)
	created_date = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	profile = models.ForeignKey('Profile', on_delete=models.CASCADE)


	def __str__(self):
		return f'{self.author.username} Post'


	def get_absolute_url(self):
		return reverse('blog:read_full_story', kwargs={
					'pk' : self.pk,
			})


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	user_image = models.ImageField(default='default.jpg', upload_to='profile_pics')
	about_you = models.TextField(null=True, blank=True)
	profession = models.CharField(max_length=30, null=True, blank=True)
	mobile_number = models.CharField(max_length=13, null=True, blank=True)

	def __str__(self):
		return f'{self.user.username}'


	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
	    if created:
	        Profile.objects.create(user=instance)



class Comments(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	comment = models.TextField()


	def __str__(self):
		return f'{self.user.username} Comment'


	def get_absolute_url(self):
		return reverse('blog:read_full_story', kwargs={
					'pk' : self.post.pk,
			})