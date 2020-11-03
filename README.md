# pyembroideryGH

- This is a set of UserObjects for [Grasshopper](https://www.rhino3d.com/6/new/grasshopper).
- Grasshopper is a Plugin for the popular CAD-System [McNeel Rhinoceros 6](https://www.rhino3d.com/).
- All code here is written in IronPython 2.7.8.0 as this is the interpreter Rhino & Grasshopper use internally.

## Purpose & Origins

The purpose of this project is to enable Rhino and Grasshopper to directly read, write and manipulate a variety of embroidery formats. This implementation relies on [ironpyembroidery](https://github.com/fstwn/ironpyembroidery/), which is an IronPython-compatible fork of [pyembroidery](https://github.com/EmbroidePy/pyembroidery/).

**The ironpyembroidery library is included here as a submodule, so you don't have to get it separately when installing! For more info read below.**

## Installation & Usage

### 1. Download release files

- Go to [releases](https://github.com/fstwn/pyembroideryGH/releases) and download the newest release
- Unzip the downloaded archive. You should get three folders `pyembroidery`, `pyembroideryGH`, `Examples` and a text-file.

### 2. Install pyembroidery python module

- Open the scripts folder of Rhino 6
  - On **Windows**:
  `C:\Users\%USERNAME%\AppData\Roaming\McNeel\Rhinoceros\6.0\scripts`

  - On **Mac OSX**:
  `~/Library/Application Support/McNeel/Rhinoceros/6.0/scripts`
- Move the whole `pyembroidery` directory to the scripts folder!

### 3. Install pyembroideryGH UserObjects

- Navigate to the Grasshopper UserObjects folder
  - On **Windows**:
  `C:\Users\%USERNAME%\AppData\Roaming\Grasshopper\UserObjects`

  - On **Mac OSX**:
  `~/Library/Application Support/McNeel/Rhinoceros/MacPlugIns/Grasshopper/UserObjects`

  - *Alternative:* Open Rhino & Grasshopper and in the Grasshopper Window click on
  `File` > `Special Folders` > `User Object Folder`

- Move the whole `pyembroideryGH` directory to the UserObjects folder.

### 4. Unblock the new UserObjects!

- Go into the `pyembroideryGH` folder inside Grasshoppers UserObjects folder
- Right click onto the first UserObject and go to **Properties**
- If the text *This file came from another computer [...]* is displayed click on **Unblock**!
- **Unfortunately you have to do this for _EVERY_ UserObject in the folder!**

### 5. Restart Rhino & Grasshopper

- If Rhino was running during the installation process, you'll have to restart it for the changes to take effect!
