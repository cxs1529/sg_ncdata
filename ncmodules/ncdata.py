import netCDF4 as nc 
import numpy as np
import pandas as pd
from datetime import datetime, UTC

# User input
# ncfile = "p6090250.nc"

# MAIN ------------------------------------------------------------------------------------------------------
# def main():
    
#     thisdive_dict = process_netcdf(ncfile)
#     print_dictionary(thisdive_dict)

#     df = pd.DataFrame(thisdive_dict, index=[0])
    










# MAIN ------------------------------------------------------------------------------------------------------






# FUNCTIONS

# prints a dictionary in a column
def print_dictionary(dict):    
    for var in dict:
        print(var, ":", dict[var])

# Returns distance over ground and bearing between 2 gps positions as dd.ddd
def haversine(lat1,lon1,lat2,lon2):
    # distance between 2 positions
    lat1, lon1, lat2, lon2 = map(np.radians, [float(lat1), float(lon1), float(lat2), float(lon2)])    
    dlon = lon2 - lon1
    dlat = lat2 - lat1    
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2    
    c = 2 * np.arcsin(np.sqrt(a))
    distance = 6378 * c # km
    # bearing between 2 positions
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)
    x = np.sin(dlon) * np.cos(lat2)
    heading = (np.arctan2(y,x) * 180/np.pi) % 360

    # return result as dictionary
    displacement = {"distance": distance, "heading" : heading}

    return displacement

