from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from processor.datetime_util import convert_millis_to_min_sec

WORDS_IN_A_LINE = 10


def transcribe_gcs(gcs_uri, language_code):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    client = speech.SpeechClient()
    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        language_code=language_code,
        enable_word_time_offsets=True)
    operation = client.long_running_recognize(config, audio)
    print('Waiting for operation to complete...')
    response = operation.result()
    return response


def process_audio(uri, language_code):
    response = transcribe_gcs(uri, language_code)
    res = []
    i = 1
    start_time = None
    line = ""
    for result in response.results:
        for word in result.alternatives[0].words:
            if i == 1:
                start_time = convert_millis_to_min_sec(word.start_time.ToMilliseconds())
            if i < WORDS_IN_A_LINE:
                line += " " + word.word
                i += 1
            if i == WORDS_IN_A_LINE:
                end_time = convert_millis_to_min_sec(word.end_time.ToMilliseconds())
                res.append({'start_time': start_time,
                            'end_time': end_time,
                            'line': line})
                i = 1
                line = ''
    return res
