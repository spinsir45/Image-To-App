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
todo: -m --modify [appimage]: allows the user to modify the given appimage .desktop file
"""


class ImageToApp:
    _APPIMG_DIR = f"{HOME_DIR}/.local/image_to_app"
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

    def __init__(self) -> None:
        pass

    def __get_real_path(path: str) -> str:
        """Finds the real paths of the files.

        Args:
            path (str): The relative file path.

        Returns:
            str: The absolute file path.
        """

        if path[0] == '/':
            if not os.path.exists(path):
                print(f"{path} does not exist.")
                exit(1)
        elif path[0] == '.' and path[1] == '/':
            path = path.replace('.', os.getcwd(), 1)
            if not os.path.exists(path):
                print(f"{path} does not exist.")
                exit(1)
        elif path[0] == '.' and path[1] == '.':
            path = os.getcwd() + f'/{path}'
            if not os.path.exists(path):
                print(f"{path} does not exist.")
                exit(1)
        else:
            path = f"{os.getcwd()}/{path}"
            if not os.path.exists(path):
                print(f"{path} does not exist.")
                exit(1)
        return path

    def __create_app_dir(self, app_name: str) -> str:
        """Creates a new dir for the new app.
        
        Args:
            app_name (str): The name of the application.

        Returns:
            str: The path to the new dir.
        """
        
        app_path: str = f"{self._APPIMG_DIR}/{app_name}"
        # Check if there is already an app with that name.
        if os.path.exists(app_path):
            print("There is already an app with that name.")
            exit(1)
        # Make a new dir for the app
        os.makedirs(app_path)
        return app_path

    def __get_user_input(self) -> None:
        """Gets input from the user to generate a .desktop file

        Returns:
            tuple (app_name, app_comment, app_catagory): contains data to help generate a .desktop file
        """
        
        app_name: str = input("Enter the name of the app: ")
        app_comment: str = input("Add a comment for the app: ")
        print("App Catagories:")
        for cat in self._CATAGORIES:
            print(f"\t{cat}")
        while True:
            app_catagory: str = input("Enter the app catagory: ")
            if app_catagory in self._CATAGORIES:
                break
        return (app_name, app_comment, app_catagory)

    def __move_files(self, app_path: str, icon_path: str, appimg_path: str) -> None:
        """Moves the executable file and icon to the new app dir.

        Args:
            app_path (str): The file path of the app.
            icon_path (str): The file path to the app icon.
            appimg_path (str): The file path to the executable file.
        """
        
        # Copy the executable and icon over
        shutil.copy(icon_path, f"{app_path}/{self.__get_file_name(icon_path)}")
        shutil.copy(appimg_path, f"{app_path}/{self.__get_file_name(appimg_path)}")

    def __create_desktop_file(self, app_name: str, app_comment: str, app_catagory: str, icon_name: str, appimg_name: str, app_path: str) -> None:
        """Creates the .desktop file and updates the desktop environment to find the app"""
        file = f"""
        [Desktop Entry]
        Type=Application
        Name={app_name}
        Icon={app_path}/{icon_name}
        Exec={app_path}/{appimg_name}
        Comment={app_comment}
        Categories={app_catagory}
        Terminal=false
        """
        if os.path.isfile(f"{LOCAL_APP_DIR}/{app_name}.desktop"):
            while True:
                response: str = input(
                    f"The file {app_name}.desktop already exists. Would you like to override this file? (y/n)"
                )
                if response.lower() == "y":
                    break
                else:
                    exit(0)
        f = open(f"{LOCAL_APP_DIR}/{app_name}.desktop", "w")
        f.write(textwrap.dedent(file))
        f.close()
        # TODO: Check for errors
        # Make the file executable
        subprocess.run(["chmod", "+x", f"{LOCAL_APP_DIR}/{app_name}.desktop"])
        # Update the environment to recognize the new .desktop file
        subprocess.run(
            ["update-desktop-database", f"{LOCAL_APP_DIR}/{app_name}.desktop"]
        )

    def create_app(self, appimg_path: str, icon_path: str) -> None:
        """Creates a .desktop app connected with an appimage

        Args:
            appimg_path (str): The path to the .Appimage file
            icon_path (str): The path to the icon file
        """        

        appimg_path, icon_path = self.__get_real_path(appimg_path, icon_path)
        app_data: tuple = self.__get_user_input()
        app_path: str = self.__create_app_dir(app_data[0])
        self.__move_files(app_path, icon_path, appimg_path)
        self.__create_desktop_file(app_data[0], app_data[1], app_data[2], self.__get_file_name(icon_path), self.__get_file_name(appimg_path), app_path)

    def delete_app(self, app_name: str) -> None:
        """Deletes both the appimg dir and its desktop file.

        Args:
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

    def __get_file_name(self, path: str) -> str:
        """Finds the file name from the given file path.

        Args:
            path (str): The file path.

        Returns:
            str: The name of the file.
        """
        split_path: list = path.split("/")
        return split_path[-1].strip()

    def update_icon(self, icon_path: str, app_name: str) -> None:
        """Updates an icon to the appimg file.

        Args:
            icon_path (str): The path to the icon file.

            appimg_name (str): The name of the appimg dir to add the icon to.
        """

        # Check if path exists
        if not os.path.exists(icon_path):
            print(f"The path '{icon_path}' does not exist.")
            exit(1)

        # Create path to copy the icon
        icon_name: str = self.__get_file_name(icon_path)
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
        self.__check_for_app_dir()
        self.__add_args()
        self.args = self.parser.parse_args()
        self.__run_commands()

    def __check_for_app_dir(self) -> None:
        """Checks if the '$HOME/.local/image_to_app' dir exists."""
        
        if os.path.exists(f"{HOME_DIR}/.local/image_to_app"):
            return
        else:
            os.makedirs(f"{HOME_DIR}/.local/image_to_app")

    def __run_commands(self) -> None:
        """ Runs the commands passed by the user."""
        
        if self.args.new:
            self.image_to_app.create_app(self.args.new[0], self.args.new[1])
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
