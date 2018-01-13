# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
import AMC.model
from AMC.model import *
from AMC.extensions import db
import json
import csv
import os
import time
from datetime import date
from datetime import datetime

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

mod = Blueprint('sysadmin', __name__, url_prefix='/sysadmin')

def date2ts(date):
    return time.mktime(time.strptime(date, '%Y-%m-%d'))

def ts2datetime(ts):
    return time.strftime('%Y-%m-%d', time.localtime(ts))


@mod.route('/')
@mod.route('/login/', methods=['GET','POST'])
def login():
    #return render_template('admin/index.html')
    result = None
    if 'logged_in' in session and session['logged_in']:
        print "pop pop", session['logged_in'], session['user']
        session.pop('user', None)
        session.pop('logged_in', None)
    if request.method == 'POST':
        pas = db.session.query(sys_user_info).filter(sys_user_info.user_login_name==request.form['user']).all()
        if pas != []:
            for pa in pas:
                if request.form['para'] == pa.user_password:
                    result = 'Right'
            if result == 'Right':
                session['logged_in'] = 'Ture'
                print "SESSION POST ", session['logged_in']
                session['user'] = request.form['user']
                flash('登录成功！')
            else:
                result = 'Wrong_pass'
        return json.dumps(result)

    return render_template('admin/login.html', result = result)


@mod.route('/index/')
def show_index():
    if 'logged_in' in session and session['logged_in']:
        print "here index"
        return render_template('admin/index.html') 
    else:
        return redirect('/sysadmin/')

@mod.route('/order/')
def show_order():
    #print session['logged_in']
    if 'logged_in' in session and session['logged_in']:
        return render_template('admin/order.html') 
    else:
        return redirect('/sysadmin/')

@mod.route('/products/')
def show_products():
    if 'logged_in' in session and session['logged_in']:
        return render_template('admin/products.html') 
    else:
        return redirect('/sysadmin/')

@mod.route('/purchasing/')
def show_purchasing():   
    if 'logged_in' in session and session['logged_in']:
        return render_template('admin/purchasing.html') 
    else:
        return redirect('/sysadmin/')

@mod.route('/customer/')
def show_customer():    
    if 'logged_in' in session and session['logged_in']:
        return render_template('admin/customer.html')
    else:
        return redirect('/sysadmin/')

@mod.route('/authrity/')
def show_authrity():    
    if 'logged_in' in session and session['logged_in']:
        return render_template('admin/authrity.html')
    else:
        return redirect('/sysadmin/')

@mod.route('/delivery/')#发货管理
def show_delivery():    
    if 'logged_in' in session and session['logged_in']:
        return render_template('admin/delivery.html')
    else:
        return redirect('/sysadmin/')

@mod.route('/receiving/')#收货管理
def show_receiving():    
    if 'logged_in' in session and session['logged_in']:
        return render_template('admin/receiving.html')
    else:
        return redirect('/sysadmin/')

@mod.route('/stock/')#库存信息查询
def show_stock():    
    if 'logged_in' in session and session['logged_in']:
        return render_template('admin/stock.html')
    else:
        return redirect('/sysadmin/')


#=================================订单管理 order.html =========================================
@mod.route('/orders_rank/')#订单信息分页
def orders_rank():
    page = 1
    countperpage = 10
    limit = 1000000
    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('countperpage'):
        countperpage = int(request.args.get('countperpage'))
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    if page == 1:
        startoffset = 0
    else:
        startoffset = (page - 1) * countperpage
    endoffset = startoffset + countperpage
    newwords = db.session.query(sale_order_summary).filter().all()
    news=[]
    n = 0
    for newword in newwords:
        if newword:
            n = n + 1
            if n > startoffset:
                if n > endoffset:
                    break

                # if newword.sale_order_status in ("未提交".decode('utf-8')) ：
                if newword.sale_order_status != "未提交".decode('utf-8'):
                    news.append({'sale_order_number':newword.sale_order_number,'customer_id':newword.customer_id,'sale_order_total_price':newword.sale_order_total_price,'sale_order_status':newword.sale_order_status.encode('utf-8'),'sale_order_create_time':newword.sale_order_create_time})
    total_pages = limit / countperpage + 1
    return json.dumps({'news': news, 'pages': total_pages},cls=ComplexEncoder)



@mod.route('/orders_de', methods=['GET','POST'])#取消订单信息
def orders_de():
    result = 'Right'
    sale_order_number = request.form['f_id']
    #print sale_order_number

    old_items = db.session.query(sale_order_summary).filter(sale_order_summary.sale_order_number==sale_order_number).all()
    if len(old_items):
        for old_item in old_items:
            ##只有订单状态为“已提交”时可以取消订单
            if old_item.sale_order_status == "已提交".decode('utf-8'):
                print "yitijiao here"
                sale_order_number = old_item.sale_order_number
                customer_id = old_item.customer_id
                sale_order_total_item_num = old_item.sale_order_total_item_num
                sale_order_total_price = old_item.sale_order_total_price
                sale_order_status = "已取消"
                sale_order_create_time = old_item.sale_order_create_time
                sale_order_submit_time = old_item.sale_order_submit_time
                sale_order_deliver_time = old_item.sale_order_deliver_time
                sale_order_pay_time = old_item.sale_order_pay_time
                pay_remind_time = old_item.pay_remind_time

                db.session.delete(old_item)
                db.session.commit()

                new_item = sale_order_summary(sale_order_number, customer_id, sale_order_total_item_num, sale_order_total_price, sale_order_status, sale_order_create_time,sale_order_submit_time,sale_order_deliver_time,sale_order_pay_time,pay_remind_time)
                db.session.add(new_item)
                db.session.commit()

            else:
                result = old_item.sale_order_status.encode('utf-8')
            
    return json.dumps(result)


@mod.route('/order_detail/')#查看订单详情
def order_detail():
    return render_template('admin/order_detail_page.html')


@mod.route('/order_detail_rank/')#某一订单详情展示
def order_detail_rank():
    page = 1
    countperpage = 4
    limit = 1000000
    sale_order_number_thisPage = 1

    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('countperpage'):
        countperpage = int(request.args.get('countperpage'))
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    if request.args.get('sale_order_number'):
        sale_order_number_thisPage = request.args.get('sale_order_number')
    #print sale_order_number_thisPage
    if page == 1:
        startoffset = 0
    else:
        startoffset = (page - 1) * countperpage
    endoffset = startoffset + countperpage
    newwords = db.session.query(sale_order_detail).filter(sale_order_detail.sale_order_number == sale_order_number_thisPage).all()
    news=[]
    n = 0
    for newword in newwords:
        if newword:
            n = n + 1
            if n > startoffset:
                if n > endoffset:
                    break

                news.append({'sale_order_number':newword.sale_order_number,'sale_order_item_number':newword.sale_order_item_number,'product_id':newword.product_id,'sale_amount':newword.sale_amount,'sale_price':newword.sale_price,'total_price_this_item':newword.total_price_this_item,'sale_item_status':newword.sale_item_status.encode('utf-8')})
    total_pages = limit / countperpage + 1
    return json.dumps({'news': news, 'pages': total_pages})


