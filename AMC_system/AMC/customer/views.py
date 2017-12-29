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


mod = Blueprint('customer', __name__, url_prefix='/AMC')

@mod.route('/')
@mod.route('/index/')
def index():
    return render_template('customer/index.html')


@mod.route('/login/')
def login():
    return render_template('customer/login.html')

@mod.route('/products/')
def products():
        return render_template('customer/products.html') 

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

