
from klustr_widget import PostgreSQLCredential, PostgreSQLKlustRDAO
from klustr_utils import qimage_argb32_from_png_decoding, ndarray_from_qimage_argb32

class Model():
    def __init__(self):
        self.credential = PostgreSQLCredential(host='localhost', port=5432, database='postgres', user='postgres', password='AAAaaa123')
        self.dao = PostgreSQLKlustRDAO(self.credential)


    def get_dataset_names(self):
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
        

    def get_images_names_from_dataset(self, dataset_name):
        # Fetches images names from a specified dataset
        if self.dao.is_available:
            images = self.dao.image_from_dataset(dataset_name, False)
            if images:
                images_names = [row[3] for row in images]
                return images_names
            else:
                return  "No Datasets", "No datasets available in the database."
        else:
            return "Database Error", "Database connection is not available."    

    def get_image_from_image_name(self, image_name):
        if self.dao.is_available:
            image = self.dao.image_from_image(image_name)
            if image:
                image_data = image[0][0]
                qimage = qimage_argb32_from_png_decoding(image_data) 
                return qimage
            else:
                return  "No Images", "No images available in the database."
        else:
            return "Database Error", "Database connection is not available."    



    def get_category_count(self, dataset_name):
        if self.dao.is_available:
            query = self.dao.label_count_from_dataset(dataset_name)
            return query[0][0]
        
    def get_training_image_count(self, dataset_name):
        if self.dao.is_available:
            query = self.dao.label_count_from_dataset()
            return query[0][0]


    def analyse_data(self):
        pass
    def perimeter(self):
        pass
    def area(self):
        pass
    def centroid(self):
        pass

    # En test
    def compactness(self):
        import numpy as np
        import sys
        # np.set_printoptions(threshold=sys.maxsize)
        sql_result = self.dao.image_from_label(1)
        sql_image_id = sql_result[0][2]
        sql_image_result = self.dao._execute_simple_query('SELECT * FROM klustr.image WHERE id=%s;', (sql_image_id,))
        sql_image = sql_image_result[0][3]
        image = qimage_argb32_from_png_decoding(sql_image)
        np_image = ndarray_from_qimage_argb32(image)
        print(np_image)
    
    def circle_ratio(self):
        pass
    def inner_circle_ratio(self):
        pass
    def area(self):
        pass
