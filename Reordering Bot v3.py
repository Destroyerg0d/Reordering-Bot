import os
import logging
import time
from datetime import datetime
from selenium import webdriver
import csv
from selenium.webdriver.common.by import By
import logging
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By  # Add this line to import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Global array to store data dynamically
global_data_array = []

# Configure logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def create_undetectable_chrome_driver():
    logger.info("Creating an undetectable Chrome driver...")

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Add more options as needed based on your requirements

    driver = webdriver.Chrome(options=options)

    logger.info("Chrome driver created successfully.")
    return driver

def read_csv_file(file_path, start_row, total_rows):
    logger.info(f"Reading CSV file '{file_path}' starting from row {start_row} and collecting data up to {total_rows} rows...")

    data = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        reader = csv.DictReader(file)
        for _ in range(start_row - 1):
            next(reader)  # Skip rows until the desired starting row

        for row in reader:
            data.append(row)
            if len(data) == total_rows:
                break  # Stop collecting data after reaching the specified total_rows

    logger.info(f"CSV file read and data collected successfully.")
    return data
def get_csv_file_path():
    logger.info("Getting the CSV file path interactively...")

    # Get the current working directory (root directory)
    root_directory = os.getcwd()

    # Ask the user for the CSV file name
    # file_name = input("Enter the CSV file name (including extension): ")
    file_name = "data.csv"
    # Construct the full path to the file
    file_path = os.path.join(root_directory, file_name)

    logger.info(f"CSV file path set to: {file_path}")
    return file_path

def get_start_row():
    logger.info("Getting the starting row interactively...")

    # Ask the user for the starting row
    start_row = input("Enter the row number to start scraping from (default is 1): ")

    # Use default value if the user does not provide input
    start_row = int(start_row) if start_row.strip() else 1

    logger.info(f"Starting row set to: {start_row}")
    return start_row

def get_total_rows():
    logger.info("Getting the total number of rows to collect data from interactively...")

    # Ask the user for the total number of rows
    total_rows = input("Enter the total number of rows to collect data from (default is all): ")

    # Use default value if the user does not provide input
    total_rows = int(total_rows) if total_rows.strip() else None

    logger.info(f"Total number of rows set to: {total_rows}")
    return total_rows

def collect_data_from_csv():
    # Get the CSV file path interactively
    csv_file_path = get_csv_file_path()

    # Get the starting row interactively
    start_row = get_start_row()

    # Get the total number of rows to collect data from interactively
    total_rows = get_total_rows()

    # Check if the file exists
    if not os.path.isfile(csv_file_path):
        logger.error(f"The file '{csv_file_path}' does not exist.")
        return  # Exit the function

    # Collect data from the CSV file
    global_data_array.extend(read_csv_file(csv_file_path, start_row, total_rows))

    logger.info("Data collected from CSV:")
    print(global_data_array)


def process_orders_with_exceptions(orders_with_exceptions, data_array):
    logger.info("Processing orders with exceptions...")

    # Check if there are any orders with exceptions
    if not orders_with_exceptions:
        logger.info("No orders with exceptions to process.")
        return

    # Create a Chrome driver
    driver = create_undetectable_chrome_driver()

    try:
        # Process each order ID in the list
        for order_id in orders_with_exceptions:
            try:
                # Find the corresponding data entry for this order ID
                matching_data_entry = next((entry for entry in data_array if entry.get('Name', '') == order_id), None)

                if matching_data_entry:
                    print(f"Processing order with exception: {order_id}")
                    # Extract variables from the data entry
                    lname = matching_data_entry.get('Shipping Name', '')
                    phone_number = matching_data_entry.get('Billing Phone', '')
                    address1 = matching_data_entry.get('Shipping Address1', '')
                    address2 = matching_data_entry.get('Shipping Address2', '')
                    city_name = matching_data_entry.get('Shipping City', '')
                    state_name = matching_data_entry.get('Shipping Province Name', '')
                    pin_code = matching_data_entry.get('Shipping Zip', '')

                    # Perform the processing actions for this order ID here
                    # Example: Open the website and fill out the form
                    website_url = 'https://example.com/'  # Replace with the actual website URL
                    driver.get(website_url)

                    # Fill out the form fields, click buttons, etc.

                    # Wait for the order to be placed (if applicable)
                    # Add appropriate wait conditions here

                    # Print a message indicating successful processing
                    print(f"Order {order_id} processed successfully.")

            except Exception as e:
                # Log the exception and continue to the next order
                logger.error(f"Error processing order {order_id}: {str(e)}")
                continue

    except Exception as e:
        # Log the exception and handle it as needed
        logger.error(f"Unexpected exception: {str(e)}")
    finally:
        # Close the driver when done
        driver.quit()
        logger.info("Chrome driver closed.")

    logger.info("Processing of orders with exceptions completed.")

