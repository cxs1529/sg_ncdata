from flask import Flask, render_template
from ncmodules import files, df_html
import pandas as pd


app = Flask(__name__)

#sgid = "668"
#dbname = sgid + ".db"
#logtable = "log_table"
sgid_list = ["609", "668"]

@app.route("/")
@app.route("/<sgid>")
def table(sgid):
    if sgid in sgid_list:
        dbname = sgid + ".db"
        logtable = "log_table"
        df = files.read_database(dbname, logtable, "descending")
    
        table_data = df_html.convert_to_table(df) # use |safe keyword in html template so jinja doesn't change characters in strings
    else:
        table_data = "<div> Glider ID not processed </div>"

    return render_template("table.html", table_data=table_data, sgid=sgid)



@app.route("/dftable")
def df_table(sgid="668"):
    dbname = sgid + ".db"
    logtable = "log_table"
    df = files.read_database(dbname, logtable, "descending")
    df_html = df.to_html(classes='data-table')

    return render_template("dftable.html", table = df_html, sgid=sgid)


if __name__ == '__main__':
    app.run(debug=True)