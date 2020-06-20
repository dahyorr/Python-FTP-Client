"""******************************************************************
   *     FTP Client                                                 *
   *     Upload/Download files to/from a ftp server                 *
   *                                                                *
   ******************************************************************"""
import pkgs


def run():
    operation = 0
    while not operation:
        pkgs.print_intro()
        operation = input()
        operation = pkgs.check_input(operation.strip())
    operation()


if __name__ == '__main__':
    print("""******************************************************************
    *     FTP Client                                                 *
    *     Upload/Download files to/from a ftp server                 *
    *     Written By Dayo Adebanjo                                   *
    ******************************************************************""")
    run()
