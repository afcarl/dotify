import React from 'react'
import Select from '../../Select'
import Operator from './Operator'

var $ = require('jquery');

var OperatorSelect = React.createClass({

  placeholder: "+",
  source: "/operators",

  getInitialState: function () {
    return {
      dropdownElements: []
    };
  },
  componentDidMount: function() {
    this.serverRequest = $.get(this.source, function (response) {
      this.setState({
        dropdownElements: response['operators'].map(function(operator) {
          return <Operator id={operator.id} name={operator.name} value={operator.value}/>;
        })
      });
    }.bind(this));
  },
  componentWillUnmount: function() {
    this.serverRequest.abort();
  },
  render: function () {
    return (
      <div className="operator-select">
        <Select dropdownElements={this.state.dropdownElements} flexOrder={this.props.flexOrder} handleValidDropdownElement={this.props.handleValidDropdownElement} placeholder={this.placeholder}/>
      </div>
    );
  }
});

module.exports = OperatorSelect;
