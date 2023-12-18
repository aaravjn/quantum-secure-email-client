from termcolors import Bcolors
import utils
import user_email


username = None
serverHost = None


def main():
    print("Welcome!")

    while True:
        uinp = input(Bcolors.BOLDPURPLE + "> " + Bcolors.ENDC)
        handle_command(uinp)


def handle_command(uinp):
    global username, serverHost

    if uinp == "help":
        utils.help()
    elif uinp == "create-account":
        utils.create_account(serverHost)
    elif uinp == "sync":
        user_email.sync_emails(username, serverHost)
    elif uinp == "list-emails":
        user_email.show_emails(username)
    elif uinp == "connect":
        serverHost = input("Please enter the host server domain: ")
    elif uinp == "compose":
        user_email.create_and_send_email(username, serverHost)
    elif uinp == "login":
        while True:
            login_username = input("Enter the username: ")
            if utils.handle_login(login_username):
                username = login_username
                break
            else:
                print(Bcolors.ERROR + "The account doesn't exist on the device" + Bcolors.ENDC)
    elif uinp == "clear-inbox":
        user_email.clearInbox(username, serverHost)
    elif uinp == "exit":
        print("Bye!")
        exit(0)
    else:
        print(Bcolors.ERROR + "Invalid command" + Bcolors.ENDC)


if __name__ == "__main__":
    main()
