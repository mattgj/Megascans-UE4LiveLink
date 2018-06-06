# Megascans - Unreal Engine LiveLink

The Megascans **LiveLink** for Unreal Engine 4 is an **open-source, python-written** integration for Megascans inside unreal engine 4. The plugin is written with UnrealEnginePython and is available for UE4 versions **4.15 and above**.
Windows binaries are currently provided, and **OSX and Linux coming soon**.
##
![Art By Wiktor Öhman](https://cdnb.artstation.com/p/assets/images/images/011/106/221/large/wiktor-ohman-final-unbranded.jpg?1527869888)Art By Wiktor Öhman

## Installing the LiveLink with Megascans Bridge
Megascans is an ecosystem consisting of a huge scan library and a set of tools to help you work with that library, and Bridge is one of those tools.
Megascans Bridge lets you Instantly access the entire Megascans library, batch export straight to your game engine or 3D software, and unleash your imagination.

To install the LiveLink with Bridge :
- go to https://megascans.se/apps/bridge and download it.
- Click on the export icon of any asset in your downloaded library, set the "Application" to UE4 and click on "Download Plugin".
- Once the plugin is downloaded.
- go to https://megascans.se/apps/bridge and download it.

Now you can start UE4 and a megascans button should be on your toolbar. Simply click on the export button of any asset in Bridge and it'll be sent to Unreal.

##
![Art By Wiktor Öhman](https://cdnb.artstation.com/p/assets/images/images/010/357/747/large/wiktor-ohman-pubg.jpg?1523996697)Art By Wiktor Öhman

## Installing the LiveLink Manually
If you're looking into installing the Megascans LiveLink on a custom Unreal Engine Build, compiling the plugin should be a fairly straightforward task.
First, you need to install **Python 3.6 - 64Bits** on your computer, you can download the latest [version right here](https://www.python.org/downloads/).

Once you've installed it please make sure that the python installation path is in your environment variable paths.
Now the next step is to go to your unreal engine installation, then "**engine/plugins**" and create a folder in there called "**UnrealEnginePython**". Clone the [Github repository of the LiveLink](https://github.com/Quixel/Megascans-UE4LiveLink) and then copy the content of the folder **LiveLink** to the **UnrealEnginePython** folder you created earlier.

Now if you start the engine it should ask you to compile the DLLs for the plugin, which you will accept to do.
This can take quite a lot of time depending on what else there is to compile on your engine and how fast your computer is.

> **For OSX/Linux ONLY** : This procedure has only been tested on Windows so far. If you're looking into building the LiveLink for Linux or OSX please consider the following steps :
>
>  - Download the latest PySide2 "wheels" for Linux, OSX or Windows **[right here](http://download.qt.io/snapshots/ci/pyside/dev/latest/pyside2/)**. Read the name of the files very carefully to make sure that you're using the correct version.
>  
>  - Build PySide2 using the following line in your system's command line tool (*change the path and filename to your specific needs*) : 
> ```
> pip install C:/My_Wheels_Path/PySide2-Super_Long_Wheel_Name.whl
> ```
> - You should now have PySide2 installed in your python directory, mine is right here :
>      **C:\Python36\Lib\site-packages\PySide2**
> Now what you will do is delete the PySide2 folder in **UnrealEnginePython/Binaries/Win64** and put the one you just built instead.
> The file is very heavy by default, just so you know. There are a lot of dependencies that you can remove to make it as lightweight as the solution we provide by default, but it's a very time-consuming task generally.
> - That's about it ! PySide2 is the only dependency that's a bit hard to build right now unfortunately, so this step is necessary. We hope to provide pre-compiled, lightweight PySide2 plugins at some point for most OS versions out there, but that's another topic :) 

And that should be it ! Once the compilation is done you should see the Megascans Logo in your toolbar. There are still a bunch of issues related to PySide2 (*UI is not visible within a C++ project on 4.17, or can be buggy on OSX*), but overall you should be up and running with this.

When you export an asset from the Bridge, pick up the "Custom Build" option in the "Build Version" dropdown menu, then click on export.

##
![ - ](https://i.imgur.com/IrnXhDI.png)

## Extending the LiveLink with Python Scripting

Having the plugin work 100% with python comes with a lot of advantages if you're looking into extending it.
First, the entire source code is completely open, and you can find all the LiveLink script files in the LiveLink folder, where they all have the .py format.
UnrealEnginePython also has it's code open-source for you to modify as you want.

The LiveLink gives you access to a set of useful commands, like this one to import a mesh for instance :

```python
ms_import_mesh('C:/Meshes/MyMesh.fbx', '/Game/Mesh_Folder')
```
Or this one to apply a texture map to a material instance :

```python
ms_apply_tex2d_to_inst(inst_uobject, '/Game/Textures/bark_Albedo', 'Albedo')
```
You could push this a lot further and write a relatively small file that automatically imports and sets up your assets : 
```python
# We start off by initializing the unreal_engine module, then we execute the Megascans LiveLink's ms_main.
import unreal_engine as ue
ue.exec('ms_main.py')
 
folderpath_ = "/Game/Wood_Tree"
 
# QFileDialog is a PySide2.QtGui class. We use it to open a file browser for the texture maps and another one for the mesh files.
Textures_Path = QFileDialog.getOpenFileNames(None, str("Select your texture maps"), "", str("Image Files (*.png *.jpg)"))
Mesh_Path = QFileDialog.getOpenFileNames(None, str("Select your geometry files"), "", str("Image Files (*.fbx *.obj)"))

texture_paths = Textures_Path[0]
meshes_ = Mesh_Path[0]

# ms_import_mesh is a ms_main function that imports a given mesh to the input path folderpath_.
for mesh_ in meshes_:
    ms_import_mesh(mesh_, folderpath_)


# ms_import_texture_list imports an array of textures to the input path folderpath_.
ms_import_texture_list(texture_paths, folderpath_)

# Now we create our material instance, which is based on the material Basic_Master.
parent_mat = ue.load_object(Material, "/Game/Basic_Master")
ms_create_material_instance(parent_mat, "Wood_Tree_inst", folderpath_)

# Then we load it.
inst_uobj = ue.load_object(MaterialInstance, folderpath_ + "/" + "Wood_Tree_inst")

# This will return a list of all the meshes available in the folderpath_ folder.
static_mesh_array = [[item, (folderpath_ + "/" + item.get_name())] for item in ue.get_assets(folderpath_) if item.is_a(StaticMesh)]

# Assigning a material instance to our geometry is done by calling ms_main's ms_inst_2_mesh function.
if mesh_path != None:
    ms_inst_2_mesh(inst_uobj, static_mesh_array)

# Once you have our material instance applied to the geometry, we can start applying the textures from texture_paths to the material instance.
for texture in [item for item in ue.get_assets(folderpath_) if item.is_a(Texture2D)]:
    try:
        text_input = ms_get_map(texture.get_name())
        text_input = "metallic" if text_input.lower() == "metalness" else text_input
        # This ms_main function takes the material instance's UObject, the texture's name and an str of the map type (albedo, normal, etc...).
        ms_apply_tex2d_to_inst(inst_uobj, texture.get_path_name(), text_input)
    except:
        pass
 
# Finally we sync the content browser to the folderpath_'s content.
ue.sync_browser_to_assets(ue.get_assets(folderpath_))

```



That file should give you an idea on how to interact with the Megascans LiveLink and UnrealEnginePython in general. If you have any questions feel free to check the UnrealEnginePython GitHub page or send a, email to adnan at quixel.se!

