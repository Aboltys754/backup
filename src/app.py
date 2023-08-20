import json
import os
from datetime import datetime
import zipfile
import traceback

fullDate = datetime.now()
keysJson = {'File': 'Введите путь до папки или файла(включая имя папки или файла)\n',
            'Backup': 'Введите путь куда копировать архив с копией\n',
            'DateBackup': 'Введите количество дней сохранений\n'}
# errorNumberString = traceback.extract_stack()[-1].lineno


def writeLog(message, numberString):
    """записывает сообщения в log.txt"""
    with open('log.txt', 'a', encoding='utf-8') as log:
        log.write(f'{fullDate.day}.{fullDate.month}.{fullDate.year}-{fullDate.hour}:{fullDate.minute}:{fullDate.second} {message} {numberString}\n')


def chekedAndAddKeyJson(key):
    """Получает строку с ключем из json и просит ввести данные в строку.
        Проверяет на корректность введеные данные. Если все хорошо возвращает введеную строку.
        Если нет то предлагает попробывать еще раз."""
    if key == 'File' or key == 'Backup':
        while True:
            keyJson = input(keysJson[key])
            if os.path.exists(keyJson) == False:
                print(f'Путь не найден, {keyJson}')
                writeLog(f'Путь не найден, {keyJson}', traceback.extract_stack()[-1].lineno)
            else:
                break
    elif key == 'DateBackup':
        while True:
            try:
                keyJson = int(input(keysJson[key]))
            except Exception:
                print(f'Ввели не число')
            else:
                break
    return keyJson

def checkedJsonProps():
    """Проверка наличия файла json с наличием путей откуда, куда копировать backup и количество сохраненных архивов.
        Если его нет то просит пользователя ввести два пути. Откуда и куда копировать.
        Также просит ввести число сохранненых архивов"""
    if os.path.exists("setting.json"):
        try:
            writeLog('json есть', traceback.extract_stack()[-1].lineno)
            with open('setting.json', 'r') as settingJson:
                setting = json.load(settingJson)
                if 'File' not in setting:
                    writeLog('Не указан путь источник (File) в json', traceback.extract_stack()[-1].lineno)
                    setting['File'] = chekedAndAddKeyJson('File')
                if 'Backup' not in setting:
                    writeLog('Не указан путь куда копировать (Backup) в json', traceback.extract_stack()[-1].lineno)
                    setting['Backup'] = chekedAndAddKeyJson('Backup')
                if 'DateBackup' not in setting:
                    writeLog('Не указано сколько архивов хранить (DateBackup) в json', traceback.extract_stack()[-1].lineno)
                    setting['DateBackup'] = chekedAndAddKeyJson('DateBackup')
            with open('setting.json', 'w') as settingJson:
                json.dump(setting, settingJson, sort_keys=True, indent=2)
        except Exception as error:
            writeLog(f"checkedJsonProps Error {error}", traceback.extract_stack()[-1].lineno)
            raise SystemExit
        else:
            writeLog("Json корректный", traceback.extract_stack()[-1].lineno)

    else:
        try:
            writeLog('файл json отсутствует', traceback.extract_stack()[-1].lineno)
            tempDict = {
                'File': chekedAndAddKeyJson('File'),
                'Backup': chekedAndAddKeyJson('Backup'),
                'DateBackup': chekedAndAddKeyJson('DateBackup')
            }
            with open('setting.json', 'w') as settingJson:
                json.dump(tempDict, settingJson, sort_keys=True, indent=2)
        except Exception as error:
            writeLog(f"checkedJsonProps Error {error}", traceback.extract_stack()[-1].lineno)
            raise SystemExit
        else:
            writeLog("Создал json файл", traceback.extract_stack()[-1].lineno)


def checkingSourseAndSaveFolders():
    """Проверка папок  откуда и куда копируются файлы"""
    try:
        with open('setting.json', 'r') as settingJson:
            setting = json.load(settingJson)
            if os.path.exists(setting['File']) == False:
                writeLog(f'Путь до {setting["File"]} не найден', traceback.extract_stack()[-1].lineno)
                raise SystemExit
            elif os.path.exists(setting['Backup']) == False:
                writeLog(f'Путь до {setting["Backup"]} не найден', traceback.extract_stack()[-1].lineno)
                raise SystemExit
    except Exception as error:
        writeLog(f"checkingSourseAndSaveFolders Error {error}", traceback.extract_stack()[-1].lineno)
    else:
        writeLog('Папка источник и папка для сохранения существует', traceback.extract_stack()[-1].lineno)



def iterationСycle(path, backup, tempPath):
    """Перебирает папку источник. Если встречается папка то запускает снова эту функцию.
        Если файл то записывает в архив изменяя исходный путь"""
    try:
        for i in os.listdir(path):
            if os.path.isdir(f'{path}\\{i}') == True:
                iterationСycle(f'{path}\\{i}', backup, tempPath)
            elif os.path.isdir(f'{path}\\{i}') == False:
                with zipfile.ZipFile(f'{backup}\\backup{fullDate.date()}.zip', 'a', allowZip64=True) as backupZip:
                    backupZip.write(f'{path}\\{i}', arcname=f'{path}\\{i}'.replace(tempPath, r'backup'))
    except Exception as error:
        writeLog(f"iterationСycle Error {error}", traceback.extract_stack()[-1].lineno)


def createArhive():
    """Создает рахив в папке Backup"""
    with open('setting.json', 'r') as settingJson:
        setting = json.load(settingJson)
        if os.path.isfile(f"{setting['Backup']}\\backup{fullDate.date()}.zip") != True:
            writeLog('Архива за сегодня нет', traceback.extract_stack()[-1].lineno)
            iterationСycle(setting['File'], setting['Backup'], setting['File'])
            writeLog('Архив создан', traceback.extract_stack()[-1].lineno)
        else:
            writeLog('Архив за сегодняшнее число есть', traceback.extract_stack()[-1].lineno)

def deletOldArhive():
    """Проверяет длинну списка архивов в папке backup. Если больше числа указанного в setting.json
        удаляет лишние"""
    with open('setting.json', 'r') as settingJson:
        setting = json.load(settingJson)
        listArchive = os.listdir(setting['Backup'])
        if len(listArchive) > setting['DateBackup']:
            writeLog(f'В папке находятся больше {setting["DateBackup"]} архивов', traceback.extract_stack()[-1].lineno)
            for i in range(0, len(listArchive) - setting['DateBackup']):
                writeLog(f"Удалили {listArchive[i]}", traceback.extract_stack()[-1].lineno)
                os.remove(f'{setting["Backup"]}\\{listArchive[i]}')
    writeLog('Программа завершена', traceback.extract_stack()[-1].lineno)