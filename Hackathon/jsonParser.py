import json
import colander
import requests

#Retrieves users location and all possible hospitals location from the database

class Hospital(colander.MappingSchema):
        hospitalId = colander.SchemaNode(colander.Int())
        hospitalLocation = colander.SchemaNode(colander.String())
        name = colander.SchemaNode(colander.String())
        resource = colander.SchemaNode(colander.Int())


class Data(colander.SequenceSchema):
        hospitals = Hospital()


def get_destination():
    link = "https://emergencyservice-1540081359676.firebaseio.com/hospitals.json"
    f = requests.get(link)
    schema = Data()
    deserialized = schema.deserialize(json.loads(f.text))
    #print(deserialized[0]['name'])
    locDist =[]
    for i in range(len(deserialized)):
        loc = ([int(loc) for loc in (deserialized[i]['hospitalLocation']).split(',')])
        locDist.append(loc[0] * 10 + loc[1])
    return locDist


class User(colander.MappingSchema):
        userId = colander.SchemaNode(colander.Int())
        userLocation = colander.SchemaNode(colander.String())
        userName = colander.SchemaNode(colander.String())


class UserData(colander.SequenceSchema):
    users = User()


def get_source():
    #threading.Timer(500.0, get_source()).start()
    link = "https://emergencyservice-1540081359676.firebaseio.com/users.json"
    f = requests.get(link)
    schema = UserData()
    deserialized = schema.deserialize(json.loads(f.text))
    if not deserialized:
        return None
    loc = ([int(loc) for loc in (deserialized[0]['userLocation']).split(',')])
    return loc[0]*10+loc[1]


get_destination()
get_source()