@mod.route('/confirm_pay_sale/')#某销售订单确认收款
def confirm_pay_sale():
    #print "confirm pay here"
    if request.args.get('id'):
        sale_order_number_thisPage = int(request.args.get('id'))
    #print sale_order_number_thisPage

    old_items = db.session.query(sale_order_summary).filter(sale_order_summary.sale_order_number==sale_order_number_thisPage).all()
    if len(old_items):
        for old_item in old_items:
            sale_order_number = old_item.sale_order_number
            customer_id = old_item.customer_id
            sale_order_total_item_num = old_item.sale_order_total_item_num
            sale_order_total_price = old_item.sale_order_total_price
            sale_order_status = "已付款"
            sale_order_create_time = old_item.sale_order_create_time
            sale_order_submit_time = old_item.sale_order_submit_time
            sale_order_deliver_time = old_item.sale_order_deliver_time
            sale_order_pay_time = datetime.now()
            pay_remind_time = old_item.pay_remind_time

            db.session.delete(old_item)
            db.session.commit()
        new_item = sale_order_summary(sale_order_number, customer_id, sale_order_total_item_num, sale_order_total_price, sale_order_status, sale_order_create_time,sale_order_submit_time,sale_order_deliver_time,sale_order_pay_time,pay_remind_time)
        db.session.add(new_item)
        db.session.commit()

    return render_template('admin/order.html')


#=================================产品管理 products.html =========================================
@mod.route('/products_rank/')#产品信息分页
def products_rank():
    page = 1
    countperpage = 4
    limit = 1000000
    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('countperpage'):
        countperpage = int(request.args.get('countperpage'))
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    if page == 1:
        startoffset = 0
    else:
        startoffset = (page - 1) * countperpage
    endoffset = startoffset + countperpage
    newwords = db.session.query(product_basic_info).filter().all()
    news=[]
    n = 0
    for newword in newwords:
        if newword:
            n = n + 1
            if n > startoffset:
                if n > endoffset:
                    break

                news.append({'product_id':newword.product_id,'product_name':newword.product_name.encode('utf-8'),'product_format':newword.product_format.encode('utf-8'),'product_introduction':newword.product_introduction.encode('utf-8'),'sale_price':newword.sale_price})
    total_pages = limit / countperpage + 1
    return json.dumps({'news': news, 'pages': total_pages})


@mod.route('/products_de', methods=['GET','POST'])#删除产品信息
def products_de():
    result = 'Right'
    products_id = request.form['f_id']
    print products_id
    old_items = db.session.query(product_basic_info).filter(product_basic_info.product_id==products_id).all()
    if len(old_items):
        for old_item in old_items:
            db.session.delete(old_item)
            db.session.commit()
    else:
        result = 'Wrong'
    return json.dumps(result)


@mod.route('/products_price_mo', methods=['GET','POST'])#修改产品售价
def products_price_mo():
    new_id = request.form['id']
    price = int(request.form['price'])
    print new_id,price
    
    old_items = db.session.query(product_basic_info).filter(product_basic_info.product_id==new_id).all()
    if len(old_items):
        for old_item in old_items:
            product_id = old_item.product_id
            product_name = old_item.product_name
            product_format = old_item.product_format
            product_introduction = old_item.product_introduction
            db.session.delete(old_item)
            db.session.commit()
        new_item = product_basic_info(product_id, product_name, product_format, price, 11, product_introduction)
        db.session.add(new_item)
        db.session.commit()
        return json.dumps('Right')
    else:        
        return json.dumps('Wrong')


@mod.route('/product_add_info/')#增加一条产品信息
def product_add_info():
    return render_template('admin/product_add_info.html')


@mod.route('/add_product', methods=['GET','POST'])#添加产品信息
def add_product():
    product_id = request.form['product_id']
    product_name = request.form['product_name']
    sale_price = request.form['sale_price']
    product_format = request.form['product_format']
    product_image = request.form['product_image']
    product_introduction = request.form['product_introduction']
   

    old_items = db.session.query(product_basic_info).filter(product_basic_info.product_id==product_id).all()
    if len(old_items):
        return json.dumps('Wrong')
    else:
        new_item = product_basic_info(product_id, product_name,product_format, sale_price, product_image,product_introduction)
        db.session.add(new_item)
        db.session.commit()
        return json.dumps('Right')



#===========产品管理：供应商部分============================
@mod.route('/suppliers_rank/')#供应商信息分页
def suppliers_rank():
    page = 1
    countperpage = 3
    limit = 1000000
    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('countperpage'):
        countperpage = int(request.args.get('countperpage'))
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    if page == 1:
        startoffset = 0
    else:
        startoffset = (page - 1) * countperpage
    endoffset = startoffset + countperpage
    newwords = db.session.query(supplier_basic_info).filter().all()
    news=[]
    n = 0
    for newword in newwords:
        if newword:
            n = n + 1
            if n > startoffset:
                if n > endoffset:
                    break

                news.append({'supplier_id':newword.supplier_id,'supplier_name':newword.supplier_name.encode('utf-8'),'supplier_address':newword.supplier_address.encode('utf-8'),'supplier_phone':newword.supplier_phone.encode('utf-8'),'supplier_email':newword.supplier_email})
    total_pages = limit / countperpage + 1
    return json.dumps({'news': news, 'pages': total_pages})


@mod.route('/suppliers_de', methods=['GET','POST'])#删除供应商信息
def suppliers_de():
    result = 'Right'
    supplier_id = request.form['f_id']
    print supplier_id
    old_items = db.session.query(supplier_basic_info).filter(supplier_basic_info.supplier_id==supplier_id).all()
    if len(old_items):
        for old_item in old_items:
            db.session.delete(old_item)
            db.session.commit()
    else:
        result = 'Wrong'

    old_items = db.session.query(supplier_available_product).filter(supplier_available_product.supplier_id==supplier_id).all()
    if len(old_items):
        for old_item in old_items:
            db.session.delete(old_item)
            db.session.commit()
    else:
        result = 'Wrong'

    return json.dumps(result)


@mod.route('/supplier_add_info/')#增加一条供应商信息
def supplier_add_info():
    return render_template('admin/supplier_add_info.html')


