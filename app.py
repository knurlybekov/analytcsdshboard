from flask import Flask
import re
from datetime import datetime

import flask_login
import numpy as np
from flask import Blueprint, render_template, request, send_file
from flask_paginate import Pagination, get_page_args
import pandas as pd
from flask_login import login_required
app = Flask(__name__)


@app.route('/')
def get_table(page=1, per_page=10):  # put application's code here
    selected_menu_item = form_submit()
    df = getDF(selected_menu_item)
    print(df)
    pd.set_option('display.max_colwidth', None)  # display full column width
    pd.set_option('display.max_columns', None)  # display all columns
    pd.set_option('display.width', None)  # auto-detect terminal width
    df.index = np.arange(1, len(df) + 1)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page = 10
    offset = (page - 1) * per_page
    paginated_df = df.iloc[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=len(df), css_framework='bootstrap4')
    return paginated_df.to_html(classes='table table-hover table-bordered'), pagination


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
