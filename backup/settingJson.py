import json
import os


def getPathsFolder():
    print(1)
    if os.path.isfile("./setting.json") == False:
        print("Заполните данные файлы setting.json")
        data = {}
        data["pathCopy"] = input(
            "введите путь до папки которую нужно копировать начиная с имени диска и до папки  "
        )
        data["pathBackup"] = input(
            "введите путь до папки в которую нужно копировать начиная с имени диска и до папки  "
        )
        with open("setting.json", "w") as outfile:
            json.dump(data, outfile)

    with open("./setting.json") as settingJson:
        data = json.load(settingJson)

    return data
