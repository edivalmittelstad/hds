import os
from src.Hd.services import HDService
from src.Hd.schemas import HDCreateInput
from src.Objeto.services import ObjetoService
from src.Objeto.schemas import ObjetoCreateInput

BASE="/home/edival/TRABALHO/"
HD = 1

def getFiles(PATH, PAI, HD):
    try:
        ROOTFILES = [f for f in os.listdir(PATH) if os.path.isfile(PATH+f)] 
        for obj in ROOTFILES:
            
            print(f"Files: {obj} ==> PAI: {PAI}")
            
    except:  # noqa: E722
        pass
        
def getDirs(PATH, PAI, HD):
    getFiles(PATH, PAI, HD)
    try:
        ROOTDIRS = [f for f in os.listdir(PATH) if os.path.isdir(PATH+f)]
        for obj in ROOTDIRS:
            print(f"Dirs: {obj} PAI: {PAI}")
            DIR = PATH + obj + "/"
            getDirs(DIR, obj, HD)
    except:  # noqa: E722
        pass

getDirs(BASE, "", HD)
