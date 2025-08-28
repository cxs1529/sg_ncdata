import pandas as pd
from .ncdata import haversine


def glider_stats(df):
    pd.set_option('display.max_columns', None)
    print(df)

    # retrieve values from last dive
    dive = df.loc[0,"dive"]
    # position
    depth_reached = df.loc[0,"depth_reached"]
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
    tgt_direction = tgt_displacement["heading"]
    tgt_time = (tgt_distance * 1000 /glider_sog )/3600 # hs

    
    dashboard_values = {
    "dive" : dive,     
    "time_end" : time_end,
    "gps_lat_end" : gps_lat_end,
    "gps_lon_end" : gps_lat_end,
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
    "roll_imax" : roll_imax,
    "pitch_imax" : pitch_imax,
    "vbd_imax" : vbd_imax,
    "roll_rate_min" : roll_rate_min,
    "pitch_rate_min" : pitch_rate_min,
    "vbd_rate_min" : vbd_rate_min,
    "vbd_i_apogee" : vbd_i_apogee,
    "vbd_rate_apogee" : vbd_rate_apogee,
    "depth_reached" : depth_reached,
    "minVoltage" : minVoltage,    
    "batteryPercent" : batteryPercent,
    "tgt_distance" : tgt_distance,
    "tgt_time" : tgt_time,
    "errors" : errors
    }

    return dashboard_values


def dashboard_html(dash_values):
    html_string = "<div class=\"dashboard-container\">\n"

    for varname in dash_values.keys():
        html_string = html_string + f"<div class=\"value-card\">\n <h3>{varname}</h3>\n <p>{dash_values[varname]}</p>\n  </div>\n"     
    
    html_string = html_string + "</div>\n"

    return html_string