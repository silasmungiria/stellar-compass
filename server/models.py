from sqlalchemy.orm import relationship
from exts import db

class BaseMixin:
    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        #self.deleted = True
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        db.session.commit()


class User(db.Model, BaseMixin):
    __tablename__ = 'users'

    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)
    contact_info = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(20), nullable=False, default='customer')  # Example: admin, customer
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    orders = relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


class Medication(db.Model, BaseMixin):
    __tablename__ = 'medications'

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    dosage = db.Column(db.String(50), nullable=True)
    manufacturer = db.Column(db.String(100), nullable=True)
    expiry_date = db.Column(db.Date, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)

    orders = relationship('Order', backref='medication', lazy=True)


class Order(db.Model, BaseMixin):
    __tablename__ = 'customer_orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    shipping = db.Column(db.Boolean, nullable=False, default=True)  # Shipping or Pickup
    total_price = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), nullable=False, default='Pending')  # Paid, Pending, Refunded
    status = db.Column(db.String(20), nullable=False, default='Approved')  # Approved, Completed, Cancelled
    sold = db.Column(db.Boolean, nullable=False, default=False)

    sale_invoices = relationship('SaleInvoice', backref='customer_order', lazy=True)


class SaleInvoice(db.Model, BaseMixin):
    __tablename__ = 'sale_invoices'

    id = db.Column(db.Integer, primary_key=True)
    customer_order_id = db.Column(db.Integer, db.ForeignKey('customer_orders.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=True)
    transaction_id = db.Column(db.String(100), nullable=True)
    active_sale = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')  # Values: Pending, Dispatched, In Transit, Delivered, Completed, Cancelled
    due_date = db.Column(db.Date, nullable=True)

    payments = relationship('Payment', backref='sale_invoice', lazy=True)


class Payment(db.Model, BaseMixin):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('sale_invoices.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=True)
    transaction_id = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Pending')  # Possible values: Paid, Pending, Refunded
    response_status = db.Column(db.String(20), nullable=True)
    response_amount = db.Column(db.Float, nullable=True)
    response_charge_response_code = db.Column(db.String(20), nullable=True)
    response_charge_response_message = db.Column(db.String(100), nullable=True)
    response_charged_amount = db.Column(db.Float, nullable=True)
    response_currency = db.Column(db.String(10), nullable=True)
    response_flw_ref = db.Column(db.String(100), nullable=True)
    response_transaction_id = db.Column(db.String(100), nullable=True)
    response_tx_ref = db.Column(db.String(100), nullable=True)
    response_customer_email = db.Column(db.String(100), nullable=True)
    response_customer_name = db.Column(db.String(100), nullable=True)
    response_customer_phone_number = db.Column(db.String(20), nullable=True)
