import urllib
import json
import pprint


class JSONParser():
    def __init__(self, data):
        self.data = data

    def print_data(self, data=None):
        if data == None:
            data = self.data
            for elem in data:
                print elem
        else:
            print "Data handling error"

    def get_data(self):
        return self.data

    def convert_to_python(self):
        return json.load(self.data)

    def pprint_JSON(self, data):
        if data == None:
            data = self.data
        print json.dumps(data, sort_keys=4, indent=4)

    def pprint_python(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.convert_to_python())

    def get_value(self, key):
        # data = self.convert_to_python()
        data = self.convert_to_python()
        return data[key]