@mod.route('/add_supplier', methods=['GET','POST'])#添加供应商信息
def add_supplier():
    supplier_id = request.form['supplier_id']
    supplier_name = request.form['supplier_name']
    supplier_address = request.form['supplier_address']
    supplier_phone = request.form['supplier_phone']
    supplier_email = request.form['supplier_email']
    supplier_add_time = request.form['supplier_add_time']
   

    old_items = db.session.query(supplier_basic_info).filter(supplier_basic_info.supplier_id==supplier_id).all()
    if len(old_items):
        return json.dumps('Wrong')
    else:
        new_item = supplier_basic_info(supplier_id, supplier_name, supplier_address, supplier_phone,supplier_email,supplier_add_time)
        db.session.add(new_item)
        db.session.commit()
        return json.dumps('Right')


######供货明细页面#####
@mod.route('/supplier_products/')#查看供应商供货明细
def supplier_products():
    return render_template('admin/supplier_products_detail.html')


@mod.route('/supply_detail_rank/')#某一供应商供货明细展示
def supply_detail_rank():
    page = 1
    countperpage = 10
    limit = 1000000
    supplier_id_thisPage = 1

    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('countperpage'):
        countperpage = int(request.args.get('countperpage'))
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    if request.args.get('supplier_id'):
        supplier_id_thisPage = request.args.get('supplier_id')
    #print supplier_id_thisPage
    if page == 1:
        startoffset = 0
    else:
        startoffset = (page - 1) * countperpage
    endoffset = startoffset + countperpage
    newwords = db.session.query(supplier_available_product).filter(supplier_available_product.supplier_id == supplier_id_thisPage).all()
    news=[]
    n = 0
    for newword in newwords:
        if newword:
            n = n + 1
            if n > startoffset:
                if n > endoffset:
                    break

                news.append({'supplier_id':newword.supplier_id,'product_id':newword.product_id,'purchase_price':newword.purchase_price})
    total_pages = limit / countperpage + 1
    return json.dumps({'news': news, 'pages': total_pages})


@mod.route('/suppplied_products_de', methods=['GET','POST'])#删除供应商供货信息
def suppplied_products_de():
    result = 'Right'
    supplier_id = request.form['supplier_id']
    product_id = request.form['product_id']
    print supplier_id
    print product_id
    old_items = db.session.query(supplier_available_product).filter(supplier_available_product.product_id==product_id,supplier_available_product.supplier_id==supplier_id).all()
    if len(old_items):
        for old_item in old_items:
            db.session.delete(old_item)
            db.session.commit()
    else:
        result = 'Wrong'
    return json.dumps(result)


@mod.route('/supplied_products_price_mo', methods=['GET','POST'])#修改供应商对产品的报价
def supplied_products_price_mo():
    supplier_id = request.form['supplier_id']
    product_id = request.form['product_id']
    price = int(request.form['price'])
  
    old_items = db.session.query(supplier_available_product).filter(supplier_available_product.product_id==product_id,supplier_available_product.supplier_id==supplier_id).all()
    if len(old_items):
        for old_item in old_items:
            product_id = old_item.product_id
            supplier_id = old_item.supplier_id
            purchase_price = old_item.purchase_price

            db.session.delete(old_item)
            db.session.commit()
        new_item = supplier_available_product(supplier_id, product_id, price)
        db.session.add(new_item)
        db.session.commit()
        return json.dumps('Right')
    else:        
        return json.dumps('Wrong')


@mod.route('/supplied_product_add_info/')#增加一条供应商供货信息
def supplied_product_add_info():
    return render_template('admin/supplied_product_add_info.html')


@mod.route('/add_supplied_product', methods=['GET','POST'])#添加供应商供货信息
def add_supplied_product():
    supplier_id = request.form['supplier_id']
    product_id = request.form['product_id']
    purchase_price = request.form['purchase_price']

    old_items = db.session.query(supplier_available_product).filter(supplier_available_product.product_id==product_id,supplier_available_product.supplier_id==supplier_id).all()
    if len(old_items):
        return json.dumps('Wrong')
    else:
        new_item = supplier_available_product(supplier_id, product_id, purchase_price)
        db.session.add(new_item)
        db.session.commit()
        return json.dumps('Right')




#=================================采购管理 purchasing.html =========================================
@mod.route('/purchasing_rank/')#采购订单信息分页
def purchasing_rank():
    page = 1
    countperpage = 10
    limit = 1000000
    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('countperpage'):
        countperpage = int(request.args.get('countperpage'))
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    if page == 1:
        startoffset = 0
    else:
        startoffset = (page - 1) * countperpage
    endoffset = startoffset + countperpage
    newwords = db.session.query(purchase_order_summary).filter().all()
    news=[]
    n = 0
    for newword in newwords:
        if newword:
            n = n + 1
            if n > startoffset:
                if n > endoffset:
                    break

                news.append({'purchase_order_number':newword.purchase_order_number,'supplier_id':newword.supplier_id,'purchase_order_total_price':newword.purchase_order_total_price,'purchase_order_status':newword.purchase_order_status.encode('utf-8'),'purchase_order_create_time':newword.purchase_order_create_time})
    total_pages = limit / countperpage + 1
    return json.dumps({'news': news, 'pages': total_pages},cls=ComplexEncoder)


@mod.route('/purchasing_de', methods=['GET','POST'])#取消采购订单
def purchasing_de():
    result = 'Right'
    purchase_order_number = request.form['f_id']
    #print purchase_order_number
    old_items = db.session.query(purchase_order_summary).filter(purchase_order_summary.purchase_order_number==purchase_order_number).all()
    if len(old_items):
        for old_item in old_items:
            ##只有订单状态为“已提交”时可以取消订单
            if old_item.purchase_order_status == "已提交".decode('utf-8'):
                print "yitijiao here"
                purchase_order_number = old_item.purchase_order_number
                supplier_id = old_item.supplier_id
                purchase_order_total_item_num = old_item.purchase_order_total_item_num
                purchase_order_total_price = old_item.purchase_order_total_price
                purchase_order_status = "已取消"
                purchase_order_create_time = old_item.purchase_order_create_time
                purchase_order_submit_time = old_item.purchase_order_submit_time
                purchase_order_receive_time = old_item.purchase_order_receive_time
                purchase_order_pay_time = old_item.purchase_order_pay_time
                
                db.session.delete(old_item)
                db.session.commit()

                new_item = purchase_order_summary(purchase_order_number, supplier_id, purchase_order_total_item_num, purchase_order_total_price, purchase_order_status, purchase_order_create_time,purchase_order_submit_time,purchase_order_receive_time,purchase_order_pay_time)
                db.session.add(new_item)
                db.session.commit()

            else:
                result = old_item.purchase_order_status.encode('utf-8')
            
    return json.dumps(result)
        



