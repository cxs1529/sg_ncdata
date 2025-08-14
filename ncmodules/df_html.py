import pandas as pd

# define warning threshold values
int_Humidity_thd = {"min":40.0, "max": 70.0}
int_Pressure_thd = {"min":9.4, "max": 10.0}
int_Temperature_thd = {"min":15, "max": 35}
SM_angle_thd = {"min":-75, "max": -50}
SM_depth_thd = {"min":0.5, "max": 1.5}
CALLS_thd = {"min":0, "max": 5}
dac_velocity_thd = {"min":0, "max": 1}
surf_velocity_thd = {"min":0, "max": 71} 

# return a formated html table from a dataframe
def convert_to_table(df):
    
    filter_headers = ['dive', 'time_start', 'time_end', 'gps_lat_start', 'gps_lon_start',
       'gps_lat_end', 'gps_lon_end', 'D_TGT', 'D_ABORT', 'T_DIVE', 'T_MISSION',
       'T_ABORT', 'C_PITCH', 'PITCH_GAIN', 'C_ROLL_DIVE', 'C_ROLL_CLIMB',
       'C_VBD', 'MAX_BUOY', 'NAV_MODE', 'HEADING', 'TGT_name', 'TGT_lat',
       'TGT_lon', 'int_Humidity', 'int_Pressure', 'int_Temperature', 'SM_CC',
       'SM_angle', 'SM_depth', 'CALLS', 'ERRORS', 'dac_velocity',
       'dac_heading', 'surf_velocity', 'surf_heading', 'glider_sog',
       'glider_dog', 'glider_hdg', 'glider_dive_time' ] # 'filePath' removed
    
    #print(df.keys())  

    print(">html for header:")  
    html_table_headers = "<tr class=\"table_header\">\n"
    for j in df.keys():
        if j in filter_headers:
            html_table_headers = html_table_headers + f"\n\t<th class=\"table_header\"> {j} </th>" 

    html_table_headers = html_table_headers + "\n</tr>\n"
    print(html_table_headers)


    print(">html for data:")  
    html_table_data = ""
    # create html table string assuming diveN is in descending order
    for i in range(0, len(df)):
        # start table row
        html_table_data = html_table_data + "\t\n<tr class=\"table_row\">\n"
        # iterate over data fields
        for col in filter_headers:
            
            data_value, data_class = get_data_class(i, col, df)

            # # check class conditions for particular parameters
            # dataclass = "data_normal"
            # if col == "int_Humidity" and df.loc[i,col] > 65.0:
            #     dataclass = "data_warning"
            # if col == "C_ROLL_DIVE":
            #     if i+1 < len(df):
            #         if df.loc[i,col] != df.loc[i+1,col]:
            #             dataclass = "data_change"

            # build each table data entry
            html_table_data = html_table_data + f"\t<td class={data_class}> {data_value} </td>\n"
        # end table row
        html_table_data = html_table_data + "</tr>\n"
    print(html_table_data)

    return html_table_headers + html_table_data


def get_data_class(i, col, df):
    data_class = "data_normal"
    data_value = df.loc[i,col]

    ctrl_parameters_int = ['D_TGT', 'D_ABORT', 'T_DIVE', 'T_MISSION',
       'T_ABORT', 'C_PITCH', 'C_ROLL_DIVE', 'C_ROLL_CLIMB',
       'C_VBD', 'MAX_BUOY', 'NAV_MODE', 'HEADING']
    ctrl_parameters_float = ['PITCH_GAIN']
    ctrl_parameters_str = ['TGT_name']

    if col == "int_Humidity":
        data_value = round(data_value, 2)
        if data_value <= int_Humidity_thd["min"] or data_value >= int_Humidity_thd["max"]:
            data_class = "data_warning"
    elif col == "int_Pressure":
        data_value = round(data_value, 2)
        if data_value <= int_Pressure_thd["min"] or data_value >= int_Pressure_thd["max"]:
            data_class = "data_warning"
    elif col == "int_Temperature":
        data_value = round(data_value, 2)
        if data_value <= int_Temperature_thd["min"] or data_value >= int_Temperature_thd["max"]:
            data_class = "data_warning"        
    elif col == "SM_angle":
        data_value = round(data_value, 2)
        if data_value <= SM_angle_thd["min"] or data_value >= SM_angle_thd["max"]:
            data_class = "data_warning"        
    elif col == "SM_depth":
        data_value = round(data_value, 2)
        if data_value <= SM_depth_thd["min"] or data_value >= SM_depth_thd["max"]:
            data_class = "data_warning"         
    elif col == "CALLS":
        data_value = round(data_value, 0)
        if data_value <= CALLS_thd["min"] or data_value >= CALLS_thd["max"]:
            data_class = "data_warning"        
    elif col == "dac_velocity":
        data_value = round(data_value, 2)
        if data_value <= dac_velocity_thd["min"] or data_value >= dac_velocity_thd["max"]:
            data_class = "data_warning"        
    elif col == "surf_velocity":
        data_value = round(data_value, 2)
        if data_value <= surf_velocity_thd["min"] or data_value >= surf_velocity_thd["max"]:
            data_class = "data_warning"         
    elif col in ctrl_parameters_int or col in ctrl_parameters_float or col in ctrl_parameters_str:
        if i+1 < len(df):            
            if df.loc[i,col] != df.loc[i+1,col]:
                data_class = "data_change"
        if col in ctrl_parameters_int:
            data_value = int(round(data_value, 0))
        elif col in ctrl_parameters_float:
            data_value = round(data_value, 3)
        else:
            pass

    return data_value, data_class

