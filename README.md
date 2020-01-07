# pyembroideryGH

- This is a set of UserObjects for [Grasshopper](https://www.rhino3d.com/6/new/grasshopper).
- Grasshopper is a Plugin for the popular CAD-System [McNeel Rhinoceros 6](https://www.rhino3d.com/).
- All code here is written in IronPython 2.7.8.0 as this is the interpreter Rhino & Grasshopper use internally.

## Purpose & Origins

The purpose of this project is to enable Rhino and Grasshopper to directly read, write and manipulate a variety of embroidery formats. This implementation relies on [ironpyembroidery](https://github.com/fstwn/ironpyembroidery/), which is an IronPython-compatible fork of [pyembroidery](https://github.com/EmbroidePy/pyembroidery/).

**The ironpyembroidery library is included here as a submodule, so you don't have to get it separately when installing! For more info read below.**

## Installing pyembroideryGH

### 1. INSTALL IRONPYEMBROIDERY

- Navigate to the scripts folder of Rhino 6:
  Open Explorer and go to "C:\Users\%USERNAME%\AppData\Roaming\McNeel\Rhinoceros\6.0\scripts"
- Move the whole "pyembroidery" directory to the scripts folder.


### 2. INSTALL PYEMBROIDERYGH

- Navigate to the Grasshopper UserObjects folder. This can be done in two ways:

  EITHER  Open explorer and go to "C:\Users\%USERNAME%\AppData\Roaming\Grasshopper\UserObjects"
  OR	  Open Rhino & Grasshopper and in the Grasshopper Window navigate to   File -> Special Folders -> User Object Folder

- Move the whole "pyembroideryGH" directory to the UserObjects folder.


### 3. UNBLOCK THE NEW USEROBJECTS!

- Go into your "pyembroideryGH" folder inside Grasshoppers UserObjects folder
- Right click onto the first UserObject and go to "Properties"
- If the text "This file came from another computer [...]" is displayed click on "Unblock"!
- REPEAT THIS FOR EVERY USEROBJECT IN THE FOLDER!