@mod.route('/purchasing_show_supplier/')#增加一条采购订单信息
def purchasing_show_supplier():
    return render_template('admin/purchasing_show_supplier.html')



@mod.route('/purchasing_suppliers_rank/')#供应商信息分页
def purchasing_suppliers_rank():
    page = 1
    countperpage = 4
    limit = 1000000
    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('countperpage'):
        countperpage = int(request.args.get('countperpage'))
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    if page == 1:
        startoffset = 0
    else:
        startoffset = (page - 1) * countperpage
    endoffset = startoffset + countperpage
    newwords = db.session.query(supplier_basic_info).filter().all()
    news=[]
    n = 0
    for newword in newwords:
        if newword:
            n = n + 1
            if n > startoffset:
                if n > endoffset:
                    break

                supplier_product_list = ""

                products_ids = db.session.query(supplier_available_product).filter(supplier_available_product.supplier_id == newword.supplier_id).all()
                for a_product in products_ids:
                    products_names = db.session.query(product_basic_info).filter(product_basic_info.product_id == a_product.product_id).all()                    
                    for a_product_item in products_names:
                        if supplier_product_list == "":
                            supplier_product_list = supplier_product_list + a_product_item.product_name
                        else:
                            supplier_product_list = supplier_product_list+ "; " + a_product_item.product_name

                news.append({'supplier_id':newword.supplier_id,'supplier_name':newword.supplier_name.encode('utf-8'),'supplier_address':newword.supplier_address.encode('utf-8'),'supplier_phone':newword.supplier_phone.encode('utf-8'),'supplier_email':newword.supplier_email,"supplier_product_list":supplier_product_list})
    total_pages = limit / countperpage + 1
    return json.dumps({'news': news, 'pages': total_pages})



@mod.route('/purchasing_supplier_products/')#点击创建订单按钮后跳转到供应商供货明细
def purchasing_supplier_products():
    return render_template('admin/purchasing_supplier_products_detail.html')

'''
@mod.route('/supply_detail_rank/')#某一供应商供货明细展示
def supply_detail_rank():
    page = 1
    countperpage = 10
    limit = 1000000
    supplier_id_thisPage = 1

    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('countperpage'):
        countperpage = int(request.args.get('countperpage'))
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    if request.args.get('supplier_id'):
        supplier_id_thisPage = int(request.args.get('supplier_id'))
    #print supplier_id_thisPage
    if page == 1:
        startoffset = 0
    else:
        startoffset = (page - 1) * countperpage
    endoffset = startoffset + countperpage
    newwords = db.session.query(supplier_available_product).filter(supplier_available_product.supplier_id == supplier_id_thisPage).all()
    news=[]
    n = 0
    for newword in newwords:
        if newword:
            n = n + 1
            if n > startoffset:
                if n > endoffset:
                    break

                news.append({'supplier_id':newword.supplier_id,'product_id':newword.product_id,'purchase_price':newword.purchase_price})
    total_pages = limit / countperpage + 1
    return json.dumps({'news': news, 'pages': total_pages})
'''

#here2




@mod.route('/purchasing_detail/')#查看采购订单详情
def purchasing_detail():
    return render_template('admin/purchasing_detail_page.html')


@mod.route('/purchasing_detail_rank/')#某一采购订单详情展示
def purchasing_detail_rank():
    page = 1
    countperpage = 4
    limit = 1000000
    purchase_order_number_thisPage = 1

    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('countperpage'):
        countperpage = int(request.args.get('countperpage'))
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    if request.args.get('purchase_order_number'):
        purchase_order_number_thisPage = request.args.get('purchase_order_number')
    #print purchase_order_number_thisPage
    if page == 1:
        startoffset = 0
    else:
        startoffset = (page - 1) * countperpage
    endoffset = startoffset + countperpage
    newwords = db.session.query(purchase_order_detail).filter(purchase_order_detail.purchase_order_number == purchase_order_number_thisPage).all()
    news=[]
    n = 0
    for newword in newwords:
        if newword:
            n = n + 1
            if n > startoffset:
                if n > endoffset:
                    break

                news.append({'purchase_order_number':newword.purchase_order_number,'purchase_order_item_number':newword.purchase_order_item_number,'product_id':newword.product_id,'purchase_amount':newword.purchase_amount,'purchase_price':newword.purchase_price,'total_price_this_item':newword.total_price_this_item,'purchase_item_status':newword.purchase_item_status.encode('utf-8')})
    total_pages = limit / countperpage + 1
    return json.dumps({'news': news, 'pages': total_pages})


@mod.route('/confirm_pay_purchasing/')#某采购订单确认付款
def confirm_pay_purchasing():
    #print "confirm pay here"
    if request.args.get('id'):
        purchase_order_number_thisPage = request.args.get('id')
    #print sale_order_number_thisPage

    old_items = db.session.query(purchase_order_summary).filter(purchase_order_summary.purchase_order_number==purchase_order_number_thisPage).all()
    if len(old_items):
        for old_item in old_items:
            purchase_order_number = old_item.purchase_order_number
            supplier_id = old_item.supplier_id
            purchase_order_total_item_num = old_item.purchase_order_total_item_num
            purchase_order_total_price = old_item.purchase_order_total_price
            purchase_order_status = "已付款"
            purchase_order_create_time = old_item.purchase_order_create_time
            purchase_order_submit_time = old_item.purchase_order_submit_time
            purchase_order_receive_time = old_item.purchase_order_receive_time
            purchase_order_pay_time = datetime.now()

            db.session.delete(old_item)
            db.session.commit()
        new_item = purchase_order_summary(purchase_order_number, supplier_id, purchase_order_total_item_num, purchase_order_total_price, purchase_order_status, purchase_order_create_time,purchase_order_submit_time,purchase_order_receive_time,purchase_order_pay_time)
        db.session.add(new_item)
        db.session.commit()

    return render_template('admin/purchasing.html')


#=================================客户管理 customer.html==========================================
@mod.route('/customers_rank/')#客户信息分页
def customers_rank():
    page = 1
    countperpage = 10
    limit = 1000000
    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('countperpage'):
        countperpage = int(request.args.get('countperpage'))
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    if page == 1:
        startoffset = 0
    else:
        startoffset = (page - 1) * countperpage
    endoffset = startoffset + countperpage
    newwords = db.session.query(customer_basic_info).filter().all()
    news=[]
    n = 0
    for newword in newwords:
        if newword:
            n = n + 1
            if n > startoffset:
                if n > endoffset:
                    break

                news.append({'customer_id':newword.customer_id,'customer_name':newword.customer_name.encode('utf-8'),'customer_register_time':newword.customer_register_time,'customer_address':newword.customer_address.encode('utf-8'),'customer_phone':newword.customer_phone})
    total_pages = limit / countperpage + 1
    print news
    return json.dumps({'news': news, 'pages': total_pages},cls=ComplexEncoder)


