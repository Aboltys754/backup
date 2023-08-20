from src.app import checkedJsonProps, checkingSourseAndSaveFolders, createArhive, deletOldArhive
def backup():
    checkedJsonProps()
    checkingSourseAndSaveFolders()
    createArhive()
    deletOldArhive()

if __name__ == '__main__':
    backup()

