from ROOT import *
from array import array

tl = TLatex()
tl.SetNDC()
cmsTextFont = 61
extraTextFont = 50
lumiTextSize = 0.6
lumiTextOffset = 0.2
cmsTextSize = 0.75
cmsTextOffset = 0.1
regularfont = 42
originalfont = tl.GetTextFont()
epsi = "#scale[1.3]{#font[122]{e}}"
epsilon = 0.0001

binning = {}
binning['Met']=[50,0,500]
binning['HardMet']=[30,0,300]
binning['Mt']=[30,0,300]
binning['Mass']=binning['Met']
binning['MStar']=binning['Mass']
binning['DmStar']=[30,0,3]
binning['NJets']=[10,0,10]
binning['NCentralJets']=[10,0,10]
binning['NForwardJets']=[10,0,10]
binning['NLeptons']=[5,0,5]
binning['NElectrons']=binning['NLeptons']
binning['NPhotons']=binning['NLeptons']
binning['NMuons']=binning['NLeptons']
binning['BTags']=[6,0,6]
binning['Ht']=[10,0,2000]
binning['St']=binning['Ht']
binning['BinNumber'] = [34,0,34]

binningNice = binning
binningNice['Met'] = [10,0,300]

ColorsByCategory = {'WJetsToLNu':kGreen+1,'TTJets':kOrange-2,'ZJetsToNuNu':kViolet,'Diboson':kTeal-4,'DYJets':kBlue-1,'QCD':kCyan-5,'Rare':kBlack}
colors = [kBlack, kBlue-4, kRed+1, kGreen+1, kRed-7, kOrange+1, kTeal-7, kViolet-1, 28, kAzure-1,kRed-1,kRed-0,kRed+1,kRed+2,kPink-1,kPink+0,kPink+1,kPink+2]

def histoStyler(h,color=kBlack):
	h.SetLineWidth(2)
	h.SetLineColor(color)
	h.SetMarkerColor(color)
	#h.SetFillColor(color)
	size = 0.059
	font = 132
	h.GetXaxis().SetLabelFont(font)
	h.GetYaxis().SetLabelFont(font)
	h.GetXaxis().SetTitleFont(font)
	h.GetYaxis().SetTitleFont(font)
	h.GetYaxis().SetTitleSize(size)
	h.GetXaxis().SetTitleSize(size)
	h.GetXaxis().SetLabelSize(size)   
	h.GetYaxis().SetLabelSize(size)
	h.GetXaxis().SetTitleOffset(1.0)
	h.GetYaxis().SetTitleOffset(1.05)
	if not h.GetSumw2N(): h.Sumw2()
	
def makeHist(name, title, nb, low, high, color):
	h = TH1F(name,title,nb,low,high)
	histoStyler(h,color)
	return h

def makeTh1(name, title, nbins, low, high, color=kBlack): 
	h = TH1F(name, title, nbins, low, high)
	histoStyler(h, color)
	return h
	
def makeTh1VB(name, title, nbins, arrayOfBins): 
	h = TH1F(name, title, nbins, np.asarray(arrayOfBins, 'd'))
	histoStyler(h, 1)
	return h
	
def makeTh2(name, title, nbinsx, lowx, highx, nbinsy, lowy, highy): 
	h = TH2F(name, title, nbinsx, lowx, highx, nbinsy, lowy, highy)
	histoStyler(h)
	return h
	
def makeTh2VB(name, title, nbinsx, arrayOfBinsx, nbinsy, arrayOfBinsy):
	h = TH2F(name, title, nbinsx, np.asarray(arrayOfBinsx, 'd'), nbinsy, np.asarray(arrayOfBinsy, 'd'))
	histoStyler(h)
	return h
	
def graphStyler(g,color):
	g.SetLineWidth(2)
	g.SetLineColor(color)
	g.SetMarkerColor(color)
	#g.SetFillColor(color)
	size = 0.055
	font = 132
	g.GetXaxis().SetLabelFont(font)
	g.GetYaxis().SetLabelFont(font)
	g.GetXaxis().SetTitleFont(font)
	g.GetYaxis().SetTitleFont(font)
	g.GetYaxis().SetTitleSize(size)
	g.GetXaxis().SetTitleSize(size)
	g.GetXaxis().SetLabelSize(size)   
	g.GetYaxis().SetLabelSize(size)
	g.GetXaxis().SetTitleOffset(1.0)
	g.GetYaxis().SetTitleOffset(1.05)

