

from CMGTools.TTHAnalysis.analyzers.treeProducerHiggsCore import *
from CMGTools.TTHAnalysis.analyzers.ntupleTypes import *

higgsToTauTau_globalVariables = higgsCore_globalVariables + [

            ##-------- custom jets ------------------------------------------
#JB            NTupleVariable("htJet25", lambda ev : ev.htJet25, help="H_{T} computed from leptons and jets (with |eta|<2.4, pt > 25 GeV)"),
#            NTupleVariable("metsig00", lambda ev : ev.mvaMetSig00, help="MET significance matrix(0,0)"),
#            NTupleVariable("metsig01", lambda ev : ev.mvaMetSig01, help="MET significance matrix(0,1)"),
#            NTupleVariable("metsig10", lambda ev : ev.mvaMetSig10, help="MET significance matrix(1,0)"),
#            NTupleVariable("metsig11", lambda ev : ev.mvaMetSig00, help="MET significance matrix(1,1)"),
#            NTupleVariable("svfitMass", lambda ev : ev.svfitMass, help="SVFit mass"),
#            NTupleVariable("svfitMassError", lambda ev : ev.svfitMassError, help="SVFit mass uncertainty"),
#            NTupleVariable("svfitPt", lambda ev : ev.svfitPt, help="SVFit pt"),

#MF            NTupleVariable("v_metsig00", lambda ev : ev.v_mvaMetSig00, help="MET significance matrix(0,0)"),

            
#            NTupleVariable("mhtJet25", lambda ev : ev.mhtJet25, help="H_{T}^{miss} computed from leptons and jets (with |eta|<2.4, pt > 25 GeV)"),
#            NTupleVariable("htJet40j", lambda ev : ev.htJet40j, help="H_{T} computed from only jets (with |eta|<2.4, pt > 40 GeV)"),
#            NTupleVariable("htJet40ja", lambda ev : ev.htJet40ja, help="H_{T} computed from only jets (with |eta|<4.7, pt > 40 GeV)"),
#            NTupleVariable("htJet40", lambda ev : ev.htJet40, help="H_{T} computed from leptons and jets (with |eta|<2.4, pt > 40 GeV)"),
#            NTupleVariable("htJet40a", lambda ev : ev.htJet40a, help="H_{T} computed from leptons and jets (with |eta|<4.7, pt > 40 GeV)"),
#            NTupleVariable("mhtJet40", lambda ev : ev.mhtJet40, help="H_{T}^{miss} computed from leptons and jets (with |eta|<2.4, pt > 40 GeV)"),
#            NTupleVariable("mhtJet40a", lambda ev : ev.mhtJet40a, help="H_{T}^{miss} computed from leptons and jets (with |eta|<4.7, pt > 40 GeV)"),
#            NTupleVariable("nSoftBJetLoose25",  lambda ev: sum([(sv.mva>0.3 and (sv.jet == None or sv.jet.pt() < 25)) for sv in ev.ivf]) + len(ev.bjetsMedium), int, help="Exclusive sum of jets with pt > 25 passing CSV medium and SV from ivf with loose sv mva"),
#            NTupleVariable("nSoftBJetMedium25", lambda ev: sum([(sv.mva>0.7 and (sv.jet == None or sv.jet.pt() < 25)) for sv in ev.ivf]) + len(ev.bjetsMedium), int, help="Exclusive sum of jets with pt > 25 passing CSV medium and SV from ivf with medium sv mva"),
#            NTupleVariable("nSoftBJetTight25",  lambda ev: sum([(sv.mva>0.9 and (sv.jet == None or sv.jet.pt() < 25)) for sv in ev.ivf]) + len(ev.bjetsMedium), int, help="Exclusive sum of jets with pt > 25 passing CSV medium and SV from ivf with tight sv mva"),
            ##--------------------------------------------------
#            NTupleVariable("minMWjj", lambda ev: ev.minMWjj, int, help="minMWjj"),
#            NTupleVariable("minMWjjPt", lambda ev: ev.minMWjjPt, int, help="minMWjjPt"),
#            NTupleVariable("bestMWjj", lambda ev: ev.bestMWjj, int, help="bestMWjj"),
#            NTupleVariable("bestMWjjPt", lambda ev: ev.bestMWjjPt, int, help="bestMWjjPt"),
#            NTupleVariable("bestMTopHad", lambda ev: ev.bestMTopHad, int, help="bestMTopHad"),
#            NTupleVariable("bestMTopHadPt", lambda ev: ev.bestMTopHadPt, int, help="bestMTopHadPt"),
            ##--------------------------------------------------
            ##------------------------------------------------
]
higgsToTauTau_globalObjects = higgsCore_globalObjects.copy()
higgsToTauTau_globalObjects.update({
            # put more here
})

#higgsToTauTau_dileptons = higgsCore_dileptons.copy()

