

def generate_subs(context, output_file_path):
    f = open(output_file_path, "w")
    try:
        for index, entry in enumerate(context):
            f.write("{}\n".format(index))
            f.write("{} --> {}\n".format(entry['start_time'], entry['end_time']))
            f.write("{}\n\n".format(entry['line'].strip()))
    except Exception, ex:
        print ex.message
        return False

    return True
