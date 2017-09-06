import json


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def print_to_json(material):
        print(json.dumps(material, ensure_ascii=False, indent=4))

    @staticmethod
    def store_json(material, filename):
        with open(filename, 'w', encoding='utf8') as makefile:
            json.dump(material, makefile, ensure_ascii=False, indent=4)

