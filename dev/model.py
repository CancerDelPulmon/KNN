
from klustr_widget import PostgreSQLCredential, PostgreSQLKlustRDAO
from klustr_utils import qimage_argb32_from_png_decoding, ndarray_from_qimage_argb32
import numpy as np

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
            image = self.dao.image_data_from_image(image_name)
            if image:
                image_data = image[0][0]
                qimage = qimage_argb32_from_png_decoding(image_data) 
                return qimage
            else:
                return  "No Images", "No images available in the database."
        else:
            return "Database Error", "Database connection is not available."  


    def get_images_data_from_dataset(self, dataset_name, training: bool = False):
        if self.dao.is_available:
            images = self.dao.image_from_dataset(dataset_name, training)
            if images:
                images_data = [row[6] for row in images]
                return images_data
            else:
                return  "No Datasets", "No datasets available in the database."
        else:
            return "Database Error", "Database connection is not available."
        
    def get_images_labels_from_dataset(self, dataset_name, training: bool = False):
        if self.dao.is_available:
            images = self.dao.image_from_dataset(dataset_name, training)
            if images:
                images_data = [row[1] for row in images]
                return images_data
            else:
                return  "No Datasets", "No datasets available in the database."
        else:
            return "Database Error", "Database connection is not available."    


    def get_translated_value(self, dataset_name):
        if self.dao.is_available:
            translated_value = self.dao.translated_from_dataset(dataset_name)
            if translated_value:
                return translated_value[0][0]
            else:
                return  "No Datasets", "No datasets available in the database."
        else:
            return "Database Error", "Database connection is not available."  
            

    def get_rotated_value(self, dataset_name):
        if self.dao.is_available:
            rotated_value = self.dao.rotated_from_dataset(dataset_name)
            if rotated_value:
                return rotated_value[0][0]
            else:
                return  "No Datasets", "No datasets available in the database."
        else:
            return "Database Error", "Database connection is not available."  


    def get_scaled_value(self, dataset_name):
        if self.dao.is_available:
            scaled_value = self.dao.scaled_from_dataset(dataset_name)
            if scaled_value:
                return scaled_value[0][0]
            else:
                return  "No Datasets", "No datasets available in the database."
        else:
            return "Database Error", "Database connection is not available."  



    def get_category_count(self, dataset_name):
        if self.dao.is_available:
            query = self.dao.label_count_from_dataset(dataset_name)
            return query[0][0]
        
    def get_image_count(self, dataset_name, training:bool):
        if self.dao.is_available:
            query = self.dao.image_count_from_dataset(dataset_name, training)
            return query[0][0]
        
    def get_total_image_count(self, dataset_name):
        if self.dao.is_available:
            query = self.dao.total_image_count_from_dataset(dataset_name)
            return query[0][0]


    def analyse_data(self, dataset_name, training : bool = False):
        images = self.get_images_data_from_dataset(dataset_name, training)
        labels = self.get_images_labels_from_dataset(dataset_name, training)
        images_points = []
        #anaylyser les images un par un
        for image_data in images:
            image = qimage_argb32_from_png_decoding(image_data)
            np_image = ndarray_from_qimage_argb32(image)
            np_image = 1 - np_image  # Invert the image

            perimeter = self.perimeter(np_image)
            area = self.area(np_image)
            centroid = self.centroid(np_image)
            outer_circle_radius = self.get_outer_circle_radius(np_image,centroid)
            inner_circle_radius = self.get_inner_circle_radius(np_image, centroid)
            compactness = self.compactness(area, perimeter)
            circle_ratio = self.circle_ratio(area, outer_circle_radius)
            inner_circle_ratio = self.inner_circle_ratio(inner_circle_radius, outer_circle_radius)
            # add point to array of all the points
            images_points.append((compactness, circle_ratio, inner_circle_ratio))
        return images_points, np.array(labels)
    
    def analyse_single_image(self, np_image):
        #calculate points for a single image
        np_image = 1 - np_image  # Invert the image
        perimeter = self.perimeter(np_image)
        area = self.area(np_image)
        centroid = self.centroid(np_image)
        outer_circle_radius = self.get_outer_circle_radius(np_image,centroid)
        inner_circle_radius = self.get_inner_circle_radius(np_image, centroid)
        compactness = self.compactness(area, perimeter)
        circle_ratio = self.circle_ratio(area, outer_circle_radius)
        inner_circle_ratio = self.inner_circle_ratio(inner_circle_radius, outer_circle_radius)
        #returns the points for the image given
        return (compactness, circle_ratio, inner_circle_ratio)   
    
    def perimeter(self, image):
        # Shift the image in all eight directions to check for boundaries
        top = np.roll(image, -1, axis=0)
        bottom = np.roll(image, 1, axis=0)
        left = np.roll(image, -1, axis=1)
        right = np.roll(image, 1, axis=1)
        top_left = np.roll(top, -1, axis=1)
        top_right = np.roll(top, 1, axis=1)
        bottom_left = np.roll(bottom, -1, axis=1)
        bottom_right = np.roll(bottom, 1, axis=1)

        # Identify boundary pixels: pixels with value 1 and at least one neighbor with value 0
        boundary_pixels = (
            (image == 1) & (
                (top == 0) | (bottom == 0) | 
                (left == 0) | (right == 0) | 
                (top_left == 0) | (top_right == 0) | 
                (bottom_left == 0) | (bottom_right == 0)
            )
        )

        # Count the perimeter pixels
        perimeter = np.sum(boundary_pixels)
        return perimeter
    
    def area(self, array):
        return np.sum(array)
    
    def centroid(self, image):
        c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
        return (np.sum(r * image), np.sum(c * image)) / self.area(image)

    def get_outer_circle_radius(self, image, centroid):
        # Get the centroid coordinates
        y_center, x_center = centroid
        
        # Get all positions of '1' pixels
        rows, cols = np.where(image == 1)
        
        # Calculate the Euclidean distances from the centroid to each '1' pixel
        distances = np.sqrt((rows - y_center) ** 2 + (cols - x_center) ** 2)
        
        # Find the maximum distance, which represents the radius
        radius = np.max(distances)
        
        return radius
    
    def get_inner_circle_radius(self, image, centroid):
        centroid_y, centroid_x = centroid

        # Shift the array to find neighbors
        top = np.roll(image, -1, axis=0)
        bottom = np.roll(image, 1, axis=0)
        left = np.roll(image, -1, axis=1)
        right = np.roll(image, 1, axis=1)
        top_left = np.roll(top, -1, axis=1)
        top_right = np.roll(top, 1, axis=1)
        bottom_left = np.roll(bottom, -1, axis=1)
        bottom_right = np.roll(bottom, 1, axis=1)

        # Identify boundary pixels: pixels with value 1 and at least one neighbor with value 0
        boundary_pixels = (
            (image == 1) & (
                (top == 0) | (bottom == 0) | 
                (left == 0) | (right == 0) | 
                (top_left == 0) | (top_right == 0) | 
                (bottom_left == 0) | (bottom_right == 0)
            )
        )

        # Get the coordinates of boundary pixels
        boundary_y, boundary_x = np.where(boundary_pixels)

        # Calculate the distances from the centroid to each boundary pixel
        distances_to_centroid = np.sqrt((boundary_y - centroid_y) ** 2 + (boundary_x - centroid_x) ** 2)

        # The largest inner circle radius is the minimum distance to the boundary
        max_inner_radius = np.min(distances_to_centroid) if distances_to_centroid.size > 0 else 0

        return max_inner_radius

    # En test
    def compactness(self, area, perimeter):
        return (4*np.pi * area) / (perimeter ** 2)
    
    def circle_ratio(self, area, radius):
        return area / (np.pi * radius ** 2)
    
    def inner_circle_ratio(self, inner_radius, outer_radius):
        return inner_radius / outer_radius
