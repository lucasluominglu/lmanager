from django.contrib import admin
from cmdb.models import Idc, Host, HostInfo, Ip


class IpInline(admin.TabularInline):
    model = Ip
    extra = 3


class HostInline(admin.TabularInline):
    model = Host
    xtra = 3


class HostAdmin(admin.ModelAdmin):
    list_display = ('idc', 'date_added','hostname',
                    'num', 'application',)
    search_fields = ['hostname',]
    list_filter = ('application',)
    inlines = [IpInline]


class IdcAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'remark',)
   # inlines = [HostInline]


#class IpAdmin(admin.ModelAdmin):
   # list_display = ('ip')


admin.site.register(Idc, IdcAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(Ip)
admin.site.register(HostInfo)