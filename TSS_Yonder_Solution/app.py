from api_client import APIClient
from excel_creator import *
import datetime
from collections import defaultdict

#Menu display
def display_menu():
    print("Welcome to the License Management System")
    print("Choose an option:")
    print("1. List suspended licenses")
    print("2. Extract valid licenses issued until today's date")
    print("3. Find licenses based on category")
    print("0. Exit")


# Function for Requested feature 1 
def create_excel_suspended_licenses(licenses):
    # Filter suspended licenses
    suspended_licenses = [license for license in licenses if license.suspended]
    formatted_licenses = [license.to_list() for license in suspended_licenses]
    # Create Excel file for suspended licenses
    header_row = ["Nume", "Prenume", "Categorie", "Data de emitere", "Data de expirare", "Suspendat"]
    file_path = "Licente_suspendate.xlsx"
    excel_creator = ExcelCreator()
    excel_creator.create_excel(header_row, formatted_licenses, file_path)

# Function for Requested feature 2
def create_excel_find_valid_licenses(licenses):
    # Get today's date
    today = datetime.date.today()
    # Filter valid licenses (not expired)
    valid_licenses = [license for license in licenses if license.expiration_date > today and license.issue_date < today]
    
    formatted_licenses = [license.to_list() for license in valid_licenses]

    header_row = ["Nume", "Prenume", "Categorie", "Data de emitere", "Data de expirare", "Suspendat"]
    file_path = "Licente_valide.xlsx"
    excel_creator = ExcelCreator()
    excel_creator.create_excel(header_row, formatted_licenses, file_path)

# Function for Requested feature 3
def create_license_frequency_excel(licenses):
    # Use defaultdict to count license frequencies
    license_counts = defaultdict(int)
    for license in licenses:
        license_counts[license.category] += 1

    # Convert defaultdict to list of tuples
    formatted_license_counts = [(category, count) for category, count in license_counts.items()]

    # Create Excel file for license frequencies
    header_row = ["Categorie", "Numar de licente"]
    file_path = "Numar_de_licente_pe_categorii.xlsx"
    excel_creator = ExcelCreator()
    excel_creator.create_excel(header_row, formatted_license_counts, file_path)

def run():
    # Create an instance of APIClient
    api_client = APIClient()
    
    # Access the list of licenses
    licenses = api_client.licenses

    #excel_creator = ExcelCreator()

    #header_row = ["Nume", "Prenume" , "Categorie" , "Data de emitere" , "Data de expirare" , "Suspendat"]
    #file_path = "my_excel_file.xlsx"
    
    #Formatting the licenses before adding them into the excel.
    

    #excel_creator.create_excel(header_row, formatted_licenses, file_path)

    print("Retrieved", len(licenses), "licenses.")
     
    while True:
        display_menu()
        choice = input("Enter your choice (1-3, 0 to quit): ")

        if choice == '1':
            print("Listing suspended licenses...")
            create_excel_suspended_licenses(licenses)
        elif choice == '2':
            print("Extracting valid licenses issued until today's date...")
            create_excel_find_valid_licenses(licenses)
        elif choice == '3':
            print("Finding licenses based on category and their count...")
            create_license_frequency_excel(licenses)
        elif choice == '0':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")