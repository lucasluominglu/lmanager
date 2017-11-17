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
                reverse('cmdb:idc'))
    context = {'idc': idc, 'name': name, 'remark': remark, 'form': form}
    return render(request, 'cmdb/edit_idc.html', context)



def hostlist(request, idc_id):
    #hostips = Host.objects.first().ip_set.all()
    hosts = Idc.objects.get(id=idc_id)
    hostlists = hosts.host_set.all()
    context = {'hostlists':hostlists,'hosts': hosts}
    return render(request, 'cmdb/hostlist.html', context)




def  add_host(request,idc_id):
    idc = Idc.objects.get(id=idc_id)

    if request.method != 'POST':
        hostform = HostForm()
        hostinfoform = HostInfoForm()
        ipform = IpForm()
    else:
        hostform = HostForm(request.POST)
        hostinfoform = HostInfoForm(request.POST)
        ipform = IpForm(request.POST)
        if hostform.is_valid() and hostinfoform.is_valid() and ipform.is_valid():
           add_hostform = hostform.save(commit=False)
           add_hostform.save()
           add_hostinfoform = hostinfoform.save(commit=False)
           add_hostinfoform.host = add_hostform
           add_hostinfoform.save()
           add_ipform = ipform.save(commit=False)
           add_ipform.host = add_hostform
           add_ipform.save()
           return HttpResponseRedirect(reverse('cmdb:hostlist', args=[idc.id]))
    context = {'idc': idc, 'hostform':hostform,'hostinfoform':hostinfoform,'ipform':ipform}
    return render(request, 'cmdb/add_host.html', context)


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
        form = hostinfoform(instance=host)
    else:
        form = hostinfoform(instance=host, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('cmdb:hostinfo', args=[host.id]))
    context = {'hostname': hostname, 'manufacturer': manufacturer,'productmode': productmode,
     'productmode': productmode,'serialnumber': serialnumber,'cpu': cpu,
     'mem': mem,'disk': disk, 'form': form}
    return render(request, 'cmdb/edit_hostinfo.html', context)
