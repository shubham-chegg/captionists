

def convert_millis_to_min_sec(millis):
    milliseconds = millis % 1000
    seconds = int(millis / 1000)
    minutes = 0

    if seconds > 60:
        minutes = int(seconds / 60)
        seconds = seconds % 60

    return "{:02}:{:02}.{:03}".format(minutes, seconds, milliseconds)