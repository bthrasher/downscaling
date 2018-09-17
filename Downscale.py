#!/usr/bin/python

import sys, os, string, ConfigParser, copy, subprocess, time, datetime

######## BCSD functions #############
def getDirs(directory):
	return[d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory,d))]
	
def createDirs(directory):
	try:
		if os.path.isdir(directory):
			pass
		else: 
			#print "Creating directory ", d
			os.makedirs(directory)
	except (OSError):
		print directory, ' cannot be created. Check permissions and try again.'
		raise SystemExit(1)

def getFiles(directory):
	return[f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f)) \
			and f.find('.nc') > 0]
	
def getFilesPrefix(directory,prefix):
	return[f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f)) \
			and f.find('.nc') > 0 and f.find(prefix) == 0]
	
def getFilesNoPrefix(directory,prefix):
	return[f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f)) \
			and f.find('.nc') > 0 and f.find(prefix) < 0]

def biasCorr(OBSDIR,dreghist,dreg21,dbchist,dbc21,var,AVG_YRS,RUN_TYPE,OBS_RES,MIN_LAT,MAX_LAT,MIN_LON,MAX_LON,REF_ST,REF_END):
	print 'Correcting bias in ', d21, ' for variable ', var
	pad = (AVG_YRS-1)/2
		
	if RUN_TYPE.lower() == 'mon':
#		prefix = 'regridded_' + str(RESOL) + 'deg'
		dobs = os.path.join(OBSDIR,RUN_TYPE,var)
		prefix = 'regridded_' 
		print dhist
		fhistall = getFilesPrefix(dreghist,prefix)
		f21all = getFilesPrefix(dreg21,prefix)
		freghist = os.path.join(dreghist,fhistall[0])
		freg21 = os.path.join(dreg21,f21all[0])		
		fbchist = os.path.join(dbchist,fhistall[0])
		fbchist = fbchist.replace('regridded','BC')
		fbc21 = os.path.join(dbc21,f21all[0])
		fbc21 = fbc21.replace('regridded','BC')
		if os.path.isfile(fbc21) and os.path.getsize(fbc21) > 1000000:
			print d21,' already bias corrected'
		else:
			callstr = 'ncl \'var="'+var+'"\' pad='+str(pad)+' ref_st='+str(REF_ST)+' ref_end='+str(REF_END)+' \'f21="'+freg21+'"\' \'fhist="'+freghist+'"\' \'dobs="'+dobs+  \
						'"\' \'fhistout="'+fbchist+'"\' \'f21out="'+fbc21+'"\' ores='+str(OBS_RES)+  \
						' min_lat='+str(MIN_LAT)+' max_lat='+str(MAX_LAT)+' min_lon='+str(MIN_LON)+' max_lon='+str(MAX_LON)+' BC.ncl'
			print callstr
			os.system(callstr)
			
	if RUN_TYPE.lower() == 'day':
		dobs = os.path.join(OBSDIR,RUN_TYPE,'agg',model)
		freghist = getFilesPrefix(dreghist,var)
		freg21 = getFilesPrefix(dreg21,var)
		numf = len(freghist)+len(freg21)
		print str(numf), ' files to bias-correct'
		
		if var == 'tasmin':
			callstr1 = 'ncl \'d21="'+dbc21+'"\' \'dhist="'+dbchist+'"\' TminBC.ncl'
			p1 = subprocess.Popen(callstr1,shell=True)
			p1.wait()
		else:
			for i in range(0,numf,4):
				callstr1 = 'ncl \'var="'+var+'"\' \'d21="'+dreg21+'"\' \'dhist="'+dreghist+'"\' \'d21out="'+dbc21+'"\' \'dhistout="'+dbchist+ \
							'"\' \'dobs="'+dobs+'"\' ores='+str(OBS_RES)+  \
							' dec='+str(i)+' min_lat='+str(MIN_LAT)+' max_lat='+str(MAX_LAT)+  \
							' min_lon='+str(MIN_LON)+' max_lon='+str(MAX_LON)+' pad='+str(pad)+' ref_st='+str(REF_ST)+' ref_end='+str(REF_END)+' BCDaily.ncl'
				print callstr1
				p1 = subprocess.Popen(callstr1,shell=True)
				if i+1 < numf:
					callstr2 = 'ncl \'var="'+var+'"\' \'d21="'+dreg21+'"\' \'dhist="'+dreghist+'"\' \'d21out="'+dbc21+'"\' \'dhistout="'+dbchist+ \
							'"\' \'dobs="'+dobs+'"\' ores='+str(OBS_RES)+  \
							' dec='+str(i+1)+' min_lat='+str(MIN_LAT)+' max_lat='+str(MAX_LAT)+  \
							' min_lon='+str(MIN_LON)+' max_lon='+str(MAX_LON)+' pad='+str(pad)+' ref_st='+str(REF_ST)+' ref_end='+str(REF_END)+' BCDaily.ncl'
					print callstr2
					p2 = subprocess.Popen(callstr2,shell=True)
				if i+2 < numf:
					callstr3 = 'ncl \'var="'+var+'"\' \'d21="'+dreg21+'"\' \'dhist="'+dreghist+'"\' \'d21out="'+dbc21+'"\' \'dhistout="'+dbchist+ \
							'"\' \'dobs="'+dobs+'"\' ores='+str(OBS_RES)+  \
							' dec='+str(i+2)+' min_lat='+str(MIN_LAT)+' max_lat='+str(MAX_LAT)+  \
							' min_lon='+str(MIN_LON)+' max_lon='+str(MAX_LON)+' pad='+str(pad)+' ref_st='+str(REF_ST)+' ref_end='+str(REF_END)+' BCDaily.ncl'
					print callstr3
					p3 = subprocess.Popen(callstr3,shell=True)
				if i+3 < numf:
					callstr4 = 'ncl \'var="'+var+'"\' \'d21="'+dreg21+'"\' \'dhist="'+dreghist+'"\' \'d21out="'+dbc21+'"\' \'dhistout="'+dbchist+ \
							'"\' \'dobs="'+dobs+'"\' ores='+str(OBS_RES)+  \
							' dec='+str(i+3)+' min_lat='+str(MIN_LAT)+' max_lat='+str(MAX_LAT)+  \
							' min_lon='+str(MIN_LON)+' max_lon='+str(MAX_LON)+' pad='+str(pad)+' ref_st='+str(REF_ST)+' ref_end='+str(REF_END)+' BCDaily.ncl'
					print callstr4
					p4 = subprocess.Popen(callstr4,shell=True)
					
				p1.wait()
				if i+1 < numf: p2.wait()
				if i+2 < numf: p3.wait()
				if i+3 < numf: p4.wait()
	
	print 'Bias correction complete for ', d21

