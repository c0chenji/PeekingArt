from django.contrib import admin

# Register your models here.
from .models import Post

class PostModelAdmin(admin.ModelAdmin):
	list_display = ['title','timestamp','updated']
	list_display_links = ["updated"]
	list_editable = ["title"]
	list_filter = ["timestamp","updated",]
	search_fields = ["title","content","updated"]

	class Meta:
		"""docstring for Meta"""
		model = Post

		# def __init__(self, arg):
		# 	super(Meta, self).__init__()
		# 	self.arg = arg
admin.site.register(Post,PostModelAdmin)