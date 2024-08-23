#Bjon's script

import epics
import meme.archive
from datetime import datetime, timezone, timedelta
import pandas as pd
import os
#from PPSConnectionStatus import sevppszone

def daycount(d2):
	d1 = datetime.now(timezone.utc)
	global daydiff
	daydiff = abs(d2 - d1)
	#Hidden here is the total days, hours, and minutes that a zone has been unsearched
	#print('\033[1m' + str(daydiff))
	#print('\033[0m')
	return daydiff

def lastsearch(stat):	
	#Getting data for a PV from 60 days ago to today
	dayhist = meme.archive.get_dataframe(stat, from_time="60 days ago", to_time="now")
	#print(dayhist)
		
	#This looks for differences between values for the search status. The search status will change when a zone GAINS and DROPS a search.
	dayhist = dayhist[dayhist.diff() != 0]
	dayhist.index.floor('S').tz_localize(None)
	
	#Dropping any values that aren't different from its neighbor
	dayhist.dropna(axis=0,inplace=True)
	
	#Selecting the last line in the dataframe, this will display the time the zone search was dropped.
	last = (dayhist.index[-1]).to_pydatetime(warn=False)
	
	#Getting day difference between today and last date of search
	daycount(last)
	return
	

#Getting search status for all PPS Zones starting from FEE to INJ West

#FEE/EBD/BTH PPS Search status
fee = "PPS:FEE0:1:SRCHRESET"
ebd = "PPS:DMP0:1:SRCHRESET"
bth = "PPS:UND0:1:SRCHRESET"

#BSY and Subzone Search status
bthw = "PPS:BSY0:1:BTHW:SEARCHRESET"
narc = "PPS:BSY0:1:NARC:PSVD_PRESET"
sarc = "PPS:BSY0:1:SARC:PSVD_PRESET"
nit = "PPS:BSY0:1:NIT:PSVD_PRESET"
sit = "PPS:BSY0:1:SIT:PSVD_PRESET"
bsy = "PPS:BSY0:1:SEARCHRESET"

#LINAC East PPS Search status 
s30 = "PPS:LI30:1:RESET"
s26s29 = "PPS:LI28:1:RESET"
s24s25 = "PPS:LI24:1:RESET"
s21s23 = "PPS:LI22:1:RESET"
s20inj = "PPS:IN20:1:SRCHPRSETSUM"

#LINAC Middle PPS Sector Secure status
s20 = "LI20:PPS:72:PANIC"
s19 = "LI19:PPS:72:PANIC"
s18 = "LI18:PPS:72:SECTOR"
s17 = "LI17:PPS:72:SECTOR"
s16 = "LI16:PPS:72:SECTOR"
s15 = "LI15:PPS:72:SECTOR"
s14 = "LI14:PPS:72:SECTOR"
s13 = "LI13:PPS:72:SECTOR"
s12 = "LI12:PPS:72:SECTOR"
s11 = "LI11:PPS:72:SECTOR"
s10 = "LI10:PPS:72:SECTOR"
s10inj = "PPS:IN10:1:SEARCHRESET"

#LINAC West PPS Search status
s8s10 = "PPS:LI08:1:SearchResetOut"
s1s7 = "PPS:LI01:1:SearchResetOut"
s0 = "PPS:LI00:1:SearchResetOut"

zones = {'EBD-FEE':fee,'EBD':ebd,'BTH':bth,'BTH West':bthw,'NARC':narc,'SARC':sarc,'NIT':nit,'SIT':sit,'BSY':bsy,
	'S30':s30,'S26-29':s26s29,'S24-25':s24s25,'S21-23':s21s23,'S20 INJ':s20inj,
	'S20':s20,'S19':s19,'S18':s18,'S17':s17,'S16':s16,'S15':s15,'S14':s14,'S13':s13,'S12':s12,'S11':s11,'S10':s10,'S10 INJ':s10inj,
	'S8-10A':s8s10,'S1-7':s1s7,'INJ West':s0}

