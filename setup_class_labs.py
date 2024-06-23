import os, sys
import requests
import zipfile

base_url = "https://github.com/tylerfarmer1/all_classes/raw/main/"
#lab_folders = ["AI-050", "DP-900", "DP-100", "DP-203", "DP-300", "PL-900", "PL-100", "PL-200", "PL-400", "PL-500", "PL-7000"]
lab_folders = ["PL-200", "PL-400", "PL-500", "PL-7001","PL-7002","PL-7003", "PL-900"]
#lab_folders.sort()
disk_drive = r"D:\\"

# Function to ask a user which lab then want
def make_choice():
    # Print the list with item numbers
    print("\n\nI am Here")
    print("\n\n\nHere is a list of classes. Please enter the class number to retrieve: ")
    for index, folder in enumerate(lab_folders, 1):
        print(f"{index}: {folder}")
    
    # Ask for user input
    choice = input("Enter the number corresponding to your class: ")
    
    # Check if the choice is valid
    if choice.isdigit() and 1 <= int(choice) <= len(lab_folders):
        return(lab_folders[int(choice) - 1])
    else:
        print("No option selected, program terminated.")
        sys.exit()

# function to delete the existing folder
def delete_existing(choice):
    #print("\nStarting Deletion Process:")
    folder_path = disk_drive + choice
    
    if os.path.exists(folder_path):
        for root,dirs,files in os.walk(folder_path, topdown=False):
            for name in files:
                try:
                    os.remove(os.path.join(root,name))
                except Exception as e:
                    #print(f"This file failed to delete: {name} but continuing on.")
                    print("Continuing...")
            for name in dirs:
                try:
                    os.rmdir(os.path.join(root, name))
                except Exception as e:
                    #print(f"This folder failed to delete: {name} but continuing on.")
                    print("Continuing...")
        try:
            os.remove(folder_path)
        except Exception as e:
            #print(f"Failed to delete root folder {folder_path} but continuing on.")
            print("Continuing...")
    else:
        #print(f"Folder {folder_path} does not exist.  Continuing on.")
        print("Continuing...")


# Function to download and extract the zip file
def download_and_extract(choice):

    print("\nStarting Download Process:")
    my_zip_file = choice + ".zip"
    url = base_url + my_zip_file
    
    print(f"Downloading file {my_zip_file} from URL {url}")
    
    response = requests.get(url)
    if response.status_code == 200:
        # Save the zip file in the root of the disk:
        with open(os.path.join(disk_drive, my_zip_file), "wb") as f:
            f.write(response.content)
    else:
        print("Failed to download the file.  Exiting Program.")
        sys.exit()

    
    print("\nStarting Extraction Process:")
    extract_path = disk_drive + choice
    print(f"Extracting to folder {extract_path}")
    full_file_name = disk_drive + my_zip_file

    with zipfile.ZipFile(full_file_name, "r") as zip_ref:
        for file in zip_ref.namelist():
            try:
                zip_ref.extract(file, extract_path)
            except PermissionError as e:
                print(f"Permission error with {file}, skipping that file and continuing on.")
            except Exception as e:
                print(f"Error extracting {file} with error {e} but continuing on.")
    
    # Delete the Zip File
    os.remove(full_file_name)


my_choice=make_choice()
delete_existing(my_choice)
download_and_extract(my_choice)
print("\n\nAll Finished.\n")
