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

def sys_id_parse_type(system_id: str):
    if system_id.startswith("C-"):
        return "Boolean"
    elif system_id.startswith("STR-"):
        return "String"
    elif system_id.startswith("S32-"):
        return "Int4"
    elif system_id.startswith("F32-"):
        return "Float4"
    else:
        return ""

def parse_ignition_path(data):
    type_prefix = ""
    modbus_suffix = ""

    if data[ADVariables.SYSTEM_ID].startswith("C-"):
        type_prefix = "C"
    elif data[ADVariables.SYSTEM_ID].startswith("STR-"):
        type_prefix = "HRS"
    elif data[ADVariables.SYSTEM_ID].startswith("S32-"):
        type_prefix = "HRI"
    elif data[ADVariables.SYSTEM_ID].startswith("F32-"):
        type_prefix = "HRF"
    else:
        return ""

    if type_prefix == "HRS":
        modbus_suffix = str(int(data[ADVariables.MOD_BUS_ADDRESS]) % 100)  + ":" + str(data[ADVariables.STRING_LENGTH])
    else :
        modbus_suffix = str(int(data[ADVariables.MOD_BUS_ADDRESS]) % 100)


    return type_prefix + modbus_suffix


if __name__ == '__main__':
    csv_data = list(read_csv("../Tags_01_extended.csv"))
    csv_data.remove(csv_data[0])

    usefulRowsOnly = [row for row in csv_data if not row[ADVariables.MOD_BUS_ADDRESS] == ""]

    ignitionFormattedList = []

    exampleIgnitionObject = {
      "valueSource": "opc",
      "opcItemPath": "[ModBusTestPLC]HRS27:40",
      "dataType": "String",
      "name": "SQLInsert_MaterialNumber",
      "tagType": "AtomicTag",
      "opcServer": "Ignition OPC UA Server"
    },

    for row in usefulRowsOnly:
        parse_ignition_path(row)
        ignitionFormattedList.append({
            "valueSource": "opc",
            "opcItemPath": "[ModBusTestPLC]" + parse_ignition_path(row),
            "dataType": sys_id_parse_type(row[ADVariables.SYSTEM_ID]),
            "name": row[ADVariables.TAG_NAME],
            "tagType": "AtomicTag",
            "opcServer": "Ignition OPC UA Server"
        })


    print(print(json.dumps(ignitionFormattedList)))
