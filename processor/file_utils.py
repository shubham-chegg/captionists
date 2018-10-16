import os


def move_file(from_file_path, to_file_path):
    return not os.system("mv {} {}".format(from_file_path, to_file_path))


def get_file_name(path):
    return path.split("/")[-1].split(".")[0]
