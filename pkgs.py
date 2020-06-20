"""******************************************************************
   *     FTP Client                                                 *
   *     Upload/Download files to/from a ftp server                 *
   *                                                                *
   ******************************************************************"""
import ftplib
import main


def print_intro():
    """Prints intro prompt for user to follow"""
    print("""What do you want to Do ?
    1. Upload
    2. Download
    3. Exit\n""")


def check_input(op):
    """Checks the text input by the user and returns the required function
    :arg op: Input value or string from user
    """
    op = op.lower()
    try:
        op = int(op)
    except ValueError:
        pass
    finally:
        if op == "upload" or op == 1:
            return upload
        elif op == "download" or op == 2:
            return download
        elif op == "exit" or op == 3:
            exit()
        else:
            print("Invalid Choice, Enter a valid number of choice")
            return 0


def credentials(ftp):
    from getpass import getpass
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
            tries = 0
        finally:
            if tries == 0:
                main.run()
                        
                        
def set_ftp(server):
    """Resolves the specified server address"""
    import socket
    try:
        if server != "":
            ftp = ftplib.FTP(server)
            return ftp
        else:
            return "\nEnter a valid server address\n"
    except TimeoutError:
        print("\nconnection attempt failed because the connected party did not properly respond after a period of time")
        return "connection timed out, check that you have the right address\n"
    except ConnectionRefusedError:
        print("\nNo connection could be made because the target machine actively refused it")
        return "connection was refused\n"
    except socket.gaierror:
        print("\nFailed to get address info ")
        return "Address Resolution Failure, check your address and try again\n"
    except:
        return "\nAn Unexpected error occ1urred\n"


def upload():
    """Performs all tasks required for a successful upload to the ftp server"""
    server = input("Enter the address you want to connect to: ")
    ftp = set_ftp(server.strip())

    if type(ftp) == ftplib.FTP:
        credentials(ftp)
        done = 0
        option = 0
        while not done:
            data = []
            try:
                ftp.dir(data.append)
            except ftplib.error_temp:
                print('Connection Timeout, Enter your credentials again\n')
                credentials(ftp)
            finally:
                print('Upload - Current Directory\n')
                print('Permissions                                Date           Name')
                for line in data:
                    print(line)
                print("\n1 - Select file to Upload, 2 - Change directory")
                print(" 3 - Make new directory, 4 - Delete file")
                print("(Enter a corresponding number)")
                input()
        ftp.quit()
    else:
        print(ftp)
        main.run()


def download():
    pass
