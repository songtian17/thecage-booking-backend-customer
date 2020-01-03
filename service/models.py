# app/models.py
from datetime import datetime
from service import db, ma
from marshmallow import fields
from sqlalchemy import event


class Admin(db.Model):
    __tablename__ = "Admin"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200), nullable=False)

    def __init__(self, user_id, password, role):
        self.user_id = user_id
        self.password = password
        self.role = role
        # self.email = email


# class AdminSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'user_id', 'password', 'name', 'role')

class AdminSchema(ma.Schema):
    id = fields.Integer()
    user_id = fields.String(required=True)
    password = fields.String(required=True)
    role = fields.String(required=True)


admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)


def insert_data(target, connection, **kw):
    connection.execute(target.insert(), {'id': 1, 'user_id': 'admin', 'password': 'password', 'role': 'SuperAdmin'})


event.listen(Admin.__table__, 'after_create', insert_data)


class Announcement(db.Model):
    __tablename__ = "Announcement"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    html_string = db.Column(db.String(200), nullable=False)
    markdown_string = db.Column(db.String(200), nullable=False)
    placement = db.Column(db.String(200), nullable=False)
    visibility = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self, html_string, markdown_string, placement, visibility, updated_at):
        self.html_string = html_string
        self.markdown_string = markdown_string
        self.placement = placement
        self.visibility = visibility
        self.updated_at = updated_at


class AnnouncementSchema(ma.Schema):
    id = fields.Integer()
    html_string = fields.String(required=True)
    markdown_string = fields.String(required=True)
    placement = fields.String(required=True)
    visibility = fields.Boolean()
    # updated_at = fields.DateTime()


announcement_schema = AnnouncementSchema()
announcements_schema = AnnouncementSchema(many=True)


class AnnouncementSchema2(ma.Schema):
    html_string = fields.String(required=True)
    placement = fields.String(required=True)
    visibility = fields.Boolean()


announcement2_schema = AnnouncementSchema2
announcement2s_schema = AnnouncementSchema2(many=True)


def insert_data(target, connection, **kw):
    connection.execute(target.insert(), {'id': 1, 'html_string': 'hello', 'markdown_string': 'hello', 'placement': 'Top', 'visibility': False}, {'id': 2, 'html_string': 'hello', 'markdown_string': 'hello', 'placement': 'Bottom', 'visibility': True})


event.listen(Announcement.__table__, 'after_create', insert_data)


class CartItem(db.Model):
    __tablename__ = "CartItem"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey("Field.id"), nullable=False)
    pitch_id = db.Column(db.Integer, db.ForeignKey("Pitch.id"), nullable=False)
    promocode_id = db.Column(db.Integer, db.ForeignKey("PromoCode.id"))
    customer_id = db.Column(db.Integer, db.ForeignKey("Customer.id"), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    end_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("Product.id"), nullable=False)
    expiry_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, nullable=False)

    def __init__(self, venue_id, field_id, pitch_id, promocode_id, customer_id, start_time, end_time, expiry_date, product_id, amount, discount_amount):
        self.venue_id = venue_id
        self.field_id = field_id
        self.pitch_id = pitch_id
        self.promocode_id = promocode_id
        self.customer_id = customer_id
        self.start_time = start_time
        self.end_time = end_time
        self.expiry_date = expiry_date
        self.product_id = product_id
        self.amount = amount
        self.discount_amount = discount_amount


class CartItemSchema(ma.Schema):
    id = fields.Integer()
    venue_id = fields.Integer(required=True)
    field_id = fields.Integer(required=True)
    pitch_id = fields.Integer(required=True)
    promo_code_id = fields.Integer()
    customer_id = fields.Integer(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    expiry_date = fields.DateTime(required=True)
    product_id = fields.Integer(required=True)
    amount = fields.Float(required=True)
    discount_amount = fields.Float(required=True)


cart_item_schema = CartItemSchema()
cart_items_schema = CartItemSchema(many=True)


class CustomTimeSlot(db.Model):
    __tablename__ = "CustomTimeSlot"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey("Field.id"), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self, start_time, end_time, field_id, duration, created_at, updated_at):
        self.start_time = start_time
        self.end_time = end_time
        self.field_id = field_id
        self.duration = duration
        self.created_at = created_at
        self.updated_at = updated_at


