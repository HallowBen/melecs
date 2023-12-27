from django.contrib import admin
from .models import Archive,measurement_list,permission_set,user,measured_place,measurement_data, all_measurement

# Register your models here.
class idadmin(admin.ModelAdmin):
    readonly_fields=('ID','Date',)
    
admin.site.register(measurement_list,idadmin)

admin.site.register(user,idadmin)

admin.site.register(measured_place,idadmin)


class msdadmin(admin.ModelAdmin):
    readonly_fields=('Start_Time','End_Time',)
admin.site.register(measurement_data,msdadmin)

class psetadmin(admin.ModelAdmin):
    readonly_fields=('ID',)
admin.site.register(permission_set,psetadmin)

admin.site.register(all_measurement)
admin.site.register(Archive)