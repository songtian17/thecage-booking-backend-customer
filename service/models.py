# app/models.py
from datetime import datetime
from service import db, ma
from marshmallow import fields

class Admin(db.Model):
    __tablename__ = "Admin"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200), nullable=False)

    def __init__(self, user_id, password, name, role):
        self.user_id = user_id
        self.password = password
        self.name = name
        self.role = role
        # self.email = email


class AdminSchema(ma.Schema):
    id = fields.Integer()
    user_id = fields.String(required=True)
    name = fields.String(required=True)
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
    class Meta:
        fields = ('id', 'markdown_string', 'placement', 'updated_at')


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
    class Meta:
        fields = ('start_time', 'field_id', 'duration', 'created_at', 'updated_at')


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


class CustomerOdoo(db.Model):
    __tablename__ = "CustomerOdoo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(
        db.Integer, db.ForeignKey("Customer.id"), nullable=False)
    odoo_id = db.Column(db.Integer, nullable=False, autoincrement=True)
    venue = db.Column(db.String(200), nullable=False)

    def __init__(self, venue):
        self.venue = venue


class CustomerOdooSchema(ma.Schema):
    class Meta:
        fields = ('id', 'customer_id', 'odoo_id', 'venue')


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
    class Meta:
        fields = ('id', 'discount_type', 'amount')


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
    pitches = db.relationship("Pitch", backref="Pitch", lazy=True)

    def __init__(self, name, venue_id, num_pitches, colour, created_at, updated_at):
        self.name = name
        self.venue_id = venue_id
        self.num_pitches = num_pitches
        self.colour = colour
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


class FieldSchema(ma.Schema):
    class Meta:
        fields = ('id', 'venue_id', 'name', 'num_pitches', 'colour', 'created_at', 'updated_at')


field_schema = FieldSchema()
fields_schema = FieldSchema(many=True)


class Pitch(db.Model):
    __tablename__ = "Pitch"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    field_id = db.Column(db.Integer, db.ForeignKey("Field.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False, unique=True)

    def __init__(self, name, field_id):
        self.name = name
        self.field_id = field_id

    
class PitchSchema(ma.Schema):
    class Meta:
        fields = ('id', 'field_id', 'name')


pitch_schema = PitchSchema()
pitches_schema = PitchSchema(many=True)


class Product(db.Model):
    __tablename__ = "Product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    promo_code_valid_products = db.relationship(
        "PromoCodeValidProduct", backref="product", lazy=True
    )
    purchase_items = db.relationship(
        "PurchaseItem", backref="product", lazy=True)

    def __init__(self, name, price):
        self.name = name
        self.price = price


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price')


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
    class Meta:
        fields = ('id', 'discountid', 'code', 'valid_from', 'valid_to', 'usage_limit', 'uses_left', 'created_at', 'updated_at')


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
    class Meta:
        fields = ('id', 'promo_code_id', 'customer_id', 'timestamp')


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
    class Meta:
        fields = ('id', 'promo_code_id', 'venue_id', 'name')


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
    class Meta:
        fields = ('id', 'promo_code_id', 'product_id', 'name')


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
    class Meta:
        fields = ('id', 'promo_code_id', 'day_of_week', 'start_time', 'end_time')


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
    class Meta:
        fields = ('id', 'purchase_log_id', 'product_id', 'field_id', 'price', 'start_time', 'end_time')


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
    class Meta:
        fields = ('id', 'customer_id', 'timestamp')


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
    class Meta:
        fields = ('id', 'discount_id', 'start_time', 'end_time', 'status')


timing_discount_schema = TimingDiscountSchema()
timing_discounts_schema = TimingDiscountSchema(many=True)


class Venue(db.Model):
    __tablename__ = "Venue"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, onupdate=datetime.now)
    fields = db.relationship("Field", backref="venue", lazy=True)
    promo_code_valid_locations = db.relationship(
        "PromoCodeValidLocation", backref="venue", lazy=True
    )

    def __init__(self, name, created_at, updated_at):
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


class VenueSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'created_at', 'updated_at')


venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)


# class VenueSchema2(Schema):
#     name = fields.String()
#     id = fields.Integer()
#     fields = fields.Nested(FieldSchema(only=("name", "id")))