def mkcanvas(name='c1'):
	c1 = TCanvas(name,name,750,630)
	c1.SetBottomMargin(.15)
	c1.SetLeftMargin(.14)
	#c1.SetTopMargin(.13)
	#c1.SetRightMargin(.04)
	return c1

def mkcanvas_wide(name):
	c1 = TCanvas(name,name,1200,700)
	c1.Divide(2,1)
	c1.GetPad(1).SetBottomMargin(.14)
	c1.GetPad(1).SetLeftMargin(.14)
	c1.GetPad(2).SetBottomMargin(.14)
	c1.GetPad(2).SetLeftMargin(.14)    
	c1.GetPad(1).SetGridx()
	c1.GetPad(1).SetGridy()
	c1.GetPad(2).SetGridx()
	c1.GetPad(2).SetGridy()    
	#c1.SetTopMargin(.13)
	#c1.SetRightMargin(.04)
	return c1

def mklegend(x1=.22, y1=.66, x2=.69, y2=.82, color=kWhite):
	lg = TLegend(x1, y1, x2, y2)
	lg.SetFillColor(color)
	lg.SetTextFont(42)
	lg.SetBorderSize(0)
	lg.SetShadowColor(kWhite)
	lg.SetFillStyle(0)
	return lg
	
def mklegend_(x1=.22, y1=.66, x2=.69, y2=.82, color=kWhite):
	lg = TLegend(x1, y1, x2, y2)
	lg.SetFillColor(color)
	lg.SetTextFont(42)
	lg.SetBorderSize(0)
	lg.SetShadowColor(kWhite)
	lg.SetFillStyle(0)
	return lg

def fillth1(h,x,weight=1):
	h.Fill(min(max(x,h.GetXaxis().GetBinLowEdge(1)+epsilon),h.GetXaxis().GetBinLowEdge(h.GetXaxis().GetNbins()+1)-epsilon),weight)

def fillth2(h,x,y,weight=1):
	h.Fill(min(max(x,h.GetXaxis().GetBinLowEdge(1)+epsilon),h.GetXaxis().GetBinLowEdge(h.GetXaxis().GetNbins()+1)-epsilon), min(max(y,h.GetYaxis().GetBinLowEdge(1)+epsilon),h.GetYaxis().GetBinLowEdge(h.GetYaxis().GetNbins()+1)-epsilon),weight)

def findbin(thebins, value):
	for bin in thebins:
		if value>=bin[0] and value<=bin[1]:
			return bin
	if value>thebins[-1]: return thebins[-1]
	if value<thebins[0]: return thebins[0]	


def namewizard(name):
	if 'HardMet' == name:
		return r'E_{T}^{miss} [GeV]'
	if 'Met' == name:
		return r'E_{T}^{miss} [GeV]'
	if 'Ht' == name:
		return r'H_{T} [GeV]'
	if 'NJets' == name:
		return r'n_{j}'        
	if 'BTags' == name:
		return r'n_{b}'                
	if 'MinDPhiHardMetJets' == name:
		return r'#Delta#phi_{min}'                        
	if 'NLeptons' == name:
		return r'n_{#ell}'
	if 'NPhotons' == name:
		return r'n_{#gamma}'		
	if 'NMuons' == name:
		return r'n(#mu)'
	if 'NTags' == name:
		return r'n_{DT}'
	if 'SumTagPtOverMet' == name:
		return r'R^{*}'
	if 'DPhiMetSumTags' == name:
		return r'#Delta#phi^{*}'
	return name


def Struct(*args, **kwargs):
	def init(self, *iargs, **ikwargs):
		for k,v in kwargs.items():
			setattr(self, k, v)
		for i in range(len(iargs)):
			setattr(self, args[i], iargs[i])
		for k,v in ikwargs.items():
			setattr(self, k, v)

	name = kwargs.pop("name", "MyStruct")
	kwargs.update(dict((k, None) for k in args))
	return type(name, (object,), {'__init__': init, '__slots__': kwargs.keys()})



