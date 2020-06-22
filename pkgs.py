"""******************************************************************
   *     FTP Client                                                 *
   *     Upload/Download files to/from a ftp server                 *
   *                                                                *
   ******************************************************************"""
import ftplib
# import ftputil
import sys
import socket
from getpass import getpass
import os
import tkinter as tk
from tkinter import filedialog
import main


def print_intro():
    """Prints intro prompt for user to follow"""
    print("""
    1. Continue
    2. Exit\n""")


def check_input(selected_operation):
    """Checks the text input by the user and returns the required function
    :arg selected_operation: Input value or string from user
    """
    selected_operation = selected_operation.lower()
    try:
        selected_operation = int(selected_operation)
    except ValueError:
        pass
    finally:
        if selected_operation == "continue" or selected_operation == 1:
            return_value = router
        elif selected_operation == "exit" or selected_operation == 2:
            sys.exit()
        else:
            print("Invalid Choice, Enter a valid number of choice")
            return_value = 0
    return return_value


def credentials(ftp):
    """Gets username and password and authenticates the ftp object"""
    tries = 3
    while tries:
        username = input('Enter Your Username: ')
        password = getpass("Enter your password: ")
        try:
            if ftp.login(username, password)[0:3] == '230':
                print("Connected successfully\n")
            break
        except ftplib.error_perm:
            print("\nInvalid Login details\n")
            tries -= 1
        except ConnectionAbortedError:
            print("\nAn Unexpected error occured\n")
            break
        finally:
            if tries == 0:
                ftp.quit()
                main.run()


def set_ftp():
    """Resolves the specified server address"""
    server = input("Enter the address you want to connect to: ")
    server = server.strip()
    try:
        if server == "":
            return "\nEnter a valid server address\n"
        ftp = ftplib.FTP(server)
        return ftp
    except TimeoutError:
        print("\nconnection attempt failed because the connected party"
              " did not properly respond after a period of time")
        return "connection timed out, check that you have the right address\n"
    except ConnectionRefusedError:
        print("\nNo connection could be made because the target machine actively refused it")
        return "connection was refused\n"
    except socket.gaierror:
        print("\nFailed to get address info ")
        return "Address Resolution Failure, check your address and try again\n"
    except ftplib.all_errors:
        return "\nAn Unexpected error occ1urred\n"


def get_dir_path(ftp):
    """Gets current working directory path"""
    try:
        query_dir = (ftp.sendcmd('PWD')).split()
        return query_dir[1].strip('"')
    except ftplib.error_temp:
        print('Connection Timeout, Enter your credentials again\n')
        credentials(ftp)


def change_dir(ftp):
    """Change FTP current Dir"""
    new_dir = input("Enter the path you wish to change to "
                    "(e.g /folder/sub_folder) or enter a folder name from current dir:\n ")
    current_directory = get_dir_path(ftp)
    if new_dir[0] != '/' and current_directory != '/':
        new_dir = current_directory + '/' + new_dir
    elif new_dir[0] != '/' and current_directory == '/':
        new_dir = '/' + new_dir
    print("changing to " + new_dir)
    try:
        ftp.cwd(new_dir)
    except ftplib.error_perm:
        print("Failed to change directory check that you have the right directory")
    except ftplib.error_temp:
        print('Connection Timeout, Enter your credentials again\n')
        credentials(ftp)
    if get_dir_path(ftp) == new_dir:
        return_val = 1
    else:
        return_val = 0
    return return_val


def pwd(ftp):
    """Prints FTP current working directory tree"""
    temp_dir = get_dir_path(ftp)
    data = []
    try:
        ftp.dir(data.append)
    except ftplib.error_temp:
        print('Connection Timeout, Enter your credentials again\n')
        credentials(ftp)
    finally:
        print('Current Directory - ' + temp_dir + '\n')
        print('Permission   Date          Filename')
        for line in data:
            line = line.split()
            try:
                ftp.cwd(temp_dir + '/' + line[8])
                file_type = 'Folder'
            except ftplib.error_perm:
                file_type = 'File'
            finally:
                ftp.cwd(temp_dir)
                file_name = line[8]
                if len(line) != 9:
                    for i in line[9:]:
                        file_name = file_name + ' ' + str(i)
            print(line[0] + '   ' + line[5], line[6], line[7] + "  "
                  + file_name + "     " + file_type)


