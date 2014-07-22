from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.template import RequestContext

from datapoints.models import DataPoint,Region,Indicator,Document
from datapoints.forms import * #RegionForm,IndicatorForm,DataPointForm,DocumentForm,DataPointSearchForm


class IndexView(generic.ListView):
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.order_by('-created_at')[:10]


class DetailView(generic.DetailView):
    pass # template name and model passed via the URL.

class CreateView(generic.CreateView):
    pass # template name and model passed via the URL.

class UpdateView(generic.UpdateView):
    pass # template name and model passed via the URL.

class DeleteView(generic.DeleteView):
    pass # template name and model passed via the URL.


class DataPointCreateView(CreateView):
    model=DataPoint
    success_url="/datapoints"
    template_name='datapoints/create.html'
    form_class = DataPointForm

    def form_valid(self, form):
    # this inserts into the changed_by field with  the user who made the insert
        obj = form.save(commit=False)
        obj.changed_by = self.request.user
        obj.save()
        return HttpResponseRedirect(self.success_url)

class DataPointUpdateView(generic.UpdateView):
    model=DataPoint
    success_url="/datapoints"
    template_name='datapoints/update.html'
    form_class = DataPointForm

    def form_valid(self, form):
    # this sets the changed_by field to the user who made the update
        obj = form.save(commit=False)
        obj.changed_by = self.request.user
        obj.save()
        return HttpResponseRedirect(self.success_url)

def search(request):
    if request.method =='POST':
      ## THIS IS UGLY ##
      kwargs = {}
      if request.POST['indicator'] != u'':
          kwargs.update({'indicator': request.POST['indicator']})
      if request.POST['region'] != u'':
          kwargs.update({'region': request.POST['region']})
      if request.POST['changed_by'] != u'':
          kwargs.update({'changed_by': request.POST['changed_by']})
      if request.POST['reporting_period'] != u'':
          kwargs.update({'reporting_period': request.POST['reporting_period']})

      results = DataPoint.objects.filter(**kwargs)

      return render_to_response('datapoints/index.html',
        {'top_datapoints':results},
        context_instance=RequestContext(request))

    else:
      return render_to_response('datapoints/search.html',
        {'form':DataPointSearchForm},
        context_instance=RequestContext(request))


class DashBoardView(generic.ListView):

    def get_queryset(self):
        cursor = connection.cursor()

        raw_sql = '''
        SELECT
             i.indicator_pct_display_name
            , d.value / d2.value as pct
            , r.full_name
        FROM datapoint d
        INNER JOIN indicator_pct i
            ON d.indicator_id = i.indicator_part_id
        INNER JOIN datapoint d2
            ON i.indicator_whole_id = d2.indicator_id
            AND d.reporting_period_id = d2.reporting_period_id
            AND d.region_id = d2.region_id
        INNER JOIN region r
            ON d.region_id = r.id

        UNION ALL

        SELECT
            i.name
            , SUM(d.value) as value
            , r.full_name
        FROM region_relationship rr
        INNER JOIN datapoint d
            ON rr.region_1_id = d.region_id
        INNER JOIN indicator i
            ON d.indicator_id = i.id
        INNER JOIN region r
            ON rr.region_0_id = r.id
        GROUP BY r.full_name, i.name,i.id ,d.reporting_period_id

        '''

        ## this should show in red if the COUNT is less than the total
        ## number of regions that exist for that relationshiop


        cursor.execute(raw_sql)
        rows = cursor.fetchall()

        return rows


def file_upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'datapoints/file_upload.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
