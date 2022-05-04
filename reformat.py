import glob
import os
from pathlib import Path
from dateutil.parser import parse

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True

    Taken from: https://stackoverflow.com/questions/25341945/check-if-string-has-date-any-format#25341965
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def moveup_and_rename(p, moveTwo=False):
    """ Appends parent dir to filename and moves it up a dir """
    if moveTwo:
        parent_dir = p.parents[2]                   
        newName = p.parents[1].name + ' ' + p.parents[0].name + ' ' + p.name
        p.rename(parent_dir / newName)
    else:
        parent_dir = p.parents[1]
        newName = p.parents[0].name + ' ' + p.name
        p.rename(parent_dir / newName)
    return

def reFormat(imgs_path, pollenTypes):
    # https://stackoverflow.com/questions/2186525/how-to-use-glob-to-find-files-recursively
    dirs_to_delete = []
    imgs_list = []
    tenX_list = []
    for file in glob.glob(imgs_path, recursive=True):
        p = Path(file).absolute()
        # Testing
        if file.endswith('.JPG'):
            imgs_list.append(file)
        if ' 10X' in file:
            tenX_list.append(file)
        # If the path is a dir and its name is not one of the pollen types, delete it later
        if os.path.isdir(file):
            if p.name not in pollenTypes:
                dirs_to_delete.append(file)
            continue
        # Handles date/Old/*.JPG
        if p.parents[0].name == "Old" and is_date(p.parents[1].name):
            if file.endswith('.JPG'):
                moveup_and_rename(p, moveTwo=True)
                continue
        # Handles /Old/*.JPG and /Date/*.JPG
        if p.parents[0].name == "Old" or is_date(p.parents[0].name):
            if file.endswith('.JPG'):
                moveup_and_rename(p)
    print("Num Images:", len(imgs_list))
    print("Num 10x Res. Images:", len(tenX_list))
    # Reverse-Sort to ensure deeper dirs get deleted first
    dirs_to_delete.sort(key=len)
    dirs_to_delete.reverse()
    return dirs_to_delete, tenX_list

def removeDirs(dirList):
    """ 
        Calls os.rmdir on each dir in dirList.
        
        On Error, prints an error message, and continues.
    """
    for dir in dirList:
        try:
            os.rmdir(dir)
        except:
            print("Error Deleting:", dir)
            continue
    return

if __name__ == "__main__":
    cwd = os.getcwd()
    imgs_path = os.path.join(cwd, "Pollen Slides", "**", "*")
    pollenTypes = [
                    'Acmispon glaber', 'Amsinckia intermedia', 'Calystegia macrostegia', 
                    'Camissonia bistorta', 'Centaurea melitensis', 'Corethrogyne filaginifolia', 
                    'Croton setigerus', 'Ericameria pinifolia', 'Eriogonum fasciculatum', 
                    'Eriogonum gracile', 'Erodium Botrys', 'Erodium cicutarium', 
                    'Heterotheca grandiflora', 'Hirschfeldia incana', 'Lepidospartum squamatum', 
                    'Lessingia glandulifera', 'Marah Macrocarpa', 'Mirabilis laevis', 
                    'Penstemon spectabilis', 'Phacelia distans', 'Ribes aureum', 
                    'Salvia apiana', 'Solanum umbelliferum'
                ]
    dirs_to_delete, tenX_list = reFormat(imgs_path, pollenTypes)
    removeDirs(dirs_to_delete)



    