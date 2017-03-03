import sys
from CMGTools.Production.datasetToSource import datasetToSource
import FWCore.ParameterSet.Config as cms
from PhysicsTools.PatAlgos.tools.tauTools import *
#from RecoMET.METPUSubtraction.MVAMETConfiguration_cff import runMVAMET
from RecoMET.METPUSubtraction.jet_recorrections import loadLocalSqlite, recorrectJets

from RecoTauTag.RecoTau.TauDiscriminatorTools import noPrediscriminants
from RecoTauTag.RecoTau.PATTauDiscriminationByMVAIsolationRun2_cff import *

#from CMGTools.diLeptonSelector.diLeptonFilter_cfi.py import

####################################################
def addNewTauID(process):
          process.rerunDiscriminationByIsolationMVArun2v1raw = patDiscriminationByIsolationMVArun2v1raw.clone(
                   PATTauProducer = cms.InputTag('slimmedTaus'),
                   Prediscriminants = noPrediscriminants,
                   loadMVAfromDB = cms.bool(True),
                   mvaName = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1"),
                   mvaOpt = cms.string("DBoldDMwLT"),
                   requireDecayMode = cms.bool(True),
                   verbosity = cms.int32(0)
          )
          
          process.rerunDiscriminationByIsolationMVArun2v1VLoose = patDiscriminationByIsolationMVArun2v1VLoose.clone(
                   PATTauProducer = cms.InputTag('slimmedTaus'),
                   Prediscriminants = noPrediscriminants,
                   toMultiplex = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1raw'),
                   key = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1raw:category'),
                   loadMVAfromDB = cms.bool(True),
                   mvaOutput_normalization = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_mvaOutput_normalization"),
                   mapping = cms.VPSet(
                            cms.PSet(
                                     category = cms.uint32(0),
                                     cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff90"),
                                     variable = cms.string("pt"),
                            )
                   )
          )
             
          process.rerunDiscriminationByIsolationMVArun2v1Loose = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
          process.rerunDiscriminationByIsolationMVArun2v1Loose.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff80")
          process.rerunDiscriminationByIsolationMVArun2v1Medium = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
          process.rerunDiscriminationByIsolationMVArun2v1Medium.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff70")
          process.rerunDiscriminationByIsolationMVArun2v1Tight = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
          process.rerunDiscriminationByIsolationMVArun2v1Tight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff60")
          process.rerunDiscriminationByIsolationMVArun2v1VTight = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
          process.rerunDiscriminationByIsolationMVArun2v1VTight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff50")
          process.rerunDiscriminationByIsolationMVArun2v1VVTight = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
          process.rerunDiscriminationByIsolationMVArun2v1VVTight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff40")
####################################################


process = cms.Process("MVAMET")
#process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(100))
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(-1))
numberOfFilesToProcess = -1

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
#process.GlobalTag.globaltag = '80X_dataRun2_2016SeptRepro_v6'
process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_TrancheIV_v8'
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')

process.load('PhysicsTools.PatAlgos.slimming.unpackedTracksAndVertices_cfi')
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
process.load('RecoBTag.Configuration.RecoBTag_cff')


dataset_user = 'CMS'
dataset_name = '/SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM'
dataset_files = '.*root'

# process.source = datasetToSource(                                                                   
#     dataset_user,
#     dataset_name,
#     dataset_files,
#     )

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring("file:root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/SUSYGluGluToBBHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/4C466283-6BC0-E611-B3AE-001517FB25E4.root")
#                            fileNames = cms.untracked.vstring("file:VBF.root")
#                           fileNames = cms.untracked.vstring("file:localTestFile_DY.root")
#                           )

process.options = cms.untracked.PSet(
    allowUnscheduled=cms.untracked.bool(True)
)

isData=False

if not hasattr(process, "p"):                                                                                                                      
          process.p = cms.Path() 

