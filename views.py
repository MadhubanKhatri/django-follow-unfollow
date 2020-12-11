from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Followers
from .forms import *

# Create your views here.
def index(request):
	if 'user' in request.session:
		return render(request, 'index.html')
	else:
		return redirect('login')



def profile(request, user_name):
	user_obj = User.objects.get(name=user_name)
	session_user = User.objects.get(name=request.session['user'])

	session_following, create = Followers.objects.get_or_create(user=session_user)
	user_following, create = Followers.objects.get_or_create(user=user_obj)
	check_user_followers = Followers.objects.filter(another_user=user_obj)
	is_followed = False
	if session_following.another_user.filter(name=user_name).exists():
		is_followed=True
	else:
		is_followed=False
	param = {'user_obj': user_obj,'followers':check_user_followers,'session_following':session_following, 'user_following': user_following,'is_followed':is_followed}
	if 'user' in request.session:
		return render(request, 'profile.html', param)
	else:
		return redirect('index')

def signup(request):
	if request.method == 'POST':
		form = ExampleForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = ExampleForm()
	param = {'form': form}
	return render(request, 'signup.html', param)



def follow_user(request, user_name):
	if request.method == 'POST':
		other_user = User.objects.get(name=user_name)
		session_user = request.session['user']
		get_user = User.objects.get(name=session_user)
		check_follower = Followers.objects.get(user=get_user)
		is_followed = False

		if check_follower.another_user.filter(name=user_name).exists():
			check_follower.another_user.remove(other_user)
			is_followed = False
			return redirect(f'/profile/{user_name}')
		else:
			check_follower.another_user.add(other_user)
			is_followed = True
			return redirect(f'/profile/{user_name}')

	else:
		return redirect(f'/profile/{user_name}')



def followers(request,user_name):
	get_user = User.objects.get(name=user_name)
	followers = get_user.another_user
	param = {'followers': followers.count(),'all_followers':followers.all()}
	return render(request, 'followers.html', param)


def following(request, user_name):
	get_user = User.objects.get(name=user_name)
	following = Followers.objects.get(user=get_user)
	param = {'following': following.another_user.count(), 'all_following':following.another_user.all()}
	return render(request, 'following.html', param)

def search(request):
	if request.method == 'GET':
		query = request.GET['query']
		search_users = User.objects.filter(name=query)
		param = {'search_users':search_users}
		return render(request, 'search.html', param)
	else:
		return redirect('index')

def login_user(request):
	if request.method == 'POST':
		name = request.POST.get('uname')
		password = request.POST.get('pwd')

		check_user = User.objects.filter(name=name, pwd=password)
		if check_user:
			request.session['user'] = check_user.first().name
			return redirect('index')
		else:
			return redirect('index')
	return render(request, 'login.html')



def logout_user(request):
	del request.session['user']
	return redirect('index')
