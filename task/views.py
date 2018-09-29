from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .forms import APIform
from django.views import generic
from django.http import HttpResponse
import requests
import json

def create(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('task:home')
	else:
		form = UserCreationForm()
	return render(request, 'task/create.html', {'form': form})

def usersearch(request):     #https://simpleisbetterthancomplex.com/tutorial/2018/02/03/how-to-use-restful-apis-with-django.html
	if request.user.is_authenticated:
		if request.method == 'GET':
			form = APIform(request.GET)
			if form.is_valid():
				git_username = form.cleaned_data.get('g_username')
				r = requests.get("https://api.github.com/users/%s"%git_username)
				r1 = requests.get("https://api.github.com/users/%s/repos"%git_username)
				repo = r1.json()
				repol = []

				for repos in repo:
					if isinstance(repos,dict):      #Used isinstance To Remove Type Error
						repol.append((repos["name"],repos["language"]))

				if r.status_code == 200:
					found = True
				else:
					found = False

				request.session['git_username'] = git_username
				return render(request, 'task/search.html', {'git_username':git_username, 'found':found, 'form':form, 'repol':repol})
		else:
			form = APIform()
		return render(request, 'task/search.html',{'form':form, 'found':False})
	else:
		return render(request, 'task/home.html')

def usercommit(request, repo_name):
	if request.user.is_authenticated:
		git_username = request.session['git_username']
		r = requests.get("https://api.github.com/repos/%s/%s/commits" %(git_username,repo_name))
		s = r.json()
		commitl = []

		for commits in s:
			if isinstance(commits,dict):
				commitl.append((commits["commit"]["author"]["date"],commits["commit"]["message"]))
		return render(request, 'task/commits.html', {'commitl':commitl, 'git_username':git_username, 'repo_name':repo_name})
	else:
		return render(request, 'task/home.html')