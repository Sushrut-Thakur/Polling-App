from django.contrib import admin
from .models import Question, Choice

# Register your models here.
class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ["question"],
        }),
        ("Date Information", {
            "fields": ["pub_date"],
        })
    )

    inlines = [ChoiceInLine]
    list_display = ["question", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question"]

admin.site.register(Question, QuestionAdmin)
