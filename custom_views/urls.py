from django.conf.urls import url
from django.contrib import admin

import views

urlpatterns = [
    url(r'^$', views.get_videos, name='get videos'),
    url(r'^list/$', views.get_videos, name='get videos'),
    url(r'^list/(?P<status>[a-z]+)/$', views.get_videos, name='get videos'),
    url(r'^process/video/(?P<action>[a-z_]+)/$', views.process_video, name='process video'),
    url(r'^edit/video/(?P<file_name>.+)/$', views.edit_views, name='edit video'),
    url(r'^subtitles/update/(?P<file_name>.+)/$', views.update_subtitles, name='update subtitles')
]
