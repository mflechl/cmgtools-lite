##########################################################
##          Higgs MODULES ARE DEFINED HERE              ##
## skimming modules are configured to not cut anything  ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.Heppy.analyzers.core.all import *
from PhysicsTools.Heppy.analyzers.objects.all import *
from PhysicsTools.Heppy.analyzers.gen.all import *
from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer import TriggerAnalyzer
from CMGTools.H2TauTau.proto.analyzers.L1TriggerAnalyzer import L1TriggerAnalyzer
from CMGTools.H2TauTau.proto.analyzers.MCWeighter import MCWeighter
from CMGTools.H2TauTau.proto.analyzers.METFilter import METFilter
import os

PDFGen = "MG" #MF LHE
#PDFGen = "aMC" #MF LHE

PDFWeights = [ ("NNPDF30_lo_as_0130",101) ]
#PDFWeights = [ ("CT10",53), ("MSTW2008lo68cl",41), ("MMHT2014lo68cl",51), ("NNPDF21_100",101) ]
#PDFWeights = [ ("NNPDF30_lo_as_0130",101) ] #("NNPDF30_lo_as_0130_nf_4",101)] 

# Find the initial events before the skim
skimAnalyzer = cfg.Analyzer(
    SkimAnalyzerCount, name='skimAnalyzerCount',
    useLumiBlocks = False,
    )

mcWeighter = cfg.Analyzer(
    MCWeighter,
    name='MCWeighter'
)

lheWeightAna = cfg.Analyzer(
    LHEWeightAnalyzer, name="LHEWeightAnalyzer",
)

# Pick individual events (normally not in the path)
eventSelector = cfg.Analyzer(
    EventSelector,name="EventSelector",
    toSelect = [1310750]  # here put the event numbers (actual event numbers from CMSSW)
    )

# Apply json file (if the dataset has one)
jsonAna = cfg.Analyzer(
    JSONAnalyzer,
    name="JSONAnalyzer",
    )

# Filter using the 'triggers' and 'vetoTriggers' specified in the dataset
triggerAna = cfg.Analyzer(
    TriggerBitFilter,
    name="TriggerBitFilter",
    )
# Create flags for trigger bits
triggerFlagsAna = cfg.Analyzer(
    TriggerBitAnalyzer,
    name="TriggerFlags",
    processName = 'HLT',
    outprefix   = 'trig',
    triggerBits = {
        # "<name>" : [ 'HLT_<Something>_v*', 'HLT_<SomethingElse>_v*' ] 
    },
    )
triggerObjsAna = cfg.Analyzer(
    TriggerAnalyzer,
    name = 'TriggerAnalyzer',
    addTriggerObjects=True,
    requireTrigger=False,
    usePrescaled=False,
    triggerResultsHandle = ('TriggerResults', '', 'HLT'),
    extraTrig = [],
)

L1triggerObjsAna = cfg.Analyzer(
    L1TriggerAnalyzer,
    name='L1TriggerAnalyzer',
    label = 'l1extraParticles',
    collections = 'IsoTau',
)

# Create flags for MET filter bits
eventFlagsAna = cfg.Analyzer(
    TriggerBitAnalyzer, name="EventFlags",
    processName = 'PAT',
    outprefix   = 'flag',
    triggerBits = {
        "HBHENoiseFilter" : [ "Flag_HBHENoiseFilter" ],
        "CSCTightHaloFilter" : [ "Flag_CSCTightHaloFilter" ],
        "hcalLaserEventFilter" : [ "Flag_hcalLaserEventFilter" ],
        "EcalDeadCellTriggerPrimitiveFilter" : [ "Flag_EcalDeadCellTriggerPrimitiveFilter" ],
        "goodVertices" : [ "Flag_goodVertices" ],
        "trackingFailureFilter" : [ "Flag_trackingFailureFilter" ],
        "eeBadScFilter" : [ "Flag_eeBadScFilter" ],
        "ecalLaserCorrFilter" : [ "Flag_ecalLaserCorrFilter" ],
        "trkPOGFilters" : [ "Flag_trkPOGFilters" ],
        "trkPOG_manystripclus53X" : [ "Flag_trkPOG_manystripclus53X" ],
        "trkPOG_toomanystripclus53X" : [ "Flag_trkPOG_toomanystripclus53X" ],
        "trkPOG_logErrorTooManyClusters" : [ "Flag_trkPOG_logErrorTooManyClusters" ],
    }
    )

# Select a list of good primary vertices (generic)
vertexAna = cfg.Analyzer(
    VertexAnalyzer, name="VertexAnalyzer",
    vertexWeight = None,
    fixedWeight = 1,
    keepFailingEvents = True,
    verbose = False
    )


