#PO!/bin/env python
from math import *
from PhysicsTools.Heppy.analyzers.core.autovars import NTupleObjectType  
from PhysicsTools.Heppy.analyzers.objects.autophobj import  *
from PhysicsTools.HeppyCore.utils.deltar import deltaR

from CMGTools.TTHAnalysis.signedSip import *

##------------------------------------------  
## LEPTON
##------------------------------------------  

leptonTypeSusy = NTupleObjectType("leptonSusy", baseObjectTypes = [ leptonType ], variables = [
    NTupleVariable("mvaIdSpring15",   lambda lepton : lepton.mvaRun2("NonTrigSpring15MiniAOD") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID for non-triggering electrons, Spring15 re-training; 1 for muons"),
    # Lepton MVA-id related variables
    NTupleVariable("mvaTTH",    lambda lepton : getattr(lepton, 'mvaValueTTH', -1), help="Lepton MVA (TTH version)"),
    NTupleVariable("jetPtRatiov1", lambda lepton : lepton.pt()/lepton.jet.pt() if hasattr(lepton,'jet') else -1, help="pt(lepton)/pt(nearest jet)"),
    NTupleVariable("jetPtRelv1", lambda lepton : ptRelv1(lepton.p4(),lepton.jet.p4()) if hasattr(lepton,'jet') else -1, help="pt of the lepton transverse to the jet axis (subtracting the lepton)"),
    NTupleVariable("jetPtRatiov2", lambda lepton: lepton.pt()/jetLepAwareJEC(lepton).Pt() if hasattr(lepton,'jet') else -1, help="pt(lepton)/[rawpt(jet-PU-lep)*L2L3Res+pt(lepton)]"),
    NTupleVariable("jetPtRelv2", lambda lepton : ptRelv2(lepton) if hasattr(lepton,'jet') else -1, help="pt of the lepton transverse to the jet axis (subtracting the lepton) - v2"),
    NTupleVariable("jetBTagCSV", lambda lepton : lepton.jet.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags') if hasattr(lepton,'jet') and hasattr(lepton.jet, 'btag') else -99, help="CSV btag of nearest jet"),
    NTupleVariable("jetBTagCMVA", lambda lepton : lepton.jet.btag('pfCombinedMVABJetTags') if hasattr(lepton,'jet') and hasattr(lepton.jet, 'btag') else -99, help="CMA btag of nearest jet"),
    NTupleVariable("jetDR",      lambda lepton : deltaR(lepton.eta(),lepton.phi(),lepton.jet.eta(),lepton.jet.phi()) if hasattr(lepton,'jet') else -1, help="deltaR(lepton, nearest jet)"),
])


leptonTypeSusyExtra = NTupleObjectType("leptonSusyExtra", baseObjectTypes = [ leptonTypeSusy, leptonTypeExtra ], variables = [
    NTupleVariable("miniRelIsoCharged",   lambda x : getattr(x,'miniAbsIsoCharged',-99)/x.pt()),
    NTupleVariable("miniRelIsoNeutral",   lambda x : getattr(x,'miniAbsIsoNeutral',-99)/x.pt()),
    # IVF variables
    NTupleVariable("hasSV",   lambda x : (2 if getattr(x,'ivfAssoc','') == "byref" else (0 if getattr(x,'ivf',None) == None else 1)), int, help="2 if lepton track is from a SV, 1 if loosely matched, 0 if no SV found."),
    NTupleVariable("svRedPt", lambda x : getattr(x, 'ivfRedPt', 0), help="pT of associated SV, removing the lepton track"),
    NTupleVariable("svRedM",  lambda x : getattr(x, 'ivfRedM', 0), help="mass of associated SV, removing the lepton track"),
    NTupleVariable("svLepSip3d", lambda x : getattr(x, 'ivfSip3d', 0), help="sip3d of lepton wrt SV"),
    NTupleVariable("svSip3d", lambda x : x.ivf.d3d.significance() if getattr(x,'ivf',None) != None else -99, help="S_{ip3d} of associated SV"),
    NTupleVariable("svNTracks", lambda x : x.ivf.numberOfDaughters() if getattr(x,'ivf',None) != None else -99, help="Number of tracks of associated SV"),
    NTupleVariable("svChi2n", lambda x : x.ivf.vertexChi2()/x.ivf.vertexNdof() if getattr(x,'ivf',None) != None else -99, help="Normalized chi2 of associated SV"),
    NTupleVariable("svDxy", lambda x : x.ivf.dxy.value() if getattr(x,'ivf',None) != None else -99, help="dxy of associated SV"),
    NTupleVariable("svMass", lambda x : x.ivf.mass() if getattr(x,'ivf',None) != None else -99, help="mass of associated SV"),
    NTupleVariable("svPt", lambda x : x.ivf.pt() if getattr(x,'ivf',None) != None else -99, help="pt of associated SV"),
    NTupleVariable("svMCMatchFraction", lambda x : x.ivf.mcMatchFraction if getattr(x,'ivf',None) != None else -99, mcOnly=True, help="Fraction of mc-matched tracks from b/c matched to a single hadron (if >= 2 tracks found), for associated SV"),
    NTupleVariable("svMva", lambda x : x.ivf.mva if getattr(x,'ivf',None) != None else -99, help="mva value of associated SV"),
    # Additional jet-lepton related variables
    NTupleVariable("jetNDau",    lambda lepton : lepton.jet.numberOfDaughters() if hasattr(lepton,'jet') and lepton.jet != lepton else -1, help="n daughters of nearest jet"),
    NTupleVariable("jetNDauCharged",    lambda lepton : sum(x.charge()!=0 for x in lepton.jet.daughterPtrVector()) if hasattr(lepton,'jet') and lepton.jet != lepton else -1, help="n charged daughters of nearest jet"),
    NTupleVariable("jetNDauPV",    lambda lepton : sum(x.charge()!=0 and x.fromPV()==3 for x in lepton.jet.daughterPtrVector()) if hasattr(lepton,'jet') and lepton.jet != lepton else -1, help="n charged daughters from PV of nearest jet"),
    NTupleVariable("jetNDauNotPV",    lambda lepton : sum(x.charge()!=0 and x.fromPV()<=2 for x in lepton.jet.daughterPtrVector()) if hasattr(lepton,'jet') and lepton.jet != lepton else -1, help="n charged daughters from PV of nearest jet"),
    NTupleVariable("jetNDauChargedMVASel",    lambda lepton : sum((deltaR(x.eta(),x.phi(),lepton.jet.eta(),lepton.jet.phi())<=0.4 and x.charge()!=0 and x.fromPV()>1 and qualityTrk(x.pseudoTrack(),lepton.associatedVertex)) for x in lepton.jet.daughterPtrVector()) if hasattr(lepton,'jet') and lepton.jet != lepton else 0, help="n charged daughters (with selection for ttH lepMVA) of nearest jet"),
    NTupleVariable("jetmaxSignedSip3D",    lambda lepton :  maxSignedSip3Djettracks(lepton), help="max signed Sip3D among jet's tracks"),
    NTupleVariable("jetmaxSip3D",    lambda lepton :   maxSip3Djettracks(lepton), help="max Sip3D among jet's tracks"),
    NTupleVariable("jetmaxSignedSip2D",    lambda lepton  : maxSignedSip2Djettracks(lepton) , help="max signed Sip2D among jet's tracks"),
    NTupleVariable("jetmaxSip2D",    lambda lepton :   maxSip2Djettracks(lepton), help="max Sip2D among jet's tracks"),
    NTupleVariable("jetPtRelv0",   lambda lepton : ptRel(lepton.p4(),lepton.jet.p4()) if hasattr(lepton,'jet') else -1, help="pt of the lepton transverse to the jet axis (not subtracting the lepton)"),
    NTupleVariable("jetMass",      lambda lepton : lepton.jet.mass() if hasattr(lepton,'jet') else -1, help="Mass of associated jet"),
    NTupleVariable("jetPrunedMass",      lambda lepton : getattr(lepton.jet, 'prunedP4', lepton.jet.p4()).M() if hasattr(lepton,'jet') else -1, help="Pruned mass of associated jet"),
    NTupleVariable("jetDecDR",      lambda lepton : lepton.jetDecDR if hasattr(lepton,'jetDecDR') else -1, help="deltaR(lepton, nearest jet) after declustering"),
    NTupleVariable("jetDecPtRel", lambda lepton : lepton.jetDecPtRel if hasattr(lepton,'jetDecPtRel') else -1, help="pt of the lepton transverse to the jet axis (subtracting the lepton), after declustering"),
    NTupleVariable("jetDecPtRatio", lambda lepton :  lepton.jetDecPtRatio if hasattr(lepton,'jetDecPtRatio') else -1, help="pt(lepton)/pt(nearest jet) after declustering"),
    NTupleVariable("jetDecPrunedMass", lambda lepton :  lepton.jetDecPrunedMass if hasattr(lepton,'jetDecPrunedMass') else -1, help="pt(lepton)/pt(nearest jet) after declustering and pruning"),
    NTupleVariable("jetDecPrunedPtRatio", lambda lepton :  lepton.jetDecPrunedPtRatio if hasattr(lepton,'jetDecPrunedPtRatio') else -1, help="pt(lepton)/pt(nearest jet) after declustering and pruning"),
    NTupleVariable("jetDec02DR",      lambda lepton : lepton.jetDec02DR if hasattr(lepton,'jetDec02DR') else -1, help="deltaR(lepton, nearest jet) after declustering 02"),
    NTupleVariable("jetDec02PtRel", lambda lepton : lepton.jetDec02PtRel if hasattr(lepton,'jetDec02PtRel') else -1, help="pt of the lepton transverse to the jet axis (subtracting the lepton), after declustering 02"),
    NTupleVariable("jetDec02PtRatio", lambda lepton :  lepton.jetDec02PtRatio if hasattr(lepton,'jetDec02PtRatio') else -1, help="pt(lepton)/pt(nearest jet) after declustering 02"),
    NTupleVariable("jetDec02PrunedPtRatio", lambda lepton :  lepton.jetDec02PrunedPtRatio if hasattr(lepton,'jetDec02PrunedPtRatio') else -1, help="pt(lepton)/pt(nearest jet) after declustering 02 and pruning"),
    NTupleVariable("jetDec02PrunedMass", lambda lepton :  lepton.jetDec02PrunedMass if hasattr(lepton,'jetDec02PrunedMass') else -1, help="pt(lepton)/pt(nearest jet) after declustering 02 and pruning"),
    NTupleVariable("jetRawPt", lambda x: x.jet.pt() * x.jet.rawFactor() if x.jet!=x else x.pt(), help="matched jet raw pt"),
    NTupleVariable("jetCorrFactor_L1", lambda x: x.jet.CorrFactor_L1 if hasattr(x.jet,'CorrFactor_L1') else 1, help="matched jet L1 correction factor"),
    NTupleVariable("jetCorrFactor_L1L2", lambda x: x.jet.CorrFactor_L1L2 if hasattr(x.jet,'CorrFactor_L1L2') else 1, help="matched jet L1L2 correction factor"),
    NTupleVariable("jetCorrFactor_L1L2L3", lambda x: x.jet.CorrFactor_L1L2L3 if hasattr(x.jet,'CorrFactor_L1L2L3') else 1, help="matched jet L1L2L3 correction factor"),
    NTupleVariable("jetCorrFactor_L1L2L3Res", lambda x: x.jet.CorrFactor_L1L2L3Res if hasattr(x.jet,'CorrFactor_L1L2L3Res') else 1, help="matched jet L1L2L3Res correction factor"),        
    NTupleVariable("jetPtRatio_Raw", lambda lepton : -1 if not hasattr(lepton,'jet') else lepton.pt()/lepton.jet.pt() if not hasattr(lepton.jet,'rawFactor') else lepton.pt()/(lepton.jet.pt()*lepton.jet.rawFactor()), help="pt(lepton)/rawpt(nearest jet)"),
    NTupleVariable("jetPtRelHv2", lambda lepton : ptRelHv2(lepton) if hasattr(lepton,'jet') else -1, help="pt of the jet (subtracting the lepton) transverse to the lepton axis - v2"),
    # variables for isolated electron trigger matching cuts
    NTupleVariable("ecalPFClusterIso", lambda lepton :  lepton.ecalPFClusterIso() if abs(lepton.pdgId())==11 else -999, help="Electron ecalPFClusterIso"),
    NTupleVariable("hcalPFClusterIso", lambda lepton :  lepton.hcalPFClusterIso() if abs(lepton.pdgId())==11 else -999, help="Electron hcalPFClusterIso"),
    NTupleVariable("dr03TkSumPt", lambda lepton: lepton.dr03TkSumPt() if abs(lepton.pdgId())==11 else -999, help="Electron dr03TkSumPt isolation"),
    NTupleVariable("trackIso", lambda lepton :  lepton.trackIso() if abs(lepton.pdgId())==11 else -999, help="Electron trackIso (in cone of 0.4)"),
])
leptonTypeSusyExtra.addSubObjects([
        NTupleSubObject("jetLepAwareJEC",lambda x: jetLepAwareJEC(x), tlorentzFourVectorType)
        ])



leptonTypeH = NTupleObjectType("leptonH", baseObjectTypes = [ leptonType ], variables = [
    NTupleVariable("eleMVAId",     lambda x : (x.electronID("POG_MVA_ID_NonTrig_full5x5") + 2*x.electronID("POG_MVA_ID_Trig_full5x5")) if abs(x.pdgId()) == 11 else -1, int, help="Electron mva id working point (2012, full5x5 shapes): 0=none, 1=non-trig, 2=trig, 3=both"),
    NTupleVariable("mvaId",         lambda lepton : lepton.mvaNonTrigV0(full5x5=True) if abs(lepton.pdgId()) == 11 else lepton.mvaId(), help="EGamma POG MVA ID for non-triggering electrons (as HZZ); MVA Id for muons (BPH+Calo+Trk variables)"),
    NTupleVariable("corrGsfTrack",   lambda lepton: lepton.gsfTrack().hitPattern().numberOfHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1 if abs(lepton.pdgId()) == 11 else 0, help="electron.gsfTrack().hitPattern().numberOfHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1" ),
    NTupleVariable("passConversionVeto",   lambda lepton: lepton.passConversionVeto() if abs(lepton.pdgId()) == 11 else 0, help="passConversionVeto" ),
    NTupleVariable("mvaIdTrig",     lambda lepton : lepton.mvaTrigV0(full5x5=True)    if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID for triggering electrons; 1 for muons"),
    NTupleVariable("looseId",       lambda lepton : lepton.isLooseMuon() if abs(lepton.pdgId()) == 13 else 0, help="loose lepton id"),
    NTupleVariable("validFraction",       lambda lepton : lepton.innerTrack().validFraction() if abs(lepton.pdgId()) == 13 else 0, help="fraction of valid tracker hits"),
    NTupleVariable("globalMuon",       lambda lepton : lepton.isGlobalMuon() if abs(lepton.pdgId()) == 13 else 0, help="global muon"),
    NTupleVariable("isTrackerMuon",       lambda lepton : lepton.isTrackerMuon() if abs(lepton.pdgId()) == 13 else 0, help="tracker muon"),
    NTupleVariable("isPFMuon",       lambda lepton : lepton.isPFMuon() if abs(lepton.pdgId()) == 13 else 0, help="PF muon"),
    NTupleVariable("normChi2Track",       lambda lepton : lepton.globalTrack().normalizedChi2() if abs(lepton.pdgId()) == 13 & lepton.isGlobalMuon() else 0, help="normChi2Track"),
    NTupleVariable("trackPosMatch",       lambda lepton : lepton.combinedQuality().chi2LocalPosition if abs(lepton.pdgId()) == 13 else 0, help="trackPosMatch"),
    NTupleVariable("kickFinder",       lambda lepton : lepton.combinedQuality().trkKink if abs(lepton.pdgId()) == 13 else 0, help="kickFinder"),
    NTupleVariable("segmentComp",       lambda lepton : lepton.segmentCompatibility() if abs(lepton.pdgId()) == 13 else 0, help="segment compatibility"),

    #NTupleVariable("iso",           lambda lepton : lepton.pfIsolationR03().sumChargedHadrPt + max(lepton.pfIsolationR03().sumNeutralHadronPt + lepton.pfIsolationR03().sumPhotonEt - 0.5*lepton.pfIsolationR03().sumPUPt, 0.0) / lepton.pt(), help "isolation")                                                   
    NTupleVariable("chargedHadrIsoR03",           lambda lepton : lepton.chargedHadronIsoR(0.3),  help= "self.physObj.pfIsolationR03().sumChargedHadronPt"),
    NTupleVariable("chargedHadrIsoR04",           lambda lepton : lepton.chargedHadronIsoR(0.4),  help= "self.physObj.pfIsolationR04().sumChargedHadronPt"),
    NTupleVariable("neutralHadrIsoR03",           lambda lepton : lepton.neutralHadronIsoR(0.3),  help= "self.physObj.pfIsolationR03().sumNeutralHadronEt"),
    NTupleVariable("neutralHadrIsoR04",           lambda lepton : lepton.neutralHadronIsoR(0.4),  help= "self.physObj.pfIsolationR04().sumNeutralHadronEt"),
    NTupleVariable("photonIsoR03",           lambda lepton : lepton.photonIsoR(0.3),  help= "self.physObj.pfIsolationR03().sumPhotonEt"),
    NTupleVariable("photonIsoR04",           lambda lepton : lepton.photonIsoR(0.4),  help= "self.physObj.pfIsolationR04().sumPhotonEt"),
    NTupleVariable("puChargedHadronIsoR03",           lambda lepton : lepton.puChargedHadronIsoR(0.3),  help= "self.physObj.pfIsolationR03().sumPUPt"),
    NTupleVariable("puChargedHadronIsoR04",           lambda lepton : lepton.puChargedHadronIsoR(0.4),  help= "self.physObj.pfIsolationR03().sumPUPt"),

    NTupleVariable("Spring16GP",   lambda lepton : lepton.mvaRun2("Spring16GP") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID for non-triggering electrons, Spring15 re-training; 1 for muons"),
    NTupleVariable("mvaIdSpring15NonTrig",   lambda lepton : lepton.mvaRun2("NonTrigSpring15MiniAOD") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID for non-triggering electrons, Spring15 re-training; 1 for muons"),
    NTupleVariable("POG_PHYS14_25ns_v1_Veto",   lambda lepton : lepton.cutBasedId('POG_PHYS14_25ns_v1_Veto') if abs(lepton.pdgId()) == 11 else 1, help="POG Phys14 25ns cut-based v1 Veto ID"),
    NTupleVariable("POG_PHYS14_25ns_v2_Veto",   lambda lepton : lepton.cutBasedId('POG_PHYS14_25ns_v2_Veto') if abs(lepton.pdgId()) == 11 else 1, help="POG Phys14 25ns cut-based v2 Veto ID"),
    NTupleVariable("POG_PHYS14_25ns_v1_ConvVeto_Veto",   lambda lepton : lepton.cutBasedId('POG_PHYS14_25ns_v1_ConvVeto_Veto') if abs(lepton.pdgId()) == 11 else 1, help="POG Phys14 25ns cut-based v1 ConvVeto Veto ID"),
    NTupleVariable("POG_PHYS14_25ns_v2_ConvVeto_Veto",   lambda lepton : lepton.cutBasedId('POG_PHYS14_25ns_v2_ConvVeto_Veto') if abs(lepton.pdgId()) == 11 else 1, help="POG Phys14 25ns cut-based v2 ConvVeto Veto ID"),
    NTupleVariable("POG_PHYS14_25ns_v2_ConvVetoDxyDz_Veto",   lambda lepton : lepton.cutBasedId('POG_PHYS14_25ns_v2_ConvVetoDxyDz_Veto') if abs(lepton.pdgId()) == 11 else 1, help="POG Phys14 25ns cut-based v2 ConvVetoDxyDz Veto ID"),
    NTupleVariable("POG_SPRING15_25ns_v1_Veto",   lambda lepton : lepton.cutBasedId('POG_SPRING15_25ns_v1_Veto') if abs(lepton.pdgId()) == 11 else 1, help="POG SPRING15 25ns cut-based v1 Veto ID"),
    NTupleVariable("POG_SPRING15_25ns_v1_ConvVeto_Veto",   lambda lepton : lepton.cutBasedId('POG_SPRING15_25ns_v1_ConvVeto_Veto') if abs(lepton.pdgId()) == 11 else 1, help="POG SPRING15 25ns cut-based v1 ConvVeto Veto ID"),
    NTupleVariable("POG_SPRING15_25ns_v1_ConvVetoDxyDz_Veto",   lambda lepton : lepton.cutBasedId('POG_SPRING15_25ns_v1_ConvVetoDxyDz_Veto') if abs(lepton.pdgId()) == 11 else 1, help="POG SPRING15 25ns cut-based v1 ConvVetoDxyDz Veto ID"),
    NTupleVariable("POG_SPRING16_25ns_v1_Veto",   lambda lepton : lepton.cutBasedId('POG_SPRING16_25ns_v1_Veto') if abs(lepton.pdgId()) == 11 else 1, help="POG SPRING16 25ns cut-based v1 Veto ID"),
    NTupleVariable("POG_SPRING16_25ns_v1_ConvVeto_Veto",   lambda lepton : lepton.cutBasedId('POG_SPRING16_25ns_v1_ConvVeto_Veto') if abs(lepton.pdgId()) == 11 else 1, help="POG SPRING16 25ns cut-based v1 ConvVeto Veto ID"),
    NTupleVariable("POG_SPRING16_25ns_v1_ConvVetoDxyDz_Veto",   lambda lepton : lepton.cutBasedId('POG_SPRING16_25ns_v1_ConvVetoDxyDz_Veto') if abs(lepton.pdgId()) == 11 else 1, help="POG SPRING16 25ns cut-based v1 ConvVetoDxyDz Veto ID"),


    NTupleVariable("superClusterEta", lambda x : x.superCluster().eta() if abs(x.pdgId())==11 else -100, help="Electron supercluster pseudorapidity"),

    NTupleVariable("muonid_loose", lambda x : x.muonID("POG_ID_Loose") if abs(x.pdgId()) == 13 else 0, int, help="loose muon id"),
    NTupleVariable("muonid_medium", lambda x : x.muonID("POG_ID_Medium") if abs(x.pdgId()) == 13 else 0, int, help="medium muon id"),
    NTupleVariable("muonid_medium_ichep", lambda x : x.muonID("POG_ID_Medium_ICHEP") if abs(x.pdgId()) == 13 else 0, int, help="medium muon id_ichep"),    
    NTupleVariable("muonid_tight", lambda x : x.muonID("POG_ID_Tight") if abs(x.pdgId()) == 13 else 0, int, help="tight muon id"),
    NTupleVariable("muonid_tightnovtx", lambda x : x.muonID("POG_ID_TightNoVtx") if abs(x.pdgId()) == 13 else 0, int, help="loose tight muon id, no vertex"),
    NTupleVariable("muonid_highpt", lambda x : x.muonID("POG_ID_HighPt") if abs(x.pdgId()) == 13 else 0, int, help="muon id highpt"),
    NTupleVariable("eid_veto", lambda x : x.cutBasedId("POG_SPRING15_25ns_v1_Veto") if abs(x.pdgId()) == 11 else 0, int, help="electron veto id"),
    NTupleVariable("eid_loose", lambda x : x.cutBasedId("POG_SPRING15_25ns_v1_Loose") if abs(x.pdgId()) == 11 else 0, int, help="electron loose id"),
    NTupleVariable("eid_medium", lambda x : x.cutBasedId("POG_SPRING15_25ns_v1_Medium") if abs(x.pdgId()) == 11 else 0, int, help="electron medium id"),
    NTupleVariable("eid_tight", lambda x : x.cutBasedId("POG_SPRING15_25ns_v1_Tight") if abs(x.pdgId()) == 11 else 0, int, help="electron tight id"),
    NTupleVariable("eid16_veto", lambda x : x.cutBasedId("POG_SPRING16_25ns_v1_Veto") if abs(x.pdgId()) == 11 else 0, int, help="electron veto id"),
    NTupleVariable("eid16_loose", lambda x : x.cutBasedId("POG_SPRING16_25ns_v1_Loose") if abs(x.pdgId()) == 11 else 0, int, help="electron loose id"),
    NTupleVariable("eid16_medium", lambda x : x.cutBasedId("POG_SPRING16_25ns_v1_Medium") if abs(x.pdgId()) == 11 else 0, int, help="electron medium id"),
    NTupleVariable("eid16_tight", lambda x : x.cutBasedId("POG_SPRING16_25ns_v1_Tight") if abs(x.pdgId()) == 11 else 0, int, help="electron tight id"),
    
#    NTupleVariable("eid_test", lambda x : x.cutBasedId("cutBasedElectronID-Summer16-80X-V1-veto") if abs(x.pdgId()) == 11 else 0, int, help="test"),

] )
##------------------------------------------  
## TAU
##------------------------------------------  

tauTypeSusy = NTupleObjectType("tauSusy",  baseObjectTypes = [ tauType ], variables = [
])

tauTypeH = NTupleObjectType("tauH",  baseObjectTypes = [ tauType ], variables = [
   
    NTupleVariable("againstElectronLooseMVA6",  lambda x : x.tauID("againstElectronLooseMVA6"), int, help="Tau discriminant against electrons, MVA6 loose"),
    NTupleVariable("againstElectronMediumMVA6",  lambda x : x.tauID("againstElectronMediumMVA6"), int, help="Tau discriminant against electrons, MVA6 medium"),
    NTupleVariable("againstElectronTightMVA6",  lambda x : x.tauID("againstElectronTightMVA6"), int, help="Tau discriminant against electrons, MVA6 tight"),
    NTupleVariable("againstElectronVLooseMVA6",  lambda x : x.tauID("againstElectronVLooseMVA6"), int, help="Tau discriminant against electrons, MVA6 Vloose"),
    NTupleVariable("againstElectronVTightMVA6",  lambda x : x.tauID("againstElectronVTightMVA6"), int, help="Tau discriminant against electrons, MVA6 Vtight"),
    
    NTupleVariable("againstMuonLoose3",  lambda x : x.tauID("againstMuonLoose3"), int, help="Tau discriminant against muons, loose3"),
    NTupleVariable("againstMuonTight3",  lambda x : x.tauID("againstMuonTight3"), int, help="Tau discriminant against muons, tight3"),

    NTupleVariable("byCombinedIsolationDeltaBetaCorrRaw3Hits",  lambda x : x.tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits"), float, help="Combined DB 3 Hits isolation"),
    NTupleVariable("byLooseCombinedIsolationDeltaBetaCorr3Hits",  lambda x : x.tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits"), int, help="Combined DB 3 Hits isolation, loose"),
    NTupleVariable("byMediumCombinedIsolationDeltaBetaCorr3Hits",  lambda x : x.tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits"), int, help="Combined DB 3 Hits isolation, medium"),
    NTupleVariable("byTightCombinedIsolationDeltaBetaCorr3Hits",  lambda x : x.tauID("byTightCombinedIsolationDeltaBetaCorr3Hits"), int, help="Combined DB 3 Hits isolation, tight"),

    NTupleVariable("byIsolationMVArun2v1DBnewDMwLTraw",  lambda x : x.tauID("byIsolationMVArun2v1DBnewDMwLTraw"), float, help="new Isolation for pair selection"),
    NTupleVariable("byIsolationMVArun2v1DBoldDMwLTraw",  lambda x : x.tauID("byIsolationMVArun2v1DBoldDMwLTraw"), float, help="old Isolation for pair selection"),

    NTupleVariable("byVLooseIsolationMVArun2v1DBoldDMwLT",  lambda x : x.tauID("byVLooseIsolationMVArun2v1DBoldDMwLT"), int, help="byVLooseIsolationMVArun2v1DBoldDMwLT"),
    NTupleVariable("byLooseIsolationMVArun2v1DBoldDMwLT",  lambda x : x.tauID("byLooseIsolationMVArun2v1DBoldDMwLT"), int, help="byLooseIsolationMVArun2v1DBoldDMwLT"),
    NTupleVariable("byMediumIsolationMVArun2v1DBoldDMwLT",  lambda x : x.tauID("byMediumIsolationMVArun2v1DBoldDMwLT"), int, help="byMediumIsolationMVArun2v1DBoldDMwLT"),
    NTupleVariable("byTightIsolationMVArun2v1DBoldDMwLT",  lambda x : x.tauID("byTightIsolationMVArun2v1DBoldDMwLT"), int, help="byTightIsolationMVArun2v1DBoldDMwLT"),
    NTupleVariable("byVTightIsolationMVArun2v1DBoldDMwLT",  lambda x : x.tauID("byVTightIsolationMVArun2v1DBoldDMwLT"), int, help="byVTightIsolationMVArun2v1DBoldDMwLT"),
    NTupleVariable("byVLooseIsolationMVArun2v1DBnewDMwLT",  lambda x : x.tauID("byVLooseIsolationMVArun2v1DBnewDMwLT"), int, help="byVLooseIsolationMVArun2v1DBnewDMwLT"),
    NTupleVariable("byLooseIsolationMVArun2v1DBnewDMwLT",  lambda x : x.tauID("byLooseIsolationMVArun2v1DBnewDMwLT"), int, help="byLooseIsolationMVArun2v1DBnewDMwLT"),
    NTupleVariable("byMediumIsolationMVArun2v1DBnewDMwLT",  lambda x : x.tauID("byMediumIsolationMVArun2v1DBnewDMwLT"), int, help="byMediumIsolationMVArun2v1DBnewDMwLT"),
    NTupleVariable("byTightIsolationMVArun2v1DBnewDMwLT",  lambda x : x.tauID("byTightIsolationMVArun2v1DBnewDMwLT"), int, help="byTightIsolationMVArun2v1DBnewDMwLT"),
    NTupleVariable("byVTightIsolationMVArun2v1DBnewDMwLT",  lambda x : x.tauID("byVTightIsolationMVArun2v1DBnewDMwLT"), int, help="byVTightIsolationMVArun2v1DBnewDMwLT"),

    NTupleVariable("NewMVAIDraw",  lambda x : x.NewMVAraw, float, help="NewMVAIDraw"),
    NTupleVariable("NewMVAIDVLoose",  lambda x : x.NewMVAVLoose, float, help="NewMVAIDVLoose"),
    NTupleVariable("NewMVAIDLoose",  lambda x : x.NewMVALoose, float, help="NewMVAIDLoose"),
    NTupleVariable("NewMVAIDMedium",  lambda x : x.NewMVAMedium, float, help="NewMVAIDMedium"),
    NTupleVariable("NewMVAIDTight",  lambda x : x.NewMVATight, float, help="NewMVAIDTight"),
    NTupleVariable("NewMVAIDVTight",  lambda x : x.NewMVAVTight, float, help="NewMVAIDVTight"),
    NTupleVariable("NewMVAIDVVTight",  lambda x : x.NewMVAVVTight, float, help="NewMVAIDVVTight"),
    
    

    #NTupleVariable("byIsolationMVA3newDMwLTraw",  lambda x : x.tauID("byIsolationMVA3newDMwLTraw"), float, help="raw MVA output of BDT based tau ID discriminator based on isolation Pt sums, trained on 1-prong, 2-prong and 3-prong tau candidates plus lifetime information"),
    #NTupleVariable("byIsolationMVA3oldDMwLTraw",  lambda x : x.tauID("byIsolationMVA3oldDMwLTraw"), float, help="raw MVA output of BDT based tau ID discriminator based on isolation Pt sums, trained on 1-prong, 2-prong and 3-prong tau candidates plus lifetime information"),
    #NTupleVariable("byIsolationMVA3newDMwoLTraw",  lambda x : x.tauID("byIsolationMVA3newDMwoLTraw"), float, help="raw MVA output of BDT based tau ID discriminator based on isolation Pt sums, trained on 1-prong, 2-prong and 3-prong tau candidates"),
    #NTupleVariable("byIsolationMVA3oldDMwoLTraw",  lambda x : x.tauID("byIsolationMVA3oldDMwoLTraw"), float, help="raw MVA output of BDT based tau ID discriminator based on isolation Pt sums, trained on 1-prong, 2-prong and 3-prong tau candidates"),                                                          


    NTupleVariable("decayModeFinding",  lambda x : x.tauID("decayModeFinding"), int, help="Tau discriminant"),
    NTupleVariable("decayModeFindingNewDMs",  lambda x : x.tauID("decayModeFindingNewDMs"), int, help="Tau discriminant"),

    NTupleVariable("chargedIsoPtSum",  lambda x : x.tauID("chargedIsoPtSum"), float, help="Deposition by charged particles in isolation cone"),
    NTupleVariable("neutralIsoPtSum",  lambda x : x.tauID("neutralIsoPtSum"), float, help="Deposition by neutral particles in isolation cone"),

    NTupleVariable("puCorrPtSum",  lambda x : x.tauID("puCorrPtSum"), float, help="puCorrPtSum"),

    NTupleVariable("packedLeadTauCanddXY",  lambda x : x.leadChargedHadrCand().dxy(), float, help="dxy of leadChargedHadrCand"),
    NTupleVariable("packedLeadTauCanddZ",  lambda x : x.leadChargedHadrCand().dz(), float, help="dz of leadChargedHadrCand"),

])
dileptonH = NTupleObjectType("dileptonH",  baseObjectTypes = [ fourVectorType ], variables = [
    #NTupleVariable("v_metsig00", lambda ev : ev.v_mvaMetSig00, help="MET significance matrix(0,0)"),                                                                                                                                                                                                               
    #NTupleVariable("vv_metsig00", lambda x : x.met().getSignificanceMatrix()(0,0), help="MET significance matrix(0,0)"),                                                                                                                                                                                           
    #NTupleVariable("svfitMass", lambda x : x.svfitMass(), float, help="SVFit mass"),
    #NTupleVariable("svfitMassError", lambda x : x.svfitMassError(), float, help="SVFit mass error"),
    #NTupleVariable("svfitPt", lambda x : x.svfitPt(), float, help="SVFit mass"),
    #NTupleVariable("svfitPtError", lambda x : x.svfitPtError(), float, help="SVFit mass error"),
    #NTupleVariable("svfitEta", lambda x : x.svfitEta(), float, help="SVFit eta"),
    #NTupleVariable("svfitPhi", lambda x : x.svfitPhi(), float, help="SVFit phi"),
    
    #NTupleVariable("metsig00", lambda x : x.met().getSignificanceMatrix()(0,0), help="MET significance matrix(0,0)"),
    #NTupleVariable("metsig01", lambda x : x.met().getSignificanceMatrix()(0,1), help="MET significance matrix(0,1)"),
    #NTupleVariable("metsig10", lambda x : x.met().getSignificanceMatrix()(1,0), help="MET significance matrix(1,0)"),
    #NTupleVariable("metsig11", lambda x : x.met().getSignificanceMatrix()(1,1), help="MET significance matrix(1,1)"),
    #NTupleVariable("l1_pt", lambda x : x.leg1().pt(), help="pt of first lepton"),
    #NTupleVariable("l1_eta", lambda x : x.leg1().eta(), help="eta of first lepton"),
    #NTupleVariable("l1_phi", lambda x : x.leg1().phi(), help="phi of first lepton"),
    #NTupleVariable("l1_mass", lambda x : x.leg1().mass(), help="mass of first lepton"),
    #NTupleVariable("l2_pt", lambda x : x.leg2().pt(), help="pt of second lepton"),
    #NTupleVariable("l2_eta", lambda x : x.leg2().eta(), help="eta of second lepton"),
    #NTupleVariable("l2_phi", lambda x : x.leg2().phi(), help="phi of second lepton"),
    #NTupleVariable("l2_mass", lambda x : x.leg2().mass(), help="mass of second lepton"),
    #NTupleVariable("met_pt", lambda x : x.met().pt(), help="met"),
    #NTupleVariable("met_phi", lambda x : x.met().phi(), help="met phi"),

    NTupleVariable("met_pt", lambda x : x.pt(), float, help="met pt"),
    NTupleVariable("met_phi", lambda x : x.phi(), float, help="met phi"),
    NTupleVariable("metsig00", lambda x : x.getSignificanceMatrix()(0,0), float, help="MET significance matrix(0,0)"),
    NTupleVariable("metsig01", lambda x : x.getSignificanceMatrix()(0,1), float, help="MET significance matrix(0,1)"),
    NTupleVariable("metsig10", lambda x : x.getSignificanceMatrix()(1,0), float, help="MET significance matrix(1,0)"),
    NTupleVariable("metsig11", lambda x : x.getSignificanceMatrix()(1,1), float, help="MET significance matrix(1,1)"),
    NTupleVariable("l2_pt", lambda x : x.userCand("lepton1").pt(), float, help="pt of first lepton"),
    NTupleVariable("l2_eta", lambda x : x.userCand("lepton1").eta(), float, help="eta of first lepton"),
    NTupleVariable("l2_phi", lambda x : x.userCand("lepton1").phi(), float, help="phi of first lepton"),
    NTupleVariable("l2_mass", lambda x : x.userCand("lepton1").mass(), float, help="mass of first lepton"),
    NTupleVariable("l2_pdgId", lambda x : x.userCand("lepton1").pdgId(), int, help="pdgId of first lepton"),
    #NTupleVariable("l1_key", lambda x : x.userCand("lepton1").key(), int, help="key of first lepton"),
    #NTupleVariable("l1_processIndex", lambda x : x.userCand("lepton1").id().processIndex(), int, help="processIndex of first lepton"),
    #NTupleVariable("l1_productIndex", lambda x : x.userCand("lepton1").id().productIndex(), int, help="productIndex of first lepton"),
    NTupleVariable("l1_pt", lambda x : x.userCand("lepton0").pt(), float, help="pt of second lepton"),
    NTupleVariable("l1_eta", lambda x : x.userCand("lepton0").eta(), float, help="eta of second lepton"),
    NTupleVariable("l1_phi", lambda x : x.userCand("lepton0").phi(), float, help="phi of second lepton"),
    NTupleVariable("l1_mass", lambda x : x.userCand("lepton0").mass(), float, help="mass of second lepton"),
    #NTupleVariable("l2_index", lambda x : x.userCand("lepton0").key(), int, help="index of second lepton"),
    NTupleVariable("l1_pdgId", lambda x : x.userCand("lepton0").pdgId(), int, help="pdg of second lepton"),

])
##------------------------------------------  
##  ISOTRACK
##------------------------------------------  


corrMetH = NTupleObjectType("corrMetH",  baseObjectTypes = [ fourVectorType ], variables = [

    NTupleVariable("met_pt", lambda x : x.pt(), float, help="met pt"),
    NTupleVariable("met_phi", lambda x : x.phi(), float, help="met phi"),
    NTupleVariable("metsig00", lambda x : x.getSignificanceMatrix()(0,0), float, help="MET significance matrix(0,0)"),
    NTupleVariable("metsig01", lambda x : x.getSignificanceMatrix()(0,1), float, help="MET significance matrix(0,1)"),
    NTupleVariable("metsig10", lambda x : x.getSignificanceMatrix()(1,0), float, help="MET significance matrix(1,0)"),
    NTupleVariable("metsig11", lambda x : x.getSignificanceMatrix()(1,1), float, help="MET significance matrix(1,1)"),

])
##------------------------------------------  
##  ISOTRACK
##------------------------------------------  

isoTrackTypeSusy = NTupleObjectType("isoTrackSusy",  baseObjectTypes = [ isoTrackType ], variables = [
])


##------------------------------------------  
## PHOTON
##------------------------------------------  

photonTypeSusy = NTupleObjectType("gammaSusy", baseObjectTypes = [ photonType ], variables = [
    NTupleVariable("genIso04",  lambda x : getattr(x, 'genIso04', -1.0), float, mcOnly=True, help="sum pt of all status 1 particles within DeltaR = 0.4 of the photon"),
    NTupleVariable("genIso03",  lambda x : getattr(x, 'genIso03', -1.0), float, mcOnly=True, help="sum pt of all status 1 particles within DeltaR = 0.3 of the photon"),
    NTupleVariable("chHadIsoRC04",  lambda x : getattr(x, 'chHadIsoRC04', -1.0), float, mcOnly=False, help="charged iso 0.4 in a random cone 90 degrees in phi from photon"),
    NTupleVariable("chHadIsoRC",  lambda x : getattr(x, 'chHadIsoRC03', -1.0), float, mcOnly=False, help="charged iso 0.3 in a random cone 90 degrees in phi from photon"),
    NTupleVariable("drMinParton",  lambda x : getattr(x, 'drMinParton', -1.0), float, mcOnly=True, help="deltaR min between photon and parton"),
])

##------------------------------------------  
## JET
##------------------------------------------  

jetTypeSusy = NTupleObjectType("jetSusy",  baseObjectTypes = [ jetTypeExtra ], variables = [
    NTupleVariable("mcMatchFlav",  lambda x : getattr(x,'mcMatchFlav',-99), int, mcOnly=True, help="Flavour of associated parton from hard scatter (if any)"),
    NTupleVariable("charge", lambda x : x.jetCharge(), float, help="Jet charge") 
])

jetTypeSusyExtra = NTupleObjectType("jetSusyExtra",  baseObjectTypes = [ jetTypeSusy ], variables = [
    NTupleVariable("prunedMass", lambda x : x.prunedP4.M() if hasattr(x,'prunedP4') else x.mass(), float, help="Pruned mass"),
    NTupleVariable("mcNumPartons", lambda x : getattr(x,'mcNumPartons',-1),int, mcOnly=True, help="Number of matched partons (quarks, photons)"),
    NTupleVariable("mcNumLeptons", lambda x : getattr(x,'mcNumLeptons',-1),int, mcOnly=True, help="Number of matched leptons"),
    NTupleVariable("mcNumTaus", lambda x : getattr(x,'mcNumTaus',-1),int, mcOnly=True, help="Number of matched taus"),
    NTupleVariable("mcAnyPartonMass", lambda x : getattr(x,"mcAnyPartonMass",-1),float, mcOnly=True, help="Mass of associated partons, leptons, taus"),
    NTupleVariable("nSubJets", lambda x : getattr(x, "nSubJets", 0), int, help="Number of subjets (kt, R=0.2)"), 
    NTupleVariable("nSubJets25", lambda x : getattr(x, "nSubJets25", 0), int, help="Number of subjets with pt > 25 (kt, R=0.2)"), 
    NTupleVariable("nSubJets30", lambda x : getattr(x, "nSubJets30", 0), int, help="Number of subjets with pt > 30 (kt, R=0.2)"), 
    NTupleVariable("nSubJets40", lambda x : getattr(x, "nSubJets40", 0), int, help="Number of subjets with pt > 40 (kt, R=0.2)"), 
    NTupleVariable("nSubJetsZ01", lambda x : getattr(x, "nSubJetsZ01", 0), int, help="Number of subjets with pt > 0.1 * pt(jet) (kt, R=0.2)"), 
    # --------------- 
    NTupleVariable("chHEF", lambda x : x.chargedHadronEnergyFraction(), float, mcOnly = False, help="chargedHadronEnergyFraction (relative to uncorrected jet energy)"),
    NTupleVariable("neHEF", lambda x : x.neutralHadronEnergyFraction(), float, mcOnly = False,help="neutralHadronEnergyFraction (relative to uncorrected jet energy)"),
    NTupleVariable("phEF", lambda x : x.photonEnergyFraction(), float, mcOnly = False,help="photonEnergyFraction (relative to corrected jet energy)"),
    NTupleVariable("eEF", lambda x : x.electronEnergyFraction(), float, mcOnly = False,help="electronEnergyFraction (relative to corrected jet energy)"),
    NTupleVariable("muEF", lambda x : x.muonEnergyFraction(), float, mcOnly = False,help="muonEnergyFraction (relative to corrected jet energy)"),
    NTupleVariable("HFHEF", lambda x : x.HFHadronEnergyFraction(), float, mcOnly = False,help="HFHadronEnergyFraction (relative to corrected jet energy)"),
    NTupleVariable("HFEMEF", lambda x : x.HFEMEnergyFraction(), float, mcOnly = False,help="HFEMEnergyFraction (relative to corrected jet energy)"),
    NTupleVariable("chHMult", lambda x : x.chargedHadronMultiplicity(), int, mcOnly = False,help="chargedHadronMultiplicity from PFJet.h"),
    NTupleVariable("neHMult", lambda x : x.neutralHadronMultiplicity(), int, mcOnly = False,help="neutralHadronMultiplicity from PFJet.h"),
    NTupleVariable("phMult", lambda x : x.photonMultiplicity(), int, mcOnly = False,help="photonMultiplicity from PFJet.h"),
    NTupleVariable("eMult", lambda x : x.electronMultiplicity(), int, mcOnly = False,help="electronMultiplicity from PFJet.h"),
    NTupleVariable("muMult", lambda x : x.muonMultiplicity(), int, mcOnly = False,help="muonMultiplicity from PFJet.h"),
    NTupleVariable("HFHMult", lambda x : x.HFHadronMultiplicity(), int, mcOnly = False,help="HFHadronMultiplicity from PFJet.h"),
    NTupleVariable("HFEMMult", lambda x : x.HFEMMultiplicity(), int, mcOnly = False,help="HFEMMultiplicity from PFJet.h"),
    NTupleVariable("CorrFactor_L1", lambda x: x.CorrFactor_L1 if hasattr(x,'CorrFactor_L1') else 0, help="L1 correction factor"),
    NTupleVariable("CorrFactor_L1L2", lambda x: x.CorrFactor_L1L2 if hasattr(x,'CorrFactor_L1L2') else 0, help="L1L2 correction factor"),
    NTupleVariable("CorrFactor_L1L2L3", lambda x: x.CorrFactor_L1L2L3 if hasattr(x,'CorrFactor_L1L2L3') else 0, help="L1L2L3 correction factor"),
    NTupleVariable("CorrFactor_L1L2L3Res", lambda x: x.CorrFactor_L1L2L3Res if hasattr(x,'CorrFactor_L1L2L3Res') else 0, help="L1L2L3Res correction factor"),
])

fatJetType = NTupleObjectType("fatJet",  baseObjectTypes = [ jetType ], variables = [
    NTupleVariable("prunedMass",  lambda x : x.userFloat("ak8PFJetsCHSPrunedMass"),  float, help="pruned mass"),
    NTupleVariable("trimmedMass", lambda x : x.userFloat("ak8PFJetsCHSTrimmedMass"), float, help="trimmed mass"),
    NTupleVariable("filteredMass", lambda x : x.userFloat("ak8PFJetsCHSFilteredMass"), float, help="filtered mass"),
    NTupleVariable("softDropMass", lambda x : x.userFloat("ak8PFJetsCHSSoftDropMass"), float, help="trimmed mass"),
    NTupleVariable("tau1", lambda x : x.userFloat("NjettinessAK8:tau1"), float, help="1-subjettiness"),
    NTupleVariable("tau2", lambda x : x.userFloat("NjettinessAK8:tau2"), float, help="2-subjettiness"),
    NTupleVariable("tau3", lambda x : x.userFloat("NjettinessAK8:tau3"), float, help="3-subjettiness"),
    NTupleVariable("topMass", lambda x : (x.tagInfo("caTop").properties().topMass if x.tagInfo("caTop") else -99), float, help="CA8 jet topMass"),
    NTupleVariable("minMass", lambda x : (x.tagInfo("caTop").properties().minMass if x.tagInfo("caTop") else -99), float, help="CA8 jet minMass"),
    NTupleVariable("nSubJets", lambda x : (x.tagInfo("caTop").properties().nSubJets if x.tagInfo("caTop") else -99), float, help="CA8 jet nSubJets"),
])
   
jetTypeH = NTupleObjectType("jetSusy",  baseObjectTypes = [ jetTypeExtra ], variables = [
    NTupleVariable("mcMatchFlav",  lambda x : getattr(x,'mcMatchFlav',-99), int, mcOnly=True, help="Flavour of associated parton from hard scatter (if any)"),
])#JB
   
##------------------------------------------  
## MET
##------------------------------------------  
  
metTypeSusy = NTupleObjectType("metSusy", baseObjectTypes = [ metType ], variables = [
])

##------------------------------------------  
## GENPARTICLE
##------------------------------------------  


##------------------------------------------  
## SECONDARY VERTEX CANDIDATE
##------------------------------------------  
svType = NTupleObjectType("sv", baseObjectTypes = [ fourVectorType ], variables = [
    NTupleVariable("charge",   lambda x : x.charge(), int),
    NTupleVariable("ntracks", lambda x : x.numberOfDaughters(), int, help="Number of tracks (with weight > 0.5)"),
    NTupleVariable("chi2", lambda x : x.vertexChi2(), help="Chi2 of the vertex fit"),
    NTupleVariable("ndof", lambda x : x.vertexNdof(), help="Degrees of freedom of the fit, ndof = (2*ntracks - 3)" ),
    NTupleVariable("dxy",  lambda x : x.dxy.value(), help="Transverse distance from the PV [cm]"),
    NTupleVariable("edxy", lambda x : x.dxy.error(), help="Uncertainty on the transverse distance from the PV [cm]"),
    NTupleVariable("ip3d",  lambda x : x.d3d.value(), help="3D distance from the PV [cm]"),
    NTupleVariable("eip3d", lambda x : x.d3d.error(), help="Uncertainty on the 3D distance from the PV [cm]"),
    NTupleVariable("sip3d", lambda x : x.d3d.significance(), help="S_{ip3d} with respect to PV (absolute value)"),
    NTupleVariable("cosTheta", lambda x : x.cosTheta, help="Cosine of the angle between the 3D displacement and the momentum"),
    NTupleVariable("mva", lambda x : x.mva, help="MVA discriminator"),
    NTupleVariable("jetPt",  lambda x : x.jet.pt() if x.jet != None else 0, help="pT of associated jet"),
    NTupleVariable("jetBTagCSV",   lambda x : x.jet.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags') if x.jet != None else -99, help="CSV b-tag of associated jet"),
    NTupleVariable("jetBTagCMVA",  lambda x : x.jet.btag('pfCombinedMVABJetTags') if x.jet != None else -99, help="CMVA b-tag of associated jet"),
    NTupleVariable("mcMatchNTracks", lambda x : getattr(x, 'mcMatchNTracks', -1), int, mcOnly=True, help="Number of mc-matched tracks in SV"),
    NTupleVariable("mcMatchNTracksHF", lambda x : getattr(x, 'mcMatchNTracksHF', -1), int, mcOnly=True, help="Number of mc-matched tracks from b/c in SV"),
    NTupleVariable("mcMatchFraction", lambda x : getattr(x, 'mcMatchFraction', -1), mcOnly=True, help="Fraction of mc-matched tracks from b/c matched to a single hadron (or -1 if mcMatchNTracksHF < 2)"),
    NTupleVariable("mcFlavFirst", lambda x : getattr(x,'mcFlavFirst', -1), int, mcOnly=True, help="Flavour of last ancestor with maximum number of matched daughters"),
    NTupleVariable("mcFlavHeaviest", lambda x : getattr(x,'mcFlavHeaviest', -1), int, mcOnly=True, help="Flavour of heaviest hadron with maximum number of matched daughters"),
    NTupleVariable("maxDxyTracks", lambda x : x.maxDxyTracks, help="highest |dxy| of vertex tracks"),
    NTupleVariable("secDxyTracks", lambda x : x.secDxyTracks, help="second highest |dxy| of vertex tracks"),
    NTupleVariable("maxD3dTracks", lambda x : x.maxD3dTracks, help="highest |ip3D| of vertex tracks"),
    NTupleVariable("secD3dTracks", lambda x : x.secD3dTracks, help="second highest |ip3D| of vertex tracks"),

])

heavyFlavourHadronType = NTupleObjectType("heavyFlavourHadron", baseObjectTypes = [ genParticleType ], variables = [
    NTupleVariable("flav", lambda x : x.flav, int, mcOnly=True, help="Flavour"),
    NTupleVariable("sourceId", lambda x : x.sourceId, int, mcOnly=True, help="pdgId of heaviest mother particle (stopping at the first one heaviest than 175 GeV)"),
    NTupleVariable("svMass",   lambda x : x.sv.mass() if x.sv else 0, help="SV: mass"),
    NTupleVariable("svPt",   lambda x : x.sv.pt() if x.sv else 0, help="SV: pt"),
    NTupleVariable("svCharge",   lambda x : x.sv.charge() if x.sv else -99., int, help="SV: charge"),
    NTupleVariable("svNtracks", lambda x : x.sv.numberOfDaughters() if x.sv else 0, int, help="SV: Number of tracks (with weight > 0.5)"),
    NTupleVariable("svChi2", lambda x : x.sv.vertexChi2() if x.sv else -99., help="SV: Chi2 of the vertex fit"),
    NTupleVariable("svNdof", lambda x : x.sv.vertexNdof() if x.sv else -99., help="SV: Degrees of freedom of the fit, ndof = (2*ntracks - 3)" ),
    NTupleVariable("svDxy",  lambda x : x.sv.dxy.value() if x.sv else -99., help="SV: Transverse distance from the PV [cm]"),
    NTupleVariable("svEdxy", lambda x : x.sv.dxy.error() if x.sv else -99., help="SV: Uncertainty on the transverse distance from the PV [cm]"),
    NTupleVariable("svIp3d",  lambda x : x.sv.d3d.value() if x.sv else -99., help="SV: 3D distance from the PV [cm]"),
    NTupleVariable("svEip3d", lambda x : x.sv.d3d.error() if x.sv else -99., help="SV: Uncertainty on the 3D distance from the PV [cm]"),
    NTupleVariable("svSip3d", lambda x : x.sv.d3d.significance() if x.sv else -99., help="SV: S_{ip3d} with respect to PV (absolute value)"),
    NTupleVariable("svCosTheta", lambda x : x.sv.cosTheta if x.sv else -99., help="SV: Cosine of the angle between the 3D displacement and the momentum"),
    NTupleVariable("svMva", lambda x : x.sv.mva if x.sv else -99., help="SV: mva value"),
    NTupleVariable("jetPt",  lambda x : x.jet.pt() if x.jet != None else 0, help="Jet: pT"),
    NTupleVariable("jetBTagCSV",  lambda x : x.jet.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags') if x.jet != None else -99, help="CSV b-tag of associated jet"),
    NTupleVariable("jetBTagCMVA",  lambda x : x.jet.btag('pfCombinedMVABJetTags') if x.jet != None else -99, help="CMVA b-tag of associated jet"),
    
])

genJetType = NTupleObjectType("genParticleWithMotherId", baseObjectTypes = [ fourVectorType ], mcOnly=True, variables = [])

def getTriggerObjectType(name, filtername = ''):
    if filtername == '':
        return particleType
    elif type(filtername) == str:
        return NTupleObjectType("triggerObject", baseObjectTypes = [ particleType ], variables = [
                                 NTupleVariable("passesFilter", lambda x : x.hasFilterLabel(filtername), int, mcOnly=False, help="passesFilter")])
    elif type(filtername) == dict:
        return NTupleObjectType("triggerObject", baseObjectTypes = [ particleType ], variables = [
                                 NTupleVariable("passesFilterLeg1", lambda x : all( [x.hasFilterLabel(fn) for fn in filtername['Leg1'] ] ), int, mcOnly=False, help="passesFilterLeg1"),
                                 NTupleVariable("passesFilterLeg2", lambda x : all( [x.hasFilterLabel(fn) for fn in filtername['Leg2'] ] ), int, mcOnly=False, help="passesFilterLeg2"),])

def ptRel(p4,axis):
    a = ROOT.TVector3(axis.Vect().X(),axis.Vect().Y(),axis.Vect().Z())
    o = ROOT.TLorentzVector(p4.Px(),p4.Py(),p4.Pz(),p4.E())
    return o.Perp(a)
def ptRelv1(p4,axis):
    axis = axis - p4
    a = ROOT.TVector3(axis.Vect().X(),axis.Vect().Y(),axis.Vect().Z())
    o = ROOT.TLorentzVector(p4.Px(),p4.Py(),p4.Pz(),p4.E())
    return o.Perp(a)
def jetLepAwareJEC(lep): # use only if jetAna.calculateSeparateCorrections==True
    p4l = lep.p4()
    l = ROOT.TLorentzVector(p4l.Px(),p4l.Py(),p4l.Pz(),p4l.E())
    if not hasattr(lep.jet,'rawFactor'): return l # if lep==jet (matched to lepton object itself)
    p4j = lep.jet.p4()
    j = ROOT.TLorentzVector(p4j.Px(),p4j.Py(),p4j.Pz(),p4j.E())
    if ((j*lep.jet.rawFactor()-l).Rho()<1e-4): return l # matched to jet containing only the lepton
    j = (j*lep.jet.rawFactor()-l*(1.0/lep.jet.l1corrFactor()))*lep.jet.corrFactor()+l
    return j
def ptRelv2(lep): # use only if jetAna.calculateSeparateCorrections==True
    m = jetLepAwareJEC(lep)
    p4l = lep.p4()
    l = ROOT.TLorentzVector(p4l.Px(),p4l.Py(),p4l.Pz(),p4l.E())
    if ((m-l).Rho()<1e-4): return 0 # lep.jet==lep (no match) or jet containing only the lepton
    return l.Perp((m-l).Vect())
def ptRelHv2(lep): # use only if jetAna.calculateSeparateCorrections==True
    m = jetLepAwareJEC(lep)
    p4l = lep.p4()
    l = ROOT.TLorentzVector(p4l.Px(),p4l.Py(),p4l.Pz(),p4l.E())
    return (m-l).Perp(l.Vect())
   
def isoRelH(lep,tag):
    iso = getattr(lep,'isoSumRawP4Charged'+tag)+getattr(lep,'isoSumRawP4Neutral'+tag)
    p4l = lep.p4()
    l = ROOT.TLorentzVector(p4l.Px(),p4l.Py(),p4l.Pz(),p4l.E())
    m = ROOT.TLorentzVector(iso.Px(),iso.Py(),iso.Pz(),iso.E())
    return m.Perp(l.Vect())
