'use strict'

var d3 = require('d3')
var moment = require('moment')

function general (value) {
  var mantissa = Math.abs(value) - Math.floor(Math.abs(value))
  var fmt = d3.format(mantissa > 0 ? '.4f' : 'n')

  return fmt(value)
}

function timeAxis (value) {
  var m = moment(value)

  if (m.month() === 0) {
    return m.format('YYYY')
  }

  return m.format('MMM')
}

module.exports = {
  general: general,
  timeAxis: timeAxis
}
