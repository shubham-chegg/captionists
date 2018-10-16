import os


def extract_audio(video_file_path, audio_file):
    if not os.system("ffmpeg -y -i {} -f flac -ab 192000 -ac 1 -vn {}".format(video_file_path, audio_file)):
        return audio_file
    return ""
