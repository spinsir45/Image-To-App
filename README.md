# Image To App

Quickly creates Desktop shortcuts for your AppImages.

## Prerequisites

> [!IMPORTANT]
> Make sure the file path `~/.local/bin` exists and that it is added to your `$PATH`.

## Installation:

1. Download the file `image_to_app.py` file.

2. Move the file into `~/.local/bin` and make the file executable.

> [!TIP]
> You can rename the file to whatever you want. Just remember that whatever you
> name the file that is the command you will call to run the app in the terminal.

## How to use.

### Making a new desktop app

This command will generate a new .desktop file and copy the appimage and icon 
into `~/.local/image_to_app/<app-name>`. 

1. Download your appimage and image you wish to use as an icon.

2. Run the command `image_to_app.py -n <path-to-appimage> <path-to-app-icon>`.

3. Answer the prompts.

### Update your desktop app

When your appimage updates it will likely break your desktop app. This can be
fixed by running the command `image_to_app.py -u <app-name>`. Or you can run
`image_to_app.py -u` to update all the applications.

### Update the desktop icon

`image_to_app.py -i <path-to-icon> <app-name>`

### View all the apps you have installed

`image_to_app.py -l`

### Delete an app

`image_to_app.py -d <app-name>`