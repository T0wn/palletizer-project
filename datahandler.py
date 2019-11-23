import json
import CustomBox

class datahandler:

    boxes = []

    @staticmethod
    def refreshBoxes():
        datahandler.boxes = []

        with open('appdata/boxes.json', 'r') as file:
            data = json.load(file)
            
            for i in data:
                datahandler.boxes.append( datahandler.obj_decoder(i) )
        
    
    @staticmethod
    def getBoxes():
        datahandler.refreshBoxes()
        return datahandler.boxes

    @staticmethod
    def addBox(object):
        datahandler.refreshBoxes()
        datahandler.boxes.append(object)

        with open('appdata/boxes.json', 'w') as outfile:
            json.dump(datahandler.boxes, outfile, default=datahandler.obj_dict)
    
    @staticmethod
    def obj_dict(obj):
        return obj.__dict__

    @staticmethod
    def obj_decoder(json_string):
        return CustomBox.CustomBox(json_string['name'], json_string['length'], json_string['width'], json_string['height'])

