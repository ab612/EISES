import sys
sys.path.append("..")
import mcb

l= range(1987,2018)
for year in l:
    mcb.main("mlrf1h"+str(year), "mlrf1", "year")

