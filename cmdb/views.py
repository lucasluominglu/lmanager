from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from cmdb.models import *
from .forms import IdcForm


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
        form = IdcForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('learning_logs:topic', args=[topic.id]))
    context = {'idc': idc, 'name': name, 'remark': remark, 'form': form}
    return render(request, 'cmdb/edit_idc.html', context)


def hostlist(request):
    hlist = Host.objects.all()
    #hostips = Host.objects.first().ip_set.all()
    #hosts = Host.objects.get(id=host_id)
   # hostips = hosts.ip_set.all()
    context = {'hlist':hlist}
    return render(request, 'cmdb/hlist.html', context)

def hostinfo(request, host_id):
    #hosts = Host.objects.all()
    #hostips = Host.objects.first().ip_set.all()
    hosts = Host.objects.get(id=host_id)
    hostinfos = hosts.hostinfo_set.all()
    hostips = hosts.ip_set.all()
    context = {'hosts': hosts,'hostips': hostips,'hostinfos':hostinfos}
    return render(request, 'cmdb/hostinfo.html', context)


