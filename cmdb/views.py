from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from cmdb.models import *
from .forms import *


def index(request):
    hosts = Host.objects.all()
    context = {'hosts': hosts}
    return render(request, 'cmdb/index.html', context)


def idc(request):
    idc = Idc.objects.all()
    context = {'idc': idc}
    return render(request, 'cmdb/idc.html', context)

def hostlist(request,host_id):
    hostlist = Host.objects.all()
    #hostips = Host.objects.first().ip_set.all()
    hosts = Host.objects.get(id=host_id)
    hostips = hosts.ip_set.all()
    context = {'hostlist':hostlist,'hosts': hosts,'hostips':hostips}
    return render(request, 'cmdb/hostlist.html', context)

def hostinfo(request, host_id):
    #hosts = Host.objects.all()
    #hostips = Host.objects.first().ip_set.all()
    hosts = Host.objects.get(id=host_id)
    hostinfos = hosts.hostinfo_set.all()
    hostips = hosts.ip_set.all()
    context = {'hosts': hosts,'hostips': hostips,'hostinfos':hostinfos}
    return render(request, 'cmdb/hostinfo.html', context)



def new_idc(request):
    if request.method != 'POST':
        form = IdcForm()
    else:
        form = IdcForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cmdb:idc'))
    context = {'form': form}
    return render(request, 'cmdb/new_idc.html', context)


def edit_idc(request, idc_id):
    idc = Idc.objects.get(id=idc_id)
    name = Idc.name
    remark = Idc.remark

    if request.method != 'POST':
        form = IdcForm(instance=idc)
    else:
        form = IdcForm(instance=idc, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('cmdb:idc', args=[idc.id]))
    context = {'idc': idc, 'name': name, 'remark': remark, 'form': form}
    return render(request, 'cmdb/edit_idc.html', context)

def edit_host(request, host_id):
    host = Host.objects.get(id=host_id)
    hostname = host.hostname
    num = host.num
    application = host.application

    if request.method != 'POST':
        form = HostForm(instance=host)
    else:
        form = HostForm(instance=host, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('cmdb:hostlist', args=[host.id]))
    context = {'host': host, 'hostname': hostname,'num': num, 'application': application, 'form': form}
    return render(request, 'cmdb/edit_host.html', context)


def edit_hostinfo(request, host_id):
    host = HostInfo.objects.get(id=host_id)
    hostname = host.host
    manufacturer = host.manufacturer
    productmode = host.productmode
    serialnumber = host.serialnumber
    cpu = host.cpu
    mem = host.mem
    disk = host.disk


    if request.method != 'POST':
        form = HostInfoFrom(instance=host)
    else:
        form = HostInfoFrom(instance=host, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('cmdb:hostinfo', args=[host.id]))
    context = {'hostname': hostname, 'manufacturer': manufacturer,'productmode': productmode,
     'productmode': productmode,'serialnumber': serialnumber,'cpu': cpu,
     'mem': mem,'disk': disk, 'form': form}
    return render(request, 'cmdb/edit_hostinfo.html', context)
