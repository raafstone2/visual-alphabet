[app]
title = سامانه الفبای تصویری
package.name = visualalphabet
package.domain = com.example.visualalphabet
source.dir = .
source.include_exts = .py,.png,.jpg,.kv,.atlas
version = 1.0
requirements = python3,kivy,pillow,pyjnius,android
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.accept_sdk_license = True
presplash.color = #1565c0

[buildozer]
log_level = 2
warn_on_root = 0
