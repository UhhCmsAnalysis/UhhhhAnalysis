from ROOT import *
from utils import *
import os,sys
gROOT.SetBatch(1)


binningAnalysis = binning

try: filenameA = sys.argv[1]
except: filenameA = 'Vault/QCD_Summer16.root'

redoBinning = binningAnalysis

gStyle.SetOptStat(0)
gROOT.ForceStyle()

fileA = TFile(filenameA)
keys = fileA.GetListOfKeys()
keys = sorted(keys,key=lambda thing: thing.GetName())
newfile = TFile('closure_rands.root','recreate')

norm = 1.0

for key in keys:
	if not ('GenSmeared' in key.GetName() or 'RplusS' in key.GetName() or 'Rebalanced' in key.GetName()): continue
	kinvar = key.GetName().replace('GenSmeared','').replace('Rebalanced','').replace('RplusS','')
	selection = kinvar[1:kinvar.find('_')]
	kinvar = kinvar[kinvar.find('_')+1:]
	if '_' in kinvar: continue
	print 'kinvar=', kinvar
	print 'here'    
	#if not 'DPhiJet1Mht' in kinvar: continue
	if 'GenSmeared' in key.GetName(): 
		method = 'GenSmeared'
		standard = 'Observed'
	if 'Rebalanced' in key.GetName(): 
		method = 'Rebalanced'
		standard = 'Gen'
	if 'RplusS' in key.GetName():
		method = 'RplusS'
		standard = 'Observed'
		
	hObserved = fileA.Get('h'+selection+'_'+kinvar+standard).Clone('h'+selection+'_'+kinvar+standard+'')
	hObserved.Scale(norm)
	hObserved.SetTitle('Observed')
	hMethod = fileA.Get('h'+selection+'_'+kinvar+method).Clone('h'+selection+'_'+kinvar+method+'')
	if 'T2' in filenameA: hMethod.SetTitle('Signal (passed through R&S)')
	else: hMethod.SetTitle('QCD (R&S)')

	if 'RplusS' in key.GetName(): 
		passcount = fileA.Get('hPassFit').Integral()
		totcount = fileA.Get('hTotFit').Integral()
		if totcount>0: hMethod.Scale(totcount/passcount)
	
	if datamc == 'Data': col = kGreen
	if datamc == 'MC': col = kBlue
	histoStyler(hObserved, 1)
	histoStyler(hMethod, kGray+1)
	hMethod.SetFillColor(col-5)
	hMethod.SetFillStyle(1002)
	hMethod.GetYaxis().SetRangeUser(0.01,7000000)
	hObserved.GetYaxis().SetRangeUser(0.01,7000000)	

	cGold = TCanvas('cEnchilada','cEnchilada', 800, 800)
	if len(redoBinning[kinvar])>3: ##this should be reinstated
		nbins = len(redoBinning[kinvar])-1
		newxs = array('d',redoBinning[kinvar])
		hObserved = hObserved.Rebin(nbins,'',newxs)
		hMethod = hMethod.Rebin(nbins,'',newxs)
	else:
		newbinning = []
		stepsize = round(1.0*(redoBinning[kinvar][2]-redoBinning[kinvar][1])/redoBinning[kinvar][0],4)
		for ibin in range(redoBinning[kinvar][0]+1): newbinning.append(redoBinning[kinvar][1]+ibin*stepsize)
		nbins = len(newbinning)-1
		newxs = array('d',newbinning)
		hObserved = hObserved.Rebin(nbins,'',newxs)
		hMethod = hMethod.Rebin(nbins,'',newxs)
		


	oldalign = tl.GetTextAlign()    
	tl.SetTextAlign(oldalign)
	leg = mklegend(x1=.5, y1=.6, x2=.92, y2=.8, color=kWhite)
	hratio = FabDraw(cGold,leg,hObserved,[hMethod],datamc='MC',lumi=lumi, title = '', LinearScale=False, fractionthing= 'method/observed')
	hratio.GetYaxis().SetRangeUser(-0.2,2.2)
	cname = (hMethod.GetName()+'_And_'+hObserved.GetName()).replace(' ','')
	cGold.Write(cname)
	print 'trying:','pdfs/ClosureTests/'+selection+'_'+method+'And'+standard+'_'+kinvar+'.pdf'
	cGold.Print('pdfs/ClosureTests/'+selection+'_'+method+'And'+standard+'_'+kinvar+'.pdf')


print 'just created', newfile.GetName()






exit(0)




















