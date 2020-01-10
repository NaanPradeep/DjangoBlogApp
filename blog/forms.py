from django import forms
from .models import Post, Profile, Comments
from allauth.account.forms import SignupForm	
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea)

	class Meta:
		model = Post
		fields = ['title', 'content', 'image']



class CustomSignupForm(SignupForm):
	

	def signup(self, request, user, *args, **kwargs):
		super().save()
		user_profile = user.profile
		user_profile.save()
		return user



class UserUpdateForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['username', 'email']



class ProfileUpdateForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ['about_you', 'profession', 'mobile_number']



class ProfilePicUpdateForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ['user_image']



class CommentForm(forms.ModelForm):

	comment = forms.Textarea(attrs={
			'class' : 'form-control',
			'id' : 'replyFormComment',
			'row': 5
		})

	class Meta:
		model = Comments
		fields = ['comment']