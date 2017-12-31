# -*- coding: utf-8 -*-

from extensions import db

__all__ = ['product_basic_info', 'stock_summary','delivery_statistics', \
            'receiving_statistics', 'supplier_basic_info', 'supplier_available_product',\
             'customer_basic_info', 'sale_order_summary', 'sale_order_detail', \
             'purchase_order_summary','purchase_order_detail','customer_register_info',\
             'sys_user_info','purview_set']

#1.1
class product_basic_info(db.Model):
    __tablename__ = 'product_basic_info'
    product_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(16), nullable=False, server_default='', unique=True)
    product_format = db.Column(db.String(16), nullable=False, server_default='')
    sale_price = db.Column(db.Float, nullable=False)
    product_image = db.Column(db.LargeBinary(length=2048), nullable=True)
    product_introduction = db.Column(db.Text, nullable=True)

    def __init__(self, product_id, product_name, product_format, sale_price, product_image, product_introduction):
        self.product_id = product_id
        self.product_name = product_name
        self.product_format = product_format
        self.sale_price = sale_price
        self.product_image = product_image
        self.product_introduction = product_introduction

    
#1.2
class stock_summary(db.Model):
    __tablename__ = 'stock_summary'
    product_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    inventory_quantity = db.Column(db.Integer, nullable=False)
    reorder_point = db.Column(db.Integer, nullable=False)
    order_volume_automatic = db.Column(db.Integer, nullable=False)

    def __init__(self, product_id, inventory_quantity, reorder_point, order_volume_automatic):
        self.product_id = product_id
        self.inventory_quantity = inventory_quantity
        self.reorder_point = reorder_point
        self.order_volume_automatic = order_volume_automatic

#1.6
class delivery_statistics(db.Model):
    __tablename__ = 'delivery_statistics'
    sale_order_number = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    sale_order_item_number = db.Column(db.Integer, nullable=False, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    delivery_quantity = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    customer_address = db.Column(db.String(30), nullable=False)
    deliver_time = db.Column(db.DateTime, nullable=False)
    delivery_operator = db.Column(db.String(30), nullable=False)
    delivery_remarks = db.Column(db.String(30), nullable=False)

    def __init__(self, sale_order_number, sale_order_item_number, product_id, delivery_quantity, customer_id, customer_address,deliver_time, delivery_operator,delivery_remarks):
        self.sale_order_number = sale_order_number
        self.sale_order_item_number = sale_order_item_number
        self.product_id = product_id
        self.delivery_quantity = delivery_quantity
        self.customer_id = customer_id
        self.customer_address = customer_address
        self.deliver_time = deliver_time
        self.delivery_operator = delivery_operator
        self.delivery_remarks = delivery_remarks

#1.7
class receiving_statistics(db.Model):
    __tablename__ = 'receiving_statistics'
    purchase_order_number = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    purchase_order_item_number = db.Column(db.Integer, nullable=False, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    receipt_quantity = db.Column(db.Integer, nullable=False)
    supplier_id = db.Column(db.Integer, nullable=False)
    receipt_time = db.Column(db.DateTime, nullable=False)
    receipt_operator = db.Column(db.String(10), nullable=False)
    receipt_remarks = db.Column(db.String(30), nullable=False)

    def __init__(self, purchase_order_number, purchase_order_item_number, product_id, receipt_quantity, supplier_id, receipt_time,receipt_operator, receipt_remarks):
        self.purchase_order_number = purchase_order_number
        self.purchase_order_item_number = purchase_order_item_number
        self.product_id = product_id
        self.receipt_quantity = receipt_quantity
        self.supplier_id = supplier_id
        self.receipt_time = receipt_time
        self.receipt_operator = receipt_operator
        self.receipt_remarks = receipt_remarks
      
#2.1 
class supplier_basic_info(db.Model):
    __tablename__ = 'supplier_basic_info'
    supplier_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    supplier_name = db.Column(db.String(30), nullable=False)
    supplier_address = db.Column(db.String(50), nullable=False)
    supplier_phone = db.Column(db.String(20), nullable=False)
    supplier_email = db.Column(db.String(20), nullable=False)
    supplier_add_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, supplier_id, supplier_name, supplier_address, supplier_phone, supplier_email, supplier_add_time):
        self.supplier_id = supplier_id
        self.supplier_name = supplier_name
        self.supplier_address = supplier_address
        self.supplier_phone = supplier_phone
        self.supplier_email = supplier_email
        self.supplier_add_time = supplier_add_time

#2.2
class supplier_available_product(db.Model):
    __tablename__ = 'supplier_available_product'
    supplier_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, nullable=False, primary_key=True)
    purchase_price = db.Column(db.Float, nullable=False)

    def __init__(self, supplier_id, product_id, purchase_price):
        self.supplier_id = supplier_id
        self.product_id = product_id
        self.purchase_price = purchase_price


