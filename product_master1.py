# product_master.py
#This form lets you add new products to the system, including images and full product details.



import sqlite3
import os
from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QPushButton,
    QFileDialog, QLabel, QVBoxLayout, QMessageBox
)

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

        self.image_label = QLabel("No Image Selected")
        self.image_button = QPushButton("Choose Image")
        self.image_button.clicked.connect(self.choose_image)

        self.submit_button = QPushButton("Add Product")
        self.submit_button.clicked.connect(self.add_product)

        form_layout.addRow("Barcode:", self.barcode_input)
        form_layout.addRow("SKU ID:", self.sku_input)
        form_layout.addRow("Category:", self.category_input)
        form_layout.addRow("Subcategory:", self.subcategory_input)
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("Tax (%):", self.tax_input)
        form_layout.addRow("Price:", self.price_input)
        form_layout.addRow("Unit of Measurement:", self.unit_input)
        form_layout.addRow("Product Image:", self.image_label)
        layout.addLayout(form_layout)
        layout.addWidget(self.image_button)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def choose_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path = file_path
            self.image_label.setText(os.path.basename(file_path))

    def add_product(self):
        try:
            barcode = self.barcode_input.text()
            sku = self.sku_input.text()
            category = self.category_input.text()
            subcategory = self.subcategory_input.text()
            name = self.name_input.text()
            description = self.description_input.text()
            tax = float(self.tax_input.text())
            price = float(self.price_input.text())
            unit = self.unit_input.text()

            # Save image to local folder
            if self.image_path:
                save_path = os.path.join("assets/product_images", os.path.basename(self.image_path))
                with open(self.image_path, "rb") as f_in, open(save_path, "wb") as f_out:
                    f_out.write(f_in.read())
            else:
                save_path = ""

            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute('''INSERT INTO product (barcode, sku, category, subcategory, image_path, name, description, tax, price, unit)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (barcode, sku, category, subcategory, save_path, name, description, tax, price, unit))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Product added successfully.")
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
        self.image_label.setText("No Image Selected")
        self.image_path = ""
