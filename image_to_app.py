#!/usr/bin/python3

import os, sys
import subprocess
import argparse
import textwrap

HOME_DIR = os.environ['HOME']
LOCAL_APP_DIR = f'{HOME_DIR}/.local/share/applications'
if not os.path.isdir(LOCAL_APP_DIR):
    print(f'ERROR: the file path "{LOCAL_APP_DIR}" could not be found.')
    exit(1)

class ImageToApp:
    _catagories = ('AudioVideo', 'Audio', 'Video', 'Development', 'Education', 'Game', 'Graphics', 'Network', 'Office', 'Science', 'Settings', 'System', 'Utility')
    _build_dir:str = None
    _app_icon_name:str = None
    _appimage_name:str = None
    _app_name:str = None
    _app_comment:str = None
    _app_category:str = None


    def __init__(self) -> None:
        pass


    def __read_details_file(self) -> None:
        """Reads the details.txt file and collects saves the information."""

        f = open('details.txt', 'r')
        # Collects data from details.txt
        for line in f:
            words = line.split('=')
            if words[0].strip().lower() == 'name':
                self._app_name:str = words[1].strip()
                continue
            if words[0].strip().lower() == 'comment':
                self._app_comment:str = words[1].strip()
                continue
            if words[0].strip().lower() == 'categories':
                self._app_category = words[1].strip()
                continue
        f.close()
        # Error handling
        if not self._app_name:
            print('"Name=" was not found the details.txt file')
            exit(1)
        if not self._app_comment:
            print('"Comment=" was not found the details.txt file')
            exit(1)
        if not self._app_category:
            print('"Categories=" was not found the details.txt file')
            exit(1)


    def __read_build_dir(self) -> None:
        """Reads the files in the current dir to find the name of the
        AppImage, the details.txt file, and a image file.
        
        Supported image files are .png, .jpg, and .jpeg
        """
        self._build_dir = os.getcwd()
        files:list = os.listdir(self._build_dir)
        is_details_file:bool = False
        is_appimage_file:bool = False
        is_icon_img:bool = False
        # Check if all files needed are found and collect file names
        for file in files:
            if 'details.txt' == file:
                is_details_file = True
                continue
            if '.AppImage' in file:
                is_appimage_file = True
                self._appimage_name:str = file
                continue
            if '.png' in file or '.jpeg' in file or '.jpg' in file:
                is_icon_img = True
                self._app_icon_name:str = file
                continue
        # Gets data to create the .desktop file
        if is_details_file and is_appimage_file and is_icon_img:
            self.__read_details_file()
        # Error handling
        elif not is_details_file:
            print('details.txt is missing')
            exit(1)
        elif not is_appimage_file:
            print('A .AppImage file was not found.')
            exit(1)
        elif not is_icon_img:
            print('A compatible image file was not found.')
            print('Supported image files are .png, .jpeg, .jpg')
            exit(1)

    def __create_desktop_file(self) -> None:
        """Creates the .desktop file and updates the desktop environment to find the app"""
        file = f"""
        [Desktop Entry]
        Type=Application
        Name={self._app_name}
        Icon={self._build_dir}/{self._app_icon_name}
        Exec={self._build_dir}/{self._appimage_name}
        Comment={self._app_comment}
        Categories={self._app_category}  # Choose the appropriate category (https://specifications.freedesktop.org/menu-spec/latest/apa.html)
        Terminal=false
        """
        if os.path.isfile(f'{LOCAL_APP_DIR}/{self._app_name}.desktop'):
            while True:
                response: str = input(f"The file {self._app_name}.desktop already exists. Would you like to override this file? (y/n)")
                if response.lower() == 'y':
                    break
                else:
                    exit(0)
        f = open(f'{LOCAL_APP_DIR}/{self._app_name}.desktop', 'w')
        f.write(textwrap.dedent(file))
        f.close()
        # TODO: Check for errors
        subprocess.run(['chmod', '+x', f'{LOCAL_APP_DIR}/{self._app_name}.desktop'])
        subprocess.run(['update-desktop-database', f'{LOCAL_APP_DIR}/{self._app_name}.desktop'])

    def run(self) -> None:
        """ Class the methods to create a desktop application. """

        self.__read_build_dir()
        self.__create_desktop_file()
        print("Finished")


if __name__ == '__main__':
    img_to_app = ImageToApp()
    img_to_app.run()