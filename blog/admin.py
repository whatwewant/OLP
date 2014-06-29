from django.contrib import admin
from blog.models import Post, Comment, CommentMeta, PostMeta
from blog.models import Category
from blog.models import PostToCategory

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostMeta)
admin.site.register(CommentMeta)

admin.site.register(PostToCategory)

