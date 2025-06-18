# product_master.py
#This form allows the operator to:
#Enter complete product details
#Upload an image
#Save data into the product table in SQLite


import os
import sqlite3
from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QPushButton, QLabel,
    QVBoxLayout, QFileDialog, QMessageBox, QHBoxLayout
)
from PySide6.QtGui import QPixmap

class ProductMaster(QWidget):
    def __init__(self):
        super().__init__()
        self.image_path = ""
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.barcode_input = QLineEdit()
        self.sku_input = QLineEdit()
        self.category_input = QLineEdit()
        self.subcategory_input = QLineEdit()
        self.name_input = QLineEdit()
        self.description_input = QLineEdit()
        self.tax_input = QLineEdit()
        self.price_input = QLineEdit()
        self.unit_input = QLineEdit()
        self.image_label = QLabel("No Image")
        self.image_label.setFixedSize(150, 150)

        self.image_button = QPushButton("Upload Image")
        self.image_button.clicked.connect(self.upload_image)

        self.submit_button = QPushButton("Save Product")
        self.submit_button.clicked.connect(self.save_product)

        form_layout.addRow("Barcode:", self.barcode_input)
        form_layout.addRow("SKU ID:", self.sku_input)
        form_layout.addRow("Category:", self.category_input)
        form_layout.addRow("Subcategory:", self.subcategory_input)
        form_layout.addRow("Product Name:", self.name_input)
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("Tax (%):", self.tax_input)
        form_layout.addRow("Price:", self.price_input)
        form_layout.addRow("Unit of Measurement:", self.unit_input)
        form_layout.addRow("Product Image:", self.image_button)

        layout.addLayout(form_layout)
        layout.addWidget(self.image_label)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Product Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            filename = os.path.basename(file_path)
            dest_path = os.path.join("assets/product_images", filename)
            os.makedirs("assets/product_images", exist_ok=True)
            with open(file_path, 'rb') as src, open(dest_path, 'wb') as dst:
                dst.write(src.read())
            self.image_path = dest_path
            pixmap = QPixmap(dest_path).scaled(150, 150)
            self.image_label.setPixmap(pixmap)

    def save_product(self):
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute('''INSERT INTO product
                         (barcode, sku, category, subcategory, image_path, name, description, tax, price, unit)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (self.barcode_input.text(), self.sku_input.text(), self.category_input.text(),
                       self.subcategory_input.text(), self.image_path, self.name_input.text(),
                       self.description_input.text(), float(self.tax_input.text()),
                       float(self.price_input.text()), self.unit_input.text()))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Product saved successfully.")
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def clear_fields(self):
        self.barcode_input.clear()
        self.sku_input.clear()
        self.category_input.clear()
        self.subcategory_input.clear()
        self.name_input.clear()
        self.description_input.clear()
        self.tax_input.clear()
        self.price_input.clear()
        self.unit_input.clear()
        self.image_label.setText("No Image")
