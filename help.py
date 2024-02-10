import sys

def help():
    if(len(sys.argv) == 2):
        print("Bhavu - A Version Control System")
        print("--------------------------------- \n")
        print("Usage: bhavu <command> [<args>]\n")

        print("The most commonly used bhavu commands are:")
        print("\n start a working area: \n")
        print("  bhavu init                - Initialize a new bhavu repository")
        print("\n working on the current change: \n")
        print("  bhavu add <file>          - Add a file to the index")
        print("  bhavu rmadd <file>        - remove a file from the index")
        print("\n examine the history and state: \n")
        print("  bhavu log                 - Display commit log")
        print("  bhavu status              - to see status")
        print("\n grow, mark, tweak your common history: \n")
        print("  bhavu commit -m <message> - Commit changes with a message")
        print("  bhavu rmcommit            - remove last commit")
        print("  bhavu checkout <commit>   - Checkout a specific commit")
        print("\n User options: \n")
        print("  bhavu user show           - to see present user")
        print("  bhavu user set <username> - to change user")
        print("\n collaborate: \n")
        print("  bhavu push <path>         - to push your file to another folder")
        print("\n Help: \n")
        print("  bhavu help                - to see this usage help")
        print("---------------------------------")
        print("Created by - Bhavya Shah")
        print("---------------------------------")

    elif len(sys.argv) == 3:
        if sys.argv[2] == "init":
            print("Usage:")
            print("  bhavu init                - Initialize a new bhavu repository")
        elif sys.argv[2] == "add":
            print("Usage:")
            print("  bhavu add <file>          - Add a file to the index")
        elif sys.argv[2] == "commit":
            print("Usage:")
            print("  bhavu commit -m <message> - Commit changes with a message")
        elif sys.argv[2] == "rmadd":
            print("Usage:")
            print("  bhavu rmadd <file>        - remove a file from the index")
        elif sys.argv[2] == "rmcommit":
            print("Usage:")
            print("  bhavu rmcommit            - remove last commit")
        elif sys.argv[2] == "log":
            print("Usage:")
            print("  bhavu log                 - Display commit log")
        elif sys.argv[2] == "checkout":
            print("Usage:")
            print("  bhavu checkout <commit>   - Checkout a specific commit")
        elif sys.argv[2] == "status":
            print("Usage:")
            print("  bhavu status              - to see status")
        elif sys.argv[2] == "user":
            print("Usage:")
            print("  bhavu user show           - to see present user")
            print("  bhavu user set <username> - to change user")
        elif sys.argv[2] == "push":
            print("Usage:")
            print("  bhavu push <path>         - to push your file to another folder")
        else:
            print("Invalid argument")
            print("Usage: ")
            print("  bhavu help                - to see this usage help")
    else:
        print("Invalid number of arguments")
        print("Usage:")
        print("  bhavu help                - to see this usage help")