# Parse NetCDF file object and return relevant log parameters as a dictionary
def process_netcdf(ncfile):
    print("=====================")
    print("Processing netCDF file: " + ncfile)
    # open and read netcdf file
    ncdata = nc.Dataset(ncfile)
    # dive number
    log_dive = ncdata.variables["log_dive"][:].tolist()
    # time and position
    log_gps_lat = ncdata.variables["log_gps_lat"][:].tolist() # [GPS1 GPS2 GPS]
    log_gps_lon = ncdata.variables["log_gps_lon"][:].tolist()
    log_gps_time = ncdata.variables["log_gps_time"][:].tolist() # epoch times for gps1 gps2 gps
    # utc times conversion
    log_gps_time_utc = []
    for t in log_gps_time:    
        dt = datetime.fromtimestamp(t, UTC)
        dt_str = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        log_gps_time_utc.append(dt_str)
        
    # derived dive time
    deltaT = log_gps_time[-1] - log_gps_time[-2] # time between last 2 gps fixes. Take into account time for maneuvers
    total_flight_time_s = ncdata.variables["total_flight_time_s"][:].tolist()
    # log_gps_lat and log_gps_lon are lists with [GPS1 GPS2 GPS] >> 1st-fix 2nd-fix --dive-- fix-post-dive > determine DOG with GPS2 and GPS
    displacement = haversine(float(log_gps_lat[1]), float(log_gps_lon[1]), float(log_gps_lat[2]), float(log_gps_lon[2])) # distance over ground [km] and bearing [deg]
    dog = displacement["distance"]
    hdg = displacement["heading"]
    sog = dog * 1000 /deltaT # speed over ground [m/s]
    # sea currents
    depth_avg_curr_east = ncdata.variables["depth_avg_curr_east"][:].tolist() # in m/s
    depth_avg_curr_north = ncdata.variables["depth_avg_curr_north"][:].tolist()
    dac_velocity = np.hypot(depth_avg_curr_north,depth_avg_curr_east)
    dac_heading = (np.pi/2 - np.arctan2(depth_avg_curr_north, depth_avg_curr_east)) * 180.0 / np.pi

    surface_curr_east = ncdata.variables["surface_curr_east"][:].tolist() # in cm/s
    surface_curr_north = ncdata.variables["surface_curr_north"][:].tolist()
    surf_velocity = np.hypot(surface_curr_north, surface_curr_east) / 100.0
    surf_heading = (np.pi/2 - np.arctan2(surface_curr_north, surface_curr_east)) * 180.0 / np.pi
    # print(dac_velocity, "m/s",dac_heading, "deg || ", surf_velocity, "m/s", surf_heading, "deg")

    # control parameters
    # depth control
    log_D_TGT = ncdata.variables["log_D_TGT"][:].tolist()
    log_D_ABORT = ncdata.variables["log_D_ABORT"][:].tolist()
    log_T_DIVE = ncdata.variables["log_T_DIVE"][:].tolist()
    log_T_MISSION = ncdata.variables["log_T_MISSION"][:].tolist()
    log_T_ABORT = ncdata.variables["log_T_ABORT"][:].tolist()
    # target control 
    log_HEADING = ncdata.variables["log_HEADING"][:].tolist()
    log_NAV_MODE = ncdata.variables["log_NAV_MODE"][:].tolist()
    log_TGT_NAME = np.char.decode(ncdata.variables["log_TGT_NAME"], encoding='utf-8')
    log_TGT_NAME = "".join(log_TGT_NAME)
    log_TGT_LATLONG = np.char.decode(ncdata.variables["log_TGT_LATLONG"], encoding='utf-8')
    log_TGT_LATLONG = "".join(log_TGT_LATLONG)
    log_TGT_LAT = log_TGT_LATLONG.split(",")[0]
    log_TGT_LON = log_TGT_LATLONG.split(",")[1]
    # GC control
    log_C_PITCH = ncdata.variables["log_C_PITCH"][:].tolist()
    log_PITCH_GAIN = ncdata.variables["log_PITCH_GAIN"][:].tolist()
    log_C_ROLL_DIVE = ncdata.variables["log_C_ROLL_DIVE"][:].tolist()
    log_C_ROLL_CLIMB = ncdata.variables["log_C_ROLL_CLIMB"][:].tolist()
    log_C_VBD = ncdata.variables["log_C_VBD"][:].tolist()
    log_MAX_BUOY = ncdata.variables["log_MAX_BUOY"][:].tolist()
    log_SM_CC = ncdata.variables["log_SM_CC"][:].tolist()
    # internal sensors
    log_HUMID = ncdata.variables["log_HUMID"][:].tolist()
    log_TEMP = ncdata.variables["log_TEMP"][:].tolist()
    log_INTERNAL_PRESSURE = np.char.decode(ncdata.variables["log_INTERNAL_PRESSURE"], encoding='utf-8') # convert numpy array of bytes to string
    log_INTERNAL_PRESSURE = float("".join(log_INTERNAL_PRESSURE))
    # surface transmission parameters
    log_SM_DEPTHo = ncdata.variables["log__SM_DEPTHo"][:].tolist()
    log_SM_ANGLEo = ncdata.variables["log__SM_ANGLEo"][:].tolist()
    log_CALLS = ncdata.variables["log__CALLS"][:].tolist()
    log_ERRORS = np.char.decode(ncdata.variables["log_ERRORS"], encoding='utf-8')
    log_ERRORS = "".join(log_ERRORS)
    #log_ERRORS = log_ERRORS.split(",")

    thisdive = {
    "dive" : int(log_dive), 
    "time_start" : str(log_gps_time_utc[1]), 
    "time_end" : str(log_gps_time_utc[2]),
    "gps_lat_start" : float(log_gps_lat[1]),
    "gps_lon_start" : log_gps_lon[1],
    "gps_lat_end" : log_gps_lat[2],
    "gps_lon_end" : log_gps_lon[2],
    "D_TGT" : log_D_TGT,
    "D_ABORT" : log_D_ABORT,
    "T_DIVE" : log_T_DIVE,
    "T_MISSION" : log_T_MISSION,
    "T_ABORT" : log_T_ABORT,
    "C_PITCH" : log_C_PITCH,
    "PITCH_GAIN" : log_PITCH_GAIN,
    "C_ROLL_DIVE" : log_C_ROLL_DIVE,
    "C_ROLL_CLIMB" : log_C_ROLL_CLIMB,
    "C_VBD" : log_C_VBD,
    "MAX_BUOY" : log_MAX_BUOY,
    "NAV_MODE" : log_NAV_MODE,
    "HEADING" : log_HEADING,
    "TGT_name" : log_TGT_NAME,
    "TGT_lat" : log_TGT_LAT,
    "TGT_lon" : log_TGT_LON,
    "int_Humidity" : log_HUMID,
    "int_Pressure" : log_INTERNAL_PRESSURE,
    "int_Temperature" : log_TEMP,
    "SM_CC" : log_SM_CC,
    "SM_angle" : log_SM_ANGLEo,
    "SM_depth" : log_SM_DEPTHo,
    "CALLS" : log_CALLS,
    "ERRORS" : log_ERRORS,
    "dac_velocity" : dac_velocity,
    "dac_heading" : dac_heading,
    "surf_velocity" : surf_velocity,
    "surf_heading" : surf_heading
    }
    #print(thisdive)

    return thisdive




# Entry point main ------------------------------------------------------------
# if __name__ == "__main__":
#     main()

