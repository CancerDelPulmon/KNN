from PySide6.QtWidgets import ( QMainWindow, QWidget, 
                                QHBoxLayout, QVBoxLayout, QTabWidget,
                                QLabel, QGroupBox, QComboBox,QFormLayout,
                                QPushButton, QSlider, QSplitter, QMessageBox, QListWidget)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, Slot  

from __feature__ import snake_case


from scatter_3d_viewer import QScatter3dViewer

from klustr_widget import PostgreSQLCredential, PostgreSQLKlustRDAO, KlustRDataSourceViewWidget


class View(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.set_window_title('KlustR KNN Classifier')
        self.__init_gui()

    def __init_gui(self):
        credential = PostgreSQLCredential(host='localhost', port=5432, database='postgres', user='postgres', password='AAAaaa123')
        klustr_dao = PostgreSQLKlustRDAO(credential)
        source_data_widget = KlustRDataSourceViewWidget(klustr_dao)

        # Main Widget (central)
        central_widget = QWidget()
        self.set_central_widget(central_widget)

        # Tabs   
        tab_widget = QTabWidget()
        klustr_source_viewer_tab = source_data_widget
        knn_image_classification_tab = KnnImageClassificationWidget(self.model, klustr_dao)
        tab_widget.add_tab(klustr_source_viewer_tab, 'KlustR Source Viewer')
        tab_widget.add_tab(knn_image_classification_tab, 'Knn Image Classification')

        # Central Layout
        central_layout = QVBoxLayout(central_widget)
        central_layout.add_widget(tab_widget)

        
class KnnImageClassificationWidget(QWidget):
    def __init__(self, model, dao, parent: QWidget = None):
        super().__init__(parent)
        self.model = model
        self.set_window_title('KlustR KNN Classification')
        scatter_3d_viewer_widget = QScatter3dViewer()
        data_selector_widget = DataSelectorWidget(model)
        splitter = QSplitter(Qt.Horizontal)
        splitter.add_widget(data_selector_widget)
        splitter.add_widget(scatter_3d_viewer_widget)

        main_layout = QHBoxLayout(self)
        main_layout.add_widget(splitter)


class DataSelectorWidget(QWidget):
    def __init__(self, model, parent: QWidget = None):
        super().__init__(parent)
        self.model = model
        self.set_window_title('Data Selector')
        # Dataset
        dataset_vertical_layout = QVBoxLayout()
        dataset_horizontal_layout = QHBoxLayout()

        dataset_widget = QGroupBox('Dataset')
        dataset_widget.set_layout(dataset_vertical_layout)
        
        self.dataset_combo = QComboBox()
        self.dataset_combo.set_placeholder_text("Select Dataset")
        dataset_vertical_layout.add_widget(self.dataset_combo)

        # Included in dataset & Transformation
        dataset_vertical_layout.add_layout(dataset_horizontal_layout)

        # Included in dataset
        included_in_dataset_group = QGroupBox('Included in dataset')
        included_in_dataset_layout = QFormLayout()

        self.category_count_label = QLabel()
        self.training_image_count_label = QLabel()
        self.test_image_count_label = QLabel()
        self.total_image_count_label = QLabel()

        included_in_dataset_layout.add_row('Category count:', self.category_count_label)
        included_in_dataset_layout.add_row('Training image count:', self.training_image_count_label)
        included_in_dataset_layout.add_row('Test image count:', self.test_image_count_label)
        included_in_dataset_layout.add_row('Total image count:',  self.total_image_count_label)

        included_in_dataset_group.set_layout(included_in_dataset_layout)
        dataset_horizontal_layout.add_widget(included_in_dataset_group)

        # Transformation
        Transformation_group = QGroupBox('Transformation')
        Transformation_layout = QFormLayout()        

        self.translated_label = QLabel()
        self.rotated_label = QLabel()
        self.scaled_label = QLabel()

        Transformation_layout.add_row("Translated:", self.translated_label)
        Transformation_layout.add_row("Rotated:", self.rotated_label)
        Transformation_layout.add_row("Scaled:", self.scaled_label)

        Transformation_group.set_layout(Transformation_layout)
        dataset_horizontal_layout.add_widget(Transformation_group)
        


        # Single test
        single_test_layout = QVBoxLayout()

        single_test_widget = QGroupBox('Single test')
        single_test_widget.set_layout(single_test_layout)
        
        self.single_test_combo = QComboBox()
        self.single_test_combo.add_item('No Dataset Selected')
        single_test_layout.add_widget(self.single_test_combo)

        
        # self.pixmap = QPixmap()
        self.image_label = QLabel()
        # Not in the center for some reason (to fix)
        self.image_label.set_alignment(Qt.AlignCenter)
        # image_label.set_fixed_size(150,150)
        # self.image_label.set_pixmap(self.pixmap)
        single_test_layout.add_widget(self.image_label)

        classify_button = QPushButton('Classify')
        single_test_layout.add_widget(classify_button)

        result_label = QLabel('not classified')
        result_label.set_alignment(Qt.AlignCenter)
        single_test_layout.add_widget(result_label)



        # Knn parameters
        knn_parameters_layout = QVBoxLayout()

        knn_parameters_widget = QGroupBox('Single test')
        knn_parameters_widget.set_layout(knn_parameters_layout)

        k_layout = QHBoxLayout()
        k_label = QLabel('K = 3')
        k_slider = QSlider(Qt.Horizontal)
        k_slider.set_maximum_width(250)
        k_slider.set_minimum(1)
        k_slider.set_maximum(10)
        k_slider.set_value(3)     
        k_slider.valueChanged.connect( lambda value: k_label.set_text(f'K = {value}') )
        k_layout.add_widget(k_label)
        k_layout.add_widget(k_slider)

        knn_parameters_layout.add_layout(k_layout)

        max_distance_layout = QHBoxLayout()
        max_distance_label = QLabel('Max dist = 0.30')
        max_distance_slider = QSlider(Qt.Horizontal)
        max_distance_slider.set_fixed_width(250)
        max_distance_slider.set_minimum(0)
        max_distance_slider.set_maximum(100)
        max_distance_slider.set_value(30) 
        max_distance_slider.valueChanged.connect( lambda value: max_distance_label.set_text(f"Max dist = {value/100:.2f}") )
        max_distance_layout.add_widget(max_distance_label)
        max_distance_layout.add_widget(max_distance_slider)

        knn_parameters_layout.add_layout(max_distance_layout)



        about_button = QPushButton('About')
        
        main_layout = QVBoxLayout(self)
        main_layout.add_widget(dataset_widget)
        main_layout.add_widget(single_test_widget)
        main_layout.add_widget(knn_parameters_widget)
        main_layout.add_widget(about_button)
        self.populate_dataset_combo()
        # Connect ComboBox selection change to data loading
        self.dataset_combo.currentIndexChanged.connect(self.on_dataset_selected)
        self.single_test_combo.currentIndexChanged.connect(self.on_image_selected)



    def populate_dataset_combo(self):
        dataset_names = self.model.get_dataset_names()
        if type(dataset_names) == list:
            self.dataset_combo.add_items(dataset_names)
        else:
            QMessageBox.warning(self, dataset_names)


    def populate_images_single_test_combo(self, dataset_name):
        self.single_test_combo.clear()
        images_names = self.model.get_images_names_from_dataset(dataset_name)
        if type(images_names) == list:
            self.single_test_combo.add_items(images_names)
        else:
            QMessageBox.warning(self, self.single_test_combo)


    def display_selected_image(self, image_name):
        image = self.model.get_image_from_image_name(image_name)
        pixmap = QPixmap.from_image(image)
        self.image_label.set_pixmap(pixmap)

        


    def get_dataset_name(self, index):
       return self.dataset_combo.item_text(index)


    def get_image_name(self, index):
        return self.single_test_combo.item_text(index)
    

    def display_dataset_info(self, index):
        dataset_name = self.get_dataset_name(index)

        # Included in dataset
        new_category_count_text = str(self.model.get_category_count(dataset_name))
        self.category_count_label.set_text(new_category_count_text)

        new_training_image_count_text = str(self.model.get_image_count(dataset_name, True))
        self.training_image_count_label.set_text(new_training_image_count_text)

        new_test_image_count_text = str(self.model.get_image_count(dataset_name, False))
        self.test_image_count_label.set_text(new_test_image_count_text)

        new_total_image_count_text = str(self.model.get_total_image_count(dataset_name))
        self.total_image_count_label.set_text(new_total_image_count_text)


        # Transformation
        new_translated_value_text = str(self.model.get_translated_value(dataset_name))
        self.translated_label.set_text(new_translated_value_text)

        new_rotated_value_text = str(self.model.get_rotated_value(dataset_name))
        self.rotated_label.set_text(new_rotated_value_text)

        new_scaled_value_text = str(self.model.get_scaled_value(dataset_name))
        self.scaled_label.set_text(new_scaled_value_text)




    @Slot(int)
    def on_dataset_selected(self, index):
        # Load the selected dataset when a new item is selected in the ComboBox
        self.index_dataset = index
        dataset_name = self.get_dataset_name(index)
        if dataset_name:
            self.populate_images_single_test_combo(dataset_name)
            self.display_dataset_info(index)
        
    
    @Slot(int)
    def on_image_selected(self, index):
        # Load the selected dataset when a new item is selected in the ComboBox
        self.index_image = index
        image_name = self.get_image_name(index)
        if image_name:
            self.display_selected_image(image_name)



    def load_data_into_viewer(self, data, title="Dataset"):
        # Clear existing series and load new data into the viewer
        """
        self.scatter_viewer.clear()
        # Convert data to NumPy array
        data_np = np.array(data)
        # Add series to viewer
        color = QColorSequence.next()
        self.scatter_viewer.add_serie(data_np, color, title=title)
        """
        pass



