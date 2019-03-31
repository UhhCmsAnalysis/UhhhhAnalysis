# Uhhhh
This is a package for analyzing events with HH-like final states on the NAF.
## Set up code

```
cmsrel CMSSW_10_1_0
cd CMSSW_10_1_0/src
cmsenv
git clone https://github.com/sbein/RebalanceAndSmear/
cd RebalanceAndSmear/
mkdir output output/smallchunks output/mediumchunks output/bigchunks
mkdir jobs
```

### run event analyzer script to generate histograms
#### examples:

run over a signal file
```
python tools/EventAnalyzer.py --fnamekeyword /pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/SpecialSM/VBFHHTo4B_CV_1_5_C2V_1_C3_1_13TeV-madgraph_file20.root_RA2AnalysisTree.root
```

run over a background file
```
python tools/EventAnalyzer.py --fnamekeyword  /pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_73_RA2AnalysisTree.root
```

## parallelize running of scripts with condor jobs

submit signal jobs (one job per input file)

```
python tools/SubmitJobs_condor.py --analyzer tools/EventAnalyzer.py --fnamekeyword  "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/SpecialSM/VBFHHTo4B*.root"
```

## run over many background files

submit background jobs (one job per input file)

```
python tools/SubmitJobs_condor.py --analyzer tools/EventAnalyzer.py --fnamekeyword  "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.TTJets_TuneCUE*.root"
python tools/SubmitJobs_condor.py --analyzer tools/EventAnalyzer.py --fnamekeyword  "/pnfs/desy.de/cms/tier2/store/user/sbein/NtupleHub/Production2016v2/Summer16.QCD*.root"
```

files will show up in the folder output/smallchunks. You can check the status of jobs and interact with jobs using
```
condor_q
condor_rm <job number>
condor_release <username>
```

## to combine the files and apply weights to the events, 
when the jobs have finished, you can combine the many files into just a few:
```
python tools/MergeHistsPropWeights.py output/smallchunks/
```

This produces a set of files with histograms weighted to lumi=1/pb in output/bigchunks

## draw stacked histograms of background overlay signal:

```
python tools/EventPlotter.py
```

This produces a file, probably plots.root, which you can open and examine the canvases within. 


