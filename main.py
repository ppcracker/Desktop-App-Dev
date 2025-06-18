# main.py
from PySide6.QtWidgets import QApplication, QStackedWidget
from login_form import LoginForm
from goods_form import GoodsForm
from sales_form import SalesForm
from product_master import ProductMaster

app = QApplication([])
stack = QStackedWidget()

# Create form instances
login = LoginForm(stack)
goods = GoodsForm()
sales = SalesForm()
product = ProductMaster()

# Add forms to stack
stack.addWidget(login)
stack.addWidget(goods)
stack.addWidget(sales)
stack.addWidget(product)

stack.setFixedSize(1000, 700)
stack.setWindowTitle("Inventory Management System")
stack.show()

app.exec()
