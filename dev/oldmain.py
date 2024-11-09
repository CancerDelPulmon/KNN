# app.py
import sys
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QComboBox, QMessageBox
)
from PySide6.QtCore import Slot
from PySide6.QtGui import QColor

from scatter_3d_viewer import QScatter3dViewer
from color_sequence import QColorSequence
from klustr_dao import PostgreSQLKlustRDAO
from db_credential import PostgreSQLCredential


# PostgreSQL connection credentials (update with your actual credentials)
class PGConnectionCredential:
    def __init__(self):
        self.connection_string = "dbname=test user=postgres password=secret host=localhost"

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Scatter Viewer with Database Integration")
        self.resize(800, 600)

        layout = QVBoxLayout()

        # ComboBox for selecting dataset
        self.dataset_combo = QComboBox()
        self.dataset_combo.setPlaceholderText("Select Dataset")
        layout.addWidget(self.dataset_combo)

        # 3D Scatter Viewer
        self.scatter_viewer = QScatter3dViewer()
        layout.addWidget(self.scatter_viewer)

        self.setLayout(layout)

        # Initialize PostgreSQLKlustRDAO and populate ComboBox
        self.credential = PostgreSQLCredential(
            host='localhost',
            port=5432,
            database='postgres',
            user='postgres',
            password='AAAaaa123')
        self.dao = PostgreSQLKlustRDAO(self.credential)
        self.populate_dataset_combo()

        # Connect ComboBox selection change to data loading
        self.dataset_combo.currentIndexChanged.connect(self.on_dataset_selected)

    def populate_dataset_combo(self):
        # Fetch dataset names from PostgreSQL and add them to the ComboBox
        if self.dao.is_available:
            datasets = self.dao.available_datasets
            if datasets:
                # Assuming the dataset name is the first column in the result
                dataset_names = [row[1] for row in datasets]
                self.dataset_combo.addItems(dataset_names)
            else:
                QMessageBox.warning(self, "No Datasets", "No datasets available in the database.")
        else:
            QMessageBox.critical(self, "Database Error", "Database connection is not available.")

    @Slot()
    def on_dataset_selected(self, index):
        # Load the selected dataset when a new item is selected in the ComboBox
        pass

    def load_data_into_viewer(self, data, title="Dataset"):
        # Clear existing series and load new data into the viewer
        self.scatter_viewer.clear()

        # Convert data to NumPy array
        data_np = np.array(data)

        # Add series to viewer
        color = QColorSequence.next()
        self.scatter_viewer.add_serie(data_np, color, title=title)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
