'use strict';

var _      = require('lodash');
var React  = require('react');
var moment = require('moment');

var Impact             = require('dashboard/management/Impact.jsx');
var Performance        = require('dashboard/management/Performance.jsx');
var Access             = require('dashboard/management/Access.jsx');
var BulletChartSection = require('./BulletChartSection.jsx');

var ManagementDashboard = React.createClass({
  propTypes : {
    dashboard  : React.PropTypes.object.isRequired,
    indicators : React.PropTypes.object.isRequired,

    campaign   : React.PropTypes.object,
    data       : React.PropTypes.array,
    loading    : React.PropTypes.bool,
    region     : React.PropTypes.object,
  },

  getDefaultProps : function () {
    return {
      data    : [],
      loading : true
    };
  },

  render : function () {
    var loading    = this.props.loading;
    var region     = _.get(this.props, 'region.name', '');
    var campaign   = this.props.campaign;
    var indicators = this.props.indicators;

    // Data index by section
    var data = {};

    // Indicator index: maps indicator IDs to one or more sections containing
    var sections = _(this.props.dashboard.charts)
      .groupBy('section')
      .transform(function (result, charts, section) {
        result[section] = _(charts)
          .pluck('indicators')
          .flatten()
          .map(_.propertyOf(indicators))
          .value();
      })
      .value();

    // Parcel out the datapoints into the correct sections based on their
    // indicator IDs
    _.each(this.props.data, function (d) {
      _(sections)
        .pick(sec => _(sec).pluck('id').includes(d.indicator.id))
        .keys()
        .each(function (s) {
          var arr = _.get(data, s, []);

          arr.push(d);
          data[s] = arr;
        })
        .value();
    });

    return (
      <div id='management-dashboard'>
        <div className='row print-only'>
          <div className='small-12 columns'>
            <h1>
              <span className='campaign'>{ campaign }</span>
              <span className='region'>{ region }</span>
            </h1>
            <h2>
              Polio<br />
              Performance<br />
              Dashboard
            </h2>
            <img src='/static/img/UNICEF.svg' className='logo'/>
          </div>
        </div>

        <div className='row'>
          <Impact data={data.impact} campaign={this.props.campaign} loading={loading} />
          <Performance data={data.performance} loading={loading} />
        </div>

        <div className='row'>
          <section className='medium-2 columns'>
            <h3>FLWs' Capacity to Perform</h3>
            <BulletChartSection data={data.capacity} campaign={campaign} indicators={sections.capacity} loading={loading} cols={2} />
          </section>

          <div className='medium-1 column'>
            <h3>Supply</h3>
            <BulletChartSection data={data.supply} campaign={campaign} indicators={sections.supply} loading={loading} cols={1} />
          </div>

          <div className='medium-1 column'>
            <h3>Polio+</h3>
            <BulletChartSection data={data.polio} campaign={campaign} indicators={sections.polio} loading={loading} cols={1} />
          </div>

          <div className='medium-1 column'>
            <h3>Resources</h3>
            <BulletChartSection data={data.resources} campaign={campaign} indicators={sections.resources} loading={loading} cols={1} />
          </div>

          <Access data={data.access} campaign={campaign} indicators={indicators} loading={loading} />
        </div>

      </div>
    );
  },

  _fetch : function (campaign, region) {
    var dt = moment(campaign.end_date, 'YYYY-MM-DD');
    var promises = [];

    // Polio cases
    promises.push(api.datapoints({
      indicator__in  : INDICATORS.cases,
      region__in     : region.id,
      campaign_start : dt.clone().startOf('year').subtract(2, 'years').format('YYYY-MM-DD'),
      campaign_end   : campaign.end
    }));

    promises.push(api.datapoints({
      indicator__in  : INDICATORS.immunityGap,
      region__in     : region.id,
      campaign_start : dt.clone().startOf('quarter').subtract(3, 'years').format('YYYY-MM-DD'),
      campaign_end   : campaign.end
    }));

    promises.push(api.datapoints({
      indicator__in: _(INDICATORS)
        .pick('inaccessibility', 'accessPlans', 'transitPoints', 'microplans', 'totalMissed')
        .values()
        .flatten()
        .value(),
      region__in     : region.id,
      campaign_start : campaign.start,
      campaign_end   : campaign.end
    }));

    promises.push(api.datapoints({
      indicator__in : _(INDICATORS)
        .pick('missed', 'conversions', 'inaccessible')
        .values()
        .flatten()
        .value(),
      region__in     : region.id,
      campaign_start : dt.clone().startOf('month').subtract(1, 'year').format('YYYY-MM-DD'),
      campaign_end   : campaign.end
    }));

    promises.push(api.datapoints({
      indicator__in     : INDICATORS.totalMissed,
      parent_region__in : region.id,
      campaign_start    : campaign.start,
      campaign_end      : campaign.end
    }));

    promises.push(api.datapoints({
      indicator__in : _(INDICATORS)
        .pick('capacity', 'polio', 'supply', 'resources')
        .values()
        .flatten()
        .value(),
      region__in     : region.id,
      campaign_start : dt.clone().subtract(4, 'months').format('YYYY-MM-DD'),
      campaign_end   : campaign.end
    }));

    Promise.all(promises).then(this._loadData);

    this.setState({ loading : true });
  },

  _loadData : function (responses) {
    var data = _(responses)
      .pluck('objects')
      .flatten()
      .map(function (o) {
        // Convert one object with an indicators array into an array of objects
        // each with a single indicator
        var base = _.omit(o, 'indicators');

        return _.map(o.indicators, function (d) {
          return _.assign({}, base, {
            indicator : d.indicator,
            value     : d.value
          });
        });
      })
      .flatten()
      .value();

    this.setState({
      data    : data,
      loading : false
    });
  }
});

module.exports = ManagementDashboard;
