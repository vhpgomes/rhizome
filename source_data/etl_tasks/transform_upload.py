from pandas import read_csv
from pandas import notnull
from pprint import pprint
import json

from django.conf import settings
from django.db import transaction
from pandas.io.excel import read_excel

from source_data.models import *
from datapoints.models import DataPoint


class DocTransform(object):

    def __init__(self,user_id,document_id,file_path=None):

        self.source_datapoints = []
        self.user_id = user_id
        self.document_id = document_id

        ## SHOULD BE USER INPUT AND STORED IN DOC_DETAIL ##
        self.file_delimiter = ','

        if not file_path:
            file_path = str(Document.objects.get(id=self.document_id).\
                docfile)

        self.file_path = file_path

        self.to_process_status = ProcessStatus.objects.\
            get(status_text='TO_PROCESS').id

        self.doc_deets ={
            'uq_id_column': None,
            'username_column': None,
            'image_col': None,
            'campaign_column': None,
            'region_column': None,
            'region_display_name': None
        }

        for k,v in self.doc_deets.iteritems():

            new_value = DocumentDetail.objects.get(
                document_id = self.document_id,
                doc_detail_type_id = DocDetailType.objects.get(name=k).id
            ).doc_detail_value

            self.doc_deets[k] = new_value


    def pre_process_file(self,full_file_path):

        f_header = open(full_file_path,'r')
        top_row = f_header.readlines()[0]
        cleaned = top_row.replace('\r','').replace('\n','')
        self.file_header = cleaned.split(self.file_delimiter)

        f_header.close()

        f = open(full_file_path,'r')
        file_stream = f.readlines()[1:]

        return file_stream

    def post_process_file(self):
        '''
        Put the submission data into a clean table for the view_raw section
        of the source data management app.
        '''

        source_submissions = SourceSubmission.objects.filter(document_id = \
            self.document_id)

        batch = []
        for i, (row) in enumerate(source_submissions):

            submission_data = row.submission_json
            submission_detail_dict = {
                'source_submission_id': row.id,
                'img_location':  submission_data[self.doc_deets['image_col']],
                'document_id':   self.document_id,
                'username_code':  submission_data[self.doc_deets['username_column']],
                'campaign_code':  submission_data[self.doc_deets['campaign_column']],
                'region_code':  submission_data[self.doc_deets['region_column']],
                'region_display':  submission_data[self.doc_deets['region_display_name']],
                'raw_data_proxy' :''
            }
            batch.append(SourceSubmissionDetail(**submission_detail_dict))

        ss = SourceSubmissionDetail.objects.bulk_create(batch)

        return ss

    def process_file(self):
        '''
        Returns a list of source submisison objects
        '''

        print 'PROCESSINGGGGG=====\n' * 5

        full_file_path = settings.MEDIA_ROOT + self.file_path
        file_stream = self.pre_process_file(full_file_path)

        batch = {}
        for i,(submission) in enumerate(file_stream):

            ss, instance_guid = self.process_source_submission(submission,i)
            if ss is not None:
                batch[instance_guid] = ss
            else:
                pass

        object_list = [SourceSubmission(**v) for k,v in batch.iteritems()]
        ss = SourceSubmission.objects.bulk_create(object_list)

        doc_deets = self.post_process_file()
        mappings = self.upsert_source_object_map()

        return ss

    def upsert_source_object_map(self):
        '''
        TODO: save the source_strings so i dont have to iterate through
        the source_submission json.

        endpoint: api/v2/doc_mapping/?document=66
        '''

        source_dp_json = SourceSubmission.objects.filter(
            document_id = self.document_id).values_list('submission_json')

        if len(source_dp_json) == 0:
            return

        all_codes = [('indicator',k) for k,v in json.loads(source_dp_json[0][0]).iteritems()]
        rg_codes, cp_codes = [],[]

        for row in source_dp_json:
            row_dict = json.loads(row[0])
            rg_codes.append(row_dict[self.doc_deets['region_column']])
            cp_codes.append(row_dict[self.doc_deets['campaign_column']])

        for r in list(set(rg_codes)):
            all_codes.append(('region',r))

        for c in list(set(cp_codes)):
            all_codes.append(('campaign',c))

        for content_type, source_object_code in all_codes:
            self.source_submission_meta_upsert(content_type, source_object_code)

    def source_submission_meta_upsert(self, content_type, source_object_code):
        '''
        Create new metadata if not exists
        Add a record tying this document to the newly inserted metadata
        '''

        sm_obj, created = SourceObjectMap.objects.get_or_create(\
            content_type = content_type\
           ,source_object_code = source_object_code\
           ,defaults = {
            'master_object_id':-1,
            'mapped_by_id':self.user_id
            })

        sm_obj, created = DocumentSourceObjectMap.objects.get_or_create\
            (document_id = self.document_id,source_object_map_id = sm_obj.id)

        return sm_obj.id


    def process_source_submission(self, submission, i):

        submission_data = dict(zip(self.file_header, \
            submission.split(self.file_delimiter)))

        instance_guid = submission_data[self.doc_deets['uq_id_column']]

        if instance_guid == '':
            return None, None

        submission_dict = {
            'submission_json': submission_data,
            'document_id': self.document_id,
            'row_number': i,
            'instance_guid': submission_data[self.doc_deets['uq_id_column']],
            'process_status': 'TO_PROCESS',
        }
        return submission_dict, instance_guid
