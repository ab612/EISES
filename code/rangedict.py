###script to hard code lower bound values for fuzzy intensities and fuzzy times.
####also stores corresponding string names of fuzzy values

__author__= "Madison.Soden"
__date__= "Thu Jul 26, 2018  02:28PM"
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
ranges['mlrf1']= {}

ranges['mlrf1']['parsurf']= [[ 0, 50, 100, 300, 500, 700, 800, 1100, 1300, 1600], standardfuzzy]
ranges['mlrf1']['windsp']= []
ranges['mlrf1']['tide1m']= []
#ranges['mlrf1']['seandbc']= [[ 15, 17, 19, 21, 24, 29, 31.4, 32, 33, 34], standardfuzzy]
ranges['mlrf1']['seandbc']= [[ 15, 17, 19, 21, 24, 29, 30, 31, 31.66, 32.5], standardfuzzy]
ranges['mlrf1']['sea1m']= [[ 15, 17, 19, 21, 24, 30.1, 30.2, 30.4, 30.8, 32.1], standardfuzzy]
ranges['mlrf1']['curveB']= []
ranges['mlrf1']['sea1mM']= []
ranges['mlrf1']['seandbcM']= [[ 15, 17, 19, 21, 24, 29, 30.4, 31, 32, 34], standardfuzzy]
ranges['mlrf1']['windsp3day']= []
ranges['mlrf1']['airt']= [[ 5, 17, 19, 21, 22, 28, 29, 30, 31, 32], standardfuzzy]
ranges['mlrf1']['dew']= [[ 15, 17, 19, 21, 22, 28, 29, 30, 31, 32], standardfuzzy]
ranges['mlrf1']['winddir']= [[ 0, 40, 80, 120, 160, 200, 240, 280, 320, 361], directionfuzzy]
ranges['mlrf1']['windsp']= [[ 0, 2, 4, 7, 10, 21, 33, 40, 64, 100], standardfuzzy]
ranges['mlrf1']['windgu']= [[ 0, 2, 4, 7, 10, 21, 33, 40, 64, 100], standardfuzzy]
ranges['mlrf1']['barom']= [[ 970, 990, 1000, 1005, 1010, 1015, 1020, 1025, 1030, 1035], standardfuzzy]
ranges['mlrf1']['surfbarom']= [[ 980, 990, 100, 1005, 1010, 1020, 1025, 1030, 1035, 1040], standardfuzzy]
ranges['mlrf1']['salin1m']= [[ 30, 31, 32, 33, 34, 36, 36.5, 37, 37.5, 38], standardfuzzy]
ranges['mlrf1']['samiPCO2']= [[ 200, 250, 300, 350, 400, 420, 450, 500, 550, 600], standardfuzzy]
ranges['mlrf1']['par1m']= [[ 0, 50, 100, 200, 400, 500, 600, 700, 800, 900], standardfuzzy]
ranges['mlrf1']['seandbc1D']= [[ 15, 17, 19, 21, 24, 29, 31.4, 32, 33, 34], standardfuzzy]
ranges['mlrf1']['winddir2']= [[ 0, 40, 80, 120, 160, 200, 240, 280, 320, 361], directionfuzzy]
ranges['mlrf1']['windsp2']= [[ 0, 2, 4, 7, 10, 21, 33, 40, 64, 100], standardfuzzy]
ranges['mlrf1']['windgu2']= [[ 0, 2, 4, 7, 10, 21, 33, 40, 64, 100], standardfuzzy]
ranges['mlrf1']['windsp3D']= [[ 2, 3, 5, 7, 10, 17, 22, 25, 30, 50], standardfuzzy]
ranges['mlrf1']['windsp7D']= [[ 3, 5, 10, 13, 15, 19, 23, 26, 30, 50], standardfuzzy]
ranges['mlrf1']['ekmandir7D']= [[ 0, 90, 180,270, 360], shorefuzzy]
ranges['mlrf1']['SseaT']= [[ 15, 24.5, 27.5, 34], spawningfuzzy]
ranges['mlrf1']['BseaT']= [[ 8, 12, 14, 16, 30.4, 31.4, 32.4, 34], sevenfuzzy]
ranges['mlrf1']['seandbcV']= [[ 0.02, 0.03, 0.04, 0.05, 0.1, 0.35, 0.4, 0.5, 0.7, 1.5], standardfuzzy]
ranges['mlrf1']['mwsst']= [[ 15, 17, 19, 21, 24, 29.8, 30, 30.2, 30.6, 32], standardfuzzy]
ranges['mlrf1']['airtV']= [[ 0.04, 0.07, 0.1, 0.2, 0.4, 1.0, 1.5, 2.0, 2.5, 4.0], standardfuzzy]
ranges['mlrf1']['photoAccum']= [[ 100, 200, 250, 300, 330, 400, 420, 440, 500, 600], standardfuzzy]
ranges['mlrf1']['satChlorA']= [[ 0.01, 0.1, 0.2, 0.5, 0.7, 1.2, 1.4, 2, 4, 6], standardfuzzy]
ranges['mlrf1']['surfcurUmin']= [[ -300, -230, -160, -100, -50, 30, 60, 90, 120, 200], standardfuzzy]

#standardtime= ['even', 'midn', 'pdawn', 'dawn', 'morn', 'midd', '????','psun', 'suns']
standardtime= ['even', 'midn', 'pdawn', 'dawn', 'morn', 'midd', 'psun', 'suns']
quartertime= ['nite', 'dayb', 'aftn', 'dayl', 'all']

times= {}
times['mlrf1']= [[ 0, 3, 6, 9, 12, 15, 18, 21, 24], standardtime]
