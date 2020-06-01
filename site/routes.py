from flask import Blueprint
import pandas as pd
import sqlite3
import os

site_mod = Blueprint('site', __name__)

basedir = os.path.abspath(os.path.join('../', os.path.dirname(__file__)))

@site_mod.route('/pandas')
def pandas():
    con = sqlite3.connect("{}hawaii.sqlite".format(basedir[:-4]))
    df = pd.read_sql_query("SELECT s.name, m.date, m.prcp FROM measurement as m JOIN station as s ON s.station == m.station WHERE date >= \"2000-0-0\" ORDER BY date desc", con)
    df.set_index('date', inplace=True)
    df.sort_values(by=['date'])
    html = df.to_html()
    return html