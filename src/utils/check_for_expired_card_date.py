import datetime


def is_expired(exp_date):
    try:
        # Parse the expiration date in the format MM/YY
        expiration_date_obj = datetime.datetime.strptime(exp_date, "%m/%y").date()
        current_date = datetime.date.today()

        # Compare the expiration date with the current date
        return expiration_date_obj < current_date
    except ValueError:
        # Handle invalid date format (e.g., if exp_date is not in the expected format)
        print("Invalid date format. Please provide a valid date (MM-YY).")
        return False
