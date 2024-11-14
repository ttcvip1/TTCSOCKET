import time
import random
import requests
from datetime import datetime, timedelta

# Sample hardcoded credentials (for demonstration purposes)
valid_username = "@TitanicTradingCommunity"
valid_password = "@ttcvip"

# Function to convert time string to datetime object
def str_to_time(time_str):
    try:
        return datetime.strptime(time_str, "%H:%M")
    except ValueError:
        print(f"Invalid time format: {time_str}. Please use HH:MM format.")
        return None

# Function to fetch signal data using the provided API
def fetch_signal(pair, time_value):
    url = "https://api.planalto.cc/quotex"
    params = {"pair": pair, "time": time_value, "key": "planalto-lifetime"}
    headers = {"User-Agent": "Mozilla/5.0"}

    # Print a message indicating that signals are being fetched (but hide the API details)
    print("Signals generating, please wait...")

    try:
        response = requests.get(url, params=params, headers=headers)

        # If the API returns a successful response (status code 200)
        if response.status_code == 200:
            try:
                data = response.json()  # Try parsing the JSON response
                if data['status'] == 'success':
                    return data['data']  # Return the signal data (direcao, o, c, etc.)
                else:
                    print("Error: API returned failure status.")
                    return None
            except ValueError:
                print("Error parsing the response JSON.")
                return None
        else:
            print(f"Error: Received status code {response.status_code}.")
            return None
    except requests.exceptions.RequestException as e:
        # If there's a problem with the request (network issue, etc.)
        print(f"Request failed: {e}")
        return None

# Function to adjust time to UTC +6
def adjust_to_utc_plus_6(current_time):
    return current_time + timedelta(hours=6)

# Function to generate signals based on the API response and time
def generate_signals(start_time_str, end_time_str, pair):
    start_time = str_to_time(start_time_str)
    end_time = str_to_time(end_time_str)

    # Validate time input
    if not start_time or not end_time:
        return []

    if start_time >= end_time:
        print("Error: Start time must be before End time.")
        return []

    signals = []
    current_time = start_time

    # Adjust times to UTC +6
    start_time = adjust_to_utc_plus_6(start_time)
    end_time = adjust_to_utc_plus_6(end_time)

    # Calculate the total duration in seconds
    total_duration = (end_time - start_time).total_seconds()

    # Define a reasonable interval in seconds (for example, 5 minutes)
    interval = 300  # Example: 5 minutes between signals (300 seconds)

    # Calculate how many signals we need
    signal_count = int(total_duration / interval)  # Signal count based on the interval

    # Fetch signal data for the pair
    data = fetch_signal(pair, start_time_str)
    if not data:
        print("Error: No data received from API.")
        return []

    # Signal options (randomize the signal to avoid always the same pattern)
    signal_options = ['call', 'put']

    # Generate signals based on the API response (using 'direcao' field)
    for i in range(signal_count):
        if i < len(data):
            signal_data = data[i]
            
            # Randomize the interval between each signal
            dynamic_interval = random.randint(100, 600)  # Random interval between 1 minute to 10 minutes (100-600 seconds)
            signal = random.choice(signal_options)  # Randomly choose between 'call' and 'put'
            
            # Increment the time by the randomized interval
            current_time += timedelta(seconds=dynamic_interval)
            
            signals.append(f"{current_time.strftime('%H:%M')} - {pair} - {signal}")
        else:
            break  # If the number of data points is less than signal_count, stop generating signals

    return signals

# Function to handle login
def login():
    print("Please login to continue...")
    username = input("Username: ")
    password = input("Password: ")

    print("Verifying, please wait...")

    # Simulating a small delay for the verification
    time.sleep(2)

    if username == valid_username and password == valid_password:
        print("Login successful!")
        return True
    else:
        print("Invalid username or password. Please try again.")
        return False

# Main function to simulate the software
def run_software():
    print("         T       T         C")
    time.sleep(1)  # Simulate delay for loading screen

    # Handle user login
    if not login():
        return  # Exit the software if login fails

    # Set start time automatically to utc +6 time
    start_time = datetime.now().strftime("%H:%M")
    print(f"Start Time (Automatic): {start_time}")

    # Input End Time
    end_time = input("Enter End Time (HH:MM): ")

    # Input pair (currency pair)
    pair = input("Enter the currency pair (e.g., USDINR_otc): ")

    # Generate the desired number of signals automatically
    signals = generate_signals(start_time, end_time, pair)

    if signals:
        print("\nGenerated Signals; TIMEZONE : UTC/GMT +6:00:")
        for signal in signals:
            print(signal)
    else:
        print("No signals generated.")

if __name__ == "__main__":
    run_software()
