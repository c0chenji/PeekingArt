from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.db.models import Q

def profile(request):
	return render (request ,'base.html')

def home(request):
	return redirect('posts:list')

def post_create(request):
	form = PostForm(request.POST or None,request.FILES or None)
	if form.is_valid():
		# print (request.POST.get("title"))
		# Post.objects.create(title="aaa")
		instance=form.save(commit=False)
		instance.user = request.user
		print(form.cleaned_data.get("content"))
		instance.save()
		messages.success(request,"Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())

	context ={
		"form":form,
	}
	return render(request,"post_form.html", context)


def post_detail(request,id):	
	instance = get_object_or_404(Post, id =id)
	queryset = Post.objects.all()
	context ={
		
		"instance":instance,
		"title": instance.title
	}
	return render (request ,'post_detail.html', context)

def post_list(request):
	
	# queryset_list = Post.objects.ative()#.order_by("-timestamp")
	# if request.user.is_staff or request.user.is_superuser:
	queryset_list = Post.objects.all()
	query =request.GET.get("q")
	if query :
		queryset_list = queryset_list.filter(
			Q(user__first_name__icontains=query)|
			Q(title__icontains=query)|
			Q(content__icontains=query)
			).distinct()

	paginator = Paginator(queryset_list, 9) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)


	context = {
		"object_list": queryset,
		"title":"My User List",
		"page_request_var":page_request_var,
	}
	# else:
	# 	context ={
	# 		"title": "List"
	# 	}	
	return render (request ,'post_list.html', context)

def post_update(request,id=None):	
	instance = get_object_or_404(Post, id =id)
	form = PostForm(request.POST or None,request.FILES or None, instance= instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user =request.user
		instance.save()
		messages.success(request,"<h2>Successfully Item Save</h2>",extra_tags='html_font')
		return HttpResponseRedirect(instance.get_absolute_url())

	context ={
		"title":instance.title,
		'instance':instance,
		"form":form,
	}
	return render(request,"post_form.html", context)

def post_delete(request,id=None):	
	instance = get_object_or_404(Post, id =id)
	messages.success(request,"Successfully deleted")
	instance.delete()
	return redirect("posts:list")