# This analyzer actually does the pile-up reweighting (generic)
pileUpAna = cfg.Analyzer(
    PileUpAnalyzer, name="PileUpAnalyzer",
    true = True,  # use number of true interactions for reweighting
    #makeHists=False
    )


## Gen Info Analyzer (generic, but should be revised)
genAna = cfg.Analyzer(
    GeneratorAnalyzer, name="GeneratorAnalyzer",
    # BSM particles that can appear with status <= 2 and should be kept
    stableBSMParticleIds = { },
    # Particles of which we want to save the pre-FSR momentum (a la status 3).
    # Note that for quarks and gluons the post-FSR doesn't make sense,
    # so those should always be in the list
    savePreFSRParticleIds = { 1,2,3,4,5, 11,12,13,14,15,16, 21,22,23,24,25 },
    # Make also the list of all genParticles, for other analyzers to handle
    makeAllGenParticles = True, #breaks code to set to false
#    makeAllGenParticles = False, #breaks code to set to false
    # Make also the splitted lists
    makeSplittedGenLists = True, #breaks code to set to false
#    makeSplittedGenLists = False, #breaks code to set to false
    allGenTaus = False, #not working?
    makeLHEweights = True,
#    allGenTaus = True,
    # Print out debug information
    verbose = False,
    )

# The following two need makeAllGenParticles and makeSplittedGenLists !
#mf genHiggsAna = cfg.Analyzer(
#mf    HiggsDecayModeAnalyzer, name="HiggsDecayModeAnalyzer",
#mf    filterHiggsDecays = False,
#mf )

#mf genHFAna = cfg.Analyzer(
#mf    GenHeavyFlavourAnalyzer, name="GenHeavyFlavourAnalyzer",
#mf    status2Only = False,
#mf    bquarkPtCut = 15.0,
#mf )

pdfwAna = cfg.Analyzer(
    PDFWeightsAnalyzer, name="PDFWeightsAnalyzer",
    PDFWeights = [ pdf for pdf,num in PDFWeights ],
    PDFGen = PDFGen #MF LHE
    )

# Lepton Analyzer (generic)
lepAna = cfg.Analyzer(
    LeptonAnalyzer, name="leptonAnalyzer",
    # input collections
    muons='slimmedMuons',
    electrons='slimmedElectrons',
    rhoMuon= 'fixedGridRhoFastjetAll',
    rhoElectron = 'fixedGridRhoFastjetAll',
    doMuonScaleCorrections=False,
    doElectronScaleCorrections=False,
    doSegmentBasedMuonCleaning=False,
    # energy scale corrections and ghost muon suppression (off by default)
    #doRochesterCorrections=False,
    #doElectronScaleCorrections=False, # "embedded" in 5.18 for regression
    #doSegmentBasedMuonCleaning=False,
    # inclusive very loose muon selection
    inclusive_muon_id  = "POG_ID_Loose",
    inclusive_muon_pt  = 5.,
    inclusive_muon_eta = 2.4,
    inclusive_muon_dxy = 0.5,
    inclusive_muon_dz  = 1.0,
    muon_dxydz_track = "muonBestTrack", #JB instead of "innerTrack"
    # loose muon selection
    loose_muon_id     = "POG_ID_Loose",
    loose_muon_pt     = 5.,
    loose_muon_eta    = 2.4,
    loose_muon_dxy    = 0.5,
    loose_muon_dz     = 1.,
    loose_muon_relIso = 1.,
    # loose_muon_relIso = 0.5, #JB
    # inclusive very loose electron selection
    inclusive_electron_id  = "",
    inclusive_electron_pt  = 5.,
    inclusive_electron_eta = 2.5,
    inclusive_electron_dxy = 0.5,
    inclusive_electron_dz  = 1.0,
    inclusive_electron_lostHits = 1.0,
    # loose electron selection
    loose_electron_id     = "",
    loose_electron_pt     = 5.,
    loose_electron_eta    = 2.5,
    loose_electron_dxy    = 0.045,
    loose_electron_dz     = 0.2,
    loose_electron_relIso = 0.5,
    loose_electron_lostHits = 1.0,
    # muon isolation correction method (can be "rhoArea" or "deltaBeta")
#    mu_isoCorr = "rhoArea" ,
    mu_isoCorr = "deltaBeta" ,
    mu_effectiveAreas = "Spring15_25ns_v1", #(can be 'Data2012' or 'Phys14_25ns_v1')
    # electron isolation correction method (can be "rhoArea" or "deltaBeta")
#    ele_isoCorr = "rhoArea" ,
    ele_isoCorr = "deltaBeta" ,
    el_effectiveAreas = "Spring15_25ns_v1" , #(can be 'Data2012' or 'Phys14_25ns_v1')
    ele_tightId = "MVA" ,
    # minimum deltaR between a loose electron and a loose muon (on overlaps, discard the electron)
    min_dr_electron_muon = 0.02,
    # do MC matching 
    do_mc_match = True, # note: it will in any case try it only on MC, not on data
    match_inclusiveLeptons = False, # match to all inclusive leptons
    )