higgsToTauTau_collections = higgsCore_collections.copy()
higgsToTauTau_collections.update({

            # put more here
            "genJets"         : NTupleCollection("genJet", genJetType, 20, help="Generated jets (not cleaned)"),
            "genParticles"     : NTupleCollection("gen",  genParticleWithMotherId, 400, help="all pruned genparticles"), # need to decide which gen collection ?
            "generatorSummary"     : NTupleCollection("genSum",  genParticleWithLinksType, 400, help="all pruned genparticles"),
            #"gentaus"     : NTupleCollection("genTau",  genParticleWithLinksType, 200, help="all pruned genparticles"),
            ## ---------------------------------------------
#            "selectedLeptons" : NTupleCollection("LepGood", leptonTypeH, 8, help="Leptons after the preselection"),
            "selectedElectrons" : NTupleCollection("el", leptonTypeH, 20, help="Electrons after the preselection"),
            "selectedMuons" : NTupleCollection("mu", leptonTypeH, 20, help="Muons after the preselection"),
#            "otherLeptons"    : NTupleCollection("LepOther", leptonTypeSusy, 8, help="Leptons after the preselection"),
            "selectedTaus"    : NTupleCollection("tau", tauTypeH, 20, help="Taus after the preselection"),
#            "selectedIsoTrack"    : NTupleCollection("track", isoTrackType, 50, help="isoTrack, sorted by pt"),
            #----------------------------------------------
            "cleanJetsAll"       : NTupleCollection("jet",     jetTypeH, 100, help="Jets after full selection and cleaning, sorted by pt"),

            "p4OutJESUpJetsUncorAbsoluteFlavMap"       : NTupleCollection("p4OutJESUpJetsUncorAbsoluteFlavMap",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorAbsoluteMPFBias"       : NTupleCollection("p4OutJESUpJetsUncorAbsoluteMPFBias",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorAbsoluteScale"         : NTupleCollection("p4OutJESUpJetsUncorAbsoluteScale",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorAbsoluteStat"          : NTupleCollection("p4OutJESUpJetsUncorAbsoluteStat",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorFlavorQCD"             : NTupleCollection("p4OutJESUpJetsUncorFlavorQCD",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorFragmentation"         : NTupleCollection("p4OutJESUpJetsUncorFragmentation",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorPileUpDataMC"          : NTupleCollection("p4OutJESUpJetsUncorPileUpDataMC",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorPileUpPtBB"            : NTupleCollection("p4OutJESUpJetsUncorPileUpPtBB",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorPileUpPtEC1"           : NTupleCollection("p4OutJESUpJetsUncorPileUpPtEC1",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorPileUpPtEC2"           : NTupleCollection("p4OutJESUpJetsUncorPileUpPtEC2",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorPileUpPtHF"            : NTupleCollection("p4OutJESUpJetsUncorPileUpPtHF",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorPileUpPtRef"           : NTupleCollection("p4OutJESUpJetsUncorPileUpPtRef",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorRelativeBal"           : NTupleCollection("p4OutJESUpJetsUncorRelativeBal",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorRelativeFSR"           : NTupleCollection("p4OutJESUpJetsUncorRelativeFSR",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorRelativeJEREC1"        : NTupleCollection("p4OutJESUpJetsUncorRelativeJEREC1",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorRelativeJEREC2"        : NTupleCollection("p4OutJESUpJetsUncorRelativeJEREC2",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorRelativeJERHF"         : NTupleCollection("p4OutJESUpJetsUncorRelativeJERHF",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorRelativePtBB"          : NTupleCollection("p4OutJESUpJetsUncorRelativePtBB",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorRelativePtEC1"         : NTupleCollection("p4OutJESUpJetsUncorRelativePtEC1",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorRelativePtEC2"         : NTupleCollection("p4OutJESUpJetsUncorRelativePtEC2",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorRelativePtHF"          : NTupleCollection("p4OutJESUpJetsUncorRelativePtHF",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorRelativeStatEC"        : NTupleCollection("p4OutJESUpJetsUncorRelativeStatEC",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorRelativeStatFSR"       : NTupleCollection("p4OutJESUpJetsUncorRelativeStatFSR",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorRelativeStatHF"        : NTupleCollection("p4OutJESUpJetsUncorRelativeStatHF",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorSinglePionECAL"        : NTupleCollection("p4OutJESUpJetsUncorSinglePionECAL",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorSinglePionHCAL"        : NTupleCollection("p4OutJESUpJetsUncorSinglePionHCAL",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorTimePtEta"             : NTupleCollection("p4OutJESUpJetsUncorTimePtEta",     jetTypeJES, 100, help=""),
            "p4OutJESUpJetsUncorTotal"                 : NTupleCollection("p4OutJESUpJetsUncorTotal",     jetTypeJES, 100, help=""),

            "p4OutJESDownJetsUncorAbsoluteFlavMap"     : NTupleCollection("p4OutJESDownJetsUncorAbsoluteFlavMap",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorAbsoluteMPFBias"     : NTupleCollection("p4OutJESDownJetsUncorAbsoluteMPFBias",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorAbsoluteScale"       : NTupleCollection("p4OutJESDownJetsUncorAbsoluteScale",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorAbsoluteStat"        : NTupleCollection("p4OutJESDownJetsUncorAbsoluteStat",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorFlavorQCD"           : NTupleCollection("p4OutJESDownJetsUncorFlavorQCD",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorFragmentation"       : NTupleCollection("p4OutJESDownJetsUncorFragmentation",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorPileUpDataMC"        : NTupleCollection("p4OutJESDownJetsUncorPileUpDataMC",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorPileUpPtBB"          : NTupleCollection("p4OutJESDownJetsUncorPileUpPtBB",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorPileUpPtEC1"         : NTupleCollection("p4OutJESDownJetsUncorPileUpPtEC1",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorPileUpPtEC2"         : NTupleCollection("p4OutJESDownJetsUncorPileUpPtEC2",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorPileUpPtHF"          : NTupleCollection("p4OutJESDownJetsUncorPileUpPtHF",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorPileUpPtRef"         : NTupleCollection("p4OutJESDownJetsUncorPileUpPtRef",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorRelativeBal"         : NTupleCollection("p4OutJESDownJetsUncorRelativeBal",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorRelativeFSR"         : NTupleCollection("p4OutJESDownJetsUncorRelativeFSR",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorRelativeJEREC1"      : NTupleCollection("p4OutJESDownJetsUncorRelativeJEREC1",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorRelativeJEREC2"      : NTupleCollection("p4OutJESDownJetsUncorRelativeJEREC2",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorRelativeJERHF"       : NTupleCollection("p4OutJESDownJetsUncorRelativeJERHF",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorRelativePtBB"        : NTupleCollection("p4OutJESDownJetsUncorRelativePtBB",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorRelativePtEC1"       : NTupleCollection("p4OutJESDownJetsUncorRelativePtEC1",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorRelativePtEC2"       : NTupleCollection("p4OutJESDownJetsUncorRelativePtEC2",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorRelativePtHF"        : NTupleCollection("p4OutJESDownJetsUncorRelativePtHF",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorRelativeStatEC"      : NTupleCollection("p4OutJESDownJetsUncorRelativeStatEC",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorRelativeStatFSR"     : NTupleCollection("p4OutJESDownJetsUncorRelativeStatFSR",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorRelativeStatHF"      : NTupleCollection("p4OutJESDownJetsUncorRelativeStatHF",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorSinglePionECAL"      : NTupleCollection("p4OutJESDownJetsUncorSinglePionECAL",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorSinglePionHCAL"      : NTupleCollection("p4OutJESDownJetsUncorSinglePionHCAL",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorTimePtEta"           : NTupleCollection("p4OutJESDownJetsUncorTimePtEta",     jetTypeJES, 100, help=""),
            "p4OutJESDownJetsUncorTotal"               : NTupleCollection("p4OutJESDownJetsUncorTotal",     jetTypeJES, 100, help=""),
      
#            "cleanJetsFwd"    : NTupleCollection("JetFwd",  jetTypeSusy, 25, help="Forward jets after full selection and cleaning, sorted by pt"),            
#mf            "fatJets"         : NTupleCollection("FatJet",  fatJetType,  15, help="AK8 jets, sorted by pt"),
            #"reclusteredFatJets" : NTupleCollection("RCFatJet",     fourVectorType,20, help="FatJets reclusterd from ak4 cleanJetsAll"),
            ##------------------------------------------------
#mf            "ivf"       : NTupleCollection("SV",     svType, 20, help="SVs from IVF"),
#mf            "genBHadrons"  : NTupleCollection("GenBHad", heavyFlavourHadronType, 20, mcOnly=True, help="Gen-level B hadrons"),
#mf            "genDHadrons"  : NTupleCollection("GenDHad", heavyFlavourHadronType, 20, mcOnly=True, help="Gen-level D hadrons"),
#ms            "dilepton"          : NTupleCollection("dilepton",     dileptonH, 1000, help="system of decay products of the two tau leptons"),
#ms            "LHE_weights"    : NTupleCollection("LHEweight",  weightsInfoType, 1000, mcOnly=True, help="LHE weight info"),

            "corrMET"          : NTupleCollection("corrMET",     corrMetH, 1000, help="corr MET"),

            #"met" : NTupleCollection("met", metTypeH, help="PF E_{T}^{miss}, after type 1 corrections"),                             


})


def getTriggerCollection(name, filterLabels):

      return { name : NTupleCollection( name.replace('HLT','triggerObject'), getTriggerObjectType(name, filterLabels.get(name,'')), 40 , help=name) }
     
#Event.diLeptons[0].met().getSignificanceMatrix()(0,0)
 
