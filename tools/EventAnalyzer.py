#Welcome to the industrial age of Sam's rebalance and smear code. You're going to have a lot of fun!
import os,sys
from ROOT import *
from array import array
from glob import glob
from utils import *
#from ra2blibs import *
import time

##read in command line arguments
defaultInfile_ = "/nfs/dust/cms/user/beinsam/CommonNtuples/NtupleMaker/March19NoTrack/CMSSW_9_4_11/src/TreeMaker/Production/test/VBFHHTo4B_CV_1_5_C2V_1_C3_1_13TeV_first.root_RA2AnalysisTree.root"
#T2qqGG.root
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", type=int, default=1,help="analyzer script to batch")
parser.add_argument("-printevery", "--printevery", type=int, default=1000,help="short run")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultInfile_,help="file")
parser.add_argument("-quickrun", "--quickrun", type=bool, default=False,help="short run")
args = parser.parse_args()
fnamekeyword = args.fnamekeyword
inputFiles = glob(fnamekeyword)
verbosity = args.verbosity
printevery = args.printevery
quickrun = args.quickrun
if quickrun: n2process = 10000
else: n2process = 9999999999999
lumi = 135 #lumi in /pb


#Dictionary list of region selection sets
regionCuts = {}
pi = 3.14159
Inf = 9999
#varlist                    = ['St',     'NCentralJets','NForwardJets', 'BTags', 'MStar',   'DmStar',    'NLeptons']
regionCuts['NoCuts']        = [[0,Inf],  [0,Inf],       [0,Inf],        [1,Inf], [-Inf,Inf], [0,Inf],  [0,Inf]]
regionCuts['LooseBaseline'] = [[200,Inf],[4,Inf],       [1,Inf],        [1,Inf], [-Inf,Inf], [0,2],    [0,Inf]]
regionCuts['TightBaseline'] = [[200,Inf],[4,Inf],       [2,Inf],        [2,Inf], [-Inf,Inf], [0,1],    [0,Inf]]

##declare and load a tree
c = TChain('TreeMaker2/PreSelection')
for fname in inputFiles: c.Add(fname)
nentries = c.GetEntries()
c.Show(0)
n2process = min(n2process, nentries)
print 'n(entries) =', n2process


varlist = ['St', 'NCentralJets','NForwardJets', 'BTags', 'MStar', 'DmStar',    'NLeptons']
indexVar = {}
for ivar, var in enumerate(varlist): indexVar[var] = ivar
indexVar[''] = -1
nmain = len(varlist)

histoStructDict = {}
for region in regionCuts:
	for var in varlist:
		histname = region+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname, binning)

def selectionFeatureVector(fvector, regionkey='', omitcuts='', omitcuts_dphi=''):
	iomits, iomits_dphi = [], []  
	for cut in omitcuts.split('Vs'): iomits.append(indexVar[cut])
	for i, feature in enumerate(fvector):
		if i==nmain: break
		if i in iomits: continue
		if not (feature>=regionCuts[regionkey][i][0] and feature<=regionCuts[regionkey][i][1]): 
			return False
	return True

##Create output file
infileID = fnamekeyword.split('/')[-1].replace('.root','')
newname = 'hists-'+infileID+'.root'
print 'creating file', newname
fnew = TFile(newname, 'recreate')

hSt = TH1F('hSt','hSt',120,0,2500)
hSt.Sumw2()
hStWeighted = TH1F('hStWeighted','hStWeighted',120,0,2500)
hStWeighted.Sumw2()

xsec_times_lumi_over_nevents = 1.0
t0 = time.time()
for ientry in range(n2process):

	if ientry%printevery==0:
		print "processing event", ientry, '/', n2process, 'time', time.time()-t0
	c.GetEntry(ientry)

	#br = 0.33
	#weight = 1.0*br*lumi/n2process#c.CrossSection
	weight = c.CrossSection
	
	recomuons = []
	#build up the vector of jets using TLorentzVectors; 
	for imu, mu in enumerate(c.Muons):
		if not mu.Pt()>10: continue
		if not abs(mu.Eta())<2.4: continue
		tlvmu = TLorentzVector()
		tlvmu.SetPtEtaPhiE(mu.Pt(), mu.Eta(), mu.Phi(), mu.E())
		recomuons.append(tlvmu)	
		
	recoelectrons = []
	#build up the vector of jets using TLorentzVectors; 
	for imu, mu in enumerate(c.Electrons):
		if not mu.Pt()>10: continue
		if not abs(mu.Eta())<2.4: continue
		tlvmu = TLorentzVector()
		tlvmu.SetPtEtaPhiE(mu.Pt(), mu.Eta(), mu.Phi(), mu.E())
		recoelectrons.append(tlvmu)		
		
	#build up the vector of jets using TLorentzVectors; 
	#this is where you have to interface with the input format you're using
	st = 0
	recojets_forward = []	
	recojets_central = []
	for ijet, jet in enumerate(c.Jets):
		if not jet.Pt()>20: continue
		if not abs(jet.Eta())<5: continue
		tlvjet = TLorentzVector()
		tlvjet.SetPtEtaPhiE(jet.Pt(), jet.Eta(), jet.Phi(), jet.E())
		st+=jet.Pt()
		if abs(jet.Eta())<2.5: 
			recojets_central.append(tlvjet)
		else: recojets_forward.append(tlvjet)		
	
	if len(recojets_central)>3:
		m01, m23 = (recojets_central[0]+recojets_central[1]).M(), (recojets_central[2]+recojets_central[3]).M()
		m02, m13 = (recojets_central[0]+recojets_central[2]).M(), (recojets_central[1]+recojets_central[3]).M()
		m03, m12 = (recojets_central[0]+recojets_central[3]).M(), (recojets_central[1]+recojets_central[2]).M()
		starlist = [[(m23+m01)/2,abs(m23-m01)/m23], [(m13+m02)/2,abs(m13-m02)/m13],  [(m12+m03)/2,abs(m12-m03)/m12]]
		mstar, dmstar = sorted(starlist, key=lambda x: x[1])[0]
		#print 'mstar, dmstar', mstar, dmstar, 'from list', starlist
	else:
		mstar, dmstar = -1, 999
				
	fillth1(hSt, st,1)
	fillth1(hStWeighted, st,weight)	
	fv = [st,len(recojets_central),len(recojets_forward), c.BTags, mstar, dmstar, len(recoelectrons)+len(recomuons)]
	for regionkey in regionCuts:
		for ivar, varname in enumerate(varlist):
			hname = regionkey+'_'+varname
			if selectionFeatureVector(fv,regionkey,varname,''): 
				fillth1(histoStructDict[hname].Observed, fv[ivar], weight)


fnew.cd()
hSt.Write()
hStWeighted.Write()
writeHistoStruct(histoStructDict)

print 'just created', fnew.GetName()
fnew.Close()






