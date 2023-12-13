from termcolors import Bcolors


def handle_command(uinp):
    if uinp == "command":
        pass
    elif uinp == "create-account":
        pass
    elif uinp == "login":
        pass
    elif uinp == "sync":
        pass
    elif uinp == "list-emails":
        pass
    elif uinp == "send":
        pass
    elif uinp == "clear-inbox":
        pass
    elif uinp == "exit":
        pass
    else:
        print(Bcolors.ERROR + "Invalid command" + Bcolors.ENDC)

def main():
    print("Welcome!")

    while True:
        uinp = input(Bcolors.BOLDPURPLE + "> " + Bcolors.ENDC)
        handle_command(uinp)


if __name__=='__main__':
    main()