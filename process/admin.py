from django.contrib import admin
from .models import (Process, Exam, PracticalCourse, TheoreticalCourse,
    TheoreticalClass, PracticalClass)

admin.site.register(Process)
admin.site.register(Exam)
admin.site.register(PracticalCourse)
admin.site.register(PracticalClass)
admin.site.register(TheoreticalCourse)
admin.site.register(TheoreticalClass)
