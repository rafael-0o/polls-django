from django.contrib import admin
from .models import Question


@admin.register(Question)
class madmin(admin.ModelAdmin):
    list_display=('id','question_text','pub_date')
# Register your models here.
