from django.contrib import admin
from cmdb.models import CPU,Disk,RAM


# Register your models here.

# @admin.register(CPU)
# class CPUAdmin(admin.ModelAdmin):
#     list_display = ['asset', 'cpu_model', 'cpu_count', 'cpu_core_count']

@admin.register(Disk)
class DiskAdmin(admin.ModelAdmin):
    list_display = ['asset','sn','slot','model','manufacturer','capacity','interface_type']
    list_editable = ['interface_type']

@admin.register(RAM)
class RamAdmin(admin.ModelAdmin):
    list_display = ['asset', 'sn', 'model', 'manufacturer','slot','capacity']


admin.site.register(CPU)