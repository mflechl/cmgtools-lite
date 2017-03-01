import os
import sys
import time
import json
import argparse
import ROOT
import das_client 
from subprocess import Popen, PIPE



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ptime',dest='ptime', help='Time between two status checks.', type=int, metavar = 'INT',default=3000)
    parser.add_argument('--nrep',dest='rep', help='Number of status checks.', type=int, metavar = 'INT',default=1)
    parser.add_argument('--resubmit',dest='resubmit', help='Resubmit all failed jobs.', action='store_true')
    parser.add_argument('--show_completed',dest='show_completed', help='Show list of completed jobs at end of status report.', action='store_true')
    parser.add_argument('--force',dest='force', help='Force resubmit finished jobs. Need to give SAMPLE and JOBIDS', action='store_true')
    parser.add_argument('--jobids',dest='jobids', help='Jobs to force resubmit', type=str, default = '')
    parser.add_argument('--add_das',dest='add_das', help='Add DAS URL for SAMPLE', action='store_true')
    parser.add_argument('--sample',dest='sample', help='SAMPLE name for force resubmit or adding das url', type=str, default = '')
    parser.add_argument('--validate',dest='validate', help='Valiate samples on DAS', action='store_true' )

    args = parser.parse_args()
    SR = StatusReport(resubmit=args.resubmit, show_completed=args.show_completed)
    

    if args.force:
        if args.jobids == '' or args.sample == '':
            print "Need to specify jobids and sample name when running force resubmit. Aborting..."
            sys.exit()

        SR.resubmitJob(args.sample, args.jobids)

    elif args.add_das:
        if args.sample == '':
            print "Need to specify sample name when adding DAS URL. Aborting..."
            sys.exit()

        SR.writeDASurl(args.sample)

    elif args.validate:
        SR.validatePublicSamples()

    elif not args.add_das and not args.force:
        if args.resubmit and args.rep > 1:
            print 'Resubmiting jobs every {0}sec {1} time(s).'.format(args.ptime, args.rep)

        for i in xrange(args.rep):
            SR.getStatusAll()
            if args.rep > 1 and i != args.rep-1:
                time.sleep(args.ptime)




