from itertools import combinations
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR

import PhysicsTools.HeppyCore.framework.config as cfg

class TriggerInfo(object):
    def __init__(self, name, index, fired=True, prescale=1.):
        self.name = name
        self.index = index
        self.fired = fired
        self.prescale = prescale
        self.objects = []
        self.objIds = set()
        self.object_names = []

    def __str__(self):
        return 'TriggerInfo: name={name}, fired={fired}, n_objects={n_o}'.format(
            name=self.name, fired=self.fired, n_o=len(self.objects))

class TriggerAnalyzer(Analyzer):
    '''Access to trigger information, and trigger selection. The required
    trigger names need to be attached to the components.'''

    def declareHandles(self):

        super(TriggerAnalyzer, self).declareHandles()
        if hasattr(self.cfg_ana, 'triggerResultsHandle'):
            myhandle = self.cfg_ana.triggerResultsHandle
            self.EDMProc = myhandle[2]
            self.handles['triggerResultsHLT'] = AutoHandle(
                (myhandle[0], myhandle[1], myhandle[2]),
                'edm::TriggerResults'
                )
        else:
            self.EDMProc = 'HLT'   
            self.handles['triggerResultsHLT'] = AutoHandle(
                ('TriggerResults', '', 'HLT'),
                'edm::TriggerResults'
                )

        if hasattr(self.cfg_ana, 'triggerObjectsHandle'):
            myhandle = self.cfg_ana.triggerObjectsHandle
            self.handles['triggerObjects'] = AutoHandle(
                (myhandle[0], myhandle[1], myhandle[2]),
                'std::vector<pat::TriggerObjectStandAlone>'
                )
        else:    
            self.handles['triggerObjects'] =  AutoHandle(
                'selectedPatTrigger',
                'std::vector<pat::TriggerObjectStandAlone>'
                )
 
        if hasattr(self.cfg_ana, 'triggerPrescalesHandle'):
            myhandle = self.cfg_ana.triggerPrescalesHandle
            self.handles['triggerPrescales'] = AutoHandle(
                (myhandle[0], myhandle[1], myhandle[2]),
                'pat::PackedTriggerPrescales'
                )
        else:    
            self.handles['triggerPrescales'] =  AutoHandle(
                'patTrigger',
                'pat::PackedTriggerPrescales'
                )
 
    def beginLoop(self, setup):
        super(TriggerAnalyzer,self).beginLoop(setup)
        self.triggerList = self.cfg_comp.triggers
        self.triggerObjects = []
        self.extraTriggerObjects = []
        if hasattr(self.cfg_comp, 'triggerobjects'):
            self.triggerObjects = self.cfg_comp.triggerobjects
        if hasattr(self.cfg_ana, 'extraTrig'):
            self.extraTrig = self.cfg_ana.extraTrig
        else:
            self.extraTrig = []
        if hasattr(self.cfg_ana, 'extraTrigObj'):
            self.extraTriggerObjects = self.cfg_ana.extraTrigObj

        self.vetoTriggerList = None

        if hasattr(self.cfg_comp, 'vetoTriggers'):
            self.vetoTriggerList = self.cfg_comp.vetoTriggers
            
        self.counters.addCounter('Trigger')
        self.counters.counter('Trigger').register('All events')
        self.counters.counter('Trigger').register(self.EDMProc)

        for trigger in self.triggerList + self.extraTrig:
            self.counters.counter('Trigger').register(trigger)
            self.counters.counter('Trigger').register(trigger + 'prescaled')



    def process(self, event):
        self.readCollections(event.input)

        event.run = event.input.eventAuxiliary().id().run()
        event.lumi = event.input.eventAuxiliary().id().luminosityBlock()
        event.eventId = event.input.eventAuxiliary().id().event()

        triggerBits = self.handles['triggerResultsHLT'].product()
        names = event.input.object().triggerNames(triggerBits)

        preScales = self.handles['triggerPrescales'].product()

        self.counters.counter('Trigger').inc('All events')

        trigger_passed = False

        # if not self.triggerList:
        #     return True

        trigger_infos = []
        triggers_fired = []
        for trigger_name in self.triggerList + self.extraTrig:
            index = names.triggerIndex(trigger_name)
            if index == len(triggerBits):
                continue
            prescale = preScales.getPrescaleForIndex(index)
            fired = triggerBits.accept(index)

            trigger_infos.append(TriggerInfo(trigger_name, index, fired, prescale))


            #print trigger_name, fired, prescale
            #if fired:
            #    import pdb ; pdb.set_trace()
            if fired and (prescale == 1 or self.cfg_ana.usePrescaled):
                if trigger_name in self.triggerList:
                    trigger_passed = True
                    self.counters.counter('Trigger').inc(trigger_name)            
                triggers_fired.append(trigger_name)
            elif fired:
                print 'WARNING: Trigger not passing because of prescale', trigger_name
                self.counters.counter('Trigger').inc(trigger_name + 'prescaled')

        

        if self.cfg_ana.requireTrigger:
            if not trigger_passed:
                return False


        event.TOE_IsoMu18 = []
        event.TOE_IsoMu20 = []
        event.TOE_IsoMu22 = []
        event.TOE_IsoMu22_eta2p1 = []
        event.TOE_IsoMu24 = []
        event.TOE_IsoMu27 = []
        event.TOE_IsoTkMu18 = []
        event.TOE_IsoTkMu20 = []
        event.TOE_IsoTkMu22 = []
        event.TOE_IsoTkMu22_eta2p1 = []
        event.TOE_IsoTkMu24 = []
        event.TOE_IsoTkMu27 = []
        event.TOE_IsoMu17_eta2p1_LooseIsoPFTau20_SingleL1 = []
        event.TOE_IsoMu17_eta2p1_LooseIsoPFTau20 = []
        event.TOE_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1 = []
        event.TOE_IsoMu19_eta2p1_LooseIsoPFTau20 = []
        event.TOE_IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1 = []
        event.TOE_Ele23_WPLoose_Gsf = []
        event.TOE_Ele24_eta2p1_WPLoose_Gsf = []
        event.TOE_Ele25_WPTight_Gsf = []
        event.TOE_Ele25_eta2p1_WPLoose_Gsf = []
        event.TOE_Ele25_eta2p1_WPTight_Gsf = []
        event.TOE_Ele27_WPLoose_Gsf = []
        event.TOE_Ele27_WPTight_Gsf = []
        event.TOE_Ele27_eta2p1_WPLoose_Gsf = []
        event.TOE_Ele27_eta2p1_WPTight_Gsf = []
        event.TOE_Ele32_eta2p1_WPTight_Gsf = []
        event.TOE_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1 = []
        event.TOE_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1 = []
        event.TOE_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20 = []
        event.TOE_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30 = []
        event.TOE_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1 = []
        event.TOE_Ele32_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1 = []
        event.TOE_Ele45_WPLoose_Gsf_L1JetTauSeeded = []

        event.TOE_VLooseIsoPFTau120_Trk50_eta2p1 = []
        event.TOE_VLooseIsoPFTau140_Trk50_eta2p1 = []
        event.TOE_DoubleMediumIsoPFTau32_Trk1_eta2p1_Reg = []
        event.TOE_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg = []
        event.TOE_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg = []
        event.TOE_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg = [] 
        
