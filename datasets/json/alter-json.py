import json

FILE_NAME = "got-characters.json"
TYPE = "characters"
UNIQUE_FIELD = "characterName"
ID_ATTRIBUTE_NAME = "id"


unique_field_values = {}
list_attributes = []


def load_file():
    with open(FILE_NAME, 'r') as file:
        jsonObject = json.load(file)
    return jsonObject


def save_file(obj):
    with open ("got-characters.json", 'w') as file:
        file.write(json.dumps(obj))


def extractUniqueFieldValues(objects):
    for obj in objects[TYPE]:
        if obj[UNIQUE_FIELD] not in unique_field_values.keys():
            unique_field_values[obj[UNIQUE_FIELD]] = obj[ID_ATTRIBUTE_NAME]


def getListAttributes(objects):
    for character in objects[TYPE]:
        for key in character:
            if isinstance(character[key], list):
                if key not in list_attributes:
                    list_attributes.append(key)


def addIdToListAttributeChildren(objects):
    for character in objects[TYPE]:
        for key in character:
            if key in list_attributes:
                data = character[key]
                character[key] = []
                if isinstance(data, list):
                    for item in data:
                        if item in unique_field_values.keys():
                            character[key].append(
                                {"id": unique_field_values[item]}
                            )
                        else:
                            character[key].append(
                                {"id": item}
                            )
                else:
                    character[key].append(
                                {"id": item}
                            )


if __name__ == '__main__':


    objects = load_file()
    extractUniqueFieldValues(objects)

    # feel free to add necessary code bellow

    # getListAttributes(objects)

    save_file(objects)
