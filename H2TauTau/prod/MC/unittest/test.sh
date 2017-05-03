#!/bin/bash

postdir=/afs/hephy.at/work/m/mflechl/git/HephyHiggs/production2016_root6/

steps=0 #0-all, n-only step n
if [ $# -ge 1 ]; then
    steps=$1
fi

nevents=100 #no. of events to be processed
if [ $# -ge 2 ]; then
    nevents=$2
fi

if [ $steps -eq 0 ] || [ $steps -eq 1 ]; then
    echo "Processing step 1..."
    fname="run_step1.py"
    ln -sf $CMSSW_BASE/src/CMGTools/H2TauTau/prod/MC/Summer16_23Sep2016HV4_DATA_UncertaintySources_AK4PFchs.txt .
    ln -sf $CMSSW_BASE/src/CMGTools/H2TauTau/prod/MC/Summer16_23Sep2016V4_MC.db .

    cat $CMSSW_BASE/src/CMGTools/H2TauTau/prod/MC/runMVAMET.py \
                           | sed s#'numberOfFilesToProcess = -1'#'numberOfFilesToProcess = 1'#g \
                           | sed s#'process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(-1))'#'process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32('${nevents}'))'#g \
			   | sed s#"dataset_name =.*"#"dataset_name = '/SUSYGluGluToBBHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'"#g \
                           >$fname
    cmsRun $fname &>log1.txt
    mv outfile_newMVA.root step1.root
    echo Step 1 done! Output file: step1.root
fi

if [ $steps -eq 0 ] || [ $steps -eq 2 ]; then
    echo "Processing step 2..."

    fname="run_step2.py"
    rm -f $fname

    record=0
    while IFS='' read -r line || [[ -n $line ]]
    do
	if [[ $line == *"FOR TESTING"* ]]; then
	    record=1
	    continue
	fi
	if [[ $line == *"###################################"* ]]; then
	    record=0
	    continue
	fi
	
	if [ $record -eq 1 ]; then
	    rec=${line/\#/}
	    echo "$rec" | sed s/"comp.files =.*"/"comp.files = ['step1.root']"/g >>$fname
	    if [[ $line == *"selectedComponents"* ]]; then
		record=0
		continue
	    fi
	fi
    done < $CMSSW_BASE/src/CMGTools/RootTools/python/samples/TEMPLATE_run_vienna_h2tau_cfg.py

    echo "" >>$fname

    grep "comp.puFile" $CMSSW_BASE/src/CMGTools/TTHAnalysis/cfg/crab_HEPHY/heppy_crab_script.py >>$fname
    grep -E "higgsCore_modules_cff.*import" $CMSSW_BASE/src/CMGTools/RootTools/python/samples/TEMPLATE_run_vienna_h2tau_cfg.py >>$fname
    grep "from CMGTools" $CMSSW_BASE/src/CMGTools/TTHAnalysis/cfg/crab_HEPHY/heppy_crab_script.py | sed s#' as seq'##g >>$fname

    record=0
    while IFS='' read -r line || [[ -n $line ]]
    do
	if [[ $line == *"from PhysicsTools.HeppyCore"* ]]; then
	    record=1
	fi
	
	if [ $record -eq 1 ]; then
	    rec=${line/\# /}
	    echo "$rec" >>$fname
	fi
    done < $CMSSW_BASE/src/CMGTools/RootTools/python/samples/TEMPLATE_run_vienna_h2tau_cfg.py

    rm -rf dtest
    heppy dtest $fname &>log2.txt
    mv dtest/*/*/tree.root step2.root
    rm -rf dtest
    echo Step 2 done! Output file: step2.root

    echo "Output of first max 24 events: met_pt:ngenSum:njet:puWeight:ntriggerObject_IsoMu22:el_pt[0]:mu_pt[0]:tau_pt[0]"
    root -l step2.root <<<"tree->Scan(\"evt:met_pt:ngenSum:njet:puWeight:ntriggerObject_IsoMu22:el_pt[0]:mu_pt[0]:tau_pt[0]\",\"\",\"\",24);" | grep "*" | grep -v TFile

fi

if [ $steps -eq 0 ] || [ $steps -eq 3 ]; then
    echo "Processing step 3..."

    cdir=/data/higgs/data_2016/cmgTuples/test_test_19800101

    mkdir -p $cdir
    cp -p step2.root $cdir
    cd $postdir
    mv var_cfg.txt var_cfg.txt.bak

    record=0
    while IFS='' read -r line || [[ -n $line ]]
    do
	echo "$line" >>var_cfg.txt
        if [[ $line == *"-Sig-"* ]]; then
            record=1
	    continue
        fi

        if [ $record -eq 1 ]; then
            rec=`echo "$line" | sed s#'[a-zA-Z0-9_]*$'#test#g`
	    echo "$rec" >>var_cfg.txt
	    record=0
        fi
    done < var_cfg.txt.bak

    rm -rf /data/higgs/data_2016/sync/BASIS_ntuple_test_test_19800101_mt_1
    python runPostprocess.py -c mt -v 1 --sync -s test &>log3.txt

    rm -rf $cdir
    mv var_cfg.txt.bak var_cfg.txt
    cd -
    cp -p /data/higgs/data_2016/sync/BASIS_ntuple_test_test_19800101_mt_1/tree.root step3.root
    echo Step 3 done! Output file: step3.root

    echo "Output of first max 24 events: evt:weight:trg_singlemuon:gen_match_2:pt_1:pt_2:met:mt_1:m_vis:iso_1:iso_2:njetspt20:jpt_1:bcsv_1"
    root -l step3.root <<<"TauCheck->Scan(\"evt:weight:trg_singlemuon:gen_match_2:pt_1:pt_2:met:mt_1:m_vis:iso_1:iso_2:njetspt20:jpt_1:bcsv_1\",\"\",\"\",24);" | grep "*" | grep -v TFile

fi
