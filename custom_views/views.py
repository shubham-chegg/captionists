# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from rest_framework.response import Response

# Create your views here.
from rest_framework.decorators import api_view

from captionists import settings
from processor.file_utils import move_file, get_file_name
from processor.main import create_subtitles_file


@api_view(['POST'])
def upload_video(request):
    if request.FILES['file']:
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        fs.save(myfile.name, myfile)
        return Response({
            'file_uploaded': True
        })


def get_videos(request, status):
    folders = {'pending': settings.PENDING_FILES,
               'created': settings.CREATED_FILES,
               'processed': settings.PROCESSED_FILES}

    actions = {'pending': [('Create Subtitles', 'create_subtitles')],
               'created': [('Approve', "approve"), ('Edit', 'edit')]}

    folder = folders.get(status)

    if not folder:
        return render(request, 'listing.html', {'error_message': 'invalid parameter'})

    files = os.listdir(folder)
    return render(request, 'listing.html', {'files': files, 'actions': actions.get(status)})


@api_view(['POST'])
def process_video(request, action):
    status = '123'
    if action == 'create_subtitles':
        if create_subtitles_file(settings.PENDING_FILES + request.POST.get('file_name'),
                                 request.POST.get('language_code'),
                                 get_file_name(request.POST.get('file_name'))):
            status = move_file(settings.PENDING_FILES + request.POST.get('file_name'),
                               settings.CREATED_FILES + request.POST.get('file_name'))
    elif action == 'approve':
        status = move_file(settings.CREATED_FILES + request.POST.get('file_name'),
                           settings.PROCESSED_FILES + request.POST.get('file_name'))

    return Response({'status': status})


def edit_views(request, file_name):
    return render(request, 'video.html', {'video_url': settings.CREATED_FILES_URL + file_name + ".mp4",
                                          'subtitles_url': settings.SUBTITLES_FILE_URL + file_name + ".vtt"})