## Lepton-based Skim (generic, but requirements depend on the final state)
#from CMGTools.TTHAnalysis.analyzers.ttHLepSkimmer import ttHLepSkimmer
#ttHLepSkim = cfg.Analyzer(
#    ttHLepSkimmer, name='ttHLepSkimmer',
#    minLeptons = 0,
#    maxLeptons = 999,
#    #idCut  = "lepton.relIso03 < 0.2" # can give a cut
#    #ptCuts = [20,10],                # can give a set of pt cuts on the leptons
#    )

## Photon Analyzer (generic)
# photonAna = cfg.Analyzer(
#    PhotonAnalyzer, name='photonAnalyzer',
#    photons='slimmedPhotons',
#    ptMin = 20,
#    etaMax = 2.5,
#    gammaID = "PhotonCutBasedIDLoose_CSA14",
#    do_mc_match = True,
#)


## Tau Analyzer (generic)
tauAna = cfg.Analyzer(
    TauAnalyzer, name="tauAnalyzer",
    inclusive_ptMin = 18,
    inclusive_etaMax = 2.5,
    inclusive_dxyMax = 1000,
    inclusive_dzMax = 10,
#    vetoLeptons = True,
    inclusive_vetoLeptons = False,
#    inclusive_leptonVetoDR = 0.3,
#    vetoLeptonsPOG = False,
    inclusive_vetoLeptonsPOG = False,
    inclusive_tauID = "decayModeFindingNewDMs",
    inclusive_tauLooseID = "decayModeFindingNewDMs",
    
    inclusive_tauAntiMuonID = "",
    inclusive_tauAntiElectronID = "",

    # loose hadronic tau selection                                                                                                                       
    loose_ptMin = 18,
    loose_etaMax = 9999,
    loose_dxyMax = 1000.,
    loose_dzMax = 1000.,
    loose_vetoLeptons = False,
    loose_decayModeID = "decayModeFindingNewDMs",
    loose_tauID = "decayModeFindingNewDMs",
    loose_vetoLeptonsPOG = False,
)

##------------------------------------------
###  ISOLATED TRACK
###------------------------------------------                                                                                                                                                                
#
## those are the cuts for the nonEMu                                                                                                                                                                         
# isoTrackAna = cfg.Analyzer(
#     IsoTrackAnalyzer, name='isoTrackAnalyzer',
#     setOff=True,
#     #####
#     candidates='packedPFCandidates',
#     candidatesTypes='std::vector<pat::PackedCandidate>',
#     ptMin = 5, # for pion 
#     ptMinEMU = 5, # for EMU
#     dzMax = 0.1,
#     #####
#     isoDR = 0.3,
#     ptPartMin = 0,
#     dzPartMax = 0.1,
#     maxAbsIso = 8,
#     #####
#     MaxIsoSum = 0.1, ### unused
#     MaxIsoSumEMU = 0.2, ### unused
#     doSecondVeto = False,
#     #####
#     doPrune = True
#     )


## Jets Analyzer (generic)                                                                                                                                                                                                                    
jetAna = cfg.Analyzer(
    JetAnalyzer, name='jetAnalyzer',
    jetCol = 'slimmedJets',
    copyJetsByValue = False,      #Whether or not to copy the input jets or to work with references (should be 'True' if JetAnalyzer is run more than once)                                    
    genJetCol = 'slimmedGenJets',
    rho = ('fixedGridRhoFastjetAll','',''),
    jetPt = 20., #JB instead 25                                                                                                                             
    jetEta = 4.7,
    jetEtaCentral = 2.4, #JB instead 2.4
    jetLepDR = 0.4, #JB instead 0.4 
    #also did the corrections in PhysicsTools/Heppy/python/analyzers/objects/JetAnalyzer.py                                                                                                               
    jetLepArbitration = (lambda jet,lepton : jet), # you can decide which to keep in case of overlaps; e.g. if the jet is b-tagged you might want to keep the jet                                     
    cleanSelectedLeptons = True, #Whether to clean 'selectedLeptons' after disambiguation. Treat with care (= 'False') if running Jetanalyzer more than once                                             
    minLepPt = 10, #by JB
    relaxJetId = False,
    doPuId = False, # Not commissioned in 7.0.X
    recalibrateJets = True, # True, False, 'MC', 'Data' 
    applyL2L3Residual = True,
    recalibrationType = "AK4PFchs",
    mcGT     = "80X_mcRun2_asymptotic_2016_miniAODv2",
    data     = "Summer15_25nsV6_DATA",
    jecPath = "${CMSSW_BASE}/src/CMGTools/RootTools/data/jec/",
    shiftJEC = 0, # set to +1 or -1 to apply +/-1 sigma shift to the nominal jet energies                                                                                                                  
    addJECShifts = True, # if true, add  "corr", "corrJECUp", and "corrJECDown" for each jet (requires uncertainties to be available!)
    smearJets = False,                                           
    shiftJER = 0, # set to +1 or -1 to get +/-1 sigma shifts
    addJERShifts = True,
    alwaysCleanPhotons = False,
    cleanJetsFromFirstPhoton = False,
    cleanJetsFromTaus = False,
    cleanJetsFromLeptons = True,
    storeLowPtJets = True,
    cleanJetsFromIsoTracks = False,
    doQG = False,
    cleanGenJetsFromPhoton = False,
    calculateSeparateCorrections = True,
    collectionPostFix = "",
    calculateType1METCorrection = False,
    type1METParams = { 'jetPtThreshold':15., 'skipEMfractionThreshold':0.9, 'skipMuons':True },
    )

