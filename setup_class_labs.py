import os, sys, re
import requests
import zipfile

base_url = "https://github.com/tylerfarmer1/all_classes/raw/main/"

disk_drive = r"D:\\"
#disk_drive = r"C:\\LabFiles\\"


# Check GitHub to see whether a zip file for this course exists
def course_exists(course):
    url = base_url + course + ".zip"
    try:
        response = requests.head(url, allow_redirects=True, timeout=30)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Could not reach GitHub ({e}). Check your internet connection.")
        return False


# Function to ask the student which course they want
def make_choice():
    print("Using the ", disk_drive)
    while True:
        choice = input("\n\nEnter your course number (for example PL-900 or PL-7001), or press Enter to quit: ").strip()

        # Blank input ends the program
        if choice == "":
            print("No course entered, program terminated.")
            sys.exit()

        # GitHub file names are case sensitive and the zip files are upper case
        choice = choice.upper()

        # Only allow letters, numbers and dashes (keeps the input safe to use as a file/folder name)
        if not re.fullmatch(r"[A-Z0-9-]+", choice):
            print(f"'{choice}' is not a valid course number. Please try again.")
            continue

        print(f"Searching GitHub for {choice}.zip ...")
        if course_exists(choice):
            return choice
        print(f"Course {choice} was not found. Please check the course number and try again.")


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








