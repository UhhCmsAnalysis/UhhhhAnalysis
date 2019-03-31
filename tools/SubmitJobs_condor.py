import os, sys
from glob import glob
from random import shuffle 
from time import sleep

test = False

import argparse
parser = argparse.ArgumentParser()
defaultfkey = 'Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2_28'
parser.add_argument("-v", "--verbosity", type=bool, default=False,help="analyzer script to batch")
parser.add_argument("-analyzer", "--analyzer", type=str,default='tools/ResponseMaker.py',help="analyzer")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultfkey,help="file")
parser.add_argument("-jersf", "--JerUpDown", type=str, default='Nom',help="JER scale factor (Nom, Up, ...)")
parser.add_argument("-dtmode", "--dtmode", type=str, default='PixAndStrips',help="PixAndStrips, PixOnly, PixOrStrips")
parser.add_argument("-pu", "--pileup", type=str, default='Nom',help="Nom, Low, Med, High")
parser.add_argument("-gk", "--useGenKappa", type=bool, default=False,help="use gen-kappa")
parser.add_argument("-SmearCands4Zed", "--SmearCands4Zed", type=str, default='True')
args = parser.parse_args()
SmearCands4Zed = args.SmearCands4Zed=='True'
fnamekeyword = args.fnamekeyword.strip()
filenames = fnamekeyword
analyzer = args.analyzer
analyzer = analyzer.replace('python/','').replace('tools/','')
JerUpDown = args.JerUpDown
useGenKappa = args.useGenKappa
    

try: 
	moreargs = ' '.join(sys.argv)
	moreargs = moreargs.split('--fnamekeyword')[-1]	
	moreargs = ' '.join((moreargs.split()[1:]))
except: moreargs = ''
moreargs = moreargs.strip()
print 'moreargs', moreargs

cwd = os.getcwd()
filelist = glob(filenames)
shuffle(filelist)


filesperjob = 1

def main():
    ijob = 1
    files = ''
    for ifname, fname in enumerate(filelist):
        files += fname+','
        print fname
        if (ifname+1)%filesperjob==filesperjob-1:
            print '==='*3
            jobname = analyzer.replace('.py','')+'-'+fname[fname.rfind('/')+1:].replace('.root','_'+str(ijob))
            if len(moreargs)>0: jobname = jobname.replace('.root',''.join(moreargs)+'.root')
            fjob = open('jobs/'+jobname+'.sh','w')
            files = files[:-1]
            fjob.write(jobscript.replace('CWD',cwd).replace('FNAMEKEYWORD',fname).replace('ANALYZER',analyzer).replace('MOREARGS',moreargs).replace('JOBNAME',jobname))
            fjob.close()
            os.chdir('jobs')
            command = 'condor_qsub -cwd '+jobname+'.sh &'
            print command
            if not test: os.system(command)
            os.chdir('..')
            files = ''
            ijob+=1
            if test: break
            sleep(0.15)
        
jobscript = '''#!/bin/zsh
source /etc/profile.d/modules.sh
source /afs/desy.de/user/b/beinsam/.bash_profile
module use -a /afs/desy.de/group/cms/modulefiles/
module load cmssw
export THISDIR=$PWD
echo "$QUEUE $JOB $HOST"
source /afs/desy.de/user/b/beinsam/.bash_profile
cd CWD
cmsenv
cd $THISDIR
export timestamp=$(date +%Y%m%d_%H%M%S%N)
mkdir $timestamp
cd $timestamp
cp -r CWD/tools .
cp -r CWD/usefulthings .
python tools/ANALYZER --fnamekeyword FNAMEKEYWORD MOREARGS > CWD/jobs/JOBNAME.out > CWD/jobs/JOBNAME.out 2> CWD/jobs/JOBNAME.err
mv *.root CWD/output/smallchunks
cd ../
rm -rf $timestamp
'''

main()
