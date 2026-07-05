[app]

# (str) Title of your application
title = Visual Alphabet

# (str) Package name
package.name = visualalphabet

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3==3.10.10,kivy==2.2.1,pillow==9.5.0

# (str) Presplash of the application
# presplash.filename = ./presplash.png

# (str) Icon of the application
# icon.filename = ./icon.png

# (str) Supported orientations (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Android API to compile for
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (bool) accepts SDK license
android.accept_sdk_license = True

# (str) Presplash color
presplash.color = #1565c0

# (str) Android logcat filters
# android.logcat_filters = *:S python:D

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0

# (str) Path to build artifact output, absolute or relative to the current working directory
bin_dir = ./bin
