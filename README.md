# CS361-SpendingSummary
The summary.py microservice is a service responsible for creating and displaying a monthly spending summary for the BudgetApp application. It operates independently from the main program and communicates through a shared text file called communicator.txt. 

When a user writes the command RUN_SUMMARY to this the text file to start the microservice. It prompts the user to enter a month and year in MM/YYYY format, then loads financial data from expenses.txt and budget.txt. The service calculates total spending per category for the selected month, compares each category’s spending against its corresponding monthly budget, and determines whether the user is within budget, over budget, or has no budget set (for each category). 

It formats these results into a small summary, saves the output to summary.txt, and sends the formatted text back to the “main program” for display. Once processing is complete, the microservice sends the output, followed by a “done” message. Also as added confirmation, the microservice prints its most recent summary into summary.txt


To request data the user must simply send “RUN_SUMMARY” into the communicator.txt with both the sender.py and summary.py active, as well as having data entries into expense.txt and budget.txt

An example request includes:

        def view_summary_flow():
            write_communicator("RUN_SUMMARY")
            wait_for_service_done()

Which sends 

RUN_SUMMARY

To communicator.txt, which is detected by 

        if read_communicator() == "RUN_SUMMARY":
            run_summary()

The microservice is also made to extract data from expense.txt and budget.txt. expense.txt should store data as

cost,category,XX/XX/XXXX

With the last portion representing a date as month, day, year, and a new line between each data entry. budget.txt will be similar with.

budget,category,monthly


Firstly the user program should continuously monitor communicator.txt for messages from the microservice. When the microservice has information to send, it writes messages with specific prefixes, such as PROMPT| to request user input, DISPLAY| to provide output for display, or STATUS|DONE to indicate that processing is complete. The client interprets these messages, prompting the user for input when required and sending responses back using INPUT| messages. Once the microservice writes a DISPLAY| message containing the summary, the client prints this output to the terminal. Finally, when the microservice writes STATUS|DONE, the client recognizes that the operation is finished, clears the communicator, and resumes normal operation. 


Rather, receiving data beings with the microservice sending a PROMPT|XXX to the user asking for the month and year, depicted as:

"PROMPT|Enter the month and year for the spending summary [MM/YYYY]: "

With the user responding with something like:

01/2026

In the terminal. This data should then be sent back through the text file using a call such as:


        if msg.startswith("PROMPT|"):
            content = msg.split("|", 1)[1]
            user_input = input(content + "\n> ")
            write_communicator(f"INPUT|{user_input}")

Rather, this example includes interpreting the PROMPT|XXX as a message, and then sending the month and year back as INPUT|XXX

Then the microservice collects and tabulates the data, outputting it as 

Spending Summary for 01/2026
________________________
car: $3000.00 | OVER budget by $250.00
groceries: $2000.00 | WITHIN budget ($500.00 remaining)

Which should be accepted by the client program using something like:


        elif msg.startswith("DISPLAY|"):
            content = msg.split("|", 1)[1]
            print("\n" + content + "\n")
            write_communicator("")

Finally, after sending the display message, the microservice send STATUS|DONE to relate to the client program that the microservice translation has been completed and the client program can move on. The code should look something like:


        elif msg == "STATUS|DONE":
            print("\nOperation completed.\n")
            write_communicator("")
            return


<img width="1902" height="1132" alt="image" src="https://github.com/user-attachments/assets/e84fc08e-4ca8-444d-9ef9-29eacdf9e24f" />
