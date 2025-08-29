from flask import Flask, render_template
from ncmodules import files, df_html, logstats, map_html
import pandas as pd

# ATTENTION: databases need to be up to date as this app reads from the databases

# create flask instance object 'app'
app = Flask(__name__)

# Create website for only these seagliders
sgid_list = ["609", "668"]

# root page
@app.route("/")
@app.route("/home")
def home():

    return render_template("home_template.html", homeFlag=True)

# home website for each seaglider
@app.route("/table_<sgid>")
def table(sgid=sgid_list[0]): # use first in list if none selected
    # check if ID is in list
    if sgid in sgid_list:
        dbname = sgid + ".db"
        logtable = "log_table" # table in nnn.db
        df = files.read_database(dbname, logtable, "descending") # query db in descending dive num order to have last dive first    
        table_data = df_html.convert_to_table(df) # Returns html string for table. use |safe keyword in html template so jinja doesn't change characters in strings
    else:
        table_data = "<div> Glider ID not processed </div>"
    
    return render_template("logtable_template.html", table_data=table_data, sgid=sgid, homeFlag=False)


# website for seaglider mapping
@app.route("/map_<sgid>")
def map(sgid=sgid_list[0]):

    if sgid in sgid_list:
        dbname = sgid + ".db"
        logtable = "log_table"
        df = files.read_database(dbname, logtable, "descending")        
        html_mapfile = map_html.create_map(sgid, df)
        map_url = f"static/maps/{html_mapfile}"        
    else:
        map_url = "<div> Glider ID not processed </div>"

    return render_template("map_template.html", sgid=sgid, map_url=map_url, homeFlag=False)
    # return map_html_str
    #return send_from_directory('static', mapfile)


@app.route("/stats_<sgid>")
def stats(sgid=sgid_list[0]): # use first in list if none selected
    # check if ID is in list
    if sgid in sgid_list:
        dbname = sgid + ".db"
        logtable = "log_table" # table in nnn.db
        df = files.read_database(dbname, logtable, "descending") # query db in descending dive num order to have last dive first    
        # table_data = df_html.convert_to_table(df) # Returns html string for table. use |safe keyword in html template so jinja doesn't change characters in strings
        dashvalues = logstats.glider_stats(df) # function to return stats information and plots 
        # html_dash = logstats.dashboard_html(dashvalues)
        navigation_dash = logstats.get_navigation_html(dashvalues)
        call_dash = logstats.get_call_html(dashvalues)

    else:
        navigation_dash = "<div> Glider ID not processed </div>"
        call_dash = "<div> Glider ID not processed </div>" 

    return render_template("glider_template.html", sgid=sgid, navigation_dash=navigation_dash, call_dash=call_dash, homeFlag=False)







# test, plots directly from dataframe
@app.route("/dftable")
def df_table(sgid="668"):
    dbname = sgid + ".db"
    logtable = "log_table"
    df = files.read_database(dbname, logtable, "descending")
    df_html = df.to_html(classes='data-table')

    return render_template("dftable.html", table = df_html, sgid=sgid)


if __name__ == '__main__':
    app.run(debug=True)