import pandas as pd
from .ncdata import haversine
from .thresholds import *


# classification lists per dashboard container: navigation, call, health, rates-currents
navigation_keys = ["dive", "time_end", "gps_lat_end", "gps_lon_end", "TGT_name", "TGT_lat",  
                    "tgt_distance", "tgt_time", "TGT_lon", "glider_sog", "glider_dog", "glider_hdg",
                    "glider_dive_time", "depth_reached"]

call_keys = ["SM_angle", "SM_depth", "CALLS"]

health_keys= ["int_Humidity", "int_Pressure", "int_Temperature", "minVoltage", "batteryPercent", "errors"]

current_rates_keys = ["roll_imax", "pitch_imax", "vbd_imax", "roll_rate_min", "pitch_rate_min", "vbd_rate_min",
                       "vbd_i_apogee", "vbd_rate_apogee",]


def glider_stats(df):
    pd.set_option('display.max_columns', None)
    print(df)

    # retrieve values from last dive
    dive = df.loc[0,"dive"]
    # position
    depth_reached = df.loc[0,"depth_reached"]
    dtarget = df.loc[0,"D_TGT"]

    time_end = df.loc[0,"time_end"]
    gps_lat_end = df.loc[0,"gps_lat_end"]
    gps_lon_end = df.loc[0,"gps_lon_end"]

    TGT_name = df.loc[0,"TGT_name"]
    TGT_lat = df.loc[0,"TGT_lat"]
    TGT_lon = df.loc[0,"TGT_lon"]
    # internal sensors
    int_Humidity = df.loc[0,"int_Humidity"]
    int_Pressure = df.loc[0,"int_Pressure"]
    int_Temperature = df.loc[0,"int_Temperature"]
    
    # tx position
    SM_angle = df.loc[0,"SM_angle"]
    SM_depth = df.loc[0,"SM_depth"]
    calls = df.loc[0,"CALLS"]
    # displacement
    glider_sog = df.loc[0,"glider_sog"] # m/s
    glider_hdg = df.loc[0,"glider_hdg"] # deg
    glider_dog = df.loc[0,"glider_dog"] # km
    glider_dive_time = df.loc[0,"glider_dive_time"] # seconds
    tdive = df.loc[0,"T_DIVE"] # minutes
    # GC currents and rates
    roll_imax = df.loc[0,"glider_sog"]
    pitch_imax = df.loc[0,"glider_sog"]
    vbd_imax = df.loc[0,"glider_sog"]

    roll_rate_min = df.loc[0,"roll_rate_min"]
    pitch_rate_min = df.loc[0,"pitch_rate_min"]
    vbd_rate_min = df.loc[0,"vbd_rate_min"]

    vbd_i_apogee = df.loc[0,"vbd_i_apogee"]
    vbd_rate_apogee = df.loc[0,"vbd_rate_apogee"]

    # battery state
    log_24_minv = df.loc[0,"log_24_minv"]
    log_10_minv = df.loc[0,"log_10_minv"]
    minVoltage = min(log_24_minv, log_10_minv)
    log_AH_total_capacity = df.loc[0,"log_AH_total_capacity"]
    log_AH_total_consumed = df.loc[0,"log_AH_total_consumed"]
    batteryPercent = (log_AH_total_capacity - log_AH_total_consumed)/log_AH_total_capacity

    # Add something for error array
    errors = df.loc[0,"ERRORS"]

    # time and distance to target
    tgt_displacement = haversine(gps_lat_end,gps_lon_end, TGT_lat, TGT_lon) # km
    tgt_distance = tgt_displacement["distance"]
    tgt_direction = tgt_displacement["heading"] # could be used to determine if glider is moving away or towards target
    tgt_time = (tgt_distance * 1000 /glider_sog )/3600 # hs

    
    dashboard_dict = {
    "dive" : dive,     
    "time_end" : time_end,
    "gps_lat_end" : gps_lat_end,
    "gps_lon_end" : gps_lon_end,
    "TGT_name" : TGT_name,
    "TGT_lat" : TGT_lat,
    "TGT_lon" : TGT_lon,
    "int_Humidity" : int_Humidity,
    "int_Pressure" : int_Pressure,
    "int_Temperature" : int_Temperature,
    "SM_angle" : SM_angle,
    "SM_depth" : SM_depth,
    "CALLS" : calls,
    "glider_sog" : glider_sog,
    "glider_dog" : glider_dog,
    "glider_hdg" : glider_hdg,
    "glider_dive_time" : glider_dive_time,
    "T_DIVE" : tdive,
    "roll_imax" : roll_imax,
    "pitch_imax" : pitch_imax,
    "vbd_imax" : vbd_imax,
    "roll_rate_min" : roll_rate_min,
    "pitch_rate_min" : pitch_rate_min,
    "vbd_rate_min" : vbd_rate_min,
    "vbd_i_apogee" : vbd_i_apogee,
    "vbd_rate_apogee" : vbd_rate_apogee,
    "depth_reached" : depth_reached,
    "D_TGT" : dtarget,
    "minVoltage" : minVoltage,    
    "batteryPercent" : batteryPercent,
    "tgt_distance" : tgt_distance,
    "tgt_time" : tgt_time,
    "errors" : errors
    }

    return dashboard_dict


def dashboard_html(dash_data):

    # navigation dahboard: dive, depth reached, time end, gps, target, sog, dog, hdg, divetime, tgt-dist, tgt-time
    nav_html = get_navigation_html(dash_data)
    call_html = get_call_html(dash_data)
    # call dashboard: SMangle, SMdepth, calltries
    # health dashboard: humidity, pressure, temperature, voltmin, battery, errors
    # rates and currents


    html_string = nav_html

    return html_string