#loadLocalSqlite(process, "Summer16_23Sep2016AllV3_DATA.db", tag = 'JetCorrectorParametersCollection_Summer16_23Sep2016AllV3_DATA_AK4PFchs') 
loadLocalSqlite(process, "Summer16_23Sep2016V4_MC.db", tag = 'JetCorrectorParametersCollection_Summer16_23Sep2016V4_MC_AK4PFchs')
recorrectJets(process, isData) 
jetCollection = "patJetsReapplyJEC"

from CMGTools.H2TauTau.eventContent.common_cff import common


# configure MVA MET
if isData:
    coll = "RECO"
else:
    coll = "PAT"


process.genEvtWeightsCounter = cms.EDProducer(
          'GenEvtWeightCounter',
          verbose = cms.untracked.bool(False)
)

####################  correct MET ###############
from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
runMetCorAndUncFromMiniAOD(process,
                           isData = isData)

process.selectedVerticesForPFMEtCorrType0.src = cms.InputTag("offlineSlimmedPrimaryVertices")

process.load("RecoMET/METProducers.METSignificance_cfi")
process.load("RecoMET/METProducers.METSignificanceParams_cfi")

process.METCorrSignificance = process.METSignificance.clone(
          srcPfJets = cms.InputTag('patJetsReapplyJEC::MVAMET'),
          srcMet = cms.InputTag('slimmedMETs::MVAMET')
)
#################################################

# runMVAMET( process, jetCollectionPF = jetCollection)
# process.MVAMET.srcMETs = cms.VInputTag( cms.InputTag("slimmedMETs", "", coll),
#                                              cms.InputTag("patpfMET"),
#                                              cms.InputTag("patpfMETT1"),
#                                              cms.InputTag("patpfTrackMET"),
#                                              cms.InputTag("patpfNoPUMET"),
#                                              cms.InputTag("patpfPUCorrectedMET"),
#                                              cms.InputTag("patpfPUMET"),
#                                              cms.InputTag("slimmedMETsPuppi", "", coll) )

# process.MVAMET.srcPFCands =  cms.InputTag("packedPFCandidates")
# process.MVAMET.srcLeptons  = cms.VInputTag("slimmedMuons", "slimmedElectrons", "slimmedTaus")
# process.MVAMET.requireOS = cms.bool(False)


process.source.inputCommands = cms.untracked.vstring(
    'keep *'
)

#########################################################
process.load('RecoTauTag.Configuration.loadRecoTauTagMVAsFromPrepDB_cfi')
addNewTauID(process)
#########################################################
    
if numberOfFilesToProcess > 0:
    process.source.fileNames = process.source.fileNames[:numberOfFilesToProcess]


process.load('CMGTools.diLeptonSelector.diLeptonFilter_cfi')
process.eventDiLeptonFilter
#########################################################
process.load('RecoMET.METFilters.BadPFMuonFilter_cfi')
process.BadPFMuonFilter.muons = cms.InputTag("slimmedMuons")
process.BadPFMuonFilter.PFCandidates = cms.InputTag("packedPFCandidates")
process.BadPFMuonFilter.taggingMode = cms.bool(True)
process.load('RecoMET.METFilters.BadChargedCandidateFilter_cfi')
process.BadChargedCandidateFilter.muons = cms.InputTag("slimmedMuons")
process.BadChargedCandidateFilter.PFCandidates = cms.InputTag("packedPFCandidates")
process.BadChargedCandidateFilter.taggingMode = cms.bool(True)
#########################################################


if not isData:
    process.genEvtWeightsCounterPath = cms.Path(process.genEvtWeightsCounter)
    #process.schedule.insert(0, process.genEvtWeightsCounterPath)
process.p = cms.Path(process.eventDiLeptonFilter*process.METCorrSignificance*process.BadChargedCandidateFilter*process.BadPFMuonFilter)

## logger
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 10

#! Output and Log                                                                                                                                      

process.output = cms.OutputModule("PoolOutputModule",
                                  fileName = cms.untracked.string('outfile_newMVA.root'),
                                  SelectEvents = cms.untracked.PSet(  SelectEvents = cms.vstring('p')),
                                  outputCommands = cms.untracked.vstring(common)                                  
                                  )

process.out = cms.EndPath(process.output)




