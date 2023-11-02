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
    catagories = ('AudioVideo', 'Audio', 'Video', 'Development', 'Education', 'Game', 'Graphics', 'Network', 'Office', 'Science', 'Settings', 'System', 'Utility')
    build_dir:str = None
    app_icon_name:str = None
    appimage_name:str = None
    app_name:str = None
    app_comment:str = None
    app_category:str = None


    def __init__(self) -> None:
        pass


    def read_details_file(self) -> None:
        """Reads the details.txt file and collects saves the information."""

        f = open('details.txt', 'r')
        # Collects data from details.txt
        for line in f:
            words = line.split('=')
            if words[0].strip().lower() == 'name':
                self.app_name:str = words[1].strip()
                continue
            if words[0].strip().lower() == 'comment':
                self.app_comment:str = words[1].strip()
                continue
            if words[0].strip().lower() == 'categories':
                self.app_category = words[1].strip()
                continue
        f.close()
        # Error handling
        if not self.app_name:
            print('"Name=" was not found the details.txt file')
            exit(1)
        if not self.app_comment:
            print('"Comment=" was not found the details.txt file')
            exit(1)
        if not self.app_category:
            print('"Categories=" was not found the details.txt file')
            exit(1)


    def read_build_dir(self) -> None:
        """Reads the files in the current dir to find the name of the
        AppImage, the details.txt file, and a image file.
        
        Supported image files are .png, .jpg, and .jpeg
        """
        self.build_dir = os.getcwd()
        files:list = os.listdir(self.build_dir)
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
                self.appimage_name:str = file
                continue
            if '.png' in file or '.jpeg' in file or '.jpg' in file:
                is_icon_img = True
                self.app_icon_name:str = file
                continue
        # Gets data to create the .desktop file
        if is_details_file and is_appimage_file and is_icon_img:
            self.read_details_file()
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

    def create_desktop_file(self) -> None:
        """Creates the .desktop file and updates the desktop environment to find the app"""
        file = f"""
        [Desktop Entry]
        Type=Application
        Name={self.app_name}
        Icon={self.build_dir}/{self.app_icon_name}
        Exec={self.build_dir}/{self.appimage_name}
        Comment={self.app_comment}
        Categories={self.app_category}  # Choose the appropriate category (https://specifications.freedesktop.org/menu-spec/latest/apa.html)
        Terminal=false
        """
        if os.path.isfile(f'{LOCAL_APP_DIR}/{self.app_name}.desktop'):
            print(f"The file {self.app_name}.desktop already exists")
            exit(1)
        f = open(f'{LOCAL_APP_DIR}/{self.app_name}.desktop', 'w')
        f.write(textwrap.dedent(file))
        f.close()
        # TODO: Check for errors
        subprocess.run(['chmod', '+x', f'{LOCAL_APP_DIR}/{self.app_name}.desktop'])
        subprocess.run(['update-desktop-database', f'{LOCAL_APP_DIR}/{self.app_name}.desktop'])


if __name__ == '__main__':
    img_to_app = ImageToApp()
    img_to_app.read_build_dir()
    img_to_app.create_desktop_file()
    print('Finished')