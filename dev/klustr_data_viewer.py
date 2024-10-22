# Importation des modules
import sys
from db_credential import PostgreSQLCredential
from klustr_dao import PostgreSQLKlustRDAO
from klustr_widget import KlustRDataSourceViewWidget
from PySide6 import QtWidgets
from __feature__ import snake_case, true_property
# Application principale de Qt
app = QtWidgets.QApplication(sys.argv)
# Information de connexion à la base de données
credential = PostgreSQLCredential(
host='localhost',
port=5432,
database='postgres',
user='postgres',
password='AAAaaa123')
# DAO utilisé
klustr_dao = PostgreSQLKlustRDAO(credential)
# Instanciation et affichage du widget de visualisation des données du projet KlustR
source_data_widget = KlustRDataSourceViewWidget(klustr_dao)
source_data_widget.show()
# Démarrage de l’engin Qt
sys.exit(app.exec_())