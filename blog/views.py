from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from itertools import chain
from operator import attrgetter
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post, Profile, Comments
from .forms import PostForm, UserUpdateForm, ProfileUpdateForm, ProfilePicUpdateForm, CommentForm





class HomeView(ListView):
	model = Post
	template_name = 'home-page.html'
	ordering = ['-created_date']



class CreatePostView(LoginRequiredMixin, CreateView):
	model = Post
	template_name = 'post_form.html'
	fields = ['title', 'content', 'image']

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.profile = self.request.user.profile
		return super().form_valid(form)


class CommentPostView(LoginRequiredMixin, CreateView):
	model = Comments
	template_name = 'post_comment.html'
	fields = ['comment']

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.instance.post = self.get_object(Post, pk=pk)
		return super().form_valid(form)

@login_required
def post_comment(request, pk):
	post = get_object_or_404(Post, pk=pk)
	user = User.objects.get(username=request.user)

	if request.method == "POST":
		form = CommentForm(request.POST)
		form.instance.user = user
		form.instance.post = post

		if form.is_valid():
			form.save()
			return redirect('blog:read_full_story', pk=post.pk)
	else:
		form = CommentForm()
	return render(request, 'post_comment.html', {'form': form})



class UpdatePostView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	model = Post
	template_name = 'post_form.html'
	fields = ['title', 'content', 'image']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class DeletePostView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
	model = Post
	template_name = 'delete_post.html'
	success_url = '/'


	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False



class FullArticleView(LoginRequiredMixin, DetailView):
	model = Post
	template_name = 'post-page.html'


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		post = get_object_or_404(Post, pk=self.kwargs['pk'])
		context['comments_list'] = Comments.objects.filter(post=post)
		return context


@login_required
def profile_view(request):
	profile = Profile.objects.get(user=request.user)
	user = User.objects.get(username=request.user)

	context = {
		'profile' : profile,
		'user' : user
	}

	return render(request, 'profile.html', context)


@login_required
def profile_update(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, "Your Profile has been successfully updated.")
			return redirect('blog:profile_view')
		messages.success(request, "Please enter valid Data.")
		return redirect('blog:profile_update')

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form' : u_form,
		'p_form' : p_form
	}

	return render(request, 'profile_update.html', context)


@login_required
def profile_pic_update(request):
	if request.method == 'POST':
		prof_pic_form = ProfilePicUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		profile_pic = Profile.objects.get(user=request.user)

		if prof_pic_form.is_valid():
			prof_pic_form.save()
			messages.success(request, "Your Profile Picture has been updated successfully.")
			return redirect('blog:profile_view')

	else:
		prof_pic_form = ProfilePicUpdateForm(instance=request.user.profile)
		profile_pic = Profile.objects.get(user=request.user)

		context = {
			'prof_pic_form' : prof_pic_form,
			'profile_pic' : profile_pic
		}

		return render(request, 'profile_picture_update.html', context)


