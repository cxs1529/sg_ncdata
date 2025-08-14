from ncmodules import files, ncdata
import pandas as pd
import sqlite3 as sql
import os

ncfile = "p6090250.nc"
dir_path = "C:\\Users\\christian.saiz\\Documents\\0_NOAA\\1_NOAA_work\\2_GLIDERS\\2025\\piloting\\668"
sgid = "668"
dbname = sgid + ".db"
logtable = "log_table"

# MAIN ------------------------------------------------------------------------------------------------------
def main():

    # get list of nc files in directory matching the glider id
    ncfiles_raw = files.list_ncdir(dir_path, sgid)    

    # filter files already processed in database
    ncfile_list = files.get_files2process(ncfiles_raw, dbname, logtable)
    print("=====================")
    print(f">> {len(ncfile_list)} files to process")

    if len(ncfile_list) > 0:
        # start empty dataframe
        df = pd.DataFrame()
        # loop through nc files and process each
        idx = 0
        for ncfile in ncfile_list:   
            # get dictionary from ncfile     
            thisdive_dict = ncdata.process_netcdf(ncfile)
            #ncdata.print_dictionary(thisdive_dict)
            # create dataframe from dictonary
            thisdive_df = pd.DataFrame(thisdive_dict, index = [idx])
            # add column with filepath
            thisdive_df["filePath"] = ncfile
            # append to main dataframe 
            df = pd.concat([df, thisdive_df])
            idx = idx + 1

        # Store values in database
        conn = sql.connect(dbname)
        df.to_sql(logtable, conn, if_exists='append', index=False)
        conn.close()

    # print(df)

    # read values from database
    print("=====================")
    print(f">> Displaying {dbname} values:\n")
    conn = sql.connect(dbname)        
    df_read = pd.read_sql_query(f"SELECT * FROM {logtable}", conn)
    conn.close()
    print(df_read)


# MAIN ------------------------------------------------------------------------------------------------------












# Entry point main ------------------------------------------------------------
if __name__ == "__main__":
    main()