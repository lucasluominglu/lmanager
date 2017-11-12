from django.contrib import admin
from cmdb.models import Idc, Host, HostInfo, Ip


class IpInline(admin.TabularInline):
    model = Ip


class HostInline(admin.TabularInline):
    model = Host


class HostAdmin(admin.ModelAdmin):
    list_display = ('idc', 'date_added','hostname',
                    'num', 'application',)
    search_fields = ['hostname',]
    list_filter = ('application',)
    inlines = [IpInline]


class IdcAdmin(admin.ModelAdmin):
    inline = [HostInline]


class IpAdmin(admin.ModelAdmin):
    list_display = ('ip')


admin.site.register(Idc, IdcAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(Ip, IdcAdmin)
admin.site.register(HostInfo)