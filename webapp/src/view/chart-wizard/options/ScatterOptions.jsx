import React from 'react'

import IndicatorDropdownMenu from 'component/IndicatorDropdownMenu.jsx'
import RadioGroup from 'component/radio-group/RadioGroup.jsx'
import ScatterAxisChooser from '../ScatterAxisChooser.jsx'

import ChartWizardActions from 'actions/ChartWizardActions'
import builderDefinitions from 'stores/chartBuilder/builderDefinitions'

export default class ScatterOptions extends React.Component {
  constructor (props) {
    super(props)
  }

  static propTypes = {
    indicatorList: React.PropTypes.array,
    indicatorSelected: React.PropTypes.array,
    groupByValue: React.PropTypes.number,
    locationLevelValue: React.PropTypes.number,
    xFormatValue: React.PropTypes.number,
    yFormatValue: React.PropTypes.number
  }

  static defaultProps = {
    indicatorList: [],
    indicatorSelected: [],
    groupByValue: 0,
    locationLevelValue: 0,
    xFormatValue: 0,
    yFormatValue: 0
  }

  render () {
    return (
      <div className='chart-wizard__options chart-wizard__options--general'>
        <p className='chart-wizard__para'>You may choose additional indicators now.</p>
        <h4>X Axis</h4>
        <ul className='list'>
          <li>{this.props.indicatorSelected[0] && this.props.indicatorSelected[0].name}</li>
        </ul>
        <h4>Y Axis</h4>
        <IndicatorDropdownMenu
          text={this.props.indicatorSelected[1] ? this.props.indicatorSelected[1].name : 'Add Indicators'}
          icon='fa-plus'
          indicators={this.props.indicatorList}
          sendValue={ChartWizardActions.changeYAxis} />

        <p className='chart-wizard__para'>You may also change additional chart settings.</p>
        <RadioGroup name='location-level' title='Location Level: '
          value={this.props.locationLevelValue}
          values={builderDefinitions.locationLevels}
          onChange={ChartWizardActions.changeLocationLevelRadio} />
        <ScatterAxisChooser xFormatValue={this.props.xFormatValue}
          onXFormatChange={ChartWizardActions.changeXFormatRadio}
          yFormatValue={this.props.yFormatValue}
          onYFormatChange={ChartWizardActions.changeYFormatRadio}
          formatValues={builderDefinitions.formats}
        />
      </div>
    )
  }
}
