# goods_form.py
#This form directly writes to the goods table in the SQLite database.



import sqlite3
from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox, QVBoxLayout

class GoodsForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.product_input = QLineEdit()
        self.supplier_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.unit_input = QLineEdit()
        self.rate_input = QLineEdit()
        self.tax_input = QLineEdit()
        self.total_display = QLineEdit()
        self.total_display.setReadOnly(True)

        self.calculate_button = QPushButton("Calculate Total")
        self.submit_button = QPushButton("Submit")

        self.calculate_button.clicked.connect(self.calculate_total)
        self.submit_button.clicked.connect(self.save_goods)

        form_layout.addRow("Product ID:", self.product_input)
        form_layout.addRow("Supplier:", self.supplier_input)
        form_layout.addRow("Quantity:", self.quantity_input)
        form_layout.addRow("Unit:", self.unit_input)
        form_layout.addRow("Rate per Unit:", self.rate_input)
        form_layout.addRow("Tax (%):", self.tax_input)
        form_layout.addRow("Total Amount:", self.total_display)

        layout.addLayout(form_layout)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def calculate_total(self):
        try:
            qty = float(self.quantity_input.text())
            rate = float(self.rate_input.text())
            tax = float(self.tax_input.text())
            total = qty * rate * (1 + tax / 100)
            self.total_display.setText(f"{total:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers.")

    def save_goods(self):
        try:
            product_id = int(self.product_input.text())
            supplier = self.supplier_input.text()
            quantity = int(self.quantity_input.text())
            unit = self.unit_input.text()
            rate = float(self.rate_input.text())
            tax = float(self.tax_input.text())
            total = float(self.total_display.text())

            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute('''INSERT INTO goods (product_id, supplier, quantity, unit, rate, total, tax)
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (product_id, supplier, quantity, unit, rate, total, tax))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Goods received recorded successfully.")
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def clear_fields(self):
        self.product_input.clear()
        self.supplier_input.clear()
        self.quantity_input.clear()
        self.unit_input.clear()
        self.rate_input.clear()
        self.tax_input.clear()
        self.total_display.clear()