def create_dir(ftp):
    """Creates new directory"""
    new_mkdir = input("Enter the new directory name: ")
    try:
        ftp.mkd(new_mkdir)
        print('Directory Created')
        return 1
    except ftplib.error_perm:
        print('You do not have write permission in this folder or this folder already exists')
        return 0
    except ftplib.error_temp:
        print('Connection Timeout, Enter your credentials again\n')
        credentials(ftp)


def remove_dir(ftp):
    """Creates new directory"""
    input_dir = input("Enter the new directory name: ")
    try:
        ftp.rmd(input_dir)
        print('Directory Removed')
        return 1
    except ftplib.error_perm:
        print('You do not have write permission in this'
              ' folder or this folder has already been removed')
        return 0
    except ftplib.error_temp:
        print('Connection Timeout, Enter your credentials again\n')
        credentials(ftp)


def delete_file(ftp):
    file_delete = input("Enter the filename to delete: ")
    try:
        ftp.delete(file_delete)
        print('\nFile Deleted\n')
    except ftplib.error_perm:
        print('Specified file does not exist or you do not have permission to delete it')
    except ftplib.error_temp:
        print('Connection Timeout, Enter your credentials again\n')
        credentials(ftp)
    except ftplib.all_errors:
        print('An unexpected error occurred\n')


def upload_file(ftp):
    print("Select file to be uploaded")
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    file_type = ""
    file = ""
    try:
        file = open(file_path, 'r')
        file.readlines()
        file_type = ftp.storlines
    except UnicodeDecodeError:
        file_type = ftp.storbinary
    except FileNotFoundError:
        print("\nFile not found\n")
        file_type = ""
        return 0
    finally:
        if file_type != "":
            file.close()
            file = open(file_path, 'rb')
            file_name = os.path.basename(file_path)
            try:
                file_type(f"STOR {file_name}", file)
                print("\nUploaded Successfully\n")
                file.close()
                return 1
            except ftplib.error_perm:
                print('\nYou dont have permission to create a file in this directory\n')
                file.close()
                return 0
        else:
            return 0


def download_file():
    """Performs all tasks required for a successful download from the ftp server"""
    file_download = input('Enter the filename to be downloaded: ') 

    pass


def router():
    """Performs all tasks required for a successful upload to the ftp server"""
    ftp = set_ftp()
    if isinstance(ftp, ftplib.FTP):
        credentials(ftp)
        done = 0
        option = 0
        while not done:
            pwd(ftp)
            print("\n1 - Upload File, 2 - Download File, 3 - Change directory, 4 - New directory,")
            print("5 - Delete file, 6 - Remove directory, 7 - Refresh, 8 - Show Current Directory,  9 - Quit")
            print("(Enter a corresponding number)")
            while not option:
                option = input()
                try:
                    option = int(option)
                except ValueError:
                    print("Invalid Selection, Select a valid number from the options")
                    option = 0
            if option == 7:
                option = 0
                continue
            elif option == 8:
                print(get_dir_path(ftp))
                input("Press enter to continue")
                option = 0
            elif option == 3:
                change_attempt = 0
                while change_attempt < 3:
                    if change_dir(ftp):
                        break
                    else:
                        change_attempt += 1
                if change_attempt == 3:
                    print("Failed, Enter the path again")
                option = 0
            elif option == 4:
                create_dir(ftp)
                option = 0
            elif option == 6:
                remove_dir(ftp)
                option = 0
            elif option == 5:
                delete_file(ftp)
                option = 0
            elif option == 1:
                upload_file(ftp)
                option = 0
            elif option == 9:
                ftp.quit()
                sys.exit()
            else:
                print('Invalid choice')
                option = 0

    else:
        print(ftp)
        main.run()
