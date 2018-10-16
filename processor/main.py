from django.conf import settings

from processor.extract_audio import extract_audio
from processor.processor_utils import process_audio
from processor.subtitles_generator import generate_subs
from processor.uploader import upload


def create_subtitles_file(video_file, language_code, output_file_name):
    audio_file_path = extract_audio(video_file, settings.AUDIO_FILES + output_file_name + ".flac")
    if audio_file_path:
        audio_file = upload(audio_file_path, 'audio.flac')
        subtitles_context = process_audio(audio_file, language_code)
        return generate_subs(subtitles_context, settings.SUBTITLES_FILE + output_file_name + ".vtt")

    print "Unable to extract audio file"
    return False
