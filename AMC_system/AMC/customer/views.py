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

def date2ts(date):
    return time.mktime(time.strptime(date, '%Y-%m-%d'))

def ts2datetime(ts):
    return time.strftime('%Y-%m-%d', time.localtime(ts))


mod = Blueprint('AMC', __name__, url_prefix='/AMC')

@mod.route('/')
@mod.route('/login/', methods=['GET', 'POST'])
def login():
    result = None
    if 'logged_in' in session and session['logged_in']:
        session.pop('user', None)
        session.pop('logged_in', None)
    if request.method == 'POST':
        pas = db.session.query(customer_register_info).filter(customer_register_info.customer_login_name ==request.form['user']).all()
        if pas != []:
            for pa in pas:
                if request.form['para'] == pa.customer_password:
                    result = 'Right'
            if result == 'Right':
                session['logged_in'] = 'Ture'
                session['user'] = request.form['user']
                flash('登录成功！')
            else:
                result = 'Wrong_pass'
        return json.dumps(result)
    return render_template('customer/login.html', result = result)

@mod.route('/index/')
def show_index():
    return render_template('customer/index.html')
    # if 'logged_in' in session and session['logged_in']:
    #     return render_template('customer/index.html')
    # else:
    #     return redirect('/AMC')
#  产品
@mod.route('/products/')
def products():
    # print session['logged_in']
    if 'logged_in' in session and session['logged_in']:
        return render_template('customer/products.html')
    else:
        return redirect('/AMC/')

@mod.route('/single/')
def single():
        return render_template('customer/single.html') 

@mod.route('/contact/')
def contact():
        return render_template('customer/contact.html') 

@mod.route('/account/')
def account():
        return render_template('customer/account.html') 

@mod.route('/cart/')
def cart():
        return render_template('customer/cart.html') 


##用户注册
@mod.route('/add_account/', methods=['GET', 'POST'])
def add_account():
    name = request.form['name']
    address = request.form['address']
    phone_number = request.form['phone_number']
    email = request.form['email']
    password = request.form['password']
    creat_time = datetime.now()

    old_items = db.session.query(customer_basic_info).filter(customer_basic_info.customer_email == email).all()
    if len(old_items):
        return json.dumps('Wrong')
    else:
        temp = db.session.query(customer_basic_info).all()
        new_item = customer_basic_info(len(temp)+1, name, address, phone_number, email, creat_time)
        db.session.add(new_item)
        db.session.commit()
        new_item1 = customer_register_info(len(temp)+1, email, password, 4)
        db.session.add(new_item1)
        db.session.commit()
        return json.dumps('Right')
        # redirect('/customer')



