# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import mimetypes
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, Http404

from user.forms import UploadFile
from user.models import File


@login_required(login_url='login')
def get_user_files(request, parent_path):
    files = File.objects.filter(user_id=request.user.id, parent_path=parent_path.strip('/') + '/',
                                deleted_at=None)
    if files:
        return files
    else:
        return []


@login_required(login_url='login')
def download_file(request, id=None):
    try:
        if id:
            file = File.objects.filter(id=id)[0]
            mimetype = mimetypes.guess_type(os.path.join(os.getenv('HOME'), 'data', 'django_drive',
                        file.filename.name))[0] or 'application/octet-stream'
            if request.user.id == file.user_id:
                with open(os.path.join(os.getenv('HOME'), 'data', file.filename.name), 'rb') as f:
                    response = HttpResponse(f.read(), content_type=mimetype)
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file.child_path)
                    return response
        raise Http404
    except:
        raise Http404


@login_required(login_url='login')
def delete_file(request, id):
    try:
        if id:
            file = File.objects.filter(id=id)[0]
            if request.user.id == file.user_id and file:
                path = file.parent_path
                file.deleted_at = datetime.now()
                file.save()
                return redirect(reverse('data', args=(path,)))
    except:
        Http404


@login_required(login_url='login')
def data(request, path='home/'):
    content = {'path': path, 'files': get_user_files(request, path), 'func': get_user_files}
    return render(request, 'drive/data.html', content)


@login_required(login_url='login')
def upload_file(request, path='home/'):
    try:
        form = UploadFile(request.POST, request.FILES)
        if request.method == 'POST':
            if form.is_valid():
                file = request.FILES.get('filename')
                ext = os.path.splitext(file.name)[-1]
                parent_path = request.POST['parent_path']
                size = file.size
                store_file = form.save(commit=False)
                store_file.user_id = request.user.id
                store_file.child_path = file.name
                store_file.parent_path = parent_path.strip('/') + '/'
                store_file.file_type = ext
                store_file.size = size
                store_file.save()
                return redirect(reverse('data', args=(path,)))
        else:
            return render(request, 'drive/upload_file.html', {'path': path, 'form': form})
    except Exception as e:
        print(e)


@login_required(login_url='login')
def create_folder(request, path='home/'):
    if request.method == 'POST':
        # import pdb;pdb.set_trace()
        parent_path = request.POST.get('parent_path')
        child_path = request.POST.get('folder')
        if not File.objects.filter(parent_path=parent_path.strip('/') + '/', child_path=child_path, deleted_at=None) :
            file_type = 'dir'
            file = File(user_id=request.user.id, child_path=child_path, parent_path=parent_path.strip('/') + '/',
                        file_type=file_type, filename=child_path)
            file.save()
            return redirect(reverse(data, args=(parent_path,)))
        else:
            messages.error(request, f'The folder name {child_path} already exists in same directory. '
                                    f'Please choose another name.')
            return redirect(reverse(data, args=(parent_path,)))
    else:
        return render(request, 'drive/create_folder.html', {'path': path})



