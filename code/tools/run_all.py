import sys
sys.path.append("..")
import mcb

yl= range(1987,2018)
ll= ['mlrf1', 'fwyf1', 'sanf1', 'smkf1'] 
for location in ll:
    for year in yl:
        mcb.main("mlrf1h"+str(year), location, "year", run_ff= True)

