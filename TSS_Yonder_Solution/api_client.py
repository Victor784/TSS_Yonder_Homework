import requests
from datetime import datetime

# Data class so that json values from the API can be converted and used inside the app
class License:
    def __init__(self, id, name, surname, category, issue_date, expiration_date, suspended):
        self.id = id
        self.name = name
        self.surname = surname
        self.category = category
        self.issue_date = datetime.strptime(issue_date, "%d/%m/%Y").date()  # Convert string to datetime.date
        self.expiration_date = datetime.strptime(expiration_date, "%d/%m/%Y").date()  # Convert string to datetime.date
        self.suspended = suspended

    #function for string representation of the data class
    def __repr__(self):
        return f"License(id={self.id}, name={self.name}, surname={self.surname}, category={self.category}, issue_date={self.issue_date}, expiration_date={self.expiration_date}, suspended={self.suspended})"

    #function needed for adding the entries to the excel
    def to_list(self):
        return [ self.name, self.surname, self.category, self.issue_date, self.expiration_date, 'DA' if self.suspended else 'NU']

class APIClient:
    def __init__(self):
        self.licenses = self.retrieve_data_points()

    def get_data_from_api(self):
        # Function to call the API endpoint and retrieve data
        url = "http://localhost:30000/drivers-licenses/list"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data from API:", response.status_code)
            return None

    def retrieve_data_points(self):
        # Function to retrieve data points from API and accumulate them in a list
        data_points = []
        for _ in range(5):  # Repeat 5 times as the API call only returns 30 entries and we need 150
            data = self.get_data_from_api()
            if data:
                data_points.extend(data)  # Append retrieved data to the list
        
        # Convert data points to License objects
        licenses = []
        for entry in data_points:
            license = License(
                id=entry['id'],
                name=entry['nume'],
                surname=entry['prenume'],
                category=entry['categorie'],
                issue_date=entry['dataDeEmitere'],
                expiration_date=entry['dataDeExpirare'],
                suspended=entry['suspendat']
            )
            licenses.append(license)
        
        return licenses
