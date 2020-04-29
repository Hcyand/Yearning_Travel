from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Article)
admin.site.register(models.Scenery)
admin.site.register(models.Shop)
admin.site.register(models.Topic)
admin.site.register(models.LikeCount)
admin.site.register(models.LikeRecord)
admin.site.register(models.Theme)
admin.site.register(models.Personality)
admin.site.register(models.ReadCount)
admin.site.register(models.ReadRecord)
