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
@mod.route('/login', methods=['GET','POST'])
def login():
    return render_template('customer/index.html', result = result)

