from app import app
from flask import render_template, request, session, redirect, url_for
from utils import get_db_connection
from models.index_model import *

@app.route('/', methods=["GET"])
def index():
    conn = get_db_connection()

    # create(conn)    
    # insert(conn)
    arr_table_name = [
        "request_1_1",
        "request_1_2", 
        "request_2_1", 
        "request_2_2",
        "request_3_1",
        "request_3_2",
        "request_4_1",
        "request_4_2", 
        "request_5" 
    ]
    arr_df = [
        get_request_1_1(conn),
        get_request_1_2(conn), 
        get_request_2_1(conn), 
        get_request_2_2(conn),
        get_request_3_1(conn),
        get_request_3_2(conn),
        get_request_5(conn)
        
    ]
    # print(df)

    html = render_template(
            'index.html',
            arr_table_name = arr_table_name,
            arr_df = arr_df,
            len = len
    )
    return html