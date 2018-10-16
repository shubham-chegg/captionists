import os

from django.conf import settings


def move_file(from_file_path, to_file_path):
    return not os.system("mv {} {}".format(from_file_path, to_file_path))


def get_file_name(path):
    file_name = path.split("/")[-1]
    if '.' in file_name:
        return '.'.join(file_name.split(".")[:-1])
    return file_name


def get_subtitles_file(file_name):
    file_name = get_file_name(file_name)
    return settings.SUBTITLES_FILE + file_name + ".vtt"


def get_video_file_with_subs(file_name):
    file_name = get_file_name(file_name)
    return settings.CREATED_FILES + file_name + ".mp4"


def get_audio_file(file_name):
    file_name = get_file_name(file_name)
    return settings.AUDIO_FILES + file_name + ".flac"


def get_pending_video_file(file_name):
    file_name = get_file_name(file_name)
    return settings.PENDING_FILES + file_name + ".mp4"


def get_processed_file(file_name):
    file_name = get_file_name(file_name)
    return settings.PROCESSED_FILES + file_name + ".mp4"