def mkHistoStruct(hname, binning):
    if '_' in hname: var = hname[hname.find('_')+1:]
    else: var =  hname
    histoStruct = Struct('Observed')#, 'Method', 'Control')
    if len(binning[var])==3:
        nbins = binning[var][0]
        low = binning[var][1]
        high = binning[var][2]
        histoStruct.Observed = TH1F('h'+hname+'Observed',hname+'Observed',nbins,low,high)
        #histoStruct.Method = TH1F('h'+hname+'Method',hname+'Method',nbins,low,high)
        #histoStruct.Control = TH1F('h'+hname+'Control',hname+'Control',nbins,low,high)
    else:
        nBin = len(binning[var])-1
        binArr = array('d',binning[var])
        histoStruct.Observed = TH1F('h'+hname+'Observed',hname+'Observed',nBin,binArr)
        #histoStruct.Method = TH1F('h'+hname+'Method',hname+'Method',nBin,binArr)
        #histoStruct.Control = TH1F('h'+hname+'Control',hname+'Control',nBin,binArr)
    histoStyler(histoStruct.Observed,kRed)
    #histoStyler(histoStruct.Method,kBlack)
    #histoStyler(histoStruct.Control,kGreen)
    return histoStruct


def writeHistoStruct(hStructDict):
    for key in sorted(hStructDict.keys()):
        #print 'writing histogram structure:', key
        hStructDict[key].Observed.Write()
        #hStructDict[key].Method.Write()
        #hStructDict[key].Control.Write()


def pause(str_='push enter key when ready'):
		import sys
		print str_
		sys.stdout.flush() 
		raw_input('')

def mkmet(metPt, metPhi):
    met = TLorentzVector()
    met.SetPtEtaPhiE(metPt, 0, metPhi, metPt)
    return met
    
    
datamc = 'Data'
def stamp(lumi='35.9', showlumi = True, WorkInProgress = True):    
	tl.SetTextFont(cmsTextFont)
	tl.SetTextSize(0.98*tl.GetTextSize())
	tl.DrawLatex(0.135,0.915, 'CMS')
	tl.SetTextFont(extraTextFont)
	tl.SetTextSize(1.0/0.98*tl.GetTextSize())
	xlab = 0.213
	if WorkInProgress: tl.DrawLatex(xlab,0.915, ' Work in progress')
	else: tl.DrawLatex(xlab,0.915, ('MC' in datamc)*' private ')
	tl.SetTextFont(regularfont)
	tl.SetTextSize(0.81*tl.GetTextSize())    
	thingy = ''
	if showlumi: thingy+='#sqrt{s}=13 TeV, L = '+str(lumi)+' fb^{-1}'
	xthing = 0.602
	if not showlumi: xthing+=0.13
	tl.DrawLatex(xthing,0.915,thingy)
	tl.SetTextSize(1.0/0.81*tl.GetTextSize())  
	
	
def stamp2(lumi='35.9', showlumi = False):    
	tl.SetTextFont(cmsTextFont)
	tl.SetTextSize(0.98*tl.GetTextSize())
	tl.DrawLatex(0.1,0.91, 'CMS')
	tl.SetTextFont(extraTextFont)
	tl.SetTextSize(1.0/0.98*tl.GetTextSize())
	xlab = 0.213
	tl.DrawLatex(xlab,0.91, ('MC' in datamc)*' private')
	tl.SetTextFont(regularfont)
	tl.SetTextSize(0.81*tl.GetTextSize())    
	thingy = ''
	if showlumi: thingy+='#sqrt{s}=13 TeV, L = '+str(lumi)+' fb^{-1}'
	xthing = 0.6202
	if not showlumi: xthing+=0.13
	tl.DrawLatex(xthing,0.91,thingy)
	tl.SetTextSize(1.0/0.81*tl.GetTextSize()) 


