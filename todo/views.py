from django.shortcuts import redirect, render
from .models import ToDo
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

# class Login(LoginView):
# 	template_name = 'todo/login.html'
# 	fields = '__all__'
# 	redirect_authenticated_user = True

# 	def get_success_url(self):
# 		return reverse_lazy('home')


def Login(request):

	if request.method == "POST":
		user_name = request.POST.get('username', '')
		user_password = request.POST.get('password', '')
		user = authenticate(username=user_name, password=user_password)
		if user:
			login(request, user)
			messages.success(request, "Logged In")
			return redirect("home")
		else:
			messages.error(request, "Invalid Credentials")
			return redirect("login")

	return render(request, 'todo/login.html')

def Register(request):
	if request.method == "POST":
		mail = request.POST.get('email', '')
		first_name = request.POST.get('firstname', '')
		last_name = request.POST.get('lastname', '')
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		confirmpassword = request.POST.get('confirmpassword', '')
		userCheck = User.objects.filter(
			username=username) | User.objects.filter(email=mail)
		if userCheck:
			messages.error(request, "Username or Email already exists!")
			return redirect("login")
		else:
			if password == confirmpassword:
				user_obj = User.objects.create_user(
					first_name=first_name, last_name=last_name, password=password, email=mail, username=username)
				user_obj.save()
				messages.success(request, "Signed Up successfully")
				return redirect("login")
			else:
				messages.error(request, "Passwords don't match!")
				return redirect("register")
	return render(request, 'todo/register.html')

@login_required
def home(request):
	# if not request.user.is_authenticated:
	# 	return render(request, "todo/login.html", {})
	tasks = ToDo.objects.all().filter(user=request.user).order_by("-date")
	count = ToDo.objects.all().filter(user=request.user).count()
	context = {"tasks": tasks, "count": count }
	return render(request, "todo/home.html", context)


@login_required
def addTask(request):
	content = request.POST.get("content")
	date = timezone.now()
	newTask = ToDo.objects.create(user=request.user, task=content, date=date)
	return HttpResponseRedirect("/")

@login_required
def deleteTask(request, task_id):
	ToDo.objects.get(id=task_id).delete()
	return HttpResponseRedirect("/")
