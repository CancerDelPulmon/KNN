from PySide6.QtWidgets import ( QMainWindow, QWidget, 
                                QHBoxLayout, QVBoxLayout, QTabWidget,
                                QLabel, QGroupBox, QComboBox,QFormLayout,
                                QPushButton, QSlider, QSplitter, QMessageBox,
                                QDialog, QTextEdit)
from PySide6.QtGui import QPixmap
from color_sequence import QColorSequence
from PySide6.QtCore import Qt, Slot  

from __feature__ import snake_case

import numpy as np
from scatter_3d_viewer import QScatter3dViewer
from klustr_utils import ndarray_from_qimage_argb32
from klustr_widget import PostgreSQLCredential, PostgreSQLKlustRDAO, KlustRDataSourceViewWidget
from KNN import KNNClassifier



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
        data_selector_widget = DataSelectorWidget(model, scatter_3d_viewer_widget)
        splitter = QSplitter(Qt.Horizontal)
        splitter.add_widget(data_selector_widget)
        splitter.add_widget(scatter_3d_viewer_widget)

        main_layout = QHBoxLayout(self)
        main_layout.add_widget(splitter)


class DataSelectorWidget(QWidget):
    def __init__(self, model, scatter_viewer, parent: QWidget = None):
        super().__init__(parent)
        #Serie
        self.series = {}

        self.scatter_viewer = scatter_viewer
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

        
        self.image_label = QLabel()
        self.image_label.set_alignment(Qt.AlignCenter)
        single_test_layout.add_widget(self.image_label)

        self.classify_button = QPushButton('Classify')
        self.classify_button.set_disabled(True)
        self.classify_button.clicked.connect(self.classify_image)
        single_test_layout.add_widget(self.classify_button)

        self.result_label = QLabel('not classified')
        self.result_label.set_alignment(Qt.AlignCenter)
        single_test_layout.add_widget(self.result_label)



        # Knn parameters
        knn_parameters_layout = QVBoxLayout()

        knn_parameters_widget = QGroupBox('Single test')
        knn_parameters_widget.set_layout(knn_parameters_layout)

        k_layout = QHBoxLayout()
        self.k_label = QLabel('K = 3')
        self.k_slider = QSlider(Qt.Horizontal)
        self.k_slider.set_maximum_width(250)
        self.k_slider.set_minimum(1)
        self.k_slider.set_maximum(10)
        self.k_slider.set_value(3)     
        self.k_slider.valueChanged.connect(self.k_changed)
        k_layout.add_widget(self.k_label)
        k_layout.add_widget(self.k_slider)

        knn_parameters_layout.add_layout(k_layout)


        about_button = QPushButton('About')
        about_button.clicked.connect(self.show_about_dialog)

        
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
            images, labels = self.model.analyse_data(dataset_name, True)
            self.populate_images_single_test_combo(dataset_name)
            self.display_dataset_info(index)
        if(images):
            self.knn = KNNClassifier(self.k_slider.value())
            self.knn.fit(images, labels)
        self.scatter_viewer.clear()
        self.result_label.set_text('not classified')
        self.series = {}
    
    @Slot(int)
    def on_image_selected(self, index):
        # Load the selected dataset when a new item is selected in the ComboBox
        self.index_image = index
        image_name = self.get_image_name(index)
        if image_name:
            self.display_selected_image(image_name)
            self.image_current_array = ndarray_from_qimage_argb32(self.model.get_image_from_image_name(image_name))
            self.classify_button.set_disabled(False)


    @Slot()
    def classify_image(self):
        points = self.model.analyse_single_image(self.image_current_array)
        points_array = np.array([points])
        
        # Predict the label
        label = str(self.knn.predict(points_array)[0])
        self.result_label.set_text(label)
        # Ajouter point au Series
        if label not in self.series.keys() :
            self.series[label] = points_array
            self.series[label + "color"] = QColorSequence.next()
        else:
            self.series[label] = np.append(self.series[label], points_array, axis=0)
            self.scatter_viewer.remove_serie(label)
        self.scatter_viewer.add_serie(self.series[label], self.series[label + "color"], title=label)
        self.classify_button.set_disabled(True)


    @Slot(int)
    def k_changed(self, value):
        if self.image_label.pixmap():
            self.k_label.set_text(f'K = {value}')
            self.classify_button.set_disabled(False)


    def show_about_dialog(self):
        about_dialog = AboutDialog()
        about_dialog.show()
        about_dialog.exec()


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_window_title("KlustR KNN Classifier")

        layout = QVBoxLayout(self)

        text_edit = QTextEdit(self)
        text_edit.set_read_only(True)
        text_edit.set_plain_text(self.get_about_text())

        layout.add_widget(text_edit)
        self.set_minimum_size(650, 600)


        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.accept)

        layout.add_widget(ok_button)


    def get_about_text(self):
        return '''
                Ce logiciel est le projet no 1 du cours C52.

                Il a été réalisé par :
                - Lyam Tremblay Martinez
                - Christopher Bray

                
                Il consiste à faire de la classification d'image avec les concepts suivants :
                - K-Nearest Neighbors (KNN)
                - Réduction de dimensionnalité
                - Analyse d'image

                
                Nos 3 descripteurs de forme sont :
                - Compacité (compactness)
                    en ratio pour le domaine [0, 1]
                    correspondant à (4 * PI * aire de la forme) / périmètre de la forme ^2.  
                    Une forme parfaitement circulaire a une compacité de 1, alors que les formes plus complexes ont des valeurs plus proches de 0.
                
                - Ratio du cercle (circle_ratio)
                    en ratio pour le domaine [0, 1]
                    correspondant à aire de la forme / aire du cercle de même taille.  
                    Compare l'aire de la forme à l'aire d'un cercle circonscrit, donnant une mesure de la circularité.
                
                - Ratio du cercle intérieur (inner_circle_ratio)
                    en ratio pour le domaine [0, 1]
                    correspondant à rayon du cercle intérieur / rayon du ercle extérieur.  
                    Mesure le rapport entre le rayon du plus grand cercle inscrit dans la forme et le rayon du plus petit cercle circonscrit, indiquant la présence de concavités.

                    
                Plus précisément, ce laboratoire permet de mettre en pratique les notions de:
                - Manipulation d'images numériques
                - Extraction de caractéristiques
                - Classification supervisée

                
                Un effort d'abstraction a été fait pour ces points :
                - La représentation des images en un espace 3D à partir des descripteurs.
                - L'implémentation générique de l'algorithme KNN.


                Finalement, l'ensemble de données le plus complexe que nous avons été capable de résoudre est :
                - Zoo-Tiny  

                Pour l'instant, le seul que nous avons trouvé qui n'arrive pas à classifier est l'image:
                - "rectangle_050_010_0052" qu'il voit comme "regular_3"
                '''
