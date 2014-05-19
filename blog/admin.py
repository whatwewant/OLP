from django.contrib import admin
from blog.models import Post, Comment, CommentMeta, PostMeta

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostMeta)
admin.site.register(CommentMeta)