def calcTrackIso(trk, tracks):
	ptsum =  -trk.pt()
	for track in tracks:
		dR = TMath.Sqrt( (trk.eta()-track.eta())**2 + (trk.phi()-track.phi())**2)
		if dR<0.3: ptsum+=track.pt()
	return ptsum/trk.pt()

def calcTrackJetIso(trk, jets):
	for jet in jets:
		if not jet.pt()>30: continue
		if  TMath.Sqrt( (trk.eta()-jet.eta())**2 + (trk.phi()-jet.phi())**2)<0.5: return False
	return True


def FabDraw(cGold,leg,hObserved,hComponents,datamc='mc',lumi=35.9, title = '', LinearScale=False, fractionthing='(bkg-obs)/obs'):
	cGold.cd()
	pad1 = TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
	pad1.SetBottomMargin(0.0)
	pad1.SetLeftMargin(0.12)
	if not LinearScale:
		pad1.SetLogy()
	
	pad1.SetGridx()
	#pad1.SetGridy()
	pad1.Draw()
	pad1.cd()
	for ih in range(1,len(hComponents[1:])+1):
		hComponents[ih].Add(hComponents[ih-1])
	hComponents.reverse()        
	if abs(hComponents[0].Integral(-1,999)-1)<0.001:
		hComponents[0].GetYaxis().SetTitle('Normalized')
	else: hComponents[0].GetYaxis().SetTitle('#Events')
	cGold.Update()
	hObserved.GetYaxis().SetTitle('Normalized')
	hObserved.GetYaxis().SetTitleOffset(1.15)
	hObserved.SetMarkerStyle(20)
	histheight = 1.5*max(hComponents[0].GetMaximum(),hObserved.GetMaximum())
	if LinearScale: low, high = 0, histheight
	else: low, high = max(0.001,max(hComponents[0].GetMinimum(),hObserved.GetMinimum())), 1000*histheight
	
	title0 = hObserved.GetTitle()
	if datamc=='MC':
		for hcomp in hComponents: leg.AddEntry(hcomp,hcomp.GetTitle(),'lf')
		leg.AddEntry(hObserved,hObserved.GetTitle(),'lpf')        
	else:
		for ihComp, hComp in enumerate(hComponents):
			leg.AddEntry(hComp, hComp.GetTitle(),'lpf')      
		leg.AddEntry(hObserved,title0,'lp')    
	hObserved.SetTitle('')
	hComponents[0].SetTitle('')	
	hComponents[0].Draw('hist')
	for h in hComponents[1:]: 
		h.Draw('hist same')
		cGold.Update()
		print 'updating stack', h
	hComponents[0].Draw('same') 
	hObserved.Draw('p same')
	hObserved.Draw('e same')    
	cGold.Update()
	hComponents[0].Draw('axis same')           
	leg.Draw()        
	cGold.Update()
	stampFab(lumi,datamc)
	cGold.Update()
	cGold.cd()
	pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.4)
	pad2.SetTopMargin(0.0)
	pad2.SetBottomMargin(0.3)
	pad2.SetLeftMargin(0.12)
	pad2.SetGridx()
	pad2.SetGridy()
	pad2.Draw()
	pad2.cd()
	hObservedCopy = hObserved.Clone('hObservedClone'+hComponents[0].GetName())
	hRatio = hObservedCopy.Clone('hRatioClone')#hComponents[0].Clone('hRatioClone')#+hComponents[0].GetName()+'testing
	hRatio.SetMarkerStyle(20)
	#hFracDiff = hComponents[0].Clone('hFracDiff')
	#hFracDiff.SetMarkerStyle(20)
	hObservedCopy.SetMarkerStyle(20)
	hObservedCopy.SetMarkerColor(1) 
	#histoStyler(hFracDiff, 1)
	histoStyler(hObservedCopy, 1)
	#hFracDiff.Add(hObservedCopy,-1)
	#hFracDiff.Divide(hObservedCopy)
	#hRatio.Divide(hObservedCopy)
	hRatio.Divide(hComponents[0])
	hRatio.GetYaxis().SetRangeUser(0.0,.1)###
	hRatio.SetTitle('')
	if 'prediction' in title0: hFracDiff.GetYaxis().SetTitle('(RS-#Delta#phi)/#Delta#phi')
	else: hRatio.GetYaxis().SetTitle(fractionthing)
	hRatio.GetXaxis().SetTitleSize(0.12)
	hRatio.GetXaxis().SetLabelSize(0.11)
	hRatio.GetYaxis().SetTitleSize(0.12)
	hRatio.GetYaxis().SetLabelSize(0.12)
	hRatio.GetYaxis().SetNdivisions(5)
	hRatio.GetXaxis().SetNdivisions(10)
	hRatio.GetYaxis().SetTitleOffset(0.5)
	hRatio.GetXaxis().SetTitleOffset(1.0)
	hRatio.GetXaxis().SetTitle(hObserved.GetXaxis().GetTitle())
	hRatio.Draw()
	hRatio.Draw('e0')    
	pad1.cd()
	hComponents.reverse()
	hObserved.SetTitle(title0)
	return hRatio