class StatusReport():
    def __init__(self,resubmit = False, show_completed = False):
        self.base = '/'.join([os.environ['CMSSW_BASE'], 'src', 'CMGTools' ])
        self.status_report = {}
        self.completed_jobs = []
        self.total_finished = 0
        self.show_completed = show_completed
        self.resubmit = resubmit
        self.getRunFolders()
        self.getStatusReport()

    def __del__(self):
        with open( '/'.join([self.base,'HephyTools', 'status_report.json']),'w' ) as FSO:
            json.dump(self.status_report, FSO, indent=4)

        if self.show_completed:
            if self.completed_jobs != []:
                print '{0}\n{1}COMPLETED\n{0}\n{2}'.format('-'*80, ' '*32, '\n'.join( self.completed_jobs ) )

        elif len(self.completed_jobs) > 0:
            print '{0} Jobs completed'.format( len(self.completed_jobs) )

        if self.total_finished > 0:
            print '\n\n','Total finished jobs this round: {0}'.format(self.total_finished)

    def getStatusReport(self):
        if os.path.exists( '/'.join([self.base,'HephyTools', 'status_report.json'])):
            with open( '/'.join([self.base,'HephyTools', 'status_report.json']),'r' ) as FSO:
                data = json.load(FSO)
            for sample in data.keys():
                if self.status_report.has_key(sample):
                    self.status_report[sample] = data[sample]
                    self.status_report[sample]['validated'] = False

    def getRunFolders(self):

        run_folders = ['H2TauTau/prod/MC', 'H2TauTau/prod/DATA', 'TTHAnalysis/cfg/crab_HEPHY/']

        for run_folder in run_folders:
            for folder in os.listdir('/'.join([ self.base, run_folder ])  ):
                if 'crab_' in folder and os.path.isdir( '/'.join([ self.base, run_folder, folder ]) ):
                    for sample in os.listdir( '/'.join([ self.base, run_folder, folder ]) ):
                        if 'crab_' in sample and os.path.isdir( '/'.join([ self.base, run_folder, folder, sample ]) ):
                            if not self.status_report.has_key(sample.replace('crab_','')):
                                self.status_report[sample.replace('crab_','')] =  {'path':'/'.join([ self.base, run_folder, folder, sample ]), 'status': 'RUNNING', 'das_url': '','finished':0, 'validated':False}


    def getStatusAll(self):
        sample_keys = self.status_report.keys()
        sample_keys.sort()
        step_1=[]
        step_2=[]
        for k in sample_keys:
            if 'CMGTools' in k:
                step_2.append(k)
            else:
                step_1.append(k)

        print '{0}\n{1}RUNNING\n{0}'.format('-'*80, ' '*32 )
        for sample in step_1 + step_2:
            
            if self.status_report[sample]['status'] == 'COMPLETED':
                self.completed_jobs.append(sample)
            else:
                print '\t\t\033[1m' + sample +'\033[0m\n'
                out = self.getStatus(sample )

                if out['error'] == '':
                    print out['head'],'\n'
                    if out['job'].has_key('string'): print out['job']['string'],'\n'
                    if out['publ'].has_key('string'): print out['publ']['string'],'\n'
                    print '{0}\n'.format('-'*80 )
                else:
                    print out['error'],'\n'
                    print '{0}\n'.format('-'*80 )



    def getStatus(self, sample):
        proc = Popen('crab status {0}'.format( self.status_report[sample]['path'] ),stdout = PIPE, shell=True)
        (out, err) = proc.communicate()

        status = { "head":'', "job": {}, "publ":{}, "das_url":"", "error":"" }
        if "Task status" in out:
            status["head"] = self.extractTaskStatus(out)

            for block in out.split('\n\n'):
                if "Jobs status" in block:
                    status['job'] = self.refineOuput(block, int(self.status_report[sample]['finished']) )
                    if len(status['job']['finished']) > 0:
                        self.status_report[sample]['finished'] = status['job']['finished'][0]

                if "Publication status" in block:
                    status['publ'] = self.refineOuput(block)

                if "Output dataset" in block:
                    status['das_url'] = self.extractDASurl( block )
                    self.status_report[sample]['das_url'] = status['das_url']

            if status['job'].get('failed',False ) and self.resubmit:
                self.resubmitJob( sample )

            if status['publ'].get('failed',False ) and self.resubmit:
                self.republishJob( sample )

            if "COMPLETED" in status["head"]:
                if status['publ'] == {}:
                    self.status_report[sample]['status'] = 'COMPLETED'

                elif status['publ']['finished'][0] == status['publ']['finished'][1]:
                        self.writeDASurl( sample )

        else:
            status['error'] = out
        return status

    def getFilesOnDAS(self, url ):



        host    = 'https://cmsweb.cern.ch'
        query   = "file dataset={0}  instance=prod/phys03".format( url )
        ckey    =  das_client.x509()
        cert    =  das_client.x509()
        capath  = os.environ.get("X509_CERT_DIR")
        das_client.check_glidein()
        das_client.check_auth(ckey)
        file_list = []
        jsondict = das_client.get_data(host, query, 0, 0, 0, 300, ckey, cert, capath, 0)
        for i in  jsondict['data']:
            try:
                file_list.append( 'root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/{0}'.format( i['file'][0]['name'] ) )
            except:
                pass
        return file_list

    def validatePublicSamples(self):

        for sample in self.status_report.keys():
            print sample 
            missing = []
            url = self.status_report[sample]['das_url']
            if url == '' or self.status_report[sample]['validated']: continue

            for f in self.getFilesOnDAS(url):
                try:
                    a = ROOT.TFile.Open(f)
                    op = a.IsOpen()
                    if a.IsZombie(): raise ReferenceError
                    a.Close()
                except ReferenceError:
                    missing.append( ''.join([ s for s in f.split('/')[-1] if s.isdigit()]) )

            if len(missing ) > 0:
                self.resubmitJob(sample,  ','.join( missing ) )
            else:
                self.status_report[sample]['validated'] = True
                print 'Validated\n'

    def resubmitJob(self, sample, jids = None):
        if not self.status_report.has_key(sample):
            print "Sample not found..."
            return

        if jids is None:
            proc = Popen('crab resubmit --sitewhitelist=T2_AT_Vienna {0}'.format( self.status_report[sample]['path'] ),stdout = PIPE, shell=True)
        if type(jids) == str:
            proc = Popen('crab resubmit --force --jobids={0} {1}'.format( jids, self.status_report[sample]['path'] ),stdout = PIPE, shell=True)
            self.status_report[sample]['status'] = 'RUNNING'

        (out, err) = proc.communicate()

        if not jids is None:
            print out
        else:
            print '\033[92mResubmitting failed jobs\033[0m' 

    def republishJob(self, sample):
        if not self.status_report.has_key(sample):
            print "Sample not found..."
            return

        proc = Popen('crab resubmit --publication {0}'.format( self.status_report[sample]['path'] ),stdout = PIPE, shell=True)
        (out, err) = proc.communicate()
        print '\033[92mRepublishing failed jobs\033[0m' 

    def refineOuput(self, block, preF = None):

        output = {'string':[],'failed': False, 'finished':[]}
        for l in block.split('\n'):
            if "failed" in l:
                output['string'].append( l.replace('failed','\033[91mfailed').replace(')',')\033[0m') )
                output['failed'] = True

            elif "transferring" in l:
                output['string'].append( l.replace('transferring','\033[93mtransferring').replace(')',')\033[0m') )

            elif "finished" in l:
                fin = ''
                output['finished'] = [ int(i,0) for i in l.split('(')[1].split(')')[0].replace(' ','').split('/') ]
                if not preF is None:
                    tmp = output['finished'][0] - preF
                    self.total_finished += int(tmp)
                    if tmp > 0:
                        fin = '\t+{0}'.format( tmp )

                output['string'].append( l.replace('finished','\033[92mfinished').replace(')','){0}\033[0m'.format(fin) ) )

            else:
                output['string'].append( l )

        output['string'] = '\n'.join( output['string'] )
        return output

    def extractTaskStatus(self,block):
        head = ''
        for l in block.split('\n'):
            if "Task status" in l:
                head = l
            if "warning" in l:
                head += l + '\n'

        return head

    def extractDASurl(self,block):
        url = ''
        for l in block.split('\n'):
            if "Output dataset:" in l:
                url = l.replace("Output dataset:","").replace("\t","")
        return url

    def writeDASurl(self,run_sample):
        if not self.status_report.has_key(run_sample):
            print "Sample not found..."
            return

        if os.path.exists( '/'.join([self.base,'HephyTools', 'datasets.json'])):
            with open( '/'.join([self.base,'HephyTools', 'datasets.json']),'r' ) as FSO:
                data = json.load(FSO)
        else:
            return

        for tranche in data.keys():
            for sample in data[tranche].keys():
                if '_'.join([sample, data[tranche][sample]['prod_label']]) in run_sample:
                    print '\033[92mAdding DAS URL\033[0m'
                    data[tranche][sample]['das_url'] = self.status_report[run_sample]['das_url']
                    self.status_report[run_sample]['status'] = 'COMPLETED'

        with open( '/'.join([self.base,'HephyTools', 'datasets.json']),'w' ) as FSO:
            json.dump(data, FSO, indent=4)








if __name__ == '__main__':
    main()




    