#         if event.eventId == 104644585: import pdb ; pdb.set_trace()
        if self.cfg_ana.addTriggerObjects:
            triggerObjects = self.handles['triggerObjects'].product()
#             if event.eventId == 104644585: import pdb ; pdb.set_trace()
            for to in triggerObjects:
                to.unpackPathNames(names)
                for info in trigger_infos:
#                     if event.eventId == 104644585: import pdb ; pdb.set_trace()
                    if to.hasPathName(info.name):

                        attr = info.name.replace('HLT','TOE').split('_v')[0]
                        if hasattr(event, attr):
                            getattr(event, attr).append(to)
                        

                        info.objects.append(to)
                        info.objIds.add(abs(to.pdgId()))
        
        
        # RIC: remove duplicated trigger objects 
        #      (is this something that may happen in first place?)
        for info in trigger_infos:
#             if event.eventId == 104644585: 
#                 for oo in info.objects: print oo.pt(), oo.eta(), oo.phi()


#MF B: REMOVE trigger objects that do not fulfill the trigger requirements

            f_IsoMu22='hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09'
            f_IsoMu22_eta2p1='hltL3crIsoL1sSingleMu20erL1f0L2f10QL3f22QL3trkIsoFiltered0p09'
            f_IsoTkMu22='hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09'
            f_IsoTkMu22_eta2p1='hltL3fL1sMu20erL1f0Tkf22QL3trkIsoFiltered0p09'
            f_VLooseIsoPFTau120_Trk50_eta2p1='hltPFTau120TrackPt50LooseAbsOrRelVLooseIso'
            f_VLooseIsoPFTau140_Trk50_eta2p1='hltPFTau140TrackPt50LooseAbsOrRelVLooseIso'

