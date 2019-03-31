"""
Quick assistant to get stuff from json files
"""

import json
import os
import errno


def dircheck(fdir):
    try:
        os.makedirs(fdir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


class Jason:
    def __init__(self):
        self.files = {}  # filepaths to json files you want the assitant to handle

    def assign(self, n, t):
        """
        :param n: string, name of file
        :param t: string, filepath
        """
        self.files[n] = t

    def fetch(self, file, field):
        with open(self.files[file], 'r') as f:
            file = json.load(f)
            return file[field]

    def store(self, file, field, data):
        with open(self.files[file], 'r') as f:
            file = json.load(f)
            file[field] = data
            f.seek(0)
            json.dump(file, f, indent=4, sort_keys=True)
            f.truncate()
