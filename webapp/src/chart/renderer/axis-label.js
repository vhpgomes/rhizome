import d3 from 'd3'

function wrap (text, width) {
  text.each(function () {
    let text = d3.select(this)
    let words = text.text().split('').reverse()
    let word
    let line = []
    let sumLineNumber = (words && words.length) ? words.length : 0
    let lineNumber = 1
    let lineHeight = 1.1
    let tspan = text.text(null).append('tspan')
    while (words.length > 0) {
      word = words.pop()
      line.push(word)
      tspan.text(line.join(' '))
      if (tspan.node().getComputedTextLength() > width) {
        line.pop()
        tspan.text(line.join(' '))
        line = [word]
        var currentLineHeight = words.length === sumLineNumber - 1 ? -Math.ceil(sumLineNumber / 2, -1) : 1
        tspan = text.append('tspan')
          .attr({
            'x': 0,
            'dy': (currentLineHeight * lineNumber * lineHeight) + 'rem'
          })
          .text(word)
      }
    }
  })
}

function axisLabel (chartOptions) {
  var _width = 1
  var _height = 1
  var _fontSize = 14
  var _xLabel, _yLabel
  var _textLength = 5

  function chart (selection) {
    if (_xLabel) {
      var xAxisLabel = selection.select('.x.axis').selectAll('.label').data(_xLabel)
        .enter().append('g')
        .attr({
          'class': 'label',
          'transform': 'translate(' + (_width / 2) + ', ' + (0.1 * _height) + ')'
        })
        .style({
          'font-size': _fontSize
        })

      xAxisLabel.append('text').text(d => { return d })
    }

    if (_yLabel) {
      var yAxisLabel = selection.select('.y.axis').selectAll('.label').data(_yLabel)
        .enter().append('g')
        .attr({
          'class': 'label',
          'transform': 'translate(' + (-0.02 * _width) + ', ' + (_height / 2) + ')'
        })
        .style({
          'font-size': _fontSize
        })

      yAxisLabel.append('text').text(d => { return d })
        .call(wrap, _textLength, 0, 0)
    }
  }

  chart.fontSize = function (value) {
    if (!arguments.length) {
      return _fontSize
    }

    _fontSize = value
    return chart
  }

  chart.width = function (value) {
    if (!arguments.length) {
      return _width
    }

    _width = value
    return chart
  }

  chart.height = function (value) {
    if (!arguments.length) {
      return _height
    }

    _height = value
    return chart
  }

  chart.fontSize = function (value) {
    if (!arguments.length) {
      return _fontSize
    }

    _fontSize = value
    return chart
  }

  chart.data = function (xValue, yValue) {
    if (!arguments.length) {
      return _xLabel
    }

    _xLabel = xValue ? [xValue] : null
    _yLabel = yValue ? [yValue] : null
    return chart
  }

  return chart
}

export default axisLabel
