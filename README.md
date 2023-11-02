# Image To App

Quickly creates Desktop shortcuts for your AppImages.

## How to use:

1. Add the file to PATH
    1. Download the image_to_app.py file.
    2. Move the file to `~/.local/bin`
    3. Make the file executable.

2. Prep your AppImage
    1. Create a new folder.
    2. Add the AppImage.
    3. Add the icon image you want for the desktop icon.
    4. Create a file called details.txt

3. Creating the details.txt file
    - Add the following text to your details.txt file
    Name = your app name
    Comment = Any comment you want
    Categories = Choose a category defined by [Freedesktop](https://specifications.freedesktop.org/menu-spec/latest/apa.html)

4. Run the script
    - Once all the files have been added run the command `image_to_app.py` while in the directory you just created.