'use strict';

var _     = require('lodash');
var d3    = require('d3');
var React = require('react');

var dom     = require('util/dom');
var palette = require('util/colorbrewer');
var util    = require('util/data');

module.exports = React.createClass({
	getDefaultProps : function () {
		return {
			getId         : function (d, i) { return d.id || i;},
			getHeaderText : _.identity,
			getSeriesName : function (s) { return s.name; },
			getValue      : function (d) { return d.value; },
			getValues     : function (s) { return s.values; },
			headers       : [],
			margin        : {
				left   : 120,
				top    : 120,
				right  : 0,
				bottom : 0
			},
			scale         : d3.scale.quantile().domain([0, 1]).range(palette.YlOrRd[9]),
			series        : [],
			sortable      : true
		};
	},

	getInitialState : function () {
		return {
			height  : 1024,
			sortCol : null,
			width   : 1024
		};
	},

	componentDidMount : function () {
		this._draw(this.props, this.state);
	},

	componentWillReceiveProps : function (nextProps) {
		this._draw(nextProps, this.state);
	},

	shouldComponentUpdate : _.constant(false),

	render : function () {
		var className = 'heatmap';

		if (this.props.sortable) {
			className += ' sortable';
		}

		return (
			<div className="chart">
				<svg className={className} ref="svg"
					viewBox={'0 0 ' + this.state.width + ' ' + this.state.height}>

					<g transform={'translate(' + this.props.margin.left + ',' + this.props.margin.top + ')'}>
						<g className="y axis" transform="translate(0,-4)"></g>
						<g className="x axis" transform="translate(-4,0)"></g>
						<g className="data" onMouseOut={this._onRowOut}></g>
					</g>
				</svg>
			</div>
		);
	},

	_draw : function (props, state) {
		var self    = this;

		// Calculate the dimensions for the heatmap based on the width of its
		// containing element
		// var contentArea = dom.contentArea(React.findDOMNode(this).parentElement);
		var width  = state.width - props.margin.left - props.margin.right;
		var height = state.height - props.margin.top - props.margin.bottom;

		var fill = function (d) {
			var v = props.getValue(d);

			return util.defined(v) ? props.scale(v) : 'transparent';
		};

		var xScale = d3.scale.ordinal()
			.domain(_.map(props.headers, props.getHeaderText))
			.rangeBands([0, width], .1);

		var x = function (d, i) {
			var xpos = xScale(props.getHeaderText(props.headers[i]));
			return xpos;
		};

		var getSortValue = function (s) {
			var val = state.sortCol == null ?
				props.getSeriesName(s) :
				props.getValues(s)[state.sortCol];

			if (_.isNull(val)) {
				val = Infinity;
			}

			return val;
		};

		var yScale = d3.scale.ordinal()
			.domain(_(props.series).sortBy(getSortValue).map(props.getSeriesName).value())
			.rangeBands([height, 0], .1);

		var y = _.flow(props.getSeriesName, yScale);

		var transform = function (d, i) {
			return 'translate(0,' + y(d) + ')';
		};

		var series = props.series;

		var svg = d3.select(React.findDOMNode(this.refs.svg));
		var row = svg.select('.data').selectAll('.row').data(series, props.getId);

		row.enter().append('g')
			.attr({
				'class'     : 'row',
				'transform' : transform,
			});

		row.exit()
			.transition().duration(300)
			.style('opacity', 0)
			.remove();

		row.on('mouseover', this._onRowHover)
			.transition().duration(750)
			.attr('transform', transform);

		// Add cells to each row
		var cell = row.selectAll('.cell').data(props.getValues, props.getId);

		cell.transition()
			.duration(500)
			.style('fill', fill)
			.attr({
				'height' : yScale.rangeBand(),
				'width'  : xScale.rangeBand(),
				'x'      : x
			});

		cell.enter().append('rect')
			.attr({
				'class'  : 'cell',
				'height' : yScale.rangeBand(),
				'x'      : x,
				'width'  : xScale.rangeBand(),
			})
			.style({
				'opacity' : 0,
				'fill'    : fill
			})
			.transition().duration(500)
			.style('opacity', 1);

		cell.exit()
			.transition().duration(300)
			.style('opacity', 0)
			.remove();

		cell.on('mouseover', function (d, i) {
				self._onMouseover(this, d, i);
			})
			.on('mouseout', function () {
				self._onMouseout(this);
			});

		svg.select('.x.axis')
			.transition().duration(300)
			.call(d3.svg.axis()
				.scale(xScale)
				.orient('top')
				.outerTickSize(0));

		svg.selectAll('.x.axis text')
				.style('text-anchor', 'start')
				.attr('transform', 'translate(' + (xScale.rangeBand() / 2) + ',0) rotate(-45)');

		svg.select('.y.axis')
			.transition().duration(300)
			.call(d3.svg.axis()
				.scale(yScale)
				.orient('left')
				.outerTickSize(0));
	},

	_onRowHover : function (d, row) {
		d3.select(React.findDOMNode(this.refs.svg)).selectAll('.row')
			.transition().duration(300)
			.style('opacity', function (d, i) {
				return i === row ? 1 : 0.4;
			});
	},

	_onRowOut : function () {
		d3.select(React.findDOMNode(this.refs.svg)).selectAll('.row')
			.transition().duration(300)
			.style('opacity', 1);
	},

	_onMouseover : function (el, d, i) {
		var p = d3.select(el.parentNode).datum();

		this.$dispatch('tooltip-show', {
			el   : el,
			data : {
				indicator : this.columnLabels[i],
				region    : p.name,
				template  : 'tooltip-heatmap',
				value     : d.value,
			}
		});
	},

	_onMouseout : function (el) {
		this.$dispatch('tooltip-hide', { el : el });
	},

	_setSort : function (d, i) {
		this.setState({sortCol : (i === this.sortCol) ? null : i});
	}

});
