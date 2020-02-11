from django.contrib import admin
from .models import Info, Programmer, Language, Book, Author

# Register your models here.
admin.site.register(Info)
admin.site.register(Programmer)
admin.site.register(Language)
admin.site.register(Book)
admin.site.register(Author)