def spatDisagg(OBSDIR,var,RUN_TYPE,OBS_RES,dhistout,d21out,dhistbc,d21bc,MIN_LAT,MAX_LAT,MIN_LON,MAX_LON,REF_ST,REF_END,model):
	print 'Beginning spatial disaggregation with BCSD'
	dobs = os.path.join(OBSDIR,RUN_TYPE,var)
	
	if RUN_TYPE.lower() == 'mon':
		fobs = getFilesNoPrefix(os.path.join(OBSDIR,RUN_TYPE,var),'aggr')
		obsfname = fobs[0]
#		prefix = 'BC_' + str(RESOL) + 'deg'
		prefix = 'BC_' 
		prefix2 = 'BCSD_'+ str(round(1./OBS_RES,3)) + 'deg'
		fhist = getFilesPrefix(dhistbc,prefix)
		fhist = os.path.join(dhistout,fhist[0])
		f21 = getFilesPrefix(d21bc,prefix)
		f21 = os.path.join(d21out,f21[0])
		fhistout = fhist.replace(prefix,prefix2)
		f21out = f21.replace(prefix,prefix2)
		if os.path.isfile(f21out) and os.path.getsize(f21out) > 1000000:
			print d21,' already processed thru BCSD'
		else:
			callstr = 'ncl \'var="'+var+'"\' \'fhistout="'+fhistout+'"\' \'f21out="'+f21out+'"\' \'obsf="'+obsfname+'"\' \'dhistreg="'+dhistreg+  \
					'"\' \'d21reg="'+d21reg+'"\' \'dobs="'+dobs+'"\' \'dhistbc="'+dhistbc+'"\' \'d21bc="'+d21bc+'"\' ores='+str(OBS_RES)+ \
					' min_lat='+str(MIN_LAT)+' max_lat='+str(MAX_LAT)+  \
					' min_lon='+str(MIN_LON)+' max_lon='+str(MAX_LON)+' ref_st='+str(REF_ST)+' ref_end='+str(REF_END)+' SD.ncl'
			print callstr
			os.system(callstr)
	
	if RUN_TYPE.lower() == 'day':
