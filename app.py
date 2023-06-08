import json

from settingJson import getPathsFolder
from checkedPaths import checkedPaths


def copyBackup():
    data = getPathsFolder()
    checkedPaths(data)


copyBackup()
