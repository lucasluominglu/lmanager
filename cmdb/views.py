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
    hosts = Host.objects.get(id=host_id)
    idc = Idc.objects.get(host=hosts)
    hostinfo = HostInfo.objects.get(host=hosts)
    ip = Ip.objects.get(host=hosts)
    if request.method != 'POST':
        hostsfrom = HostForm(instance=hosts)
        idcfrom   = IdcForm(instance=idc)
        hostinfofrom = HostInfoForm(instance=hostinfo)
        ipfrom = IpForm(instance=ip)
    else:
        hostsfrom = HostForm(instance=hosts, data=request.POST)
        idcfrom = IdcForm(instance=idc, data=request.POST)
        hostinfofrom = HostInfoForm(instance=hostinfo, data=request.POST)
        ipfrom = IpForm(instance=ip, data=request.POST)
        if hostsfrom.is_valid() and idcfrom.is_valid() and hostinfofrom.is_valid() and ipfrom.is_valid():
            hostsfrom.save()
            idcfrom.save()
            hostinfofrom.save()
            ipfrom.save()
            return HttpResponseRedirect(
                reverse('cmdb:hostlist', args=[hosts.id]))
    context = {'hosts': hosts, 'hostsfrom': hostsfrom, 'idcfrom': idcfrom, 'hostinfofrom': hostinfofrom, 'ipfrom': ipfrom}
    return render(request, 'cmdb/edit_host.html', context)



