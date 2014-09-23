import xlrd, csv, pandas, pprint as pp

from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.db import IntegrityError
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from datapoints.mixins import PermissionRequiredMixin


from pandas.io.excel import read_excel

from source_data.forms import *
from source_data.models import *
from source_data.etl_tasks.ingest_document import DocIngest
from datapoints.models import Source


def file_upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.created_by = request.user
            newdoc.save()
            document_id = newdoc.id

            file_path = newdoc.docfile.url

            if file_path.endswith('xls') or file_path.endswith('xlsx'):

                ## FIND MAPPINGS ##
                mappings = pre_process_xls(file_path,newdoc.id)

                ## MOVE XLS INTO DATAPOINTS TABLE ##
                d = DocIngest(document_id,mappings)
                # process_sheet_df(df,document_id,mappings)

                return document_review(request,newdoc.id,mappings)

            else:
                messages.add_message(request, messages.INFO, 'Please\
                    upload either .CSV, .XLS or .XLSX file format')

    else:
        form = DocumentForm()

    return render_to_response(
        'upload/file_upload.html',
        {'form': form},
        context_instance=RequestContext(request)
    )



def pre_process_xls(f_path,document_id):
    ''' in this method we create or find the source metadata and return the
    values as a dictionary.'''

    wb = xlrd.open_workbook(f_path)

    for sheet in wb.sheets():
        # process_sheet(sheet)

        if sheet.nrows == 0:
            pass
        else:
            mappings = pre_process_sheet(f_path,sheet.name,document_id)
            return mappings


def pre_process_sheet(file_path,sheet_name,document_id):

    sheet_df = read_excel(file_path,sheet_name)
    cols = [col.lower() for col in sheet_df]


    all_meta_mappings = {}
    source_id = Source.objects.get(source_name ='Spreadsheet Upload').id

    all_meta_mappings['campaigns'] = map_campaigns(sheet_df,source_id)
    all_meta_mappings['indicators'] = map_indicators(sheet_df,source_id)
    all_meta_mappings['regions'] = map_regions(sheet_df,source_id)

    return all_meta_mappings


def map_indicators(sheet_df,source_id):
    indicator_mapping = {}
    cols = [col.lower() for col in sheet_df]

    for col_name in cols:

        source_indicator, created = SourceIndicator.objects.get_or_create(
            source_id = source_id,
            indicator_string = col_name
        )

        try:
            indicator_id = IndicatorMap.objects.get(source_indicator_id = source_indicator.id).master_indicator_id
            indicator_mapping[col_name] = indicator_id
            source_indicator.mapped_status='MAPPED'
        except ObjectDoesNotExist:
            indicator_mapping[col_name] = None

    return indicator_mapping


def map_campaigns(sheet_df,source_id):

    ## CAMPAIGN MAPPING ##
    campaign_mapping = {}
    campaigns = sheet_df.groupby('DateSoc')

    for campaign in campaigns:
        print campaign[0]

        source_campaign, created = SourceCampaign.objects.get_or_create(
            source_id = source_id,
            campaign_string = campaign[0]
        )
        try:
            campaign_id = CampaignMap.objects.get(source_campaign_id = source_campaign.id).master_campaign_id
            campaign_mapping[campaign[0]] = campaign_id
        except ObjectDoesNotExist:
            campaign_mapping[source_campaign] = None

    return campaign_mapping

def map_regions(df,source_id):
    ## REGION MAPPING ##
    region_mapping = {}

    # df['region_string'] = df['Lga'] + '-' + df['State'] + df['Ward']
    df['region_string'] = df['Lga'] + '-' + df['State'] + df['Ward'] + '-' + str(df['Settlement'])

    regions = df.groupby('region_string')

    for region in regions:
        print 'THIS IS A REGION: ' + region[0]

        source_region_id, created = SourceRegion.objects.get_or_create(
            source_id = source_id,
            region_string = region[0]
        )

        try:
            region_id = RegionMap.objects.get(source_region_id = source_region_id.id)
            region_mapping[region[0]] = region_id
        except ObjectDoesNotExist:
            region_mapping[region[0]] = None

    return region_mapping

def document_review(request,document_id,mappings):

    doc_data = []

    r =  {'problem':'Indicators to Map','recs':len(mappings['indicators']),'model':'indicator'}
    r2 = {'problem':'Campaigns to Map','recs':len(mappings['campaigns']),'model':'campaign'}
    r3 = {'problem':'Regions To Map','recs':len(mappings['regions']),'model':'region'}

    doc_data.append(r)
    doc_data.append(r2)
    doc_data.append(r3)


    return render_to_response(
        'upload/document_review.html',
        {'doc_data': doc_data},
        context_instance=RequestContext(request),
    )


######### META MAPPING ##########


class CreateMap(PermissionRequiredMixin, generic.CreateView):

    template_name='map/map.html'
    success_url=reverse_lazy('datapoints:datapoint_index')
    # permission_required = 'datapoints.add_datapoint'

    def form_valid(self, form):
    # this inserts into the changed_by field with  the user who made the insert
        obj = form.save(commit=False)
        obj.mapped_by = self.request.user
        # obj.source_id = Source.objects.get(source_name='data entry').id
        obj.save()
        return HttpResponseRedirect(self.success_url)


class IndicatorMapCreateView(CreateMap):

    model=IndicatorMap
    form_class = IndicatorMapForm
    context_object_name = 'indicator_to_map'
    template_name = 'map/map.html'
    success_url=reverse_lazy('source_data:to_map')



    def get_initial(self):
        return { 'source_indicator': self.kwargs['pk'] }



class RegionMapCreateView(CreateMap):

    model=RegionMap
    form_class = RegionMapForm


class CampaignMapCreateView(CreateMap):

    model=CampaignMap
    form_class = CampaignMapForm


class ToMap(generic.ListView):

    model = SourceIndicator
    template_name = 'map/to_map.html'
    context_object_name = 'items'

    def get_queryset(self):

        return SourceIndicator.objects.filter(indicatormap__isnull=True)



class ShowSourceIndicator(generic.DetailView):

    context_object_name = "source_indicator"
    template_name = 'map/source_indicator.html'
    model = SourceIndicator
