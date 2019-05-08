import os.path
import mcb

yl= range(1987,2018)
ll= ['mlrf1', 'fwyf1', 'sanf1', 'smkf1']
for location in ll:
    for year in yl:
        file_path = "../data/data/"+location+"h"+str(year)+".txt"
        if os.path.isfile(file_path):
            mcb.main( location, str(year), run_ff= True)
        else:
            print("unable to find file ../data/data/"+location+"h"+str(year)+".txt")
