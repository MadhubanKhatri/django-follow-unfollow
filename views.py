from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Followers
# Create your views here.
def index(request):
	if 'user' in request.session:
		return render(request, 'index.html')
	else:
		return redirect('login')



def profile(request, user_name):
	user_obj = User.objects.get(name=user_name)
	session_user = User.objects.get(name=request.session['user'])
	following, create = Followers.objects.get_or_create(user=session_user.id)
	check_user_followers = Followers.objects.filter(another_user=user_obj)
	
	is_followed = False
	if following.another_user.filter(name=user_name).exists():
		is_followed=True
	else:
		is_followed=False
	param = {'user_obj': user_obj,'followers':check_user_followers, 'following': following,'is_followed':is_followed}
	if 'user' in request.session:
		return render(request, 'profile.html', param)
	else:
		return redirect('index')


def follow_user(request, user_name):
	other_user = User.objects.get(name=user_name)
	session_user = request.session['user']
	get_user = User.objects.get(name=session_user)
	check_follower = Followers.objects.get(user=get_user.id)
	is_followed = False
	if other_user.name != session_user:
		if check_follower.another_user.filter(name=other_user).exists():
			add_usr = Followers.objects.get(user=get_user)
			add_usr.another_user.remove(other_user)
			is_followed = False
			return redirect(f'/profile/{session_user}')
		else:
			add_usr = Followers.objects.get(user=get_user)
			add_usr.another_user.add(other_user)
			is_followed = True
			return redirect(f'/profile/{session_user}')

		return redirect(f'/profile/{session_user}')
	else:
		return redirect(f'/profile/{session_user}')








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