def execute_process():
    logger.info("Executing process on collected data...")

    # Check if there is any data collected
    if not global_data_array:
        logger.warning("No data available. Please collect data before executing the process.")
        return

    # Create a Chrome driver
    driver = create_undetectable_chrome_driver()

    # Initialize a list to store order IDs with errors
    orders_with_exceptions = []

    start_time = time.time()
    print("Time before loop:", start_time)

    # Get the current date and time
    current_datetime = datetime.now()


    try:
        # Process each entry in the collected data
        for i, person_data in enumerate(global_data_array):
            try:
                print(f"Iteration {i + 1}")
                # Extract variables from the collected data
                orderid = person_data.get('Name', '')
                lname = person_data.get('Shipping Name', '')
                phone_number = person_data.get('Billing Phone', '')
                address1 = person_data.get('Shipping Address1', '')
                address2 = person_data.get('Shipping Address2', '')
                city_name = person_data.get('Shipping City', '')
                state_name = person_data.get('Shipping Province Name', '')
                pin_code = person_data.get('Shipping Zip', '')


                print('Order for : ' + lname + ' '+ phone_number + ' '+ address1 + ' '+ address2 +  ' '+ city_name +  ' '+ state_name + ' '+ pin_code)
                # Open the website (you might want to move this inside the loop if you want to open a different website for each row)
                website_url = 'https://55d71b-8d.myshopify.com/products/monex-new-latest-black-gold-shoes-for-mens'
                driver.get(website_url)

                # time.sleep(5)
                #
                # buy_now_button = driver.find_element(By.XPATH, "//div[@id='es-popup-button']")
                # buy_now_button.click()
                # buy_now_button = driver.find_element(By.XPATH, "//div[@class='product-form__buttons']")
                # buy_now_button.click()

                time.sleep(1)
                #
                # buy_now_button = driver.find_element(By.XPATH, "//div[@class='product-form__buttons']")
                # buy_now_button.click()
                #Loop to find COD button
                while True:
                    try:
                        buy_now_button = driver.find_element(By.XPATH, "//div[@class='product-form__buttons']")
                        buy_now_button.click()
                        break  # Exit the loop if the button is found and clicked successfully
                    except NoSuchElementException:
                        # If the button is not found, wait for a short time and try again
                        time.sleep(1)
                    except ElementClickInterceptedException:
                        # If the button is found but unable to be clicked due to an overlay, wait and try again
                        time.sleep(1)

                # name_fill = driver.find_element(By.XPATH, "//input[@id='es-first_name']")
                # name_fill.send_keys(f'{fname}')


                name_fill = driver.find_element(By.XPATH, "//input[@id='es-last_name']")
                name_fill.send_keys(f'{lname}')

                phone_number_fill = driver.find_element(By.XPATH, "//input[@id='es-phone']")
                phone_number_fill.send_keys(f'{phone_number}')

                address_fill = driver.find_element(By.XPATH, "//input[@id='es-address']")
                address_fill.send_keys(f'{address1}')

                address_fill1 = driver.find_element(By.XPATH, "//input[@id='es-address2']")
                address_fill1.send_keys(f'{address2}')

                city_name_fill = driver.find_element(By.XPATH, "//input[@id='es-city']")
                city_name_fill.send_keys(f'{city_name}')

                pin_code_fill = driver.find_element(By.XPATH, "//input[@id='es-zip']")
                pin_code_fill.send_keys(f'{pin_code}')

                time.sleep(1)

                state_name_fill = driver.find_element(By.XPATH, "//select[@id='es-province']")
                state_name_fill.click()
                state_select = Select(state_name_fill)
                state_select.select_by_visible_text(f'{state_name}')

                time.sleep(1)

                while True:
                    try:
                        submit_button = driver.find_element(By.XPATH, "//button[@id='es-form-button']")
                        submit_button.click()
                        break  # Exit the loop if the button is found and clicked successfully
                    except NoSuchElementException:
                        # If the button is not found, wait for a short time and try again
                        time.sleep(1)

                time.sleep(3)
                a = 1
                while True:
                    try:
                        order_no1 = driver.find_element(By.XPATH, "//span[@class='os-order-number']")
                        order_no = order_no1.text
                        print(order_no + ' : Reordered for : ' + orderid + ' ' + lname)
                        break  # Exit the loop if the button is found and clicked successfully
                    except NoSuchElementException:
                        # If the button is not found, wait for a short time and try again
                        a=a+1
                        if a > 10:
                            print("------------Wasted 10 Sec Time on fetching Order ID probably done------------")
                            print("------------Possible ERROR in ORDER :  " + orderid)
                            orders_with_exceptions.append(orderid)
                            break
                        time.sleep(1)
                    except ElementClickInterceptedException:
                        # If the button is found but unable to be clicked due to an overlay, wait and try again
                        time.sleep(1)
            except Exception as e:
                # Log the exception and continue to the next iteration
                logger.error(f"Maybe Failure in Order {i + 1}: {str(e)} : " + orderid)
                orders_with_exceptions.append(orderid)
                continue

    except Exception as e:
        # Log the exception and handle it as needed
        logger.error(f"Unexpected exception : {str(e)}")
    finally:
        # Close the driver when done
        driver.quit()
        logger.info("Chrome driver closed.")

    if orders_with_exceptions:
        logger.info("Orders with exceptions:")
        for order_id in orders_with_exceptions:
            print(order_id)


    # Print the current date and time
    print("Before Loop date and time:", current_datetime)
    # Get the current date and time
    current_datetime = datetime.now()

    # Print the current date and time
    print("After Loop date and time:", current_datetime)

    end_time = time.time()

    time_difference_seconds = end_time - start_time
    time_difference_hours = time_difference_seconds / 3600

    # Output the time before and after loop, and the difference

    print("Time difference:", time_difference_seconds, "seconds")
    print("Time difference:", time_difference_hours, "hours")

    logger.info("Process executed successfully.")

def main():
    # Set up logging
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

    logger.info("Starting the script...")

    while True:
        # Display menu options
        print("\nOptions:")
        print("1. Collect data from CSV")
        print("2. Execute process on collected data")
        print("0. Exit")

        # Ask the user for option input
        option = input("Enter option (0/1/2): ")

        if option == '0':
            break  # Exit the loop and end the program
        elif option == '1':
            # Collect data from the CSV file
            collect_data_from_csv()
        elif option == '2':
            # Execute the process on the collected data
            execute_process()
        else:
            logger.warning("Invalid option. Please enter a valid option.")

    logger.info("Script completed successfully.")

if __name__ == "__main__":
    main()
