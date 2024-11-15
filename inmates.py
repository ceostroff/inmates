import csv
import requests
from bs4 import BeautifulSoup
import time
import re

def get_employee_data():
    employee_data = []
    base_url = "https://directory.psc.gov/hhsdir/eeKey.asp?Key="
    page_no = 0
    existing_page_numbers = set()  

    try:
        with open('hhs_employee_directory.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    existing_page_numbers.add(int(row['page_no'])) 
                except (KeyError, ValueError):
                    pass 
    except FileNotFoundError:
        pass

    while True:
        try:
            page_no += 1
            print(f"Checking page: {page_no}")
            if page_no in existing_page_numbers:
                print(f"Page {page_no} already exists. Skipping.")
                continue  

            full_url = base_url + str(page_no)
            r = requests.get(full_url, timeout=10)  
            r.raise_for_status()  
            time.sleep(1)
            soup = BeautifulSoup(r.content, 'html.parser')

            data_elements = {}
            for label in ["Last name", "First name", "Agency", "Organization", "Job title", "E-mail"]:
                try:
                    element = soup.find(string=re.compile(label)).find_next()
                    data_elements[label.lower().replace(" ", "_")] = element.text.strip()
                except AttributeError:
                    data_elements[label.lower().replace(" ", "_")] = ""

            data_elements['page_no'] = page_no 

            employee_data.append(data_elements)
            print(data_elements)

        except requests.exceptions.RequestException as e:
            print(f"Network error on page {page_no}: {e}")
            break 
        except (AttributeError, Exception) as e:
            print(f"Error processing page {page_no}: {e}")
            break  


    return employee_data


def save_data(employee_data):
    filename = 'hhs_employee_directory.csv'
    fieldnames = ['page_no', 'last_name', 'first_name', 'agency', 'organization', 'job_title', 'email']
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:  #Add newline='' and encoding
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(employee_data)


if __name__ == "__main__":
    employee_data = get_employee_data()
    save_data(employee_data)
