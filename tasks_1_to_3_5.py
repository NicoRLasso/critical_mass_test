import os
import pandas as pd
import time
import math
import concurrent.futures
from datetime import datetime
from typing import List
# <---------| First Task Classes and Objects |--------->
print("---"*20)
print("Classes and Objects")
print("---"*20)


class Transaction:
    """
    Initializes a new instance of the Transaction class.
    :param amount: float, the amount of the transaction
    :param transaction_date: datetime, the date of the transaction
    :param currency: str, the currency of the transaction amount
    """

    def __init__(self, amount: float, transaction_date: datetime, currency: str):
        self.amount = amount
        self.transaction_date = transaction_date
        self.currency = currency

    def display_details(self) -> None:
        """
        Prints the details of the transaction including amount, currency, and date.
        """
        print(f"Amount: {self.amount} {self.currency}")
        print(f"Transaction Date: {self.transaction_date}")


transaction1 = Transaction(
    150.50, datetime.strptime('2024-05-07', '%Y-%m-%d'), 'USD')
transaction2 = Transaction(
    2000, datetime.strptime('2024-04-25', '%Y-%m-%d'), 'EUR')
transaction3 = Transaction(
    340.75, datetime.strptime('2024-05-06', '%Y-%m-%d'), 'JPY')

transaction1.display_details()
transaction2.display_details()
transaction3.display_details()

# <---------| End First Task  |--------->

# <---------| Second task Parallelization |--------->


def compute_factorial(number: int) -> str:
    """
    Function to compute the factorial of a given number.
    """
    return f"Factorial of {number} is {math.factorial(number)}"


def main_process(numbers: List[int]) -> None:
    """
    Using ThreadPoolExecutor to run factorial calculations in parallel,
    Mapping the compute_factorial function to each number
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(compute_factorial, numbers)
        for result in results:
            print(result)


print("---"*20)
print("Parallelization")
print("---"*20)
main_process(range(1, 11))

# <---------| End Second task |--------->

# <---------| Third task Decorators |--------->
print("---"*20)
print("Decorators")
print("---"*20)


def log_execution_time(func):
    """
    Decorator that logs the execution time of the function it decorates.
    """
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"{func.__name__} executed in {
              end_time - start_time:.4f} seconds")
        return result
    return wrapper


@log_execution_time
def sum_numbers(n):
    """
    Function to compute the sum of numbers from 1 to n.
    """
    return sum(range(1, n + 1))


total = sum_numbers(1000000)
print(f"The sum of numbers from 1 to 1000000 is {total}")


# <---------| End Third task |--------->

# <---------| Fifth task DataFrames |--------->
print("---"*20)
print("DataFrames")
print("---"*20)


def initialize_csv(file_path: str) -> None:
    """
    Ensures that the CSV file exists and has the initial structure. If not,
    it creates the file and populates it with an empty DataFrame with specified columns.
    """
    columns = ['transaction_id', 'amount', 'transaction_date', 'currency']

    if not os.path.exists(file_path):
        print("CSV file does not exist. Creating and initializing.")
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)
    else:
        print("CSV file exists.")


def load_transactions(file_path: str) -> pd.DataFrame:
    """
    Loads transaction data from a CSV file into a DataFrame.
    """
    try:
        return pd.read_csv(file_path, parse_dates=['transaction_date'])
    except Exception as e:
        print(f"Error loading data: {e}")
        raise


def add_transaction(df: pd.DataFrame, file_path: str, transaction_id: int, amount: float, transaction_date: str, currency: str) -> pd.DataFrame:
    """
    Adds a new transaction to the DataFrame, saves the updated DataFrame to a CSV file,
    and returns the updated DataFrame.    
    """
    try:
        data_types = {
            'transaction_id': int,
            'amount': float,
            'transaction_date': 'datetime64[ns]',
            'currency': str
        }
        new_data = {
            'transaction_id': [transaction_id],
            'amount': [amount],
            'transaction_date': [pd.to_datetime(transaction_date)],
            'currency': [currency]
        }
        new_df = pd.DataFrame(new_data)
        new_df = new_df.astype(data_types)
        updated_df = pd.concat([df, new_df], ignore_index=True)
        updated_df.to_csv(file_path, index=False)
        print("Transaction added and data saved to CSV.")
        return updated_df
    except Exception as e:
        print(f"Error adding transaction and saving data: {e}")
        raise


def filter_by_currency(df:  pd.DataFrame, currency: str) -> pd.DataFrame:
    """
    Returns a DataFrame of transactions filtered by currency.
    """
    return df[df['currency'] == currency]


def calculate_total_in_date_range(df: pd.DataFrame, start_date: str, end_date: str) -> float:
    """
    Returns the total amount of transactions within a specified date range.
    """
    try:
        mask = (df['transaction_date'] >= pd.to_datetime(start_date)) & (
            df['transaction_date'] <= pd.to_datetime(end_date))
        return df.loc[mask, 'amount'].sum()
    except Exception as e:
        print(f"Error calculating total: {e}")
        raise


file_path = 'transactions.csv'

# Initialize and load data
initialize_csv(file_path)

# Load data
df = load_transactions('transactions.csv')

# Add a transaction
df = add_transaction(df, file_path, 101, 200.00, '2024-05-07', 'USD')

# Filter transactions by currency
filtered_df = filter_by_currency(df, 'USD')
print("Filtered Transactions:")
print(filtered_df)

# Calculate the total amount for a date range
total_amount = calculate_total_in_date_range(
    df, '2024-01-01', '2024-12-31')
print(f"Total Amount in Range: {total_amount}")


# <---------| End Fifth task |--------->
