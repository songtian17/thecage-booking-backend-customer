# app/models.py
from datetime import datetime
from service import db, ma
from marshmallow import fields


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


class Announcement(db.Model):
    __tablename__ = "Announcement"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    markdown_string = db.Column(db.String(200), nullable=False)
    placement = db.Column(db.String(200), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self, markdown_string, placement, updated_at):
        self.markdown_string = markdown_string
        self.placement = placement
        self.updated_at = updated_at


class AnnouncementSchema(ma.Schema):
    id = fields.Integer()
    markdown_string = fields.String(required=True)
    placement = fields.String(required=True)
    updated_at = fields.DateTime()


announcement_schema = AnnouncementSchema()
announcements_schema = AnnouncementSchema(many=True)


class CustomTimeSlot(db.Model):
    __tablename__ = "CustomTimeSlot"
    start_time = db.Column(db.Time, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey("Field.id"), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self, start_time, duration, created_at, updated_at):
        self.start_time = start_time
        self.duration = duration
        self.created_at = created_at
        self.updated_at = updated_at


class CustomTimeSlotSchema(ma.Schema):
    start_time = fields.Time(required=True)
    field_id = fields.Integer()
    duration = fields.Integer(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


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
        "CustomerOdoo", backref="customer", lazy=True)
    purchase_logs = db.relationship(
        "PurchaseLog", backref="customer", lazy=True)
    promocode_logs = db.relationship(
        "PromoCodeLog", backref="customer", lazy=True)

    def __init__(self, email, password, name, phone_no):
        self.email = email
        self.password = password
        self.name = name
        self.phone_no = phone_no


class CustomerSchema(ma.Schema):
    id = fields.Integer()
    email = fields.String(required=True)
    name = fields.String(required=True)
    password = fields.String(required=True)
    phone_no = fields.String(required=True)


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


class CustomerOdoo(db.Model):
    __tablename__ = "CustomerOdoo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(
        db.Integer, db.ForeignKey("Customer.id"), nullable=False)
    odoo_id = db.Column(db.Integer, nullable=False, autoincrement=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)

    def __init__(self, venue_id):
        self.venue_id = venue_id
        self.odoo_id = odoo_id
        self.customer_id = customer_id


class CustomerOdooSchema(ma.Schema):
    id = fields.Integer()
    customer_id = fields.Integer()
    odoo_id = fields.Integer()
    venue_id = fields.Integer()


customer_odoo_schema = CustomerOdooSchema()
customer_odoos_schema = CustomerOdooSchema(many=True)


class Discount(db.Model):
    __tablename__ = "Discount"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    discount_type = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timing_discounts = db.relationship(
        "TimingDiscount", backref="discount", lazy=True, uselist=False
    )
    promo_codes = db.relationship("PromoCode", backref="discount", lazy=True)

    def __init__(self, discount_type, amount):
        self.discount_type = discount_type
        self.amount = amount


class DiscountSchema(ma.Schema):
    id = fields.Integer()
    discount_type = fields.String(required=True)
    amount = fields.Float(required=True)


discount_schema = DiscountSchema()
discounts_schema = DiscountSchema(many=True)


class Field(db.Model):
    __tablename__ = "Field"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False, unique=True)
    num_pitches = db.Column(db.Integer, nullable=False)
    colour = db.Column(db.String(7))
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now, nullable=False)
    custom_timeslots = db.relationship(
        "CustomTimeSlot", backref="field", lazy=True)
    pitches = db.relationship("Pitch", backref="Pitch", lazy=True, cascade="all, delete")

    def __init__(self, name, venue_id, num_pitches, colour, created_at, updated_at):
        self.name = name
        self.venue_id = venue_id
        self.num_pitches = num_pitches
        self.colour = colour
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.pitches = []
        self.custom_timeslots = []


class FieldSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    venue_id = fields.Integer()
    num_pitches = fields.Integer()
    colour = fields.String(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


field_schema = FieldSchema()
fields_schema = FieldSchema(many=True)


class FieldSchema3(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    venue_id = fields.Integer()
    colour = fields.String(required=True)
    num_pitches = fields.Integer()


field3_schema = FieldSchema3()
fields3_schema = FieldSchema3(many=True)


class Pitch(db.Model):
    __tablename__ = "Pitch"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    field_id = db.Column(db.Integer, db.ForeignKey("Field.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False, unique=True)

    def __init__(self, name, field_id):
        self.name = name
        self.field_id = field_id


class PitchSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    field_id = fields.Integer()


pitch_schema = PitchSchema()
pitches_schema = PitchSchema(many=True)


class FieldSchema2(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    pitches = fields.List(fields.Nested(PitchSchema(only=("id", "name"))))


field2_schema = FieldSchema2()
fields2_schema = FieldSchema2(many=True)


class Product(db.Model):
    __tablename__ = "Product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    odoo_id = db.Column(db.Integer, nullable=False)
    promo_code_valid_products = db.relationship(
        "PromoCodeValidProduct", backref="product", lazy=True
    )
    purchase_items = db.relationship(
        "PurchaseItem", backref="product", lazy=True)

    def __init__(self, name, price, odoo_id):
        self.name = name
        self.price = price
        self.odoo_id = odoo_id


class ProductSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    price = fields.Float(required=True)
    odoo_id = fields.Integer(required=True)


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


class PromoCode(db.Model):
    __tablename__ = "PromoCode"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    discount_id = db.Column(db.Integer, db.ForeignKey(
        "Discount.id"), nullable=False)
    code = db.Column(db.String(200), unique=True, nullable=False)
    valid_from = db.Column(db.DateTime, default=datetime.now, nullable=False)
    valid_to = db.Column(db.DateTime, default=datetime.now, nullable=False)
    usage_limit = db.Column(db.Integer, nullable=False)
    uses_left = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    promo_code_logs = db.relationship(
        "PromoCodeLog", backref="promocode", lazy=True)
    promo_code_valid_products = db.relationship(
        "PromoCodeValidProduct", backref="promocode", lazy=True
    )
    promo_code_valid_timings = db.relationship(
        "PromoCodeValidTiming", backref="promocode", lazy=True
    )
    promo_code_valid_locations = db.relationship(
        "PromoCodeValidLocation", backref="promocode", lazy=True
    )

    def __init__(self, code, valid_from, valid_to, usage_limit, uses_left):
        self.code = code
        self.valid_from = valid_from
        self.valid_to = valid_to
        self.usage_limit = usage_limit
        self.uses_left = uses_left


class PromoCodeSchema(ma.Schema):
    id = fields.Integer()
    discount_id = fields.Integer()
    code = fields.String(required=True)
    valid_from = fields.DateTime(required=True)
    valid_to = fields.DateTime(required=True)
    usage_limit = fields.Integer(required=True)
    uses_left = fields.Integer(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


promo_code_schema = PromoCodeSchema()
promo_codes_schema = PromoCodeSchema(many=True)


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

    def __init__(self, name):
        self.name = name


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

    def __init__(self, name):
        self.name = name


class PromoCodeValidProductSchema(ma.Schema):
    id = fields.Integer()
    promo_code_id = fields.Integer()
    product_id = fields.Integer()
    name = fields.String(required=True)


promo_code_valid_product_schema = PromoCodeValidProductSchema()
promo_code_valid_products_schema = PromoCodeValidProductSchema(many=True)


class PromoCodeValidTiming(db.Model):
    __tablename__ = "PromoCodeValidTiming"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    promo_code_id = db.Column(db.Integer, db.ForeignKey(
        "PromoCode.id"), nullable=False)
    day_of_week = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def __init__(self, start_time, end_time, day_of_week):
        self.start_time = start_time
        self.end_time = end_time
        self.day_of_week = day_of_week


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
    price = db.Column(db.Float, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    def __init__(self, price, start_time, end_time):
        self.price = price
        self.start_time = start_time
        self.end_time = end_time


class PurchaseItemSchema(ma.Schema):
    id = fields.Integer()
    purchase_log_id = fields.Integer()
    product_id = fields.Integer()
    field_id = fields.Integer()
    price = fields.Float(required=True)
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)


purchase_item_schema = PurchaseItemSchema()
purchase_items_schema = PurchaseItemSchema(many=True)


class PurchaseLog(db.Model):
    __tablename__ = "PurchaseLog"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        "Customer.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)
    purchase_items = db.relationship(
        "PurchaseItem", backref="purchaselog", lazy=True)

    def __init__(self, timestamp):
        self.timestamp = timestamp


class PurchaseLogSchema(ma.Schema):
    id = fields.Integer()
    customer_id = fields.Integer()
    timestamp = fields.DateTime()


purchase_log_schema = PurchaseLogSchema()
purchase_logs_schema = PurchaseLogSchema(many=True)


class TimingDiscount(db.Model):
    __tablename__ = "TimingDiscount"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    discount_id = db.Column(db.Integer, db.ForeignKey(
        "Discount.id"), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(200), nullable=False)

    def __init__(self, start_time, end_time, status):
        self.start_time = start_time
        self.end_time = end_time
        self.status = status


class TimingDiscountSchema(ma.Schema):
    id = fields.Integer()
    discount_id = fields.Integer()
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)
    status = fields.String(required=True)


timing_discount_schema = TimingDiscountSchema()
timing_discounts_schema = TimingDiscountSchema(many=True)


class Venue(db.Model):
    __tablename__ = "Venue"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, onupdate=datetime.now)
    fields = db.relationship("Field", backref="venue", lazy=True, cascade="all, delete")
    promo_code_valid_locations = db.relationship(
        "PromoCodeValidLocation", backref="venue", lazy=True
    )

    def __init__(self, name, created_at, updated_at):
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.fields = []
        self.promo_code_valid_locations = []


class VenueSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)


class VenueSchema2(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    fields = fields.List(fields.Nested(FieldSchema(only=("id", "name"))))


venue2_schema = VenueSchema2()
venue2s_schema = VenueSchema2(many=True)
