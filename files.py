import os


def get_all_files():
    return list([f for f in os.listdir('.') if os.path.isfile(f)])


def get_all_photos():
    return list(filter(lambda x: x.endswith("png"), get_all_files()))

