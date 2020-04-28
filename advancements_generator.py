import os
from shutil import rmtree
from zipfile import ZipFile
import json
import time
import sys

def create_path(filepath):
    if not os.path.exists(filepath):
        try:
            os.makedirs(filepath)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
                
def create_file(filename, contents):
    create_path(os.path.dirname(filename))
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(contents)
            
def create_file(filename, contents):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filename, "w") as f:
        f.writelines(contents)

def create_pack_mcmeta(version, description):
    contents = {
        "pack": {
            "pack_format": version,
            "description": description
        }
    }
    return json.dumps(contents, indent=4)

def create_impossible_root():
    contents = {
        "parent": "totally not possible",
        "criteria": {
            "impossible": {
                "trigger": "minecraft:impossible"
            }
        }
    }
    return json.dumps(contents, indent=4)

def create_impossible_advancement():
    contents = {
        "criteria": {
            "impossible": {
                "trigger": "minecraft:impossible"
            }
        }
    }
    return json.dumps(contents, indent=4)

def zip_files(dirname, zipname):
    path_length = len(dirname)
    with ZipFile(zipname, "w") as archive:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(dirname):
            zipFolderName = folderName[path_length:]
            for filename in filenames:
                # Create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                zipPath = os.path.join(zipFolderName, filename)
                # Add file to zip
                archive.write(filePath, zipPath)

def generate_impossible_advancements(jar_file):
    jar_file = jar_file.strip('"')

    # Verify jar file
    if os.path.splitext(jar_file)[1] != ".jar":
        raise ValueError("Error: Invalid file type. Expected '.jar'.")

    pack_format = 1
    while True:
        try:
            pack_format = eval(input("Enter a value for pack_format: "))
            break
        except:
            print("Invalid value type, must be an integer.")
    
    # Create Directories
    mc_version = os.path.splitext(os.path.basename(jar_file))[0]
    disable_advancements_dir = "versions/{0}/disable_advancements".format(mc_version)
    empty_advancements_dir = "versions/{0}/empty_advancements".format(mc_version)
    disable_advancements_zip = "{0}.zip".format(disable_advancements_dir)
    empty_advancements_zip = "{0}.zip".format(empty_advancements_dir)
    advancements_dir = "data/minecraft/advancements"
    pack_dir = "pack.mcmeta"

    # Reset datapacks to prepare for generation
    if os.path.exists(disable_advancements_dir):
        rmtree(disable_advancements_dir)
    if os.path.exists(empty_advancements_dir):
        rmtree(empty_advancements_dir)
    create_path(disable_advancements_dir)
    create_path(empty_advancements_dir)

    # Create pack mcmetas
    with open(os.path.join(disable_advancements_dir, pack_dir), "w") as f:
        f.writelines(create_pack_mcmeta(pack_format, "Disable Advancements ({0})".format(mc_version)))
    with open(os.path.join(empty_advancements_dir, pack_dir), "w") as f:
        f.writelines(create_pack_mcmeta(pack_format, "Empty Advancements ({0})".format(mc_version)))

    # Get impossible advancement templates
    impossible_root = create_impossible_root()
    impossible_advancement = create_impossible_advancement()

    # Generate advancements
    with ZipFile(jar_file, "r") as archive:
        for file in archive.namelist():
            if file.startswith(advancements_dir) and os.path.splitext(file)[1] == ".json":
                # Generate disable_advancements
                if os.path.split(file)[1] == "root.json":
                    filename = os.path.join(disable_advancements_dir, *file.split("/"))
                    create_file(filename, impossible_root)
                    
                # Generate empty_advancements
                filename = os.path.join(empty_advancements_dir, *file.split("/"))
                create_file(filename, impossible_advancement)

    # Delete old zips
    if os.path.exists(disable_advancements_zip):
        os.remove(disable_advancements_zip)
    if os.path.exists(empty_advancements_zip):
        os.remove(empty_advancements_zip)

    # Zip new datapacks
    zip_files(disable_advancements_dir, disable_advancements_zip)
    zip_files(empty_advancements_dir, empty_advancements_zip)

if __name__ == "__main__":
    try:
        jar_file = sys.argv[1]
        try:
            print("Generating advancements...")
            generate_impossible_advancements(jar_file)
            input("Finished generating. Press 'enter' or close this window to finish.")
        except:
            print("Stopped.")
    except:
        print("Impossible Advancements Generator by Onnowhere")
        print("Source: https://github.com/onnowhere/advancement-disabler")
        print("----------------------------------------------")
        print("This generates two datapacks based on the input Minecraft jar file.")
        print("Both packs accomplish the same goal, but there are some differences.")
        print("- disable_advancements")
        print("    This pack invalidates all root advancements by setting an invalid parent.")
        print("    Lightweight and likely futureproof but floods the output log with errors.")
        print("    The vanilla advancements will no longer be able to be given via commands.")
        print("- empty_advancements")
        print("    This pack changes every possible recipe and advancement to be impossible.")
        print("    This pack must be updated for new advancements in every Minecraft update.")
        print("    The vanilla advancements will still be able to be given through commands.")
        while True:
            try:
                print("----------------------------------------------")
                print("Minecraft jar files can be found in '.minecraft/versions'.")
                jar_file = input("Drop Minecraft jar file here and hit enter: ")
                print("Generating advancements...")
                generate_impossible_advancements(jar_file)
                input("Finished generating. Press 'enter' to generate again or close this window to finish.")
            except KeyboardInterrupt:
                print(e)
                break
            except EOFError:
                print(e)
                break
            except Exception as e:
                print(e)
                print("Error encountered while generating. Please try again.")
    print("Shutting down...")
    sys.exit()
        