##X            for obj in info.objects:
##X
##X                if info.name=='HLT_IsoTkMu22_eta2p1_v4':
##X                    if not f_IsoTkMu22_eta2p1 in obj.filterLabels(): info.objects.remove(obj)


#MF E

#             print '###########'
#             print event.eventId
#             print info.name
#             print len(info.objects),' XXX'
#             for obj in info.objects: 
#                 print len(obj.filterLabels())
#                 toFilter = set(sorted(list(obj.filterLabels())))

#                 print 'fffffffffff'
# #                print 'filterLabels:',toFilter
#                 print 'filterLabels:',set(sorted(list(obj.filterLabels())))
#                 print 'FFFFFFFFFFF'

#                 print 'ppppppppppp'
#                 print 'pathNames:',set(sorted(list(obj.pathNames())))
#                 print 'PPPPPPPPPPP'

#                 print 'aaaaaaaaaaa'
#                 print 'hasFilterLabel hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09:',obj.hasFilterLabel('hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09')
#                 print 'hasConditionName hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09:',obj.hasConditionName('hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09')
#                 print 'hasPathLastFilterAccepted',obj.hasPathLastFilterAccepted()
#                 print 'hasPathL3FilterAccepted',obj.hasPathL3FilterAccepted()
#                 print 'AAAAAAAAAAA'


# #               if 'hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09' in obj.filterLabels() or 'hltL3crIsoL1sSingleMu20erL1f0L2f10QL3f22QL3trkIsoFiltered0p09' in obj.filterLabels():
# #                   print 'YYY hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09 hltL3crIsoL1sSingleMu20erL1f0L2f10QL3f22QL3trkIsoFiltered0p09'
# #                if 'hltL2fL1sSingleMu18erIorSingleMu20erL1f0L2Filtered10Q' in obj.filterLabels():
# #                    print 'test YYY'
#             print '###########'

            objs = info.objects     
            for to1, to2 in combinations(info.objects, 2):
                to1Filter = set(sorted(list(to1.filterLabels())))
                to2Filter = set(sorted(list(to2.filterLabels())))
                if to1Filter != to2Filter:
                    continue
                dR = deltaR(to1.eta(), to1.phi(), to2.eta(), to2.phi())
                if dR<0.01 and to2 in objs:
                    objs.remove(to2)
            info.objects = objs
#             if event.eventId == 104644585: 
#                 for oo in info.objects: print oo.pt(), oo.eta(), oo.phi()
                                                
        event.trigger_infos = trigger_infos

        if self.cfg_ana.verbose:
            print 'run %d, lumi %d,event %d' %(event.run, event.lumi, event.eventId) , 'Triggers_fired: ', triggers_fired  
        if hasattr(self.cfg_ana, 'saveFlag'):
            if self.cfg_ana.saveFlag:
                setattr(event, 'tag', False)    
                setattr(event, 'probe', False)
                for trig in self.triggerList:
                    if trig in triggers_fired:
                        setattr(event, 'tag', True)    
                        break
                for trig in self.extraTrig:
                    if trig in triggers_fired:
                        setattr(event, 'probe', True)
                        break

        self.counters.counter('Trigger').inc(self.EDMProc)
        return True

    def __str__(self):
        
        tmp = super(TriggerAnalyzer,self).__str__()
        triglist = str(self.triggerList)
        return '\n'.join([tmp, triglist])

setattr(TriggerAnalyzer, 'defaultConfig', 
    cfg.Analyzer(
        class_object=TriggerAnalyzer,
        requireTrigger=True,
        usePrescaled=False,
        addTriggerObjects=True,
        # vetoTriggers=[],
    )
)
