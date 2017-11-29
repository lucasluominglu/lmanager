import os
from datetime import datetime
from fabric.api import *
from fabric.tasks import execute
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import JsonResponse
from .models import *
from .forms import *


def index(request):
    hosts = Host.objects.all()
    context = {'hosts': hosts}
    return render(request, 'cmdb/index.html', context)


@login_required
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
    context = {'hostlists': hostlists, 'hosts': hosts}
    return render(request, 'cmdb/hostlist.html', context)


def add_host(request, idc_id):
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
    context = {'idc': idc, 'hostform': hostform,
               'hostinfoform': hostinfoform, 'ipform': ipform}
    return render(request, 'cmdb/add_host.html', context)


def edit_host(request, host_id):
    hosts = Host.objects.get(id=host_id)
    idc = Idc.objects.get(host=hosts)
    hostinfo = HostInfo.objects.get(host=hosts)
    ip = Ip.objects.get(host=hosts)
    if request.method != 'POST':
        hostsfrom = HostForm(instance=hosts)
        idcfrom = IdcForm(instance=idc)
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
    context = {'hosts': hosts, 'hostsfrom': hostsfrom,
               'idcfrom': idcfrom, 'hostinfofrom': hostinfofrom, 'ipfrom': ipfrom}
    return render(request, 'cmdb/edit_host.html', context)


def handle_uploaded_file(f):
    filename = settings.BASE_DIR + "/name.txt"
    print(filename)
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_file(request):
    if request.method == 'POST':
        #form = UploadFileForm(request.POST, request.FILES)
        form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        # handle_uploaded_file(request.FILES['file'])
        # form.save()
        if form.is_valid():
            print("valid")
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('cmdb:index'))
    else:
        form = UploadFileForm()
    return render(request, 'cmdb/upload_file.html', {'form': form})


def pack():
    """打包"""
    tag = datetime.now().strftime('%Y%m%d')
    app_path, app_name = os.path.split(settings.BASE_DIR)
    local(
        'tar -czvf {0}{1}.tar.gz {2}'.format(app_name, tag, settings.BASE_DIR))


def upload():
    env.user = 'root'
    env.hosts = ['120.78.186.44']
    env.key_filename = "~/.ssh/id_rsa.pub"
    remote_tmp_dir = '/tmp'
    app_path, app_name = os.path.split(settings.BASE_DIR)
    tag = datetime.now().strftime('%Y%m%d')
    deploy_file = '{0}{1}.tar.gz'.format(app_name, tag)
    put(deploy_file, remote_tmp_dir)
    run('ls /tmp')


def dep():
    env.user = 'root'
    env.hosts = ['114.67.228.225']
    env.key_filename = "~/.ssh/id_rsa.pub"
    remote_tmp_dir = '/tmp'
    app_path, app_name = os.path.split(settings.BASE_DIR)
    tag = datetime.now().strftime('%Y%m%d')
    deploy_file = '{0}{1}.tar.gz'.format(app_name, tag)
    put(deploy_file, remote_tmp_dir)
    run('ls /tmp')
    run('tar -xf {0}/{1} -C /home'.format(remote_tmp_dir, deploy_file))
    run('ls /home')


def get_rollback_file():
    env.user = 'root'
    env.hosts = ['120.78.186.44']
    env.key_filename = "~/.ssh/id_rsa.pub"
    app_path, app_name = os.path.split(settings.BASE_DIR)
    # rb_file = run('ls /tmp/{0}*'.format(app_name))
    rb_file = run('ls /tmp/')
    rb_list = rb_file.split("  ")
    rb_list = [os.path.basename(i) for i in rb_file.split("  ")]
    return rb_list


def deploy(request):
    if request.method == "GET":
        rb_list = execute(get_rollback_file)
        print(rb_list)
        context = {'rb_list': rb_list}
        return render(request, 'cmdb/deploy.html', context)
    # lif request.method == "POST":
    #    pack()
     #   context = {"status": 200, "message": "ok"}
      #  return JsonResponse(context)


def packs(request):
    if request.method == "POST":
        # myFile =request.POST.get("myfile", None)
        execute(pack)
        context = {"status": 200, "message": "ok"}
        return JsonResponse(context)


def uploads(request):
    if request.method == "POST":
        execute(upload)
        context = {"status": 200, "message": "ok"}
        return JsonResponse(context)


def deploys(request):
    if request.method == "POST":
        execute(dep)
        context = {"status": 200, "message": "ok"}
        return JsonResponse(context)


def rollback(request):
    if request.method == "POST":
        name = request.POST.get('name')
        context = {"status": 200, "message": "ok", "name": name}
        return JsonResponse(context)
