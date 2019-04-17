import os.path
import mcb

yl= range(1987,2018)
ll= ['mlrf1'] 
for location in ll:
    for year in yl:
        file_path = "../data/data/"+location+"h"+str(year)+".txt"
        if os.path.isfile(file_path):
            mcb.main(location+'h'+str(year), location, "year", run_ff= True)