@mod.route('/customers_de', methods=['GET','POST'])#删除客户信息
def customers_de():
    result = 'Right'
    customers_id = request.form['f_id']
    print customers_id
    old_items = db.session.query(customer_basic_info).filter(customer_basic_info.customer_id==customers_id).all()
    if len(old_items):
        for old_item in old_items:
            db.session.delete(old_item)
            db.session.commit()
    else:
        result = 'Wrong'
    return json.dumps(result)


@mod.route('/customers_phone_mo', methods=['GET','POST'])#修改客户联系方式
def customers_phone_mo():
    new_id = request.form['id']
    phone = str(request.form['phone'])
    print new_id,phone
    
    old_items = db.session.query(customer_basic_info).filter(customer_basic_info.customer_id==new_id).all()
    if len(old_items):
        for old_item in old_items:
            customer_id = old_item.customer_id
            customer_name = old_item.customer_name
            customer_address = old_item.customer_address
            customer_email = old_item.customer_email
            customer_register_time = old_item.customer_register_time
            db.session.delete(old_item)
            db.session.commit()
        new_item = customer_basic_info(customer_id, customer_name, customer_address, phone, customer_email, customer_register_time)
        db.session.add(new_item)
        db.session.commit()
        return json.dumps('Right')
    else:        
        return json.dumps('Wrong')

@mod.route('/customers_address_mo', methods=['GET','POST'])#修改客户地址
def customers_address_mo():
    new_id = request.form['id']
    address = str(request.form['address'].encode('utf-8'))
    print new_id,address
    
    old_items = db.session.query(customer_basic_info).filter(customer_basic_info.customer_id==new_id).all()
    if len(old_items):
        for old_item in old_items:
            customer_id = old_item.customer_id
            customer_name = old_item.customer_name
            customer_phone = old_item.customer_phone
            customer_email = old_item.customer_email
            customer_register_time = old_item.customer_register_time
            db.session.delete(old_item)
            db.session.commit()
        new_item = customer_basic_info(customer_id, customer_name, address, customer_phone, customer_email, customer_register_time)
        db.session.add(new_item)
        db.session.commit()
        return json.dumps('Right')
    else:        
        return json.dumps('Wrong')


@mod.route('/customer_add_info/')#增加一条客户信息
def customer_add_info():
    return render_template('admin/customer_add_info.html')


@mod.route('/add_customer', methods=['GET','POST'])#添加客户信息
def add_customer():
    customer_id = request.form['customer_id']
    customer_name = request.form['customer_name']
    customer_address = request.form['customer_address']
    customer_phone = request.form['customer_phone']
    customer_email = request.form['customer_email']
    customer_register_time = request.form['customer_register_time']
   

    old_items = db.session.query(customer_basic_info).filter(customer_basic_info.customer_id==customer_id).all()
    if len(old_items):
        return json.dumps('Wrong')
    else:
        new_item = customer_basic_info(customer_id, customer_name,customer_address, customer_phone, customer_email,customer_register_time)
        db.session.add(new_item)
        db.session.commit()
        return json.dumps('Right')


@mod.route('/customer_order_history/')#查看客户订单历史
def customer_order_history():
    return render_template('admin/customer_order_history_page.html')


@mod.route('/customer_order_history_rank/')#某一客户订单历史详情展示
def customer_order_history_rank():
    page = 1
    countperpage = 4
    limit = 1000000
    customer_id_thisPage = 1

    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('countperpage'):
        countperpage = int(request.args.get('countperpage'))
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    if request.args.get('customer_id'):
        customer_id_thisPage = request.args.get('customer_id')
    #print customer_id_thisPage
    if page == 1:
        startoffset = 0
    else:
        startoffset = (page - 1) * countperpage
    endoffset = startoffset + countperpage
    newwords = db.session.query(sale_order_summary).filter(sale_order_summary.customer_id == customer_id_thisPage).all()
    news=[]

    n = 0
    for newword in newwords:
        if newword:
            n = n + 1
            if n > startoffset:
                if n > endoffset:
                    break

                news.append({'sale_order_number':newword.sale_order_number,'customer_id':newword.customer_id,'sale_order_total_price':newword.sale_order_total_price,'sale_order_status':newword.sale_order_status.encode('utf-8'),'sale_order_create_time':newword.sale_order_create_time})
    total_pages = limit / countperpage + 1
    return json.dumps({'news': news, 'pages': total_pages},cls=ComplexEncoder)


##==========================================仓库管理==============================================================
###================发货管理======================####
@mod.route('/noDeliver_orders_rank/')#未发货订单信息分页
def noDeliver_orders_rank():
    page = 1
    countperpage = 4
    limit = 1000000
    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('countperpage'):
        countperpage = int(request.args.get('countperpage'))
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    if page == 1:
        startoffset = 0
    else:
        startoffset = (page - 1) * countperpage
    endoffset = startoffset + countperpage
    newwords = db.session.query(sale_order_summary).filter().all()

    news=[]
    n = 0
    for newword in newwords:
        if newword:
            n = n + 1
            if n > startoffset:
                if n > endoffset:
                    break

                if newword.sale_order_status in ("已提交".decode('utf-8'),"部分发货".decode('utf-8')):
                    news.append({'sale_order_number':newword.sale_order_number,'customer_id':newword.customer_id,'sale_order_total_price':newword.sale_order_total_price,'sale_order_status':newword.sale_order_status.encode('utf-8'),'sale_order_create_time':newword.sale_order_create_time})
    total_pages = limit / countperpage + 1
    return json.dumps({'news': news, 'pages': total_pages},cls=ComplexEncoder)



@mod.route('/noDeliver_order_detail/')#查看未发货订单详情
def noDeliver_order_detail():
    return render_template('admin/noDeliver_order_detail_page.html')


