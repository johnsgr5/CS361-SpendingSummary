import time
import os
from decimal import Decimal

# Files
COMM_FILE = "communicator.txt"
EXPENSE_FILE = "expenses.txt"
BUDGET_FILE = "budget.txt"
SUMMARY_FILE = "summary.txt"


def read_communicator():
    if not os.path.exists(COMM_FILE):
        return ""
    with open(COMM_FILE, "r") as f:
        return f.read().strip()


def write_communicator(message):
    with open(COMM_FILE, "w") as f:
        f.write(message)


def wait_for_input():
    """Wait for INPUT| message from main"""
    while True:
        time.sleep(0.2)
        msg = read_communicator()

        if msg.startswith("INPUT|"):
            user_input = msg.split("|", 1)[1].strip()
            write_communicator("")  # Clear after reading
            return user_input


def clear_summary_file():
    with open(SUMMARY_FILE, "w") as f:
        f.write("")


def load_expenses():
    expenses = {}

    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                amount_str, category, date_str = line.split(",")

                month = date_str.split("/")[0]
                year = date_str.split("/")[2]
                key = f"{month}/{year}"

                amount = Decimal(amount_str)

                if key not in expenses:
                    expenses[key] = {}

                expenses[key][category] = (
                    expenses[key].get(category, Decimal("0.00")) + amount
                )

    return expenses


def load_budgets():
    budgets = {}

    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                amount_str, category, period = line.split(",")

                if period != "monthly":
                    continue

                budgets[category] = Decimal(amount_str)

    return budgets


def format_money(value):
    return f"${value:.2f}"


def run_summary():
    clear_summary_file()

    # Ask user for month/year
    write_communicator("PROMPT|Enter the month and year for the spending summary [MM/YYYY]: ")
    month_year = wait_for_input()

    # Validate format MM/YYYY
    if len(month_year) != 7 or month_year[2] != "/":
        write_communicator("STATUS|CANCELLED")
        return

    month, year = month_year.split("/")
    key = f"{month}/{year}"

    expenses = load_expenses()
    budgets = load_budgets()

    categories_expenses = expenses.get(key, {})

    output_lines = []
    output_lines.append(f"Spending Summary for {key}")
    output_lines.append("________________________")

    if not categories_expenses:
        output_lines.append("No expenses recorded for this month.")
    else:
        # Sort by highest spending first
        sorted_categories = sorted(
            categories_expenses.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for category, spent in sorted_categories:
            budget = budgets.get(category, Decimal("0.00"))
            difference = spent - budget

            if budget == Decimal("0.00"):
                line = f"{category}: {format_money(spent)} | NO budget set"
            elif difference > 0:
                line = f"{category}: {format_money(spent)} | OVER budget by {format_money(difference)}"
            else:
                remaining = budget - spent
                line = f"{category}: {format_money(spent)} | WITHIN budget ({format_money(remaining)} remaining)"

            output_lines.append(line)

    output_text = "\n".join(output_lines)

    # Save to summary.txt
    with open(SUMMARY_FILE, "w") as f:
        f.write(output_text + "\n")

    # Send display message (no input expected)
    write_communicator("DISPLAY|" + output_text)

    # Small delay ensures main reads DISPLAY before DONE
    time.sleep(0.3)

    # Signal completion
    write_communicator("STATUS|DONE")


if __name__ == "__main__":
    clear_summary_file()

    while True:
        time.sleep(0.2)

        if read_communicator() == "RUN_SUMMARY":
            run_summary()