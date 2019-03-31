from ROOT import *
from utils import *
import os,sys
gROOT.SetBatch(1)
gStyle.SetOptStat(0)
gROOT.ForceStyle()

lumi = 135.9#/fb
signal_mag = 10000

listOfBackgroundFiles = ['output/bigchunks/TTJets.root', 'output/bigchunks/QCD.root']
listOfSignalFiles = ['output/bigchunks/VBFHHTo4B_CV_1_C2V_2_C3_1.root']


binningAnalysis = binning
redoBinning = binningAnalysis


fileA = TFile(listOfBackgroundFiles[0])
keys = fileA.GetListOfKeys()
names = []
for key in keys: names.append(key.GetName())
fileA.Close()
keys = sorted(keys,key=lambda thing: thing.GetName())
newfile = TFile('plots.root','recreate')


bkghistlists = {}
sighistlists = {}
canv = mkcanvas('canv')
canv.SetLogy()
for name in names:
	if not 'Observed' in name: continue
	kinvar = name.replace('Observed','')
	selection = kinvar[1:kinvar.find('_')]
	kinvar = kinvar[kinvar.find('_')+1:]
	if '_' in kinvar: continue
	print 'kinvar=', kinvar
	bkghistlists[name] = []
	for ib, bfilename in enumerate(listOfBackgroundFiles):
		f = TFile(bfilename)
		h = f.Get(name).Clone(name+bfilename)
		h.Scale(1000*lumi)
		bkghistlists[name].append(h)
		bkghistlists[name][-1].SetDirectory(0)
		keyw = bfilename.split('/')[-1].replace('.root','')
		col = ColorsByCategory[keyw]
		histoStyler(bkghistlists[name][-1], col)
		bkghistlists[name][-1].SetFillStyle(1001)
		bkghistlists[name][-1].SetFillColor(col)
		bkghistlists[name][-1].SetTitle(keyw)
		bkghistlists[name][-1].SetLineColor(col+1)
		f.Close()
		if ib>0: bkghistlists[name][-1].Add(bkghistlists[name][-2])
		if ib==len(listOfBackgroundFiles)-1: 
			bkghistlists[name][-1].SetLineColor(kGray+2)
			bkghistlists[name][-1].SetLineWidth(3)
	sighistlists[name] = []
	for iS, sfilename in enumerate(listOfSignalFiles):
		f = TFile(sfilename)
		h = f.Get(name).Clone(name+sfilename)
		h.Scale(1000*lumi)		
		h.Scale(signal_mag)
		sighistlists[name].append(h)
		sighistlists[name][-1].SetDirectory(0)
		col = colors[iS]
		histoStyler(sighistlists[name][-1], col)
		sighistlists[name][-1].SetLineWidth(3)
		sighistlists[name][-1].SetTitle(sfilename.split('/')[-1].replace('.root',''))
		f.Close()
	arg = 'hist'
	bkghistlists[name].reverse()
	legsig = mklegend(x1=.14, y1=.76, x2=.65, y2=.88, color=kWhite)
	legbkg = mklegend(x1=.64, y1=.76, x2=.93, y2=.88, color=kWhite)
	for bkghist in bkghistlists[name]:
		bkghist.Draw(arg)
		bkghist.GetYaxis().SetTitle('Events')
		bkghist.GetXaxis().SetTitle(kinvar+(units[kinvar]!='')*' ['+units[kinvar]+(units[kinvar]!='')*']')
		legbkg.AddEntry(bkghist, bkghist.GetTitle(), 'fl')
		arg = 'hist same'
	for sighist in sighistlists[name]:
		sighist.Draw('same')		
		legsig.AddEntry(sighist, sighist.GetTitle()+' #times '+str(signal_mag), 'fl')
	bkghistlists[name][0].SetTitle('')
	bkghistlists[name][0].GetYaxis().SetRangeUser(0.001, 2000*bkghistlists[name][0].GetMaximum())
	bkghistlists[name][0].Draw('axis same')
	legbkg.Draw()
	legsig.Draw()
	stamp()
	newfile.cd()
	canv.Write('c_'+name)	
	

print 'just created', newfile.GetName()
newfile.Close()





exit(0)




