class CustomTimeSlotSchema(ma.Schema):
    id = fields.Integer()
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)
    field_id = fields.Integer()
    duration = fields.Integer(required=True)


customtimeslot_schema = CustomTimeSlotSchema()
customtimeslots_schema = CustomTimeSlotSchema(many=True)


class Customer(db.Model):
    __tablename__ = "Customer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    phone_no = db.Column(db.String(200), nullable=False, unique=True)
    customer_odoos = db.relationship(
        "CustomerOdoo", backref="customer", lazy=True, cascade="all, delete")
    purchase_logs = db.relationship(
        "PurchaseLog", backref="customer", lazy=True, cascade="all, delete")
    promocode_logs = db.relationship(
        "PromoCodeLog", backref="customer", lazy=True, cascade="all, delete")
    cart_item = db.relationship(
        "CartItem", backref="customer", lazy=True, cascade="all, delete")

    def __init__(self, email, name, password, phone_no):
        self.email = email
        self.name = name
        self.password = password
        self.phone_no = phone_no


class CustomerSchema(ma.Schema):
    id = fields.Integer()
    email = fields.String(required=True)
    name = fields.String(required=True)
    password = fields.String(required=True)
    phone_no = fields.String(required=True)


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


class CustomerSchema2(ma.Schema):
    id = fields.Integer()
    email = fields.String(required=True)
    name = fields.String(required=True)
    phone_no = fields.String(required=True)


customer_schema2 = CustomerSchema2()
customers_schema2 = CustomerSchema2(many=True)


class CustomerOdoo(db.Model):
    __tablename__ = "CustomerOdoo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(
        db.Integer, db.ForeignKey("Customer.id"), nullable=False)
    odoo_id = db.Column(db.Integer, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)

    def __init__(self, customer_id, odoo_id, venue_id):
        self.venue_id = venue_id
        self.odoo_id = odoo_id
        self.customer_id = customer_id


class CustomerOdooSchema(ma.Schema):
    id = fields.Integer()
    customer_id = fields.Integer()
    odoo_id = fields.Integer(required=True)
    venue_id = fields.Integer()


customer_odoo_schema = CustomerOdooSchema()
customer_odoos_schema = CustomerOdooSchema(many=True)


class Field(db.Model):
    __tablename__ = "Field"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False, unique=True)
    field_type = db.Column(db.String(200), nullable=False) # "5-A-Side" / "7-A-Side"
    num_pitches = db.Column(db.Integer, nullable=False)
    colour = db.Column(db.String(7))
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now, nullable=False)
    odoo_id = db.Column(db.Integer, nullable=False)
    custom_timeslots = db.relationship(
        "CustomTimeSlot", backref="field", lazy=True, cascade="all, delete")
    pitches = db.relationship("Pitch", backref="field", lazy=True, cascade="all, delete")
    cart_item = db.relationship("CartItem", backref="field", lazy=True, cascade="all, delete")

    def __init__(self, name, venue_id, field_type, num_pitches, colour, created_at, updated_at, odoo_id):
        self.name = name
        self.venue_id = venue_id
        self.field_type = field_type
        self.num_pitches = num_pitches
        self.colour = colour
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.odoo_id = odoo_id
        self.pitches = []
        self.custom_timeslots = []


class FieldSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    venue_id = fields.Integer()
    field_type = fields.String(required=True)
    num_pitches = fields.Integer()
    colour = fields.String(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    odoo_id = fields.Integer(required=True)


field_schema = FieldSchema()
fields_schema = FieldSchema(many=True)


class FieldSchema3(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    venue_id = fields.Integer()
    field_type = fields.String(required=True)
    colour = fields.String(required=True)
    num_pitches = fields.Integer()
    odoo_id = fields.Integer(required=True)


field3_schema = FieldSchema3()
fields3_schema = FieldSchema3(many=True)


class Pitch(db.Model):
    __tablename__ = "Pitch"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    field_id = db.Column(db.Integer, db.ForeignKey("Field.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    odoo_id = db.Column(db.Integer)
    cart_item = db.relationship("CartItem", backref="pitch", lazy=True, cascade="all, delete")

    def __init__(self, name, field_id, odoo_id):
        self.name = name
        self.field_id = field_id
        self.odoo_id = odoo_id


class PitchSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    field_id = fields.Integer()
    odoo_id = fields.Integer()


pitch_schema = PitchSchema()
pitches_schema = PitchSchema(many=True)


class FieldSchema2(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    venue_id = fields.Integer()
    odoo_id = fields.Integer(required=True)
    field_type = fields.String(required=True)
    num_pitches = fields.Integer()
    colour = fields.String(required=True)
    pitches = fields.List(fields.Nested(PitchSchema(only=("id", "name", "odoo_id"))))


field2_schema = FieldSchema2()
fields2_schema = FieldSchema2(many=True)


class Product(db.Model):
    __tablename__ = "Product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    odoo_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    promo_code_valid_products = db.relationship(
        "PromoCodeValidProduct", backref="product", lazy=True, cascade="all, delete"
    )
    purchase_items = db.relationship(
        "PurchaseItem", backref="product", lazy=True, cascade="all, delete")
    cart_item = db.relationship(
        "CartItem", backref="product", lazy=True, cascade="all, delete")

    def __init__(self, name, price, odoo_id, start_time, end_time):
        self.name = name
        self.price = price
        self.odoo_id = odoo_id
        self.start_time = start_time
        self.end_time = end_time


class ProductSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    price = fields.Float(required=True)
    odoo_id = fields.Integer(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


class PromoCode(db.Model):
    __tablename__ = "PromoCode"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # discount_id = db.Column(db.Integer, db.ForeignKey(
    #     "TimingDiscount.id"), nullable=False)
    code = db.Column(db.String(200), unique=True, nullable=False)
    valid_from = db.Column(db.DateTime, default=datetime.now, nullable=False)
    valid_to = db.Column(db.DateTime, default=datetime.now, nullable=False)
    usage_limit = db.Column(db.Integer, nullable=False)
    times_used = db.Column(db.Integer, nullable=False)
    usage_per_user = db.Column(db.Integer, nullable=False)
    discount_type = db.Column(db.String(200), nullable=False)
    discount = db.Column(db.Float, nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    promo_code_logs = db.relationship(
        "PromoCodeLog", backref="promocode", lazy=True, cascade="all, delete")
    promo_code_valid_products = db.relationship(
        "PromoCodeValidProduct", backref="promocode", lazy=True, cascade="all, delete")
    promo_code_valid_timings = db.relationship(
        "PromoCodeValidTiming", backref="promocode", lazy=True, cascade="all, delete")
    promo_code_valid_locations = db.relationship(
        "PromoCodeValidLocation", backref="promocode", lazy=True, cascade="all, delete")
    cart_item = db.relationship(
        "CartItem", backref="promocode", lazy=True, cascade="all, delete"
    )

    def __init__(self, code, valid_from, valid_to, usage_limit, times_used, usage_per_user, discount_type, discount, created_at, updated_at):
        self.code = code
        self.valid_from = valid_from
        self.valid_to = valid_to
        self.usage_limit = usage_limit
        self.times_used = times_used
        self.usage_per_user = usage_per_user
        self.discount_type = discount_type
        self.discount = discount
        self.created_at = created_at
        self.updated_at = updated_at


class PromoCodeLog(db.Model):
    __tablename__ = "PromoCodeLog"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    promo_code_id = db.Column(db.Integer, db.ForeignKey(
        "PromoCode.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        "Customer.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self, timestamp):
        self.timestamp = timestamp


class PromoCodeLogSchema(ma.Schema):
    id = fields.Integer()
    promo_code_id = fields.Integer()
    customer_id = fields.Integer()
    timestamp = fields.DateTime()


promo_code_log_schema = PromoCodeLogSchema()
promo_scode_logs_schema = PromoCodeLogSchema(many=True)


class PromoCodeValidLocation(db.Model):
    __tablename__ = "PromoCodeValidLocation"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    promo_code_id = db.Column(db.Integer, db.ForeignKey(
        "PromoCode.id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)

    def __init__(self, name, promo_code_id, venue_id):
        self.name = name
        self.promo_code_id = promo_code_id
        self.venue_id = venue_id


class PromoCodeValidLocationSchema(ma.Schema):
    id = fields.Integer()
    promo_code_id = fields.Integer()
    venue_id = fields.Integer()
    name = fields.String(required=True)


promo_code_valid_location_schema = PromoCodeValidLocationSchema()
promo_code_valid_locations_schema = PromoCodeValidLocationSchema(many=True)


class PromoCodeValidProduct(db.Model):
    __tablename__ = "PromoCodeValidProduct"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    promo_code_id = db.Column(db.Integer, db.ForeignKey(
        "PromoCode.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        "Product.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)

    def __init__(self, name, promo_code_id, product_id):
        self.name = name
        self.promo_code_id = promo_code_id
        self.product_id = product_id


class PromoCodeValidProductSchema(ma.Schema):
    id = fields.Integer()
    promo_code_id = fields.Integer()
    product_id = fields.Integer()
    name = fields.String(required=True)


promo_code_valid_product_schema = PromoCodeValidProductSchema()
promo_code_valid_products_schema = PromoCodeValidProductSchema(many=True)


class PromoCodeSchema(ma.Schema):
    id = fields.Integer()
    discount_id = fields.Integer()
    code = fields.String(required=True)
    valid_from = fields.DateTime(required=True)
    valid_to = fields.DateTime(required=True)
    usage_limit = fields.Integer(required=True)
    times_used = fields.Integer(required=True)
    usage_per_user = fields.Integer(required=True)
    discount = fields.Integer(required=True)
    discount_type = fields.String(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    promo_code_valid_products = fields.List(fields.Nested(PromoCodeValidProductSchema(only=("id", "name"))))
    promo_code_valid_locations = fields.List(fields.Nested(PromoCodeValidLocationSchema(only=("id", "name"))))


promo_code_schema = PromoCodeSchema()
promo_codes_schema = PromoCodeSchema(many=True)


class PromoCodeValidTiming(db.Model):
    __tablename__ = "PromoCodeValidTiming"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    promo_code_id = db.Column(db.Integer, db.ForeignKey(
        "PromoCode.id"), nullable=False)
    day_of_week = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def __init__(self, start_time, end_time, day_of_week, promo_code_id):
        self.start_time = start_time
        self.end_time = end_time
        self.day_of_week = day_of_week
        self.promo_code_id = promo_code_id


class PromoCodeValidTimingSchema(ma.Schema):
    id = fields.Integer()
    promo_code_id = fields.Integer()
    day_of_week = fields.String(required=True)
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)


promo_code_valid_timing_schema = PromoCodeValidTimingSchema()
promo_code_valid_timings_schema = PromoCodeValidTimingSchema(many=True)


class PurchaseItem(db.Model):
    __tablename__ = "PurchaseItem"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    purchase_log_id = db.Column(
        db.Integer, db.ForeignKey("PurchaseLog.id"), nullable=False
    )
    product_id = db.Column(db.Integer, db.ForeignKey(
        "Product.id"), nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey("Field.id"), nullable=False)
    pitch_id = db.Column(db.Integer, db.ForeignKey("Pitch.id"), nullable=False)
    price = db.Column(db.Float, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, purchase_log_id, product_id, field_id, pitch_id, price, start_time, end_time):
        self.purchase_log_id = purchase_log_id
        self.product_id = product_id
        self.field_id = field_id
        self.pitch_id = pitch_id
        self.price = price
        self.start_time = start_time
        self.end_time = end_time


class PurchaseItemSchema(ma.Schema):
    id = fields.Integer()
    purchase_log_id = fields.Integer()
    product_id = fields.Integer()
    field_id = fields.Integer()
    pitch_id = fields.Integer()
    price = fields.Float(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)


purchase_item_schema = PurchaseItemSchema()
purchase_items_schema = PurchaseItemSchema(many=True)


class PurchaseLog(db.Model):
    __tablename__ = "PurchaseLog"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        "Customer.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)
    purchase_items = db.relationship(
        "PurchaseItem", backref="purchaselog", lazy=True, cascade="all, delete")

    def __init__(self, customer_id, timestamp):
        self.timestamp = timestamp
        self.customer_id = customer_id


class PurchaseLogSchema(ma.Schema):
    id = fields.Integer()
    customer_id = fields.Integer()
    timestamp = fields.DateTime()


purchase_log_schema = PurchaseLogSchema()
purchase_logs_schema = PurchaseLogSchema(many=True)


class PurchaseLogSchema2(ma.Schema):
    id = fields.Integer()
    customer_id = fields.Integer()
    timestamp = fields.DateTime()
    fields = fields.List(fields.Nested(PurchaseItemSchema(only=(
        "id", "product_id", "field_id", "price", "start_time", "end_time"
        ))))


purchase_log2_schema = PurchaseLogSchema2()
purchase_log2s_schema = PurchaseLogSchema2(many=True)


class TimingDiscount(db.Model):
    __tablename__ = "TimingDiscount"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    discount_type = db.Column(db.String(200), nullable=False)
    discount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, default=False)
    # promo_codes = db.relationship("PromoCode", backref="timingdiscount", lazy=True)

    def __init__(self, start_time, end_time, discount_type, discount, status):
        self.start_time = start_time
        self.end_time = end_time
        self.discount_type = discount_type
        self.discount = discount
        self.status = status


class TimingDiscountSchema(ma.Schema):
    id = fields.Integer()
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)
    discount_type = fields.String(required=True)
    discount = fields.Float(required=True)
    status = fields.Boolean()


timingdiscount_schema = TimingDiscountSchema()
timingdiscounts_schema = TimingDiscountSchema(many=True)


def insert_data(target, connection, **kw):
    connection.execute(target.insert(), {'id': 1, 'start_time': '12:00', 'end_time': '13:00', 'discount_type': 'Percent', 'discount': 20, 'status': False})


event.listen(TimingDiscount.__table__, 'after_create', insert_data)


class Venue(db.Model):
    __tablename__ = "Venue"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False, unique=True) # "Kallang05"
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False) 
    updated_at = db.Column(db.DateTime, nullable=False, onupdate=datetime.now)
    # odoo_id = db.Column(db.Integer, nullable=False)
    fields = db.relationship("Field", backref="venue", lazy=True, cascade="all, delete")
    promo_code_valid_locations = db.relationship(
        "PromoCodeValidLocation", backref="venue", lazy=True, cascade="all, delete"
    )
    cart_item = db.relationship("CartItem", backref="venue", lazy=True, cascade="all, delete")

    def __init__(self, name, created_at, updated_at):
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        # self.odoo_id = odoo_id
        self.fields = []
        self.promo_code_valid_locations = []


class VenueSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    # odoo_id = fields.Integer(required=True)


venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)


class VenueSchema2(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    fields = fields.List(fields.Nested(FieldSchema(only=("id", "name", "field_type"))))


venue2_schema = VenueSchema2()
venue2s_schema = VenueSchema2(many=True)
