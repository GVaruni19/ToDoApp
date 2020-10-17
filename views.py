from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import HttpResponseRedirect
# Create your views here.
from .models import Todo

@csrf_exempt
def home(request):
 	todo_items = Todo.objects.all().order_by("-added_date")
 	return render(request, "index.html", {"todo_items": todo_items})


@csrf_exempt
def add_todo(request):
	date=timezone.now()
	content=request.POST.get('content')
	#if 'content' in request.POST:
	created_obj = Todo.objects.create(added_date=date, text=content)
	length = Todo.objects.all().count()
	print(length)
	return HttpResponseRedirect("/")

	
@csrf_exempt
def delete_todo(request,todo_id):
	Todo.objects.get(id=todo_id).delete()
	return HttpResponseRedirect("/")
