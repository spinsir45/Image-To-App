#!/usr/bin/python3

import os
import shutil
import subprocess
import argparse
import textwrap

HOME_DIR = os.environ["HOME"]
LOCAL_APP_DIR = f"{HOME_DIR}/.local/share/applications"
if not os.path.isdir(LOCAL_APP_DIR):
    print(f'ERROR: the file path "{LOCAL_APP_DIR}" could not be found.')
    exit(1)

""" 
todo: -n --new [appimage_name]: creates a new folder in the .local/appimages dir for the new appimage
todo: -u --update [none or appimage_name]: updates all appimages by default. Else it will updated the given appimage.
todo: -i --icon [file_path, appimage_name]: Adds a icon to an appimage
todo: -l --list: Lists all appimages found in the .local/appimages dir
todo: -d --delete [appimage]: deletes the given appimage
todo: -m --modify [appimage]: allows the user to modify the given appimage .desktop file
"""


class ImageToApp:
    _APPIMG_DIR = f"{HOME_DIR}/.local/appimages"
    _CATAGORIES = (
        "AudioVideo",
        "Audio",
        "Video",
        "Development",
        "Education",
        "Game",
        "Graphics",
        "Network",
        "Office",
        "Science",
        "Settings",
        "System",
        "Utility",
    )
    _build_dir: str = None
    _app_icon_name: str = None
    _appimage_name: str = None
    _app_name: str = None
    _app_comment: str = None
    _app_category: str = None

    def __init__(self) -> None:
        pass

    def __read_details_file(self) -> None:
        """Reads the details.txt file and collects saves the information."""

        f = open("details.txt", "r")
        # Collects data from details.txt
        for line in f:
            words = line.split("=")
            if words[0].strip().lower() == "name":
                self._app_name: str = words[1].strip()
                continue
            if words[0].strip().lower() == "comment":
                self._app_comment: str = words[1].strip()
                continue
            if words[0].strip().lower() == "categories":
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
        files: list = os.listdir(self._build_dir)
        is_details_file: bool = False
        is_appimage_file: bool = False
        is_icon_img: bool = False
        # Check if all files needed are found and collect file names
        for file in files:
            if "details.txt" == file:
                is_details_file = True
                continue
            if ".AppImage" in file:
                is_appimage_file = True
                self._appimage_name: str = file
                continue
            if ".png" in file or ".jpeg" in file or ".jpg" in file:
                is_icon_img = True
                self._app_icon_name: str = file
                continue
        # Gets data to create the .desktop file
        if is_details_file and is_appimage_file and is_icon_img:
            self.__read_details_file()
        # Error handling
        elif not is_details_file:
            print("details.txt is missing")
            exit(1)
        elif not is_appimage_file:
            print("A .AppImage file was not found.")
            exit(1)
        elif not is_icon_img:
            print("A compatible image file was not found.")
            print("Supported image files are .png, .jpeg, .jpg")
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
        if os.path.isfile(f"{LOCAL_APP_DIR}/{self._app_name}.desktop"):
            while True:
                response: str = input(
                    f"The file {self._app_name}.desktop already exists. Would you like to override this file? (y/n)"
                )
                if response.lower() == "y":
                    break
                else:
                    exit(0)
        f = open(f"{LOCAL_APP_DIR}/{self._app_name}.desktop", "w")
        f.write(textwrap.dedent(file))
        f.close()
        # TODO: Check for errors
        # Make the file executable
        subprocess.run(["chmod", "+x", f"{LOCAL_APP_DIR}/{self._app_name}.desktop"])
        # Update the environment to recognize the new .desktop file
        subprocess.run(
            ["update-desktop-database", f"{LOCAL_APP_DIR}/{self._app_name}.desktop"]
        )

    def create_app(self, appimg_path: str, icon_path: str) -> None:
        """Creates a .desktop app connected with an appimage

        Args:
            appimg_path (str): The path to the .Appimage file
            icon_path (str): The path to the icon file
        """        

        self.__read_build_dir()
        self.__create_desktop_file()

    def delete_app(self, app_name: str) -> None:
        """Deletes both the appimg dir and its desktop file.

        Arguments:
            appimg_name (str): The name of the appimg dir to be deleted.
        """

        file_path: str = f"{self._APPIMG_DIR}/{app_name}"
        # check if the file exists
        os.path.exists(file_path)
        try:
            shutil.rmtree(file_path)
            print(f"{app_name} has been deleted.")
        except Exception as e:
            print("An error occurred while attempting to delete the files:\n")
            print(e)

    def list_apps(self) -> None:
        """Lists all current apps found in the appimages dir."""

        try:
            files: str = os.listdir(self._APPIMG_DIR)
        except Exception as e:
            print("An error occurred while fetching files:\n")
            print(e)
            exit(1)
        for file in files:
            print(file)

    def __get_icon_name(self, path: str) -> str:
        """Finds the icon name from the given file path.

        Arguments:
            path (str): The file path of the icon.

        Returns:
            str: The name of the icon.
        """
        split_path: list = path.split("/")
        return split_path[-1].strip()

    def update_icon(self, icon_path: str, app_name: str) -> None:
        """Updates an icon to the appimg file.

        Arguments:
            icon_path (str): The path to the icon file.

            appimg_name (str): The name of the appimg dir to add the icon to.
        """

        # Check if path exists
        if not os.path.exists(icon_path):
            print(f"The path '{icon_path}' does not exist.")
            exit(1)

        # Create path to copy the icon
        icon_name: str = self.__get_icon_name(icon_path)
        destination_path: str = f"{self._APPIMG_DIR}/{app_name}/{icon_name}"

        # Copy the icon to the appimg dir
        try:
            shutil.copy(icon_path, destination_path)
        except Exception as e:
            print("A failure occurred while trying to add the icon:\n")
            print(e)
            exit(1)
        # update the .desktop file
        # todo: prompt the user for details on the .desktop file instead of
        # having them create a details.txt file.


class TerminalInterface:

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            prog="Image to App",
            description="Creates desktop files for your Appimages."
        )
        self.image_to_app = ImageToApp()
        self.__add_args()
        self.args = self.parser.parse_args()
        self.__run_commands()

    def __run_commands(self) -> None:
        """ Runs the commands passed by the user."""
        
        if self.args.new:
            self.image_to_app.create_app()
        if self.args.update:
            print('update')
        if self.args.icon:
            self.image_to_app.update_icon(self.args.icon[0], self.args.icon[1])
        if self.args.list:
            self.image_to_app.list_apps()
        if self.args.delete:
            self.image_to_app.delete_app(self.args.delete)

    def __add_args(self) -> None:
        """ Adds arguments to the parser. """

        self.parser.add_argument(
            '-n',
            '--new',
            nargs=2,
            help="Creates a new .desktop file.",
            metavar=("[appimg_path]", "[icon_path]"),
            )
        self.parser.add_argument(
            '-u',
            '--update',
            help="Updates the .desktop file to match the .Appimage name.",
            metavar="[app_name]"
            )
        self.parser.add_argument(
            '-i',
            '--icon',
            help="Updates the icon of a given app.",
            metavar=("[icon_path]", "[app_name]"),
            nargs=2
            )
        self.parser.add_argument(
            '-l',
            '--list',
            help="Lists all app names.",
            metavar='',
            action='store_const',
            const=None
            )
        self.parser.add_argument(
            '-d',
            '--delete',
            help="Deletes the Appimage, icon, and .desktop file.",
            metavar="[app_name]"
            )
        # self.parser.add_argument('-m', '--modify') #TODO: add feature to modify .desktop file


if __name__ == "__main__":
    term_interface = TerminalInterface()
