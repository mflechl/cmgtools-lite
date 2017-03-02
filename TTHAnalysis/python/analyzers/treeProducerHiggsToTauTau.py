

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
 
