import sys
from pathlib import Path
import os
import shutil
import zipfile
import tarfile
from Helper.translate import normalize


DIR_PATH = ""


EXTENSIONS = {"images": ["jpeg", "png", "jpg", "svg"],
              "video": ["avi", "mp4", "mov", "mpk"],
              "documents": ["doc", "docx", "txt", "pdf", "xlsx", "pptx"],
              "audio": ["mp3", "ogg", "wav", "amr"],
              "archives": ["zip", "gz", "tar"],
              "unknown": []}


def get_folder_name():
    """
    This function create a path to the folder
    """
    if len(sys.argv) == 2:
        global DIR_PATH
        DIR_PATH = sys.argv[1]
    else:
        while True:
            DIR_PATH = input(
                "Please type a path to the folder you want to clean: ")
            if DIR_PATH in ["cancel", "close", "exit"]:
                DIR_PATH = ""
                return print("Work with files have been canceled")
            path = Path(DIR_PATH)
            if not path.exists():
                DIR_PATH = ""
                while True:
                    answer = input(
                        "Wrong path. Do you want to try one more time? (y/n) ")
                    if answer.lower() == "y":
                        break
                    elif answer.lower() in ["n", "cancel"]:
                        return print("You have canceled work with files")
                    else:
                        print("Wrong command")
                        continue
            else:
                return print(f"Cleaning {DIR_PATH} folder")


names_dict = {"images": [],
              "documents": [],
              "audio": [],
              "video": [],
              "archives": [],
              "unknown": []}


known_extension = set()
unknown_extension = set()


def get_and_rename_files_names(path):
    """
    This function rename files in order way 
    """
    path_obj = Path(path)
    for entry in path_obj.iterdir():
        if entry.is_file():
            try:
                for key, values in EXTENSIONS.items():
                    if str(entry).split(".")[-1].lower() in values:
                        os.chdir(path_obj)
                        os.rename(entry.name, normalize(entry.name))
                        names_dict[key].append(normalize(entry.name))
                        known_extension.add(str(entry).split(".")[-1].lower())
                        break
                if str(entry).split(".")[-1].lower() not in known_extension:
                    os.chdir(path_obj)
                    os.rename(entry.name, normalize(entry.name))
                    names_dict["unknown"].append(
                        normalize(entry.name))
                    unknown_extension.add(str(entry).split(".")[-1].lower())
            except IndexError as e:
                names_dict["unknown"].append(entry.name)
        else:
            get_and_rename_files_names(f"{path}\{entry.name}")


FOLDER_NAMES = list([key for key in names_dict])


def create_folders(path):
    """
    This function create empty folders for files we have
    """
    for key, values in names_dict.items():
        if values:
            for value in values:
                os.makedirs(
                    rf"{path}\{key}\{value.split('.')[-1].lower()}", exist_ok=True)


def remove_files(path):
    """
    This function remove files to correct directory
    """
    steps = 0
    remove_files_info_logs = []
    counter = 0
    obj_path = Path(path)
    for file in obj_path.iterdir():
        try:
            if file.is_dir():
                if file.name in FOLDER_NAMES:
                    continue
                else:
                    remove_files(f'{path}\{file.name}')
                try:
                    os.remove(file)
                except:
                    remove_files_info_logs.append(
                        f"Folder {file} is not empty")
            elif file.is_file():
                for key, values in names_dict.items():
                    if file.name in values:
                        try:
                            shutil.move(
                                rf"{file}", rf"{DIR_PATH}\{key}\{str(file).split('.')[-1].lower()}")
                        except shutil.Error:
                            os.rename(str(file), str(
                                f'{str(file).split(".")[0]}_{counter}.{str(file).split(".")[-1]}'))
                            new_name = str(
                                f'{str(file).split(".")[0]}_{counter}.{str(file).split(".")[-1]}')
                            shutil.move(
                                rf"{new_name}", rf"{DIR_PATH}\{key}\{str(file).split('.')[-1].lower()}")
                            counter += 1
        except Exception as e:
            remove_files_info_logs.append(e)
    return f"Remove files info logs: {remove_files_info_logs}"


def deleted_folders(path):
    """
    This func delete empty folders
    """
    deleted_folders_info_logs = []
    obj_path = Path(path)
    for file in obj_path.iterdir():
        try:
            if file.is_dir():
                deleted_folders(f'{path}\{file.name}')
                os.rmdir(file)
        except OSError as e:
            deleted_folders_info_logs.append(f"Folder {file} is not empty")
    return f"Deleted folders info logs: {deleted_folders_info_logs}"


existed_archives = set()


def unpack_archives(path):
    """
    This func unpach archives
    """
    unpack_archives_info_logs = []
    try:
        for extension in existed_archives:
            if extension == "zip":
                for file in os.listdir(rf"{path}\archives\zip"):
                    data_zip = zipfile.ZipFile(
                        rf"{path}\archives\zip\{file}", 'r')
                    os.makedirs(
                        rf"{path}\archives\zip\{file.split('.')[0]}", exist_ok=True)
                    data_zip.extractall(
                        path=rf"{path}\archives\zip\{file.split('.')[0]}")
            elif extension == "tar":
                try:
                    for file in os.listdir(rf"{path}\archives\tar"):
                        with tarfile.open(
                                rf"{path}\archives\tar\{file}", 'r') as data_tar:
                            os.makedirs(
                                rf"{path}\archives\tar\{file.split('.')[0]}", exist_ok=True)
                            data_tar.extractall(
                                path=rf"{path}\archives\tar\{file.split('.')[0]}")
                except tarfile.ReadError as e:
                    print("Something wrong with your archive:", e)
    except PermissionError as e:
        unpack_archives_info_logs.append(e)
    return f"Unpack archives info logs: {unpack_archives_info_logs}"


def clean():
    if not DIR_PATH:
        get_folder_name()
    if DIR_PATH:
        get_and_rename_files_names(DIR_PATH)
        create_folders(DIR_PATH)
        remove_files(DIR_PATH)
        existed_archives = set([value.split(".")[1]
                                for value in names_dict["archives"]])
        if existed_archives:
            unpack_archives(DIR_PATH)
        deleted_folders(DIR_PATH)
        deleted_folders(DIR_PATH)
        print(f"Folder {DIR_PATH} has been cleaned")


if __name__ == "__main__":
    clean()