metAna = cfg.Analyzer(
    METAnalyzer, name="metAnalyzer",
    metCollection     = "slimmedMETs::MVAMET",
    noPUMetCollection = "slimmedMETs::MVAMET",
    copyMETsByValue = False,
    doTkMet = True,
    doMetNoPU = False,
    doMetNoMu = False,
    doMetNoEle = False,
    doMetNoPhoton = False,
    recalibrate = False,
    applyJetSmearing = False, # does nothing unless the jet smearing is turned on in the jet analyzer                                                                                                     
    old74XMiniAODs = False,   # can't be true, since MET NoHF wasn't there in old 74X MiniAODs                                                                                                            
    jetAnalyzerPostFix = "",
    candidates='packedPFCandidates',
    candidatesTypes='std::vector<pat::PackedCandidate>',
    dzMax = 0.1,
    collectionPostFix = "",
    )

metFilter = cfg.Analyzer(
    METFilter,
    name='METFilter',
    processName='RECO',
    triggers=[
        'Flag_HBHENoiseFilter', 
        'Flag_HBHENoiseIsoFilter', 
        'Flag_EcalDeadCellTriggerPrimitiveFilter',
        'Flag_goodVertices',
        'Flag_eeBadScFilter',
        'Flag_globalTightHalo2016Filter'
        ]
    )

# Core Event Analyzer (computes basic quantities like HT, dilepton masses)
from CMGTools.TTHAnalysis.analyzers.ttHCoreEventAnalyzer import ttHCoreEventAnalyzer
ttHCoreEventAna = cfg.Analyzer(
    ttHCoreEventAnalyzer, name='ttHCoreEventAnalyzer',
    maxLeps = 4, ## leptons to consider
    mhtForBiasedDPhi = "mhtJet40jvec",
    jetForBiasedDPhi = "cleanJets",
    jetPt = 20.,
    )

## Jet-MET based Skim (generic, but requirements depend on the final state)
#ttHJetMETSkim = cfg.Analyzer(
#    'ttHJetMETSkimmer',
#    jets      = "cleanJets", # jet collection to use
#    jetPtCuts = [],  # e.g. [60,40,30,20] to require at least four jets with pt > 60,40,30,20
#    jetVetoPt =  0,  # if non-zero, veto additional jets with pt > veto beyond the ones in jetPtCuts
#    metCut    =  0,  # MET cut
#    htCut     = ('htJet40j', 0), # cut on HT defined with only jets and pt cut 40, at zero; i.e. no cut
#                                 # see ttHCoreEventAnalyzer for alternative definitions
#    mhtCut    = ('mhtJet40', 0), # cut on MHT defined with all leptons, and jets with pt > 40.
#    nBJet     = ('CSVv2IVFM', 0, "jet.pt() > 30"),     # require at least 0 jets passing CSV medium and pt > 30
#    )


# Core sequence of all common modules
    
higgsCoreSequence = [
    skimAnalyzer,
    mcWeighter,
    genAna,
    vertexAna,
    lepAna,
    jetAna,
    metAna,
    metFilter,
#    lheWeightAna,
#    eventSelector,
    jsonAna,
    pileUpAna,
    #genHiggsAna,
    #genHFAna,
#    pdfwAna,
    #susyScanAna,
    #ttHLepSkim,
    #ttHLepMCAna,
    #photonAna,
    tauAna,
    #isoTrackAna,
    #ttHCoreEventAna,
    #ttHJetMETSkim
    triggerFlagsAna,
    triggerObjsAna,
    triggerAna,
#    L1triggerObjsAna,
#    eventFlagsAna,
]