def FabDrawSystyRatio(cGold,leg,hObserved,hComponents,datamc='mc',lumi=35.9, title = '', LinearScale=False, fractionthing='(bkg-obs)/obs'):
	cGold.cd()
	pad1 = TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
	pad1.SetBottomMargin(0.0)
	pad1.SetLeftMargin(0.12)
	if not LinearScale:
		pad1.SetLogy()
	
	#pad1.SetGridx()
	#pad1.SetGridy()
	pad1.Draw()
	pad1.cd()
	for ih in range(1,len(hComponents[1:])+1):
		hComponents[ih].Add(hComponents[ih-1])
	hComponents.reverse()        
	if abs(hComponents[0].Integral(-1,999)-1)<0.001:
		hComponents[0].GetYaxis().SetTitle('Normalized')
	else: hComponents[0].GetYaxis().SetTitle('#Events')
	cGold.Update()
	hObserved.GetYaxis().SetTitle('Normalized')
	hObserved.GetYaxis().SetTitleOffset(1.15)
	hObserved.SetMarkerStyle(20)
	histheight = 1.5*max(hComponents[0].GetMaximum(),hObserved.GetMaximum())
	if LinearScale: low, high = 0, histheight
	else: low, high = max(0.001,max(hComponents[0].GetMinimum(),hObserved.GetMinimum())), 1000*histheight
	
	title0 = hObserved.GetTitle()
	if datamc=='MC':
		for hcomp in hComponents: leg.AddEntry(hcomp,hcomp.GetTitle(),'lf')
		leg.AddEntry(hObserved,hObserved.GetTitle(),'lpf')        
	else:
		for ihComp, hComp in enumerate(hComponents):
			leg.AddEntry(hComp, hComp.GetTitle(),'lpf')      
		leg.AddEntry(hObserved,title0,'lp')    
	hObserved.SetTitle('')
	hComponents[0].SetTitle('')	
	xax = hComponents[0].GetXaxis()
	hComponentsUp = hComponents[0].Clone(hComponents[0].GetName()+'UpVariation')
	hComponentsUp.SetLineColor(kWhite)	
	hComponentsDown = hComponents[0].Clone(hComponents[0].GetName()+'DownVariation')	
	hComponentsDown.SetFillColor(10)
	hComponentsDown.SetFillStyle(1001)
	hComponentsDown.SetLineColor(kWhite)
	for ibin in range(1, xax.GetNbins()+1):
		hComponentsUp.SetBinContent(ibin, hComponents[0].GetBinContent(ibin)+hComponents[0].GetBinError(ibin))
		hComponentsDown.SetBinContent(ibin, hComponents[0].GetBinContent(ibin)-hComponents[0].GetBinError(ibin))		
	
	#hComponents[0].Draw('hist')
	hComponentsUp.Draw('hist')
	hComponentsDown.Draw('hist same')
	for h in hComponents[1:]: 
		print 'there are actually components here!'
		h.Draw('hist same')
		cGold.Update()
		print 'updating stack', h
	#hComponents[0].Draw('same') 
	hObserved.Draw('p same')
	hObserved.Draw('e same')    
	cGold.Update()
	hComponents[0].Draw('axis same')           
	leg.Draw()        
	cGold.Update()
	stampFab(lumi,datamc)
	cGold.Update()
	cGold.cd()
	pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.4)
	pad2.SetTopMargin(0.0)
	pad2.SetBottomMargin(0.3)
	pad2.SetLeftMargin(0.12)
	#pad2.SetGridx()
	pad2.SetGridy()
	pad2.Draw()
	pad2.cd()
	hObservedCopy = hObserved.Clone('hObservedClone'+hComponents[0].GetName())
	hRatio = hObservedCopy.Clone('hRatioClone')#hComponents[0].Clone('hRatioClone')#+hComponents[0].GetName()+'testing
	hRatio.SetMarkerStyle(20)
	#hFracDiff = hComponents[0].Clone('hFracDiff')
	#hFracDiff.SetMarkerStyle(20)
	hObservedCopy.SetMarkerStyle(20)
	hObservedCopy.SetMarkerColor(1) 
	#histoStyler(hFracDiff, 1)
	histoStyler(hObservedCopy, 1)
	#hFracDiff.Add(hObservedCopy,-1)
	#hFracDiff.Divide(hObservedCopy)
	#hRatio.Divide(hObservedCopy)
	histoByWhichToDivide = hComponents[0].Clone()
	for ibin in range(1, xax.GetNbins()+1): histoByWhichToDivide.SetBinError(ibin, 0)
	hRatio.Divide(histoByWhichToDivide)
	hRatio.GetYaxis().SetRangeUser(0.0,.1)###
	hRatio.SetTitle('')
	if 'prediction' in title0: hFracDiff.GetYaxis().SetTitle('(RS-#Delta#phi)/#Delta#phi')
	else: hRatio.GetYaxis().SetTitle(fractionthing)
	hRatio.GetXaxis().SetTitleSize(0.12)
	hRatio.GetXaxis().SetLabelSize(0.11)
	hRatio.GetYaxis().SetTitleSize(0.12)
	hRatio.GetYaxis().SetLabelSize(0.12)
	hRatio.GetYaxis().SetNdivisions(5)
	hRatio.GetXaxis().SetNdivisions(10)
	hRatio.GetYaxis().SetTitleOffset(0.5)
	hRatio.GetXaxis().SetTitleOffset(1.0)
	hRatio.GetXaxis().SetTitle(hObserved.GetXaxis().GetTitle())
	hRatio.Draw()
	

	histoMethodFracErrorNom = hComponents[0].Clone(hComponents[0].GetName()+'hMethodSystNom')
	histoMethodFracErrorNom.SetLineColor(kBlack)
	histoMethodFracErrorNom.SetFillStyle(1)
	histoMethodFracErrorUp = hComponents[0].Clone(hComponents[0].GetName()+'hMethodSystUp')
	histoMethodFracErrorUp.SetFillStyle(3001)
	histoMethodFracErrorUp.SetLineColor(kWhite)	
	histoMethodFracErrorUp.SetFillColor(hComponents[0].GetFillColor())	
	histoMethodFracErrorDown = hComponents[0].Clone(hComponents[0].GetName()+'hMethodSystDown')
	histoMethodFracErrorDown.SetLineColor(kWhite)
	#histoMethodFracErrorDown.SetFillStyle(1001)
	histoMethodFracErrorDown.SetFillColor(10)
	for ibin in range(1, xax.GetNbins()+1): 
		content = histoMethodFracErrorUp.GetBinContent(ibin)
		if content>0: err = histoMethodFracErrorUp.GetBinError(ibin)/content
		else: err = 0
		histoMethodFracErrorUp.SetBinContent(ibin, 1+err)
		histoMethodFracErrorUp.SetBinError(ibin, 0)
		histoMethodFracErrorDown.SetBinContent(ibin, 1-err)
		histoMethodFracErrorDown.SetBinError(ibin, 0)		
		histoMethodFracErrorNom.SetBinContent(ibin, 1)		
		histoMethodFracErrorNom.SetBinError(ibin, 0)
	hRatio.GetYaxis().SetRangeUser(-0.2,3.2)	
	hRatio.Draw('e0')    
	histoMethodFracErrorUp.Draw('same hist')	
	histoMethodFracErrorNom.Draw('same')
	histoMethodFracErrorDown.Draw('same hist')
	hRatio.Draw('e0 same')
	hRatio.Draw('axis same')
	pad1.cd()
	hComponents.reverse()
	hObserved.SetTitle(title0)
	pad1.Update()
	
	return hRatio, [histoMethodFracErrorNom, histoMethodFracErrorUp, histoMethodFracErrorDown, hComponentsUp, hComponentsDown]
	
