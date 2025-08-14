import os
import sqlite3 as sql

# dirpath = "C:\\Users\\christian.saiz\\Documents\\0_NOAA\\1_NOAA_work\\2_GLIDERS\\2025\\piloting\\668"

# test only N files
test = True # False: process all .nc in dir / True: process only first nfiles
nfiles = 25 # no. of .nc files to process

def list_ncdir(dir, sgid):
    print("=====================")
    print("Scanning directory: " + dir)
    
    ncpath_list = []
    # Check if the path is a valid directory
    if os.path.isdir(dir) == True: 
        # list dir files
        filelist = os.listdir(dir)        

        index = 0
        # if dir is valid, loop throgh list of files and create full absolute path       
        for file in filelist:
            # if run is a test loop nfiles times only
            if test == True:
                if index >= nfiles:
                    break
            # create full path based on OS
            fullpath = os.path.join(dir,file)

            if os.path.isfile(fullpath) == True:
                # check that the file is netcdf
                if file.endswith(".nc") == True:
                    print("Found netCDF file: ", file)    
                    # check that is the correct glider ID
                    if file.startswith("p"+ sgid) == True:               
                        ncpath_list.append(fullpath)
                        index = index + 1
                    else:
                        print("Glider ID doesn't match " + sgid + "!")
                # if not a netcdf file, print warning
                else:
                    print(fullpath + " is not an .nc file!")            
            # if not a file, print warning
            else:
                print(fullpath + " is not a file")
    
    # if not a directory, print warning
    else:
        print(dir + " is not a directory!")

    # return complete dataframe of dir data
    return ncpath_list



def get_files2process(ncfile_list, dbname, logtable):
    # check if db exists and return list of files not in the table
    if os.path.isfile(dbname) == True:
        print("=====================")
        print(f">> Database {dbname} found!")
        # get list of files already processed and in database
        dbcon = sql.connect(dbname)
        dbcursor = dbcon.cursor()
        dbcursor.execute(f"SELECT filePath from {logtable}")
        items = dbcursor.fetchall()   
        print("=====================")     
        print(">> Files in database:")  
        dbfiles = []
        for f in items:           
            print(f[0])
            dbfiles.append(f[0])

        # compare list and create list with files not processed
        print("=====================")
        print(">> Filtering out processed files:") 
        newfiles = []
        for f in ncfile_list:
            if f in dbfiles:
                print(f"{f} already processed")
            else:
                newfiles.append(f)   
                print(f"{f} not processed")         

        return newfiles
    
    # else return same input list
    else:
        print("=====================")
        print(f">> {dbname} database NOT found!")
        return ncfile_list

