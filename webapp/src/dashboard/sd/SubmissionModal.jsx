import _ from 'lodash'
import React from 'react'
import Modal from 'react-modal'

import SubmissionModalStore from 'stores/SubmissionModalStore'

var appElement = document.getElementById('main')
Modal.setAppElement(appElement)
Modal.injectCSS()

var SubmissionModal = React.createClass({
  propTypes: {
    source_submission_id: React.PropTypes.number.isRequired
  },

  getInitialState: function () {
    return {
      modalIsOpen: false,
      source_submission_id: null,
      submission_data: null
    }
  },

  openModal: function () {
    SubmissionModalStore.getSubmission({id: this.props.source_submission_id}).then(data => {
      this.setState({submission_data: data, modalIsOpen: true})
    })
  },

  closeModal: function () {
    this.setState({modalIsOpen: false})
  },

  render: function () {
    var source_submission_id = this.props.source_submission_id
    var modalStyle = {width: '450', height: '75%', marginLeft: '20%'}

    var submission_data = []
    if (this.state.modalIsOpen &&
      this.state.submission_data !== null &&
      this.state.submission_data.submission_json !== null
    ) {
      var submission_json = this.state.submission_data.submission_json
      _.forIn(submission_json, function (value, key) {
        submission_data.push(<li><b>{key}</b> : {value} </li>)
      })
    }

    return (
      <div>
        <button
          className='tiny'
          onClick={this.openModal} >
          view raw data!
        </button>
        <Modal
          style={modalStyle}
          isOpen={this.state.modalIsOpen}
          onRequestClose={this.closeModal} >
          <h1> Source_submission_id: {source_submission_id} </h1>
          {submission_data}
        </Modal>
      </div>
    )
  }
})

export default SubmissionModal