def get_call_html(dash_data):

    callanglestr = f"<div class='call-div'>\n <h3>CALL ANGLE</h3>\n <p class='p-normal'>{dash_data["SM_angle"]}</p>\n </div>\n"
    calldepthestr = f"<div class='call-div'>\n <h3>CALL DETPH</h3>\n <p class='p-normal'>{dash_data["SM_depth"]}</p>\n </div>\n"
    callnumstr = f"<div class='call-div'>\n <h3>CALLS</h3>\n <p class='p-normal'>{dash_data["CALLS"]}</p>\n </div>\n"

    html_string = "<div class=\"call-container\">\n" + callanglestr +  calldepthestr + callnumstr + "</div>\n"
    return html_string



# create html for navigation parameters dashboard
def get_navigation_html(dash_data):
    divestr = f"<div class='nav-div'>\n <h3>DIVE</h3>\n <p class='p-normal'>{dash_data["dive"]}</p>\n </div>\n"

    depthstr = f"<div class='nav-div'>\n <h3>MAX DEPTH</h3>\n <p class={get_class(dash_data,"depth_reached")}>{round(dash_data["depth_reached"],0)} m</p>\n </div>\n"    

    timestr = f"<div class='nav-div'>\n <h3>DATE TIME</h3>\n <p class='p-normal'>{dash_data["time_end"]}</p>\n </div>\n"

    positionstr = f"<div class='nav-div'>\n <h3>POSITION</h3>\n <p class='p-normal'>{str(f"{round(dash_data["gps_lat_end"], 4):.4f}")} N, \
                    {str(f"{round(dash_data["gps_lon_end"], 4):.4f}")} W</p>\n </div>\n" 
       
    targetstr = f"<div class='nav-div'>\n <h3>TARGET</h3>\n <p class='p-normal'>{dash_data["TGT_name"]} <br> {str(f"{round(dash_data["TGT_lat"], 4):.4f}")} N, \
                    {str(f"{round(dash_data["TGT_lon"], 4):.4f}")} W <br>Dist: {str(f"{round(dash_data["tgt_distance"], 2):.2f}")} km \
                    <br>Time:{str(f"{round(dash_data["tgt_time"], 1):.1f}")} h | {str(f"{round(dash_data["tgt_time"]/24, 1):.1f}")} days </p>\n </div>\n"
    
    sogstr = f"<div class='nav-div'>\n <h3>SOG</h3>\n <p class='p-normal'>{str(round(dash_data["glider_sog"],2))} m/s \
                    ({str(round(dash_data["glider_sog"] * 3600 /1000, 2))} km/h) </p>\n </div>\n"

    dogstr = f"<div class='nav-div'>\n <h3>DOG</h3>\n <p class={get_class(dash_data,"glider_dog")}>{str(round(dash_data["glider_dog"],2))} km | \
                    {str(round(dash_data["glider_hdg"],0))} {chr(176)} </p>\n </div>\n"

    divetime = f"<div class='nav-div'>\n <h3>DIVE TIME</h3>\n <p class={get_class(dash_data,"glider_dive_time")}>{str(f"{round(dash_data["glider_dive_time"],0):.0f}")} s | \
        {str(round(dash_data["glider_dive_time"]/60.0,0))} min | {str(round(dash_data["glider_dive_time"]/3600.0,1))} h</p>\n </div>\n"

    html_string = "<div class=\"dive-container\">\n" + divestr + depthstr + timestr + positionstr + targetstr + sogstr + dogstr + divetime + "</div>\n"
    
    return html_string



# return paragraph item class based on thresholds
def get_class(dict,key):
    key_class = "p-normal"

    if key == "glider_dog":
        if dict[key] <= dog_thd["min"] or dict[key] >= dog_thd["max"]:
            key_class = "p-warning"
    elif key == "glider_dive_time":
        if (dict[key]/60) <= dict["T_DIVE"] * 0.85 or (dict[key]/60) >= dict["T_DIVE"] * 1.15:
            key_class = "p-warning" 
    elif key == "depth_reached":
        if dict[key] <= dict["D_TGT"] * 0.95 or dict[key] >= dict["D_TGT"] * 1.05:
            key_class = "p-warning" 
    else:
        pass

    return key_class 
          
        


# def get_card_string(key, dict):

#     if key in navigation_keys:
#         card_class = "nav-div"
#     elif key in call_keys:
#         card_class = "call-div"    
#     elif key in health_keys:
#         card_class = "health-div"
#     elif key in current_rates_keys:
#         card_class = "currents-div"
#     else:
#         pass
    
    
#     if key == "dive":
#           card_title = "DIVE"
#           card_value_class = "p-normal"
#           card_value = str(int(dict[key]))
#     elif key == "time_end":
#           card_title = "TIME"
#           card_value_class = "p-normal"
#           card_value = dict[key]
#     elif key == "gps_lat_end":
#           card_title = "LAT"
#           card_value_class = "p-normal"
#           card_value = str(f"{round(dict[key], 4):.4f}")  
#     elif key == "gps_lon_end":
#           card_title = "LON"
#           card_value_class = "p-normal"
#           card_value = str(f"{round(dict[key], 4):.4f}")
#     elif key == "TGT_name":
#           card_title = "TARGET"
#           card_value_class = "p-normal"
#           card_value = dict[key]

#     htmlstr = f"<div class={card_class}>\n <h3>{card_title}</h3>\n <p class={card_value_class} >{card_value}</p>\n  </div>\n"

#     return htmlstr