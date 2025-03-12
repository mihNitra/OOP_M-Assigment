"""
Library Management System - Login Module
----------------------------------------
Current Date and Time (UTC): 2025-03-12 02:32:02
Current User's Login: CenJi03
"""

import csv
import logging
import datetime
import os
import socket

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging settings
logging.basicConfig(filename='logs/login.log', 
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# Get the hostname and IP address of the machine
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

def get_local_ip():
    """Retrieve the local IP address of the computer."""
    try:
        # Create a socket connection to a remote server (doesn't actually send data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google's public DNS server
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        logging.error(f"Failed to retrieve IP address: {e}")
        return "Unknown IP"

def login(username, password):
    """Authenticate the user using credentials from a CSV file."""
    with open("UserInfo/UserAccounts.csv", newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if username == row[0] and password == row[1]:
                return True
    return False

def log_login_success(username):
    """Log a successful login attempt."""
    ip_address = get_local_ip()
    greeting = f"Login Successful, Welcome {username}!"
    log_message = (
        f"Login Successful\n"
        f"  Greeting\t\t: {greeting}\n"
        f"  Account\t\t\t: {username}\n"
        f"  IP Address\t: {ip_address}\n"
        f"  Timestamp\t\t: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )
    logging.info(log_message)
    print(greeting)

def log_login_failure(username):
    """Log a failed login attempt."""
    ip_address = get_local_ip()
    error_message = "Login Failed, Please Try Again!"
    log_message = (
        f"Login Failed\n"
        f"  Error\t\t\t\t: {error_message}\n"
        f"  Account\t\t\t: {username}\n"
        f"  IP Address\t: {ip_address}\n"
        f"  Timestamp\t\t: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )
    logging.warning(log_message)
    print(error_message)

def authenticate_user():
    """Handle the user authentication process and return success status and username"""
    max_attempts = 3
    attempt = 0
    
    while attempt < max_attempts:
        print('======================================================= LOGIN SYSTEM ========================================================')
        username = input("- Enter Username\t.\t.\t.\t.\t.\t: ")
        password = input("- Enter Password\t.\t.\t.\t.\t.\t: ")
        print('\t')
        
        # Authenticate the user
        if login(username, password):
            log_login_success(username)
            return True, username
        else:
            attempt += 1
            log_login_failure(username)
            remaining = max_attempts - attempt
            if remaining > 0:
                print(f"Login failed. {remaining} attempts remaining.")
            else:
                print("Maximum login attempts exceeded. Access denied.")
                
    return False, None