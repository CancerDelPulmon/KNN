
from klustr_widget import PostgreSQLCredential, PostgreSQLKlustRDAO

class Model():
    def __init__(self):
        credential = PostgreSQLCredential(host='localhost', port=5432, database='postgres', user='postgres', password='AAAaaa123')
        self.dao = PostgreSQLKlustRDAO(credential)
    @staticmethod
    def getNames(self):
        # Fetch dataset names from PostgreSQL and add them to the ComboBox
        if self.dao.is_available:
            datasets = self.dao.available_datasets
            if datasets:
                dataset_names = [row[1] for row in datasets]
                return dataset_names
            else:
                return  "No Datasets", "No datasets available in the database."
        else:
            return "Database Error", "Database connection is not available."
    def analyse_data(self):
        pass
    def perimeter(self):
        pass
    def area(self):
        pass
    def centroid(self):
        pass
    def compactness(self):
        pass
    def circle_ratio(self):
        pass
    def inner_circle_ratio(self):
        pass
    def area(self):
        pass
