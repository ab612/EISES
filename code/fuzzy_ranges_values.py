#!/usr/bin/env python3

###script to hard code lower bound values for fuzzy intensities and fuzzy times.
####also stores corresponding string names of fuzzy values

__author__= "Madison.Soden"
__date__= "Thu Sep 20, 2018  04:29PM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"

import datetime

standardfuzzy= ['dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh', 'High', 'vHigh', 'dHigh']
directionfuzzy= ['n-ne', 'ne-ene', 'ene-ese', 'ese-sse', 'sse-ssw', 'ssw-wsw', 'wsw-w', 'w-nw', 'nw-n']
shorefuzzy= ['onshore', 'downshore', 'offshore', 'upshore']
spawningfuzzy= ['toolow', 'conductive', 'toohigh']
sevenfuzzy= ['dLow', 'vLow', 'Low', 'average', 'High', 'vHigh', 'dHigh']

ranges= {}
ranges['mlrf1']=  {}

ranges['mlrf1']['tide1m']= []
ranges['mlrf1']['seandbc']= [[ 15, 17, 19, 21, 24, 29, 30, 31, 31.66, 32.5], standardfuzzy]
ranges['mlrf1']['seandbcM']= [[ 15, 17, 19, 21, 24, 29, 30.4, 31, 32, 34], standardfuzzy]
ranges['mlrf1']['windsp']= [[ 0, 2, 4, 7, 10, 21, 33, 40, 64, 100], standardfuzzy]
ranges['mlrf1']['windsp3day']= [[ 2, 3, 5, 7, 10, 17, 22, 25, 30, 50], standardfuzzy]

ranges['fwyf1']= {}
ranges['fwyf1']['tide1m']= []
ranges['fwyf1']['seandbc']= [[15, 17, 19, 21, 24, 29, 30, 31, 32, 34], standardfuzzy]
ranges['fwyf1']['windsp']= [[0, 2, 4, 7, 10, 21, 33, 40, 64, 100], standardfuzzy]
ranges['fwyf1']['seandbcM']= [[15, 17, 19, 21, 24, 29, 30.4, 30.9, 31.4, 33], standardfuzzy]
ranges['fwyf1']['windsp3day']= [[2, 3, 5, 7, 10, 17, 22, 25, 30, 50], standardfuzzy]

ranges['smkf1'] = {}
ranges['smkf1']['seandbcM']= [[15, 17, 19, 21, 24, 29.5, 30.9, 31.5, 32, 34], standardfuzzy]
ranges['smkf1']['seandbc']= [[16.8, 22.7, 24.1, 25, 25.3, 30.5, 31.9, 32.4, 33, 34], standardfuzzy]
ranges['smkf1']['windsp3day']= [[2, 3, 5, 7, 10, 17, 22, 25, 30, 50], standardfuzzy]
ranges['smkf1']['windsp']= [[0, 2, 4, 7, 10, 21, 33, 40, 64, 100], standardfuzzy]
ranges['smkf1']['tide1m']= [[9.0, 9.4, 10.0, 11.0, 11.5, 12.0, 12.5, 13.0, 14.0, 15.0], standardfuzzy]

ranges['sanf1']= {}
ranges['sanf1']['seandbc']= [[15, 17, 19, 21, 24, 29, 30, 31, 32, 34], standardfuzzy]
ranges['sanf1']['windsp']= [[0, 2, 4, 7, 10, 21, 33, 40, 64, 100], standardfuzzy]
ranges['sanf1']['tide1m']= [[8.7, 8.9, 9.1, 9.3, 9.5, 10.5, 10.7, 10.9, 11.1, 11.5], standardfuzzy]
ranges['sanf1']['seandbcM']= [[15, 17, 19, 21, 24, 29, 30.4, 31, 32, 34], standardfuzzy]
ranges['sanf1']['windsp3day']= []

standardtime= ['even', 'midn', 'pdaw', 'dawn', 'morn', 'midd', 'psun', 'suns']
quartertime= ['nite', 'dayb', 'aftn', 'dayl', 'all']

times= {}
times['mlrf1']= {}
times['mlrf1']['standard_time']= [[ 0, 3, 6, 9, 12, 15, 18, 21, 24], standardtime]
times['mlrf1']['local_midnight']= ['0500']