sevppszone = {'FEE' : 'PLC:FEE0:PPS1:COMMLINK',
'EBD': 'PLC:FEE0:PPS1:COMMLINK',
'BTH' : 'PLC:UND0:PPS1:COMMLINK',
'BTHW' : 'PPS:BSY0:1:S7_STATUS',
'NARC' : 'PPS:BSY0:1:S7_STATUS',
'SARC' : 'PPS:BSY0:1:S7_STATUS',
'NIT' : 'PPS:BSY0:1:S7_STATUS',
'SIT' : 'PPS:BSY0:1:S7_STATUS',
'BSY' : 'PPS:BSY0:1:S7_STATUS',
'S30' : 'PPS:LI28:1:S7_STATUS',
'S29-26' : 'PPS:LI28:1:S7_STATUS',
'S25-24' : 'PPS:LI24:1:S7_STATUS',
'S23-21' : 'PPS:LI22:1:S7_STATUS',
'S20 INJ' : 'PPS:IN20:1:DOORSUM',
'S20' : 'PPS:LI20:1:STATSUMY.SEVR',
'S19' : 'PPS:LI19:1:STATSUMY.SEVR',
'S18' : 'PPS:LI18:1:STATSUMY.SEVR',
'S17' : 'PPS:LI17:1:STATSUMY.SEVR',
'S16' : 'PPS:LI16:1:STATSUMY.SEVR',
'S15' : 'PPS:LI15:1:STATSUMY.SEVR',
'S14' : 'PPS:LI14:1:STATSUMY.SEVR',
'S13' : 'PPS:LI13:1:STATSUMY.SEVR',
'S12': 'PPS:LI12:1:STATSUMY.SEVR',
'S11' : 'PPS:LI11:1:STATSUMY.SEVR',
'S10' : 'PPS:LI10:1:STATSUMY.SEVR',
'S10 INJ' : 'PPS:IN10:1:S7_STATUS',
'S8-10A' : 'PLC:LI08:1:S7_STATUS',
'S1-7' : 'PLC:LI01:1:S7_STATUS',
'INJ West' : 'PLC:LI00:1:S7_STATUS'}


df = pd.DataFrame(columns=['Zone', 'Days', 'Color'])


#Iterating through 'zones' Dictionary to display Search Status OR Days since Last Search (refered to as daydiff)
#Here x = keys, y = values
for (x,y), (x2,y2) in zip(zones.items(),sevppszone.items()):
#'#affa4d'
	if epics.caget(y) == 1:
		df_temp = [{'Zone': x, 'Days': " ", 'Color': 'lightgreen'}]
		#df = df.concat(pd.DataFrame(df_temp), ignore_index=True)
		df = pd.concat([df, pd.DataFrame(df_temp)])
	
	if epics.caget(y) == 0 or epics.caget(y) == 2:
		lastsearch(y)
		print(daycount)
		if daydiff.days >= 20:
			df_temp = [{'Zone': x + ":", 'Days': str(daydiff.days), 'Color': '#ff4c4c'}]	
			#df = df.concat(pd.DataFrame(df_temp), ignore_index=True)
			df = pd.concat([df, pd.DataFrame(df_temp)])
		elif daydiff.days >= 10 and daydiff.days < 20:
			df_temp = [{'Zone':x + ":", 'Days': str(daydiff.days), 'Color': 'orange'}]	
			#df = df.concat(pd.DataFrame(df_temp), ignore_index=True)			
			df = pd.concat([df, pd.DataFrame(df_temp)])
		else:
			df_temp = [{'Zone':x + ":", 'Days': str(daydiff.days), 'Color': '#ffef00'}]	
			#df = df.concat(pd.DataFrame(df_temp), ignore_index=True)
			df = pd.concat([df, pd.DataFrame(df_temp)])
			
	if epics.caget(y) not in [0, 1, 2] :
		df_temp = [{'Zone': x, 'Days': "Err", 'Color': 'lightpurple'}]
		df = df.concat(pd.DataFrame(df_temp), ignore_index=True)
		
			
			
df.to_csv('search_data.csv', index=False)