#3.1 
class customer_basic_info(db.Model):
    __tablename__ = 'customer_basic_info'
    customer_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(30), nullable=False)
    customer_address = db.Column(db.String(50), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_email = db.Column(db.String(20), nullable=False)
    customer_register_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, customer_id, customer_name, customer_address, customer_phone, customer_email, customer_register_time):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.customer_address = customer_address
        self.customer_phone = customer_phone
        self.customer_email = customer_email
        self.customer_register_time = customer_register_time


#4.1
class sale_order_summary(db.Model):
    __tablename__ = 'sale_order_summary'
    sale_order_number = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, nullable=False)
    sale_order_total_item_num = db.Column(db.Integer, nullable=False)
    sale_order_total_price = db.Column(db.Float, nullable=False)
    sale_order_status = db.Column(db.String(15), nullable=False)
    sale_order_create_time = db.Column(db.DateTime, nullable=False)
    sale_order_submit_time = db.Column(db.DateTime, nullable=False)
    sale_order_receive_time = db.Column(db.DateTime, nullable=False)
    sale_order_pay_time = db.Column(db.DateTime, nullable=False)
    pay_remind_time = db.Column(db.Integer, nullable=False)

    def __init__(self, sale_order_number, customer_id, sale_order_total_item_num, sale_order_total_price, sale_order_status, sale_order_create_time,sale_order_submit_time,sale_order_receive_time,sale_order_pay_time,pay_remind_time):
        self.sale_order_number = sale_order_number
        self.customer_id = customer_id
        self.sale_order_total_item_num = sale_order_total_item_num
        self.sale_order_total_price = sale_order_total_price
        self.sale_order_status = sale_order_status
        self.sale_order_create_time = sale_order_create_time
        self.sale_order_submit_time = sale_order_submit_time
        self.sale_order_receive_time = sale_order_receive_time
        self.sale_order_pay_time = sale_order_pay_time
        self.pay_remind_time = pay_remind_time


    # 采购订单编号 purchase_order_number
    # 供应商代码 supplier_id
    # 采购条目总数 purchase_order_total_item_num
    # 采购订单总金额 purchase_order_total_price
    # 采购订单状态 purchase_order_status
    # 采购订单创建时间 purchase_order_create_time
    # 采购订单提交时间 purchase_order_submit_time
    # 采购订单收货时间 purchase_order_receive_time
    # 采购订单付款时间 purchase_order_pay_time