@mod.route('/noDeliver_order_detail_rank/')#某一未发货订单详情展示
def noDeliver_order_detail_rank():
    page = 1
    countperpage = 4
    limit = 1000000
    sale_order_number_thisPage = 1

    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('countperpage'):
        countperpage = int(request.args.get('countperpage'))
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    if request.args.get('sale_order_number'):
        sale_order_number_thisPage = request.args.get('sale_order_number')
    #print sale_order_number_thisPage
    if page == 1:
        startoffset = 0
    else:
        startoffset = (page - 1) * countperpage
    endoffset = startoffset + countperpage
    newwords = db.session.query(sale_order_detail).filter(sale_order_detail.sale_order_number == sale_order_number_thisPage).all()
    news=[]
    n = 0
    for newword in newwords:
        if newword:
            n = n + 1
            if n > startoffset:
                if n > endoffset:
                    break

                news.append({'sale_order_number':newword.sale_order_number,'sale_order_item_number':newword.sale_order_item_number,'product_id':newword.product_id,'sale_amount':newword.sale_amount,'sale_price':newword.sale_price,'total_price_this_item':newword.total_price_this_item,'sale_item_status':newword.sale_item_status.encode('utf-8')})
    total_pages = limit / countperpage + 1
    return json.dumps({'news': news, 'pages': total_pages})



##发货管理 / 待发货订单详情  发货确认按钮
@mod.route('/deliver_confirm/') ##发货确认
def deliver_confirm():
    if request.args.get('sale_order_number'):
        sale_order_number = request.args.get('sale_order_number')
    if request.args.get('sale_order_item_number'):
        sale_order_item_number = request.args.get('sale_order_item_number')
    if request.args.get('delivery_operator'):
        delivery_operator = (request.args.get('delivery_operator'))

    right_flag = 0 ##标志位


    ###修改 sale_order_detail 表对应条目的订单状态，并根据 sale_order_summary 表中这一订单所有条目的状态判断是否需要修改这一订单的状态   
    old_items = db.session.query(sale_order_detail).filter(sale_order_detail.sale_order_number==sale_order_number,sale_order_detail.sale_order_item_number==sale_order_item_number).all()
    if len(old_items):
        for old_item in old_items:
            sale_order_number = old_item.sale_order_number
            sale_order_item_number = old_item.sale_order_item_number
            product_id = old_item.product_id
            sale_amount = old_item.sale_amount
            sale_price = old_item.sale_price
            total_price_this_item = old_item.total_price_this_item
            sale_item_status = "已发货"

            db.session.delete(old_item)
            db.session.commit()
            
        new_item = sale_order_detail(sale_order_number,sale_order_item_number, product_id, sale_amount,sale_price,total_price_this_item,sale_item_status)
        db.session.add(new_item)
        db.session.commit()

        #return json.dumps('Right')
        right_flag = 1
        print "aaa",right_flag
    else:        
        #return json.dumps('Wrong')
        right_flag = 0
        print "bbb",right_flag


    ###修改sale_order_summary订单状态的几种情况
    old_items = db.session.query(sale_order_detail).filter(sale_order_detail.sale_order_number==sale_order_number).all()
    if len(old_items):
        sale_item_status_list = []
        for old_item in old_items:
            sale_item_status_list.append(old_item.sale_item_status)

    #订单条目的几种状态：未提交、已提交、已收货
    #订单的几种状态：未提交、已提交、部分发货、已发货、已付款       
    if "已提交".decode('utf-8') in sale_item_status_list:
        new_status = "部分发货"
    else:
        new_status = "已发货"    

    old_items = db.session.query(sale_order_summary).filter(sale_order_summary.sale_order_number==sale_order_number).all()
    if len(old_items):
        for old_item in old_items:
            sale_order_number = old_item.sale_order_number
            customer_id = old_item.customer_id
            sale_order_total_item_num = old_item.sale_order_total_item_num
            sale_order_total_price = old_item.sale_order_total_price
            sale_order_status = new_status
            sale_order_create_time = old_item.sale_order_create_time
            sale_order_submit_time = old_item.sale_order_submit_time
            sale_order_deliver_time = date.now()
            sale_order_pay_time = old_item.sale_order_pay_time
            pay_remind_time = old_item.pay_remind_time

            db.session.delete(old_item)
            db.session.commit()

        new_item = sale_order_summary(sale_order_number,customer_id, sale_order_total_item_num, sale_order_total_price,sale_order_status,sale_order_create_time,sale_order_submit_time,sale_order_deliver_time,sale_order_pay_time,pay_remind_time)
        db.session.add(new_item)
        db.session.commit()

        #return json.dumps('Right')
        right_flag = 1
        print "ccc",right_flag
    else:        
        #return json.dumps('Wrong')
        right_flag = 0
        print "ddd",right_flag


    ###发货后向 delivery_statistics 发货统计表中添加信息
    old_items = db.session.query(customer_basic_info).filter(customer_basic_info.customer_id==customer_id).all()
    if len(old_items):
        for old_item in old_items:
            customer_address = old_item.customer_address
 
    delivery_quantity = sale_amount
    deliver_time = datetime.now()

    ##发货备注，暂且不写
    delivery_remarks = ""

    old_items = db.session.query(delivery_statistics).filter(delivery_statistics.sale_order_number==sale_order_number,delivery_statistics.sale_order_item_number==sale_order_item_number).all()
    if len(old_items):
        #return json.dumps('Wrong')
        right_flag = 0
        print "eee",right_flag
    else:
        new_item = delivery_statistics(sale_order_number,sale_order_item_number,product_id,delivery_quantity,customer_id,customer_address,deliver_time,delivery_operator, delivery_remarks)
        db.session.add(new_item)
        db.session.commit()
       #return json.dumps('Right')
        right_flag = 1
        print "fff",right_flag


    ###发货后 不用 修改 stock_summary 库存表中对应产品的库存量信息！！ 已经在提交订单时修改了库存量信息
    old_items = db.session.query(stock_summary).filter(stock_summary.product_id==product_id).all()
    if len(old_items):
        for old_item in old_items:
            product_id = old_item.product_id

            inventory_quantity = old_item.inventory_quantity - sale_amount
            if inventory_quantity < 0:
                inventory_quantity = 0
                right_flag = 0

            reorder_point = old_item.reorder_point
            order_volume_automatic = old_item.order_volume_automatic
           
            db.session.delete(old_item)
            db.session.commit()

        new_item = stock_summary(product_id,inventory_quantity,reorder_point,order_volume_automatic)
        db.session.add(new_item)
        db.session.commit()

        #return json.dumps('Right')
        right_flag = 1
        print "ggg",right_flag
    else:        
        #return json.dumps('Wrong')
        print "stock_summary 未能正确修改，请检查库存表中是否有对应产品信息"
        right_flag = 0
        print "hhh",right_flag

    if right_flag == 1:
        return json.dumps('Right')
    else:
        return json.dumps('Wrong')


