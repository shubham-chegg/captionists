# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from rest_framework.response import Response

# Create your views here.
from rest_framework.decorators import api_view

from captionists import settings
from processor.file_utils import move_file, get_file_name, get_subtitles_file, \
    get_pending_video_file, get_video_file_with_subs, get_processed_file
from processor.main import create_subtitles_file


def get_videos(request, status=None):
    if not status:
        status = 'pending'

    file_uploaded = False
    if status == 'pending' and request.method == 'POST' and request.FILES.get('file'):
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        fs.save(myfile.name, myfile)


    folders = {'pending': settings.PENDING_FILES,
               'created': settings.CREATED_FILES,
               'processed': settings.PROCESSED_FILES}

    actions = {'pending': [('Create Subtitles', 'create_subtitles')],
               'created': [('Approve', "approve"), ('Edit', 'edit')]}

    folder = folders.get(status)

    if not folder:
        return render(request, 'listing.html', {'error_message': 'invalid parameter'})

    files = os.listdir(folder)
    return render(request, 'listing.html', {'files': files, 'actions': actions.get(status),
                                            'file_uploaded': file_uploaded})


@api_view(['POST'])
def process_video(request, action):
    status = ''
    file_name = request.POST.get('file_name')
    if action == 'create_subtitles':
        if create_subtitles_file(get_pending_video_file(file_name),
                                 request.POST.get('language_code'),
                                 get_file_name(request.POST.get('file_name'))):
            status = move_file(get_pending_video_file(file_name),
                               get_video_file_with_subs(file_name))
    elif action == 'approve':
        status = move_file(get_video_file_with_subs(file_name), get_processed_file(file_name))

    return Response({'status': status})


@api_view(['POST'])
def update_subtitles(request, file_name):
    file_path = get_subtitles_file(file_name)

    if not os.path.exists(file_path):
        status = -1
    elif not request.POST.get('data'):
        status = -2

    else:
        status = 0
        f = open(file_path, 'w')
        f.write(request.POST.get('data', ''))
        f.close()

    return Response({'status':status})


def edit_views(request, file_name):
    return render(request, 'video.html', {'video_url': settings.CREATED_FILES_URL + file_name + ".mp4",
                                          'subtitles_url': settings.SUBTITLES_FILE_URL + file_name + ".vtt"})