#		if os.path.isfile(var+'_'+str(round(1./OBS_RES,3))+'_aggobsclimo_'+str(REF_ST)+'-'+str(REF_END)+'.nc') and \
#					os.path.isfile(var+'_'+str(round(1./OBS_RES,3))+'_obsclimo_'+str(REF_ST)+'-'+str(REF_END)+'.nc'):
#			pass
#		else:
#			callstr = 'ncl \'var="'+var+'"\' \'dobs="'+dobs+ \
#						'"\' ores='+str(OBS_RES)+' ref_st='+str(REF_ST)+' ref_end='+str(REF_END)+' daily_climo.ncl'
#			p = subprocess.Popen(callstr,shell=True)
#			p.wait()		
		
#		prefix = 'BC_' + str(RESOL) + 'deg_'
		prefix = '' 
		fhistall = getFilesPrefix(dhistbc,prefix)
		f21all = getFilesPrefix(d21bc,prefix)
		numf = len(fhistall) + len(f21all)
		daggobs = os.path.join(OBSDIR,RUN_TYPE,"agg",model)
		print str(numf), ' BC decades to process via SD'
		
		for i in range(0,numf,4):
			callstr1 = 'ncl \'var="'+var+'"\' \'dobs="'+dobs+'"\' \'daggobs="'+daggobs+'"\' \'dhistout="'+dhistout+ \
						'"\' \'d21out="'+d21out+'"\' \'dhistbc="'+dhistbc+'"\' \'d21bc="'+d21bc+ \
						'"\' ores='+str(OBS_RES)+' min_lat='+str(MIN_LAT)+' max_lat='+str(MAX_LAT)+  \
						' min_lon='+str(MIN_LON)+' max_lon='+str(MAX_LON)+' ref_st='+str(REF_ST)+' ref_end='+str(REF_END)+' dec='+str(i)+' SDDaily.ncl'
			print callstr1
			p1 = subprocess.Popen(callstr1,shell=True)
			if i+1 < numf:
				callstr2 = 'ncl \'var="'+var+'"\' \'dobs="'+dobs+'"\' \'daggobs="'+daggobs+'"\' \'dhistout="'+dhistout+ \
							'"\' \'d21out="'+d21out+'"\' \'dhistbc="'+dhistbc+'"\' \'d21bc="'+d21bc+ \
							'"\' ores='+str(OBS_RES)+' min_lat='+str(MIN_LAT)+' max_lat='+str(MAX_LAT)+  \
							' min_lon='+str(MIN_LON)+' max_lon='+str(MAX_LON)+' ref_st='+str(REF_ST)+' ref_end='+str(REF_END)+' dec='+str(i+1)+' SDDaily.ncl'
				print callstr2
				p2 = subprocess.Popen(callstr2,shell=True)
			if i+2 < numf:
				callstr3 = 'ncl \'var="'+var+'"\' \'dobs="'+dobs+'"\' \'daggobs="'+daggobs+'"\' \'dhistout="'+dhistout+ \
							'"\' \'d21out="'+d21out+'"\' \'dhistbc="'+dhistbc+'"\' \'d21bc="'+d21bc+ \
							'"\' ores='+str(OBS_RES)+' min_lat='+str(MIN_LAT)+' max_lat='+str(MAX_LAT)+  \
							' min_lon='+str(MIN_LON)+' max_lon='+str(MAX_LON)+' ref_st='+str(REF_ST)+' ref_end='+str(REF_END)+' dec='+str(i+2)+' SDDaily.ncl'
				print callstr3
				p3 = subprocess.Popen(callstr3,shell=True)
			if i+3 < numf:
				callstr4 = 'ncl \'var="'+var+'"\' \'dobs="'+dobs+'"\' \'daggobs="'+daggobs+'"\' \'dhistout="'+dhistout+ \
							'"\' \'d21out="'+d21out+'"\' \'dhistbc="'+dhistbc+'"\' \'d21bc="'+d21bc+ \
							'"\' ores='+str(OBS_RES)+' min_lat='+str(MIN_LAT)+' max_lat='+str(MAX_LAT)+  \
							' min_lon='+str(MIN_LON)+' max_lon='+str(MAX_LON)+' ref_st='+str(REF_ST)+' ref_end='+str(REF_END)+' dec='+str(i+3)+' SDDaily.ncl'
				print callstr4
				p4 = subprocess.Popen(callstr4,shell=True)
				
			p1.wait()
			if i+1 < numf: p2.wait()
			if i+2 < numf: p3.wait()
			if i+3 < numf: p4.wait()
	
	print 'BCSD spatial disaggregation complete for ',d21out
	
def constAnalog(OBSDIR,var,RUN_TYPE,OBS_RES,dhistout,d21out,dhistbc,d21bc,REF_ST,REF_END,MIN_LAT,MAX_LAT,MIN_LON,MAX_LON):
	print 'Beginning spatial disaggregation with BCCA'
	dobs = os.path.join(OBSDIR,RUN_TYPE,var)
	prefix = 'BC_' 
#	prefix = 'BC_' + str(RESOL) + 'deg_'
	fhistall = getFilesPrefix(dhistbc,prefix)
	f21all = getFilesPrefix(d21bc,prefix)
	numf = len(fhistall) + len(f21all)
	print str(numf), ' BC decades to process via CA'
	
	for i in range(0,numf,4):
		callstr1 = 'ncl \'var="'+var+'"\' \'dobs="'+dobs+'"\' \'dhistout="'+dhistout+ \
					'"\' \'d21out="'+d21out+'"\' \'dhistbc="'+dhistbc+'"\' \'d21bc="'+d21bc+'"\' ores='+str(OBS_RES)+  \
					' dec='+str(i)+' ref_st='+str(REF_ST)+' ref_end='+str(REF_END)+' min_lon='+str(MIN_LON)+' max_lon='+str(MAX_LON)+ \
					' min_lat='+str(MIN_LAT)+' max_lat='+str(MAX_LAT)+' CA.ncl'
		print callstr1
		p1 = subprocess.Popen(callstr1,shell=True)

		if i+1 < numf:
			callstr2 = 'ncl \'var="'+var+'"\' \'dobs="'+dobs+'"\' \'dhistout="'+dhistout+ \
						'"\' \'d21out="'+d21out+'"\' \'dhistbc="'+dhistbc+'"\' \'d21bc="'+d21bc+'"\' ores='+str(OBS_RES)+  \
						' dec='+str(i+1)+' ref_st='+str(REF_ST)+' ref_end='+str(REF_END)+' min_lon='+str(MIN_LON)+' max_lon='+str(MAX_LON)+ \
						' min_lat='+str(MIN_LAT)+' max_lat='+str(MAX_LAT)+' CA.ncl'

			print callstr2
			p2 = subprocess.Popen(callstr2,shell=True)
		if i+2 < numf:
			callstr3 = 'ncl \'var="'+var+'"\' \'dobs="'+dobs+'"\' \'dhistout="'+dhistout+ \
						'"\' \'d21out="'+d21out+'"\' \'dhistbc="'+dhistbc+'"\' \'d21bc="'+d21bc+'"\' ores='+str(OBS_RES)+  \
						' dec='+str(i+2)+' ref_st='+str(REF_ST)+' ref_end='+str(REF_END)+' min_lon='+str(MIN_LON)+' max_lon='+str(MAX_LON)+ \
						' min_lat='+str(MIN_LAT)+' max_lat='+str(MAX_LAT)+' CA.ncl'

			print callstr3
			p3 = subprocess.Popen(callstr3,shell=True)
		if i+3 < numf:
			callstr4 = 'ncl \'var="'+var+'"\' \'dobs="'+dobs+'"\' \'dhistout="'+dhistout+ \
						'"\' \'d21out="'+d21out+'"\' \'dhistbc="'+dhistbc+'"\' \'d21bc="'+d21bc+'"\' ores='+str(OBS_RES)+  \
						' dec='+str(i+3)+' ref_st='+str(REF_ST)+' ref_end='+str(REF_END)+' min_lon='+str(MIN_LON)+' max_lon='+str(MAX_LON)+ \
						' min_lat='+str(MIN_LAT)+' max_lat='+str(MAX_LAT)+' CA.ncl'

			print callstr4
			p4 = subprocess.Popen(callstr4,shell=True)
			
		p1.wait()
		if i+1 < numf: p2.wait()
		if i+2 < numf: p3.wait()
		if i+3 < numf: p4.wait()
	
	print 'BCCA spatial disaggregation complete for ',d21out
	
def postProc(var,RUN_TYPE,OUTDIR,BCDIR,OBS_RES):
	# Read input data directory structure 
	scenarios = []
	allscens = getDirs(BCDIR)
	allscens.sort()
	for i in xrange(len(allscens)):
		if os.path.isdir(os.path.join(BCDIR,allscens[i],RUN_TYPE)): scenarios.append(allscens[i])
	runs = []
	for i in xrange(len(scenarios)):
		runs.append(getDirs(os.path.join(BCDIR,scenarios[i],RUN_TYPE)))
				
	print 'Adding global attributes'				
	for i in xrange(len(scenarios)):
		for j in xrange(len(runs[i])):
			dbc = os.path.join(BCDIR,scenarios[i],RUN_TYPE,runs[i][j],var)
			dout = os.path.join(OUTDIR,scenarios[i],RUN_TYPE,runs[i][j],var)
			if os.path.isdir(din):
				fin = getFilesPrefix(din,'regridded')
				fbc = getFiles(dbc)
				fout = getFiles(dout)
				for b in xrange(len(fbc)):
					downf = os.path.join(BCDIR,scenarios[i],RUN_TYPE,runs[i][j],var,fbc[b])
					callstr = 'ncl \'gcmf="'+gcmf+'"\' \'downf="'+downf+'"\' ores='+str(OBS_RES)+' Postproc.ncl'
					print callstr
					os.system(callstr)
				for b in xrange(len(fout)):
					downf = os.path.join(OUTDIR,scenarios[i],RUN_TYPE,runs[i][j],var,fout[b])
					callstr = 'ncl \'gcmf="'+gcmf+'"\' \'downf="'+downf+'"\' ores='+str(OBS_RES)+' Postproc.ncl'
					print callstr
					os.system(callstr)
					if RUN_TYPE == 'mon':
						downf = downf.replace('BCSD','SD_noBC')
						callstr = 'ncl \'gcmf="'+gcmf+'"\' \'downf="'+downf+'"\' ores='+str(OBS_RES)+' Postproc.ncl'
						print callstr
						os.system(callstr)


########## Starting BCSD downscaling #########

# Test for correct program call
if len(sys.argv) != 4:
	print 'Usage: NewBCSD.py <model_name> <pr, tas, tasmin, or tasmax> <config file>'
	raise SystemExit(1)
	
# Read variable specified by user
model = (sys.argv[1]).lower()
var = (sys.argv[2])
config = sys.argv[3]

# Read configuration file
print 'Reading configuration file ',config
cfg = ConfigParser.ConfigParser()
cfg.read(config)
OBSDIR = cfg.get('directories','obs_root')
GCMDIR = cfg.get('directories','gcm_root')
BCDIR = cfg.get('directories','bc_root')
OUTDIR0 = cfg.get('directories','output_root')
RUN_TYPE = cfg.get('misc','type')
OBS_RES = cfg.getint('misc','obs_res')
MIN_LAT = cfg.getint('misc','min_lat')
MAX_LAT = cfg.getint('misc','max_lat')
MIN_LON = cfg.getint('misc','min_lon')
MAX_LON = cfg.getint('misc','max_lon')
AVG_YRS = cfg.getint('misc','num_avg_yrs')
REF_ST = cfg.getint('misc','ref_st')
REF_END = cfg.getint('misc','ref_end')
ADD_LEAP = cfg.get('flags','add_leap')
BIAS_CORR = cfg.getboolean('flags','bias_corr')
SPAT_DISAGG = cfg.getboolean('flags','spat_disagg')
CONST_ANA = cfg.getboolean('flags','const_analog')
POSTPROC = cfg.getboolean('flags','postproc')

GCMDIR = os.path.join(GCMDIR,model)
BCDIR = os.path.join(BCDIR,model)
ADD_LEAP = ADD_LEAP.lower()
RUN_TYPE = RUN_TYPE.lower()
if RUN_TYPE.find('m') == 0: 
	RUN_TYPE = 'mon'
	OUTDIR = os.path.join(OUTDIR0,'BCSD',model)
if RUN_TYPE.find('d') == 0: 
	RUN_TYPE = 'day'
	OUTDIR = os.path.join(OUTDIR0,model)


# Read scenarios input data directory structure
print 'Reading model input data directories' 
scenarios = []
allscens = getDirs(GCMDIR)
allscens.sort()
for i in xrange(len(allscens)):
	if os.path.isdir(os.path.join(GCMDIR,allscens[i],RUN_TYPE)): scenarios.append(allscens[i])
runs = []
for i in xrange(len(scenarios)):
	runs.append(getDirs(os.path.join(GCMDIR,scenarios[i],RUN_TYPE)))
#	runs.append(['r1i1p1'])		# Only process first realization in each model
allvars = copy.deepcopy(runs)
for i in xrange(len(allvars)):
	for j in xrange(len(allvars[i])):
		allvars[i][j] = getDirs(os.path.join(GCMDIR,scenarios[i],RUN_TYPE,runs[i][j]))

# Create mirror directory structure for output and check for corresponding data tree in histc3m
print 'Creating downscaling output directories'
for i in xrange(len(scenarios)):
	for j in xrange(len(runs[i])):
		for k in xrange(len(allvars[i][j])):
			dbc21out = os.path.join(BCDIR,scenarios[i],RUN_TYPE,runs[i][j],allvars[i][j][k])
			createDirs(dbc21out)
			d21out = os.path.join(OUTDIR,scenarios[i],RUN_TYPE,runs[i][j],allvars[i][j][k])
			createDirs(d21out)
			if RUN_TYPE == 'mon':
				d21out = os.path.join(OUTDIR0,'SD_noBC',model,scenarios[i],RUN_TYPE,runs[i][j],allvars[i][j][k])
				createDirs(d21out)

# Aggregate obs data to native GCM grid
print 'Aggregating obs to native GCM grid'
callstr = 'ncl \'dobs="'+os.path.join(OBSDIR,RUN_TYPE)+'"\' \'var="'+var+'"\' \'model="'+model+'"\' AggObs.ncl'
p1 = subprocess.Popen(callstr,shell=True)
p1.wait()
# exec(callstr)


# Bias correction
if BIAS_CORR:
	for i in range(1,len(scenarios)):
		for j in xrange(len(runs[i])):
			dhist = os.path.join(GCMDIR,scenarios[0],RUN_TYPE,runs[i][j],var)
			d21 = os.path.join(GCMDIR,scenarios[i],RUN_TYPE,runs[i][j],var)
			dhistbc = os.path.join(BCDIR,scenarios[0],RUN_TYPE,runs[i][j],var)
			d21bc = os.path.join(BCDIR,scenarios[i],RUN_TYPE,runs[i][j],var)
			print 'Entering BC'
			if os.path.isdir(dhist) and os.path.isdir(d21):
				biasCorr(OBSDIR,dhist,d21,dhistbc,d21bc,var,AVG_YRS,RUN_TYPE,OBS_RES,MIN_LAT,MAX_LAT,MIN_LON,MAX_LON,REF_ST,REF_END)
			else:
				print 'Either ',dhist,' or ',d21,' does not exist'

# Spatial disaggregation
if SPAT_DISAGG: 
	for i in range(1,len(scenarios)):
		for j in xrange(len(runs[i])):
			dhistbc = os.path.join(BCDIR,scenarios[0],RUN_TYPE,runs[i][j],var)
			d21bc = os.path.join(BCDIR,scenarios[i],RUN_TYPE,runs[i][j],var)
			dhistout = os.path.join(OUTDIR,scenarios[0],RUN_TYPE,runs[i][j],var)
			d21out = os.path.join(OUTDIR,scenarios[i],RUN_TYPE,runs[i][j],var)
			if os.path.isdir(dhistbc) and os.path.isdir(d21bc):
				spatDisagg(OBSDIR,var,RUN_TYPE,OBS_RES,dhistout,d21out,dhistbc,d21bc,MIN_LAT,MAX_LAT,MIN_LON,MAX_LON,REF_ST,REF_END,model)


if CONST_ANA: 
	for i in xrange(1,len(scenarios)):
		for j in xrange(len(runs[i])):
			dhistbc = os.path.join(BCDIR,scenarios[0],RUN_TYPE,runs[i][j],var)
			d21bc = os.path.join(BCDIR,scenarios[i],RUN_TYPE,runs[i][j],var)
			dhistout = os.path.join(OUTDIR,scenarios[0],RUN_TYPE,runs[i][j],var)
			d21out = os.path.join(OUTDIR,scenarios[i],RUN_TYPE,runs[i][j],var)
			if os.path.isdir(dhistbc) and os.path.isdir(d21bc):
				constAnalog(OBSDIR,var,RUN_TYPE,OBS_RES,dhistout,d21out,dhistbc,d21bc,REF_ST,REF_END,MIN_LAT,MAX_LAT,MIN_LON,MAX_LON)

if POSTPROC: postProc(var,RUN_TYPE,OUTDIR,BCDIR,OBS_RES)

