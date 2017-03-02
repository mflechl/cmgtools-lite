##########################################################
##       CONFIGURATION FOR Higgs->tautau TREES          ##
## skim condition: >= 0 loose leptons, no pt cuts or id ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg


#Load all analyzers
from CMGTools.TTHAnalysis.analyzers.higgsCore_modules_cff import * 

# Redefine what I need
lepAna.loose_muon_relIso = 999 #reliso03
lepAna.mu_isoCorr = "deltaBeta" 

lepAna.loose_electron_relIso = 999 #reliso03 
lepAna.ele_isoCorr = "deltaBeta" 

tauAna.tauLooseID = "decayModeFindingNewDMs"
tauAna.tauID = "decayModeFindingNewDMs"
tauAna.vetoLeptons = False
tauAna.vetoLeptonsPOG = False
tauAna.ptMin = 20
tauAna.etaMax = 2.5


jetAna.minLepPt = 10
jetAna.jetPt = 20
jetAna.jetEta = 4.7

jetAna.mcGT   = "Summer16_23Sep2016V4_MC"
# jetAna.dataGT = "Summer16_23Sep2016BCDV4_DATA"
# jetAna.dataGT = "Summer16_23Sep2016EFV4_DATA"
# jetAna.dataGT = "Summer16_23Sep2016GV4_DATA"
# jetAna.dataGT = "Summer16_23Sep2016HV4_DATA"
jetAna.do_mc_match = True
jetAna.smearJets = False #should be false in susycore, already                                      
jetAna.calculateSeparateCorrections = True 
jetAna.recalibrateJets =  True #For data  
jetAna.applyJetSmearing = False                                                                                                                                                        

metAna.recalibrate = False #should be false in susycore, already 
metAna.isDilepton=False
metAna.isTauMu=True
metAna.isTauEle=False

# --- LEPTON SKIMMING ---
#ttHLepSkim.minLeptons = 0
#ttHLepSkim.maxLeptons = 999
##LepSkim.idCut  = ""
##LepSkim.ptCuts = []

# --- JET-LEPTON CLEANING ---

#ttHReclusterJets = cfg.Analyzer(
#            'ttHReclusterJetsAnalyzer',
#            )


## isoTrackAna.setOff=False

#from CMGTools.TTHAnalysis.analyzers.ttHReclusterJetsAnalyzer  import ttHReclusterJetsAnalyzer
#ttHReclusterJets = cfg.Analyzer(
#    ttHReclusterJetsAnalyzer, name="ttHReclusterJetsAnalyzer",
#    )
from CMGTools.TTHAnalysis.analyzers.ttHLepEventAnalyzer import ttHLepEventAnalyzer
ttHEventAna = cfg.Analyzer(
    ttHLepEventAnalyzer, name="ttHLepEventAnalyzer",
    minJets25 = 0,
    )



TriggerTag = 'HLT'

triggerFlagsAna.processName = TriggerTag
triggerFlagsAna.triggerBits = {

 # "HLT_IsoMu18"                                              :["HLT_IsoMu18_v*"],
 # "HLT_IsoMu20"                                              :["HLT_IsoMu20_v*"],
 # "HLT_IsoMu22"                                              :["HLT_IsoMu22_v*"],
 # "HLT_IsoMu22_eta2p1"                                       :["HLT_IsoMu22_eta2p1_v*"],
 # "HLT_IsoMu24"                                              :["HLT_IsoMu24_v*"],
 # "HLT_IsoMu27"                                              :["HLT_IsoMu27_v*"],
 # "HLT_IsoTkMu18"                                            :["HLT_IsoTkMu18_v*"],
 # "HLT_IsoTkMu20"                                            :["HLT_IsoTkMu20_v*"],
 # "HLT_IsoTkMu22"                                            :["HLT_IsoTkMu22_v*"],
 # "HLT_IsoTkMu22_eta2p1"                                     :["HLT_IsoTkMu22_eta2p1_v*"],
 # "HLT_IsoTkMu24"                                            :["HLT_IsoTkMu24_v*"],
 # "HLT_IsoTkMu27"                                            :["HLT_IsoTkMu27_v*"],
 # "HLT_IsoMu17_eta2p1_LooseIsoPFTau20_SingleL1"              :["HLT_IsoMu17_eta2p1_LooseIsoPFTau20_SingleL1_v*"],
 # "HLT_IsoMu17_eta2p1_LooseIsoPFTau20"                       :["HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v*"],
 # "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1"              :["HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v*"],
 "HLT_IsoMu19_eta2p1_LooseIsoPFTau20"                       :["HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v*"],
 # "HLT_IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1"              :["HLT_IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1_v*"],
 
 # "HLT_Ele23_WPLoose_Gsf"                                    :["HLT_Ele23_WPLoose_Gsf_v*"],
 # "HLT_Ele24_eta2p1_WPLoose_Gsf"                             :["HLT_Ele24_eta2p1_WPLoose_Gsf_v*"],
 # "HLT_Ele25_WPTight_Gsf"                                    :["HLT_Ele25_WPTight_Gsf_v*"],
 # "HLT_Ele25_eta2p1_WPLoose_Gsf"                             :["HLT_Ele25_eta2p1_WPLoose_Gsf_v*"],
 # "HLT_Ele25_eta2p1_WPTight_Gsf"                             :["HLT_Ele25_eta2p1_WPTight_Gsf_v*"],
 # "HLT_Ele27_WPLoose_Gsf"                                    :["HLT_Ele27_WPLoose_Gsf_v*"],
 # "HLT_Ele27_WPTight_Gsf"                                    :["HLT_Ele27_WPTight_Gsf_v*"],
 # "HLT_Ele27_eta2p1_WPLoose_Gsf"                             :["HLT_Ele27_eta2p1_WPLoose_Gsf_v*"],
 # "HLT_Ele27_eta2p1_WPTight_Gsf"                             :["HLT_Ele27_eta2p1_WPTight_Gsf_v*"],
 # "HLT_Ele32_eta2p1_WPTight_Gsf"                             :["HLT_Ele32_eta2p1_WPTight_Gsf_v*"],
 # "HLT_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1"    :["HLT_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v*"],
 # "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1"    :["HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v*"],
 # "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20"             :["HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v*"],
 # "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30"             :["HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30_v*"],
 # "HLT_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1"    :["HLT_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v*"],
 # "HLT_Ele32_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1"    :["HLT_Ele32_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v*"],
 # "HLT_Ele45_WPLoose_Gsf_L1JetTauSeeded"                     :["HLT_Ele45_WPLoose_Gsf_L1JetTauSeeded_v*"],

 # "HLT_VLooseIsoPFTau120_Trk50_eta2p1"                       :["HLT_VLooseIsoPFTau120_Trk50_eta2p1_v*"],
 # "HLT_VLooseIsoPFTau140_Trk50_eta2p1"                       :["HLT_VLooseIsoPFTau140_Trk50_eta2p1_v*"],
 # "HLT_DoubleMediumIsoPFTau32_Trk1_eta2p1_Reg"               :["HLT_DoubleMediumIsoPFTau32_Trk1_eta2p1_Reg_v*"],
 # "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg"               :["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v*"],
 # "HLT_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg"               :["HLT_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg_v*"],
 # "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg"       :["HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v*"],
}
triggerObjsAna.triggerResultsHandle = ('TriggerResults', '', TriggerTag)

