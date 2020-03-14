import os


class Config(object):
    def __init__(self):
        self.data_folder = 'backend/data'
        self.bugs_json = os.path.join(self.data_folder, 'bugs.json')
        self.bugs_converted_json = os.path.join(self.data_folder, 'bugs_converted.json')


CONFIG = Config()
