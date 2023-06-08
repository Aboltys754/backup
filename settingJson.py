import json
import os


def getPathsFolder():
    if os.path.isfile("./setting.json") == False:
        print("Заполните данные файлы setting.json")
        data = dict(pathCopy=[])
        while True:
            tempStringInput = input(
                "введите путь до папки которую нужно копировать начиная с имени диска и до папки  "
            )
            if len(tempStringInput) == 0:
                print(11)
                if len(data["pathCopy"]) == 0:
                    print("В списке нет ни одного пути копирования. Список путей откуда копировать не может быть пустым.")
                else:
                    print(21)
                    break
            else:
                data["pathCopy"].append(tempStringInput)
                print(12)

        data["pathBackup"] = input(
            "введите путь до папки в которую нужно копировать начиная с имени диска и до папки  "
        )
        with open("setting.json", "w") as outfile:
            json.dump(data, outfile)

    with open("./setting.json") as settingJson:
        data = json.load(settingJson)

    return data