###发货记录列表####
@mod.route('/delivery_statistics_rank/')#发货信息分页
def delivery_statistics_rank():
    page = 1
    countperpage = 4
    limit = 1000000
    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('countperpage'):
        countperpage = int(request.args.get('countperpage'))
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    if page == 1:
        startoffset = 0
    else:
        startoffset = (page - 1) * countperpage
    endoffset = startoffset + countperpage
    newwords = db.session.query(delivery_statistics).filter().all()
    news=[]
    n = 0
    for newword in newwords:
        if newword:
            n = n + 1
            if n > startoffset:
                if n > endoffset:
                    break

                news.append({'sale_order_number':newword.sale_order_number,'sale_order_item_number':newword.sale_order_item_number,'product_id':newword.product_id,'delivery_quantity':newword.delivery_quantity,'customer_id':newword.customer_id,'customer_address':newword.customer_address.encode('utf-8'),'deliver_time':newword.deliver_time,'delivery_operator':newword.delivery_operator.encode('utf-8'),'delivery_remarks':newword.delivery_remarks.encode('utf-8')})
    total_pages = limit / countperpage + 1
    return json.dumps({'news': news, 'pages': total_pages},cls=ComplexEncoder)



###================收货管理======================####
@mod.route('/noReceiving_orders_rank/')#未收货订单信息分页
def noReceiving_orders_rank():
    page = 1
    countperpage = 4
    limit = 1000000
    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('countperpage'):
        countperpage = int(request.args.get('countperpage'))
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    if page == 1:
        startoffset = 0
    else:
        startoffset = (page - 1) * countperpage
    endoffset = startoffset + countperpage
    newwords = db.session.query(purchase_order_summary).filter().all()

    news=[]
    n = 0
    for newword in newwords:
        if newword:
            n = n + 1
            if n > startoffset:
                if n > endoffset:
                    break

                if newword.purchase_order_status in ("已提交".decode('utf-8'),"部分收货".decode('utf-8')):
                    news.append({'purchase_order_number':newword.purchase_order_number,'supplier_id':newword.supplier_id,'purchase_order_total_price':newword.purchase_order_total_price,'purchase_order_status':newword.purchase_order_status.encode('utf-8'),'purchase_order_create_time':newword.purchase_order_create_time})
    total_pages = limit / countperpage + 1
    return json.dumps({'news': news, 'pages': total_pages},cls=ComplexEncoder)


@mod.route('/noReceiving_order_detail/')#查看未收货订单详情
def noReceiving_order_detail():
    return render_template('admin/noReceiving_order_detail_page.html')


@mod.route('/noReceiving_order_detail_rank/')#某一未收货订单详情展示
def noReceiving_order_detail_rank():
    page = 1
    countperpage = 4
    limit = 1000000
    purchase_order_number_thisPage = 1

    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('countperpage'):
        countperpage = int(request.args.get('countperpage'))
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    if request.args.get('purchase_order_number'):
        purchase_order_number_thisPage = request.args.get('purchase_order_number')
    #print purchase_order_number_thisPage
    if page == 1:
        startoffset = 0
    else:
        startoffset = (page - 1) * countperpage
    endoffset = startoffset + countperpage
    newwords = db.session.query(purchase_order_detail).filter(purchase_order_detail.purchase_order_number == purchase_order_number_thisPage).all()
    news=[]
    n = 0
    for newword in newwords:
        if newword:
            n = n + 1
            if n > startoffset:
                if n > endoffset:
                    break

                news.append({'purchase_order_number':newword.purchase_order_number,'purchase_order_item_number':newword.purchase_order_item_number,'product_id':newword.product_id,'purchase_amount':newword.purchase_amount,'purchase_price':newword.purchase_price,'total_price_this_item':newword.total_price_this_item,'purchase_item_status':newword.purchase_item_status.encode('utf-8')})
    total_pages = limit / countperpage + 1
    return json.dumps({'news': news, 'pages': total_pages})



##收货管理 / 待收货订单详情  收货确认按钮
@mod.route('/receiving_confirm/') ##收货确认
def receiving_confirm():
    if request.args.get('purchase_order_number'):
        purchase_order_number = request.args.get('purchase_order_number')
    if request.args.get('purchase_order_item_number'):
        purchase_order_item_number = request.args.get('purchase_order_item_number')
    if request.args.get('receiving_operator'):
        receiving_operator = (request.args.get('receiving_operator'))

    right_flag = 0 ##标志位

    ###修改 purchase_order_detail 表对应条目的订单状态，并根据 purchase_order_summary 表中这一订单所有条目的状态判断是否需要修改这一订单的状态   
    old_items = db.session.query(purchase_order_detail).filter(purchase_order_detail.purchase_order_number==purchase_order_number,purchase_order_detail.purchase_order_item_number==purchase_order_item_number).all()
    if len(old_items):
        for old_item in old_items:
            purchase_order_number = old_item.purchase_order_number
            purchase_order_item_number = old_item.purchase_order_item_number
            product_id = old_item.product_id
            purchase_amount = old_item.purchase_amount
            purchase_price = old_item.purchase_price
            total_price_this_item = old_item.total_price_this_item
            purchase_item_status = "已收货"

            db.session.delete(old_item)
            db.session.commit()
            
        new_item = purchase_order_detail(purchase_order_number,purchase_order_item_number, product_id, purchase_amount,purchase_price,total_price_this_item,purchase_item_status)
        db.session.add(new_item)
        db.session.commit()

        #return json.dumps('Right')
        right_flag = 1
        print "aaa2",right_flag
    else:        
        #return json.dumps('Wrong')
        right_flag = 0
        print "bbb2",right_flag


    ###修改purchase_order_summary订单状态的几种情况
    old_items = db.session.query(purchase_order_detail).filter(purchase_order_detail.purchase_order_number==purchase_order_number).all()
    if len(old_items):
        purchase_item_status_list = []
        for old_item in old_items:
            purchase_item_status_list.append(old_item.purchase_item_status)

    #采购订单条目的几种状态：已提交、已收货
    #采购订单的几种状态：已提交、部分收货、已收货、已付款      
    if "已提交".decode('utf-8') in purchase_item_status_list:
        new_status = "部分收货"
    else:
        new_status = "已收货"    

    old_items = db.session.query(purchase_order_summary).filter(purchase_order_summary.purchase_order_number==purchase_order_number).all()
    if len(old_items):
        for old_item in old_items:
            purchase_order_number = old_item.purchase_order_number
            supplier_id = old_item.supplier_id
            purchase_order_total_item_num = old_item.purchase_order_total_item_num
            purchase_order_total_price = old_item.purchase_order_total_price
            purchase_order_status = new_status
            purchase_order_create_time = old_item.purchase_order_create_time
            purchase_order_submit_time = old_item.purchase_order_submit_time
            purchase_order_receive_time = old_item.purchase_order_receive_time
            purchase_order_pay_time = old_item.purchase_order_pay_time

            db.session.delete(old_item)
            db.session.commit()

        new_item = purchase_order_summary(purchase_order_number,supplier_id, purchase_order_total_item_num, purchase_order_total_price,new_status,purchase_order_create_time,purchase_order_submit_time,purchase_order_receive_time,purchase_order_pay_time)
        db.session.add(new_item)
        db.session.commit()

        #return json.dumps('Right')
        right_flag = 1
        print "ccc2",right_flag
    else:        
        #return json.dumps('Wrong')
        right_flag = 0
        print "ddd2",right_flag


    ###收货后向 receiving_statistics 收货统计表中添加信息
    receipt_quantity = purchase_amount
    receipt_time = datetime.now()

    ##收货备注，暂且不写
    receipt_remarks = ""

    old_items = db.session.query(receiving_statistics).filter(receiving_statistics.purchase_order_number==purchase_order_number,receiving_statistics.purchase_order_item_number==purchase_order_item_number).all()
    if len(old_items):
        #return json.dumps('Wrong')
        right_flag = 0
        print "eee2",right_flag
    else:
        new_item = receiving_statistics(purchase_order_number,purchase_order_item_number,product_id,receipt_quantity,supplier_id,receipt_time,receiving_operator, receipt_remarks)
        db.session.add(new_item)
        db.session.commit()
       #return json.dumps('Right')
        right_flag = 1
        print "fff2",right_flag


    ###收货后 修改 stock_summary 库存表中对应产品的库存量信息！！ 
    old_items = db.session.query(stock_summary).filter(stock_summary.product_id==product_id).all()
    if len(old_items):
        for old_item in old_items:
            product_id = old_item.product_id

            inventory_quantity = old_item.inventory_quantity + purchase_amount

            reorder_point = old_item.reorder_point
            order_volume_automatic = old_item.order_volume_automatic
           
            db.session.delete(old_item)
            db.session.commit()

        new_item = stock_summary(product_id,inventory_quantity,reorder_point,order_volume_automatic)
        db.session.add(new_item)
        db.session.commit()

        #return json.dumps('Right')
        right_flag = 1
        print "ggg2",right_flag
    else:        
        #return json.dumps('Wrong')
        print "stock_summary 未能正确修改，请检查库存表中是否有对应产品信息"
        right_flag = 0
        print "hhh2",right_flag

    if right_flag == 1:
        return json.dumps('Right')
    else:
        return json.dumps('Wrong')