#4.2
class sale_order_detail(db.Model):
    __tablename__ = 'sale_order_detail'
    sale_order_number = db.Column(db.Integer, nullable=False, primary_key=True)
    sale_order_item_number = db.Column(db.Integer, nullable=False, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    sale_amount = db.Column(db.Integer, nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    total_price_this_item = db.Column(db.Float, nullable=False)
    sale_item_status = db.Column(db.String(15), nullable=False)

    def __init__(self, sale_order_number, sale_order_item_number, product_id, sale_amount, sale_price, total_price_this_item,sale_item_status):
        self.sale_order_number = sale_order_number
        self.sale_order_item_number = sale_order_item_number
        self.product_id = product_id
        self.sale_amount = sale_amount
        self.sale_price = sale_price
        self.total_price_this_item = total_price_this_item
        self.sale_item_status = sale_item_status

    # 采购订单编号 purchase_order_number
    # 采购条目编号 purchase_order_item_number
    # 产品代码 product_id
    # 购买量 purchase_amount
    # 采购价格 purchase_price
    # 本条目总价 total_price_this_item
    # 本条目状态 purchase_item_status

#4.3
class purchase_order_summary(db.Model):
    __tablename__ = 'purchase_order_summary'
    purchase_order_number = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    supplier_id = db.Column(db.Integer, nullable=False)
    purchase_order_total_item_num = db.Column(db.Integer, nullable=False)
    purchase_order_total_price = db.Column(db.Float, nullable=False)
    purchase_order_status = db.Column(db.String(15), nullable=False)
    purchase_order_create_time = db.Column(db.DateTime, nullable=False)
    purchase_order_submit_time = db.Column(db.DateTime, nullable=False)
    purchase_order_receive_time = db.Column(db.DateTime, nullable=False)
    purchase_order_pay_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, purchase_order_number, supplier_id, purchase_order_total_item_num, purchase_order_total_price, purchase_order_status, purchase_order_create_time,purchase_order_submit_time,purchase_order_receive_time,purchase_order_pay_time):
        self.purchase_order_number = purchase_order_number
        self.supplier_id = supplier_id
        self.purchase_order_total_item_num = purchase_order_total_item_num
        self.purchase_order_total_price = purchase_order_total_price
        self.purchase_order_status = purchase_order_status
        self.purchase_order_create_time = purchase_order_create_time
        self.purchase_order_submit_time = purchase_order_submit_time
        self.purchase_order_receive_time = purchase_order_receive_time
        self.purchase_order_pay_time = purchase_order_pay_time

    # 采购订单编号 purchase_order_number
    # 供应商代码 supplier_id
    # 采购条目总数 purchase_order_total_item_num
    # 采购订单总金额 purchase_order_total_price
    # 采购订单状态 purchase_order_status
    # 采购订单创建时间 purchase_order_create_time
    # 采购订单提交时间 purchase_order_submit_time
    # 采购订单收货时间 purchase_order_receive_time
    # 采购订单付款时间 purchase_order_pay_time

#4.4
class purchase_order_detail(db.Model):
    __tablename__ = 'purchase_order_detail'
    purchase_order_number = db.Column(db.Integer, nullable=False, primary_key=True)
    purchase_order_item_number = db.Column(db.Integer, nullable=False, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    purchase_amount = db.Column(db.Integer, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    total_price_this_item = db.Column(db.Float, nullable=False)
    purchase_item_status = db.Column(db.String(15), nullable=False)
 
    def __init__(self, purchase_order_number, purchase_order_item_number, product_id, purchase_amount, purchase_price, total_price_this_item,purchase_item_status):
        self.purchase_order_number = purchase_order_number
        self.purchase_order_item_number = purchase_order_item_number
        self.product_id = product_id
        self.purchase_amount = purchase_amount
        self.purchase_price = purchase_price
        self.total_price_this_item = total_price_this_item
        self.purchase_item_status = purchase_item_status

    # 采购订单编号 purchase_order_number
    # 采购条目编号 purchase_order_item_number
    # 产品代码 product_id
    # 购买量 purchase_amount
    # 采购价格 purchase_price
    # 本条目总价 total_price_this_item
    # 本条目状态 purchase_item_status

#5.1
class customer_register_info(db.Model):
    __tablename__ = 'customer_register_info'
    customer_id = db.Column(db.Integer, nullable=False, primary_key=True)
    customer_login_name = db.Column(db.String(30), nullable=False)
    customer_password = db.Column(db.String(30), nullable=False)
    customer_purview = db.Column(db.Integer, nullable=False)

    def __init__(self, customer_id, customer_login_name, customer_password,customer_purview):
        self.customer_id = customer_id
        self.customer_login_name = customer_login_name
        self.customer_password = customer_password
        self.customer_purview = customer_purview

    # 客户代码 customer_id
    # 客户登陆名 customer_login_name
    # 客户密码 customer_password
    # 客户权限 customer_purview

#5.2
class sys_user_info(db.Model):
    __tablename__ = 'sys_user_info'
    user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_login_name = db.Column(db.String(30), nullable=False)
    user_password = db.Column(db.String(30), nullable=False)
    user_purview = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, user_login_name, user_password,user_purview):
        self.user_id = user_id
        self.user_login_name = ususer_login_nameer_id
        self.user_password = user_password
        self.user_purview = user_purview

    # 系统用户代码 user_id
    # 用户登陆名 user_login_name
    # 用户密码 user_password
    # 用户权限 user_purview

#5.3
class purview_set(db.Model):
    __tablename__ = 'purview_set'
    purview_id = db.Column(db.Integer, nullable=False, primary_key=True)
    purview_description = db.Column(db.String(30), nullable=False)

    def __init__(self, purview_id, purview_description):
        self.purview_id = purview_id
        self.purview_description = purview_description

    # 权限代码 purview_id
    # 权限内容 purview_description