triggerObjsAna.extraTrig = triggerFlagsAna.triggerBits.keys()



filter_dict = { 
    'HLT_IsoMu18':   'hltL3crIsoL1sMu16L1f0L2f10QL3f18QL3trkIsoFiltered0p09',
    'HLT_IsoMu20':   'hltL3crIsoL1sMu18L1f0L2f10QL3f20QL3trkIsoFiltered0p09',
    'HLT_IsoMu22':   'hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09',
    'HLT_IsoMu22_eta2p1': 'hltL3crIsoL1sSingleMu20erL1f0L2f10QL3f22QL3trkIsoFiltered0p09',
    'HLT_IsoMu24':   'hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09',
    'HLT_IsoMu27':  'hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p09',
    'HLT_IsoTkMu18':   'hltL3fL1sMu16L1f0Tkf18QL3trkIsoFiltered0p09',
    'HLT_IsoTkMu20':   'hltL3fL1sMu18L1f0Tkf20QL3trkIsoFiltered0p09',
    'HLT_IsoTkMu22_eta2p1': 'hltL3fL1sMu20erL1f0Tkf22QL3trkIsoFiltered0p09',
    'HLT_IsoTkMu22':   'hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09',
    'HLT_IsoTkMu24':   'hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09',
    'HLT_IsoTkMu27':  'hltL3fL1sMu22Or25L1f0Tkf27QL3trkIsoFiltered0p09',
    'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1':['hltL3crIsoL1sSingleMu18erIorSingleMu20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09','hltOverlapFilterSingleIsoMu19LooseIsoPFTau20'],
    "HLT_IsoMu19_eta2p1_LooseIsoPFTau20": ["hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09","hltPFTau20TrackLooseIsoAgainstMuon","hltOverlapFilterIsoMu19LooseIsoPFTau20"],

    'HLT_VLooseIsoPFTau120_Trk50_eta2p1' : 'hltPFTau120TrackPt50LooseAbsOrRelVLooseIso' ,
    'HLT_VLooseIsoPFTau140_Trk50_eta2p1' : 'hltPFTau140TrackPt50LooseAbsOrRelVLooseIso' ,
    'HLT_Ele25_eta2p1_WPTight_Gsf' : 'hltEle25erWPTightGsfTrackIsoFilter',
    'HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg' : 'hltDoublePFTau35TrackPt1MediumIsolationDz02Reg',
    'HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg' : 'hltDoublePFTau35TrackPt1MediumCombinedIsolationDz02Reg',
}

jsonAna.json='$CMSSW_BASE/src/CMGTools/RootTools/data/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'

# Tree Producer
from CMGTools.TTHAnalysis.analyzers.treeProducerHiggsToTauTau import *
## Tree Producer

for name in triggerFlagsAna.triggerBits.keys():
    higgsToTauTau_collections.update( getTriggerCollection(name, filter_dict) )

treeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='treeProducerHiggsToTauTau',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     PDFWeights = PDFWeights,
     PDFGen = PDFGen,
     globalVariables = higgsToTauTau_globalVariables,
     globalObjects = higgsToTauTau_globalObjects,
     collections = higgsToTauTau_collections,
)



sequence = cfg.Sequence(
    higgsCoreSequence+[
#    ttHEventAna,
#    ttHReclusterJets,
    treeProducer,
    ])


selectedComponents = [ ]

####################### FOR TESTING ###############################                
from CMGTools.RootTools.samples.samples_13TeV_test import *
comp = VBF
comp.files = ['root://cms-xrd-global.cern.ch//store/user/mspanrin/VBFHToTauTau_M125_13TeV_powheg_pythia8/VBFHToTauTau_M125_powheg_MCSummer16_170222/170221_232256/0000/outfile_newMVA_13.root']
print comp.files
selectedComponents = [comp]
#     comp.splitFactor = 250
#     comp.puFileData = '../MyDataPileupHistogram_observed_new.root'
#     comp.puFileMC = '../MyMCPileupHistogram_normOfficial.root'
###################################################################   

from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = [],
                     events_class = Events)
