"""
Library Management System - Main Module
"""

import os
import datetime
from login_system import authenticate_user
from library_system import manageLibrary

def display_header():
    """Display a welcome header for the application"""
    print("\n")
    print("=============================================================================================================================")
    print("                                            WELCOME TO LIBRARY MANAGEMENT SYSTEM")
    print("=============================================================================================================================")
    print("\n")

def display_user_info(username):
    """Display current date/time and logged in user"""
    # Get current UTC time using timezone-aware approach (avoiding deprecation warning)
    try:
        # For Python 3.11+ which has datetime.UTC
        current_time = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S')
    except AttributeError:
        # For older Python versions
        current_time = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        
    print(f"Current Date and Time\t.\t: {current_time}")
    print(f"Current User's Login\t.\t: {username}")

def main():
    """Main function that runs the application"""
    # Ensure required directories exist
    os.makedirs('UserInfo', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Check if user accounts file exists, if not create a sample one
    if not os.path.exists('UserInfo/UserAccounts.csv'):
        print("Creating sample user accounts file...")
        with open('UserInfo/UserAccounts.csv', 'w', newline='') as f:
            f.write("admin,admin\n")
        print("Sample user accounts created. You can use admin/admin123 to login.")
    
    display_header()
    
    # Authenticate the user first
    auth_successful, username = authenticate_user()
    
    if auth_successful:
        # Display user info but remove the "Access granted" message
        display_user_info(username)
        print("-" * 60)
        input("\nPress any key to continue to the Library Management System...\n")
        
        # If authentication is successful, proceed to library management
        manageLibrary()
    else:
        print("\nAccess denied. Please contact the system administrator.")

if __name__ == "__main__":
    main()   