def stampFab(lumi,datamc='MC'):
	tl.SetTextFont(cmsTextFont)
	tl.SetTextSize(1.6*tl.GetTextSize())
	tl.DrawLatex(0.152,0.82, 'CMS')
	tl.SetTextFont(extraTextFont)
	tl.DrawLatex(0.14,0.74, ('MC' in datamc)*' private')
	tl.SetTextFont(regularfont)
	if lumi=='': tl.DrawLatex(0.62,0.82,'#sqrt{s} = 13 TeV')
	else: tl.DrawLatex(0.5,0.82,'#sqrt{s} = 13 TeV, L = '+str(lumi)+' fb^{-1}')
	#tl.DrawLatex(0.64,0.82,'#sqrt{s} = 13 TeV')#, L = '+str(lumi)+' fb^{-1}')	
	tl.SetTextSize(tl.GetTextSize()/1.6)
	

	
units = {}
units['HardMet']='GeV'
units['Met']=units['HardMet']
units['Ht']='GeV'
units['St']='GeV'
units['NJets']=''
units['NCentralJets']=''
units['NForwardJets']=''
units['NLeptons']=''
units['BTags']=''
units['Jet1Pt']='GeV'
units['Jet1Eta']=''
units['Jet2Pt']='GeV'
units['Jet2Eta']=''
units['Jet3Pt']='GeV'
units['Jet3Eta']=''
units['Jet4Pt']='GeV'
units['Jet4Eta']=''
units['HardMetPhi']='rad'
units['DPhi1']='rad'
units['DPhi2']='rad'
units['DPhi3']='rad'
units['DPhi4']='rad'
units['SearchBins']=''
units['BestDijetMass']='GeV'
units['MinDeltaM']='GeV'
units['MaxDPhi']='rad'
units['MaxForwardPt'] = 'GeV'
units['MaxHemJetPt'] = 'GeV'
units['HtRatio'] = ''
units['MinDeltaPhi'] = ''
units['NPhotons'] = ''
units['DPhiPhoPho'] = ''
units['DmStar'] = ''
units['MStar'] = 'GeV'


