# sales_form.py
#This form records a sale with product ID, customer details, and sale amounts.


import sqlite3
from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox, QVBoxLayout

class SalesForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.product_input = QLineEdit()
        self.customer_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.unit_input = QLineEdit()
        self.rate_input = QLineEdit()
        self.tax_input = QLineEdit()
        self.total_display = QLineEdit()
        self.total_display.setReadOnly(True)

        self.calculate_button = QPushButton("Calculate Total")
        self.submit_button = QPushButton("Submit")

        self.calculate_button.clicked.connect(self.calculate_total)
        self.submit_button.clicked.connect(self.save_sale)

        form_layout.addRow("Product ID:", self.product_input)
        form_layout.addRow("Customer:", self.customer_input)
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

    def save_sale(self):
        try:
            product_id = int(self.product_input.text())
            customer = self.customer_input.text()
            quantity = int(self.quantity_input.text())
            unit = self.unit_input.text()
            rate = float(self.rate_input.text())
            tax = float(self.tax_input.text())
            total = float(self.total_display.text())

            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute('''INSERT INTO sales (product_id, customer, quantity, unit, rate, total, tax)
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (product_id, customer, quantity, unit, rate, total, tax))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Sale recorded successfully.")
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def clear_fields(self):
        self.product_input.clear()
        self.customer_input.clear()
        self.quantity_input.clear()
        self.unit_input.clear()
        self.rate_input.clear()
        self.tax_input.clear()
        self.total_display.clear()
