[app]
title = Visual Alphabet
package.name = visualalphabet
package.domain = org.example
source.dir = .
source.include_exts = .py,.png,.jpg,.jpeg
version = 1.0
requirements = python3,kivy,pillow
orientation = portrait
fullscreen = 0
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
presplash.color = #1565c0

[buildozer]
log_level = 2
warn_on_root = 0
