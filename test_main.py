import time
import os

COMM_FILE = "communicator.txt"


def write_communicator(message):
    #Send message to communicator
    with open(COMM_FILE, "w") as f:
        f.write(message)


def read_communicator():
    #Read current message from communicator
    if not os.path.exists(COMM_FILE):
        return ""
    with open(COMM_FILE, "r") as f:
        return f.read().strip()


def wait_for_service_done():
    #Wait for service response
    while True:
        time.sleep(0.2)
        msg = read_communicator()

        if not msg:
            continue

        # PROMPT (input)
        if msg.startswith("PROMPT|"):
            content = msg.split("|", 1)[1]
            user_input = input(content + "\n> ")
            write_communicator(f"INPUT|{user_input}")

        # DISPLAY (no input)
        elif msg.startswith("DISPLAY|"):
            content = msg.split("|", 1)[1]
            print("\n" + content + "\n")
            write_communicator("")

        # DONE
        elif msg == "STATUS|DONE":
            print("\nOperation completed.\n")
            write_communicator("")
            return

        # CANCELLED
        elif msg == "STATUS|CANCELLED":
            print("\nOperation cancelled.\n")
            write_communicator("")
            return


def view_summary_flow():
    write_communicator("RUN_SUMMARY")
    wait_for_service_done()


def main():
    print("\nWelcome to BudgetApp\n")

    # Clear communicator on startup
    write_communicator("")

    def exit_app():
        print("\nGoodbye!\n")
        exit(0)

    # Map input options to functions    
    options = {
        # If option 1 picked run summary
        "1": view_summary_flow,
        "view monthly summary": view_summary_flow,
        "summary": view_summary_flow,

        # If option 2 picked run exit function
        "2": exit_app,
        "exit": exit_app,
    }

    while True:
        print("""
Home/Dashboard
________________________

1. View Monthly Summary
2. Exit
""")

        choice = input("Please select an option (number or name): ").strip().lower()

        action = options.get(choice)

        if action:
            action()
        else:
            print("\nInvalid selection.\n")


if __name__ == "__main__":
    main()