###收货记录列表####
@mod.route('/receiving_statistics_rank/')#收货信息分页
def receiving_statistics_rank():
    page = 1
    countperpage = 4
    limit = 1000000
    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('countperpage'):
        countperpage = int(request.args.get('countperpage'))
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    if page == 1:
        startoffset = 0
    else:
        startoffset = (page - 1) * countperpage
    endoffset = startoffset + countperpage
    newwords = db.session.query(receiving_statistics).filter().all()
    news=[]
    n = 0
    for newword in newwords:
        if newword:
            n = n + 1
            if n > startoffset:
                if n > endoffset:
                    break

                news.append({'purchase_order_number':newword.purchase_order_number,'purchase_order_item_number':newword.purchase_order_item_number,'product_id':newword.product_id,'receipt_quantity':newword.receipt_quantity,'supplier_id':newword.supplier_id,'receipt_time':newword.receipt_time,'receipt_operator':newword.receipt_operator.encode('utf-8'),'receipt_remarks':newword.receipt_remarks.encode('utf-8')})
    total_pages = limit / countperpage + 1
    return json.dumps({'news': news, 'pages': total_pages},cls=ComplexEncoder)




###================库存管理======================####
@mod.route('/stock_rank/')#库存信息分页
def stock_rank():
    page = 1
    countperpage = 10
    limit = 1000000
    if request.args.get('page'):
        page = int(request.args.get('page'))
    if request.args.get('countperpage'):
        countperpage = int(request.args.get('countperpage'))
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    if page == 1:
        startoffset = 0
    else:
        startoffset = (page - 1) * countperpage
    endoffset = startoffset + countperpage

    newwords = db.session.query(stock_summary).filter().all()
    news=[]
    n = 0
    for newword in newwords:
        if newword:
            n = n + 1
            if n > startoffset:
                if n > endoffset:
                    break

                product_words = db.session.query(product_basic_info).filter(product_basic_info.product_id == newword.product_id).all()
                for product_word in product_words:
                    product_name = product_word.product_name

                news.append({'product_id':newword.product_id,'product_name':product_name.encode('utf-8'),'inventory_quantity':newword.inventory_quantity,'reorder_point':newword.reorder_point,'order_volume_automatic':newword.order_volume_automatic})
    total_pages = limit / countperpage + 1
    print news
    return json.dumps({'news': news, 'pages': total_pages},cls=ComplexEncoder)


@mod.route('/reorder_point_mo', methods=['GET','POST'])#修改客户联系方式
def reorder_point_mo():
    product_id = request.form['id']
    reorder_point = str(request.form['reorder_point'])
    print product_id,reorder_point
    
    old_items = db.session.query(stock_summary).filter(stock_summary.product_id==product_id).all()
    if len(old_items):
        for old_item in old_items:
            product_id = old_item.product_id
            inventory_quantity = old_item.inventory_quantity          
            order_volume_automatic = old_item.order_volume_automatic
          
            db.session.delete(old_item)
            db.session.commit()

        new_item = stock_summary(product_id, inventory_quantity, reorder_point, order_volume_automatic)
        db.session.add(new_item)
        db.session.commit()
        return json.dumps('Right')
    else:        
        return json.dumps('Wrong')


@mod.route('/order_volume_automatic_mo', methods=['GET','POST'])#修改客户地址
def order_volume_automatic_mo():
    product_id = request.form['id']
    order_volume_automatic = request.form['order_volume_automatic']
    
    old_items = db.session.query(stock_summary).filter(stock_summary.product_id==product_id).all()
    if len(old_items):
        for old_item in old_items:
            product_id = old_item.product_id
            inventory_quantity = old_item.inventory_quantity          
            reorder_point = old_item.reorder_point

            db.session.delete(old_item)
            db.session.commit()
            
        new_item = stock_summary(product_id, inventory_quantity, reorder_point, order_volume_automatic)
        db.session.add(new_item)
        db.session.commit()
        return json.dumps('Right')
    else:        
        return json.dumps('Wrong')



def nwefunc():
    print hello

##################

#########new try

#########try 22222



def afun():
    print "ggggggggg"