from enum import IntEnum
import csv
import json


class ADVariables(IntEnum):
    SYSTEM_ID = 0
    TAG_NAME = 1
    MOD_BUS_ADDRESS = 4
    STRING_LENGTH = 6


def read_csv(fileName):
    with open(fileName) as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        next(reader, None)  # skip the headers
        data_read = [row for row in reader]

    return data_read

def sys_id_parse_type(_system_id: str):
    sys_id = _system_id
    if sys_id.startswith('AR1'):
        sys_id = sys_id[3:]

    if sys_id.startswith("C-"):
        return "Boolean"
    elif sys_id.startswith("STR-"):
        return "String"
    elif sys_id.startswith("S32-"):
        return "Int4"
    elif sys_id.startswith("F32-"):
        return "Float4"
    else:
        return ""

def parse_ignition_path(data):
    type_prefix = ""
    modbus_suffix = ""
    sys_id = data[ADVariables.SYSTEM_ID]
    if sys_id.startswith('AR1'):
        sys_id = sys_id[3:]

    if sys_id.startswith("C-"):
        type_prefix = "C"
    elif sys_id.startswith("STR-"):
        type_prefix = "HRS"
    elif sys_id.startswith("S32-"):
        type_prefix = "HRI"
    elif sys_id.startswith("F32-"):
        type_prefix = "HRF"
    else:
        return ""

    # modulo is maybe not the best way to handle this but it works for now
    # Some modbus addresses are prefixed with a number (not part of the actual address ex. 400021)
    # so 400021 % 10000 gives 21 which is the value we care about
    if type_prefix == "HRS":
        modbus_suffix = str(int(data[ADVariables.MOD_BUS_ADDRESS]) % 10000)  + ":" + str(data[ADVariables.STRING_LENGTH])
    else :
        modbus_suffix = str(int(data[ADVariables.MOD_BUS_ADDRESS]) % 10000)


    return type_prefix + modbus_suffix


if __name__ == '__main__':
    csv_data = list(read_csv("../Tags_01_extended.csv"))
    csv_data.remove(csv_data[0])

    usefulRowsOnly = [row for row in csv_data if not row[ADVariables.MOD_BUS_ADDRESS] == ""]

    ignitionFormattedTagList = []

    for row in usefulRowsOnly:
        ignitionFormattedTagList.append({
            "valueSource": "opc",
            "opcItemPath": "[ModBusTestPLC]" + parse_ignition_path(row),
            "dataType": sys_id_parse_type(row[ADVariables.SYSTEM_ID]),
            "name": row[ADVariables.TAG_NAME],
            "tagType": "AtomicTag",
            "opcServer": "Ignition OPC UA Server"
        })

    ignitionFormattedObject = {
        "name": "MyImportFolder",
        "tagType": "Folder",
        "tags": ignitionFormattedTagList
    }

    print(json.dumps(ignitionFormattedObject))

    f = open("tags_01_extended.json", "x")
    f.write(json.dumps(ignitionFormattedObject))
    f.close()