def mkLabel(str_,kinvar,selection=''):
	newstr = str_
	if newstr[0]=='h':newstr = newstr[1:]
	newstr = newstr.replace('GenSmeared',' gen-smeared ')
	newstr = newstr.replace('Rebalanced',' rebalanced ')
	newstr = newstr.replace('RplusS','QCD R&S')
	newstr = newstr.replace('Observed','QCD Observed')
	newstr = newstr.replace(kinvar,'')
	newstr = newstr.replace('_b','').replace('_','')
	newstr = newstr.replace(selection+' ','')
	return newstr


def nicelabel(label):
	label_ = label
	label_ = label_.replace('Vs',' vs ')
	label_ = label_.replace('HardMet','E_{T}^{miss}')
	label_ = label_.replace('Met','E_{T}^{miss}')
	label_ = label_.replace('Ht','H_{T}')
	label_ = label_.replace('NJets','N_{jets}')
	label_ = label_.replace('BTags','N_{b-jets}')
	label_ = label_.replace('Pt',' p_{T}')
	label_ = label_.replace('Eta',' #eta')
	if 'DPhi' in label_:
		label_ = label_.replace('DPhi','#Delta#phi(H^{miss}_{T}, jet')
		label_ = label_+')'
		numberloc = max(label_.find('1'),label_.find('2'),label_.find('3'),label_.find('4'))+1
		label_ = label_[:numberloc]+', '+label_[numberloc:]
		label_ = label_.replace(', )',')')
	return label_    