#this module should work just like hadd
from ROOT import *
import glob, os, sys
import numpy as np
from utils import *

istest = False
try: folder = sys.argv[1]
except:
    print 'please give folder name as first argument'
    exit(0)
    
keywordsOfContribution = {}#one element for each color on the final plot
keywordsOfContribution['TTJets'] = ['TTJets_TuneCUET']
keywordsOfContribution['QCD'] = ['QCD_HT200to300','QCD_HT300to500','QCD_HT500to700','QCD_HT700to1000','QCD_HT1000to1500','QCD_HT1500to2000','QCD_HT2000toInf']
keywordsOfContribution['VBFHHTo4B_CV_1_C2V_2_C3_1'] = ['VBFHHTo4B_CV_1_C2V_2_C3_1']

for contkey in keywordsOfContribution.keys():
	thingsInHadd = ''
	for keyword in keywordsOfContribution[contkey]:
		command = 'python tools/ahadd.py -f output/mediumchunks/unwghtd'+keyword+'.root '+folder+'/hists*'+keyword+'*.root'
		print 'command', command
		if not istest: os.system(command)    
		fuw = TFile('output/mediumchunks/unwghtd'+keyword+'.root')
		fw = TFile('output/mediumchunks/'+keyword+'.root', 'recreate')
		thingsInHadd+='output/mediumchunks/'+keyword+'.root '
		hHt = fuw.Get('hHt')
		nentries = hHt.GetEntries()
		keys = fuw.GetListOfKeys()
		for key in keys:
			name = key.GetName()
			if not len(name.split('/'))>0: continue
			hist = fuw.Get(name)
			hist.Scale(1.0/nentries)
			fw.cd()
			hist.Write()
		fuw.Close()
		command = 'rm output/mediumchunks/unwghtd'+keyword+'.root'
		print command
		if not istest: os.system(command)
		fw.Close()
	command = 'hadd -f output/bigchunks/'+contkey+'.root '+thingsInHadd
	print 'command', command
	os.system(command)
