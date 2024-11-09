

import sys


from PySide6.QtWidgets import ( QApplication, QMainWindow, QWidget, 
                                QHBoxLayout, QVBoxLayout, QTabWidget,
                                QLabel, QGroupBox, QComboBox,QFormLayout,
                                QPushButton, QSlider, QSplitter)

from PySide6.QtGui import QPixmap

from PySide6.QtCore import Qt

from __feature__ import snake_case


from scatter_3d_viewer import QScatter3dViewer

from klustr_widget import PostgreSQLCredential, PostgreSQLKlustRDAO, KlustRDataSourceViewWidget
 




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        knn_image_classification_tab = knnImageClassificationWidget()
        tab_widget.add_tab(klustr_source_viewer_tab, 'KlustR Source Viewer')
        tab_widget.add_tab(knn_image_classification_tab, 'Knn Image Classification')

        # Central Layout
        central_layout = QVBoxLayout(central_widget)
        central_layout.add_widget(tab_widget)




        
class knnImageClassificationWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.set_window_title('KlustR KNN Classification')
        self.__init_gui()

    def __init_gui(self):
        scatter_3d_viewer_widget = QScatter3dViewer()
        data_selector_widget = dataSelectorWidget()

        splitter = QSplitter(Qt.Horizontal)
        splitter.add_widget(data_selector_widget)
        splitter.add_widget(scatter_3d_viewer_widget)

        main_layout = QHBoxLayout(self)
        main_layout.add_widget(splitter)







class dataSelectorWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.set_window_title('Data Selector')
        self.__init_gui()

    def __init_gui(self):
        # Dataset
        dataset_vertical_layout = QVBoxLayout()
        dataset_horizontal_layout = QHBoxLayout()

        dataset_widget = QGroupBox('Dataset')
        dataset_widget.set_layout(dataset_vertical_layout)
        
        dataset_combo = QComboBox()
        dataset_combo.add_item('ABC [2][10]')
        dataset_vertical_layout.add_widget(dataset_combo)

        # Included in dataset & Transformation
        dataset_vertical_layout.add_layout(dataset_horizontal_layout)

        # Included in dataset
        included_in_dataset_group = QGroupBox('Included in dataset')
        included_in_dataset_layout = QFormLayout()

        included_in_dataset_layout.add_row('Category count:', QLabel('2'))
        included_in_dataset_layout.add_row('Training image count:', QLabel('4'))
        included_in_dataset_layout.add_row('Test image count:', QLabel('6'))
        included_in_dataset_layout.add_row('Total image count:', QLabel('10'))

        included_in_dataset_group.set_layout(included_in_dataset_layout)
        dataset_horizontal_layout.add_widget(included_in_dataset_group)

        # Transformation
        Transformation_group = QGroupBox('Transformation')
        Transformation_layout = QFormLayout()        

        Transformation_layout.add_row("Translated:", QLabel("true"))
        Transformation_layout.add_row("Rotated:", QLabel("false"))
        Transformation_layout.add_row("Scaled:", QLabel("false"))

        Transformation_group.set_layout(Transformation_layout)
        dataset_horizontal_layout.add_widget(Transformation_group)
        


        # Single test
        single_test_layout = QVBoxLayout()

        single_test_widget = QGroupBox('Single test')
        single_test_widget.set_layout(single_test_layout)
        
        single_test_combo = QComboBox()
        single_test_combo.add_item('img_ellipsoid_200_200_100_0031')
        single_test_layout.add_widget(single_test_combo)

        pixmap = QPixmap('../image_test.jpg')
        image_label = QLabel()
        # Not in the center for some reason (to fix)
        image_label.set_alignment(Qt.AlignCenter)
        image_label.set_fixed_size(150,150)
        image_label.set_pixmap(pixmap)
        single_test_layout.add_widget(image_label)

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
        max_distance_slider.valueChanged.connect( lambda value: max_distance_label.setText(f"Max dist = {value/100:.2f}") )
        max_distance_layout.add_widget(max_distance_label)
        max_distance_layout.add_widget(max_distance_slider)

        knn_parameters_layout.add_layout(max_distance_layout)



        about_button = QPushButton('About')
        
        main_layout = QVBoxLayout(self)
        main_layout.add_widget(dataset_widget)
        main_layout.add_widget(single_test_widget)
        main_layout.add_widget(knn_parameters_widget)
        main_layout.add_widget(about_button)






def main ():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()