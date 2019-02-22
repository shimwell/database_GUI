// run this app with npm start

import React, { Component } from "react";
//import { render } from "react-dom";
//import logo from './logo.svg';

import "./App.css";

import "bootstrap/dist/css/bootstrap.min.css";

import Select from "react-select";

import Plot from "react-plotly.js";

import ReactTable from "react-table";
import "react-table/react-table.css";
//import checkboxHOC from "react-table/lib/hoc/selectTable";

//import {Grid, Row, Col} from 'react-bootstrap';
import { Container, Row, Col } from "reactstrap";

const REST_API_EXAMPLE_URL = `http://127.0.0.1:5000`;






function LabelsForDropdowns(props){
  const filter_data = props.filter_data;

  return  (
    <div>
      {
        filter_data.map((x, i) => {
          const field_values = x["field"][0];

          return <div key={i} className="filter_labels">{field_values}:</div>;
        })
      }
      <br />
      <div className="filter_labels">Select X axis:</div>
      <div className="filter_labels">Select Y axis:</div>
    </div>
  );
}


function FilterDropdowns(props){
  const filter_data = props.filter_data;
  return (
    <div>
    {filter_data.map((x, i) => {
    const meta_data_dropdown_dict = [];
    const list_of_dropdown_values = x["distinct_values"];
    const field_values = x["field"][0];

    meta_data_dropdown_dict.push({
      value: {
        field: field_values,
        value: '',
      },
      label: ''
    });

    for (var j = 0; j < list_of_dropdown_values.length; j++) {
      meta_data_dropdown_dict.push({
        value: {
          field: field_values,
          value: list_of_dropdown_values[j]
        },
        label: list_of_dropdown_values[j]
      });
    }

    return (
      <Select
        key ={i}
        options={meta_data_dropdown_dict}
        //placeholder={field_values}
        name={field_values}
        //isClearable={true}
        onChange={props.event_handler}
        className="meta_data_dropdown"
      />
    );
  })}
  </div>)
}

function AxisDropdowns(props){
  return (
              <Select
                options={props.axis_data}
                //placeholder={props.placeholder}
                isClearable={false}
                onChange={props.event_handler}
                className="axis_data_dropdown"
              />
 )
}

function PlotlyGraph(props){
  console.log('props.plotted_data',props.plotted_data)
  console.log('props.plotted_data.length',props.plotted_data.length)
  const list_of_data_dictionaries=[]
  if (props.plotted_data === {} || props.x_axis_values_list === "" || props.y_axis_values_list === ""){
    console.log()
    list_of_data_dictionaries.push({'x':[],
                                    'y':[],
                                    'type': "scatter",
                                    'mode': "lines+points"
                                  })
  }else{
     for (var key in props.plotted_data) {

     //for (var i = 0; i < props.plotted_data.length; i++) {
       // console.log('i=',i)
       //
       // console.log( 'key x=',props.x_axis_label)
       // console.log( 'key y=',props.y_axis_label)
       //
       // console.log( 'y=',props.plotted_data)
       list_of_data_dictionaries.push({'x': props.plotted_data[key][props.x_axis_label],
                                      'y': props.plotted_data[key][props.y_axis_label],
                                      'type': "scatter",
                                      'mode': "lines+points",
                                      'name':props.plotted_data[key]['filename']
                                    })
     }
  }

  return (
  <Plot
    data={list_of_data_dictionaries}
    layout={{
      xaxis: { title: props.x_axis_label },
      yaxis: { title: props.y_axis_label },
      margin: {
        r: 0,
        t: 0,
        pad: 1
      },
      legend:{
        x:0,
        y:1,
      }
    }}
  />
  )
}

class App extends Component {
  html;
  constructor(props) {
    super(props);

    this.state = {
      filter_data: [],
      axis_data: [],
      //query:{'filename':'sdf.csv','uploader':}
      query: {},
      query_result: [],
      plotted_data: {},
      x_axis_label: "",
      y_axis_label: "",
      columns: [],
      data: [],

      selected: {},


    };

    this.handle_y_axis_data_dropdown_change_function = this.handle_y_axis_data_dropdown_change_function.bind(this);
    this.handle_x_axis_data_dropdown_change_function = this.handle_x_axis_data_dropdown_change_function.bind(this);

    this.handle_meta_data_dropdown_change_function = this.handle_meta_data_dropdown_change_function.bind(this);

    this.toggleRow = this.toggleRow.bind(this);
  }


  handle_meta_data_dropdown_change_function(optionSelected) {
    console.log("new metadata field selected", optionSelected.value);

    console.log("new metadata field selected", optionSelected.placeholder);
    let queryCopy = JSON.parse(JSON.stringify(this.state.query));
    console.log(queryCopy);

    if (optionSelected.value["value"] === ''){
      delete queryCopy[optionSelected.value["field"]];
      console.log('deleting field from query', optionSelected.value["field"])
    }else{
    queryCopy[optionSelected.value["field"]] = optionSelected.value["value"];
  }// console.log(queryCopy)

    this.setState({ query: queryCopy }, () => {
      console.log("state =", this.state);
      console.log("JSON.stringify(this.state.query)=",JSON.stringify(this.state.query));
      console.log(REST_API_EXAMPLE_URL + "/get_matching_entrys?query=" + JSON.stringify(this.state.query));
      fetch(REST_API_EXAMPLE_URL + "/get_matching_entrys?query=" + JSON.stringify(this.state.query))
        .then(result => {
          if (result.ok) {
            return result.json();
          }
        })
        .then(data => {
          this.setState({ query_result: data });
          console.log("state =", this.state);
        })
        .catch(err => {
          console.log(
            "Cannot connect to server "+REST_API_EXAMPLE_URL+"get_matching_entrys?query=" +
              JSON.stringify(this.state.query)
          );
        });
    });

    console.log("current query", this.state.query);
  }

  handle_x_axis_data_dropdown_change_function(optionSelected) {
    const value = optionSelected.value;

    console.log("new x axis field selected", value);

    this.setState({ x_axis_label: value }, () => {
      console.log("new X axis label state", this.state.x_axis_label);
    });
  }

  handle_y_axis_data_dropdown_change_function(optionSelected) {
    const value = optionSelected.value;

    console.log("new y axis field selected", value);

    this.setState({ y_axis_label: value }, () => {
      console.log("new Y axis label state", this.state.y_axis_label);
    });
  }

  toggleRow(filename) {
		const newSelected = Object.assign({}, this.state.selected);
		newSelected[filename] = !this.state.selected[filename];
		console.log('check box clicked',filename, 'state=',newSelected[filename])
		this.setState({
			selected: newSelected,
		});





    let plotted_dataCopy = JSON.parse(JSON.stringify(this.state.plotted_data));
    if (newSelected[filename]===true){
      console.log('looking for filename in query data')
      for (var i = 0; i < this.state.query_result.length; i++) {
        console.log(this.state.query_result[i]['filename'],filename)
        if (this.state.query_result[i]['filename'] === filename){
            console.log('found filename in query data')
            plotted_dataCopy[filename] = this.state.query_result[i]
        }
      }
    }else{
      delete plotted_dataCopy[filename];
    }

    console.log('plotted_dataCopy',plotted_dataCopy)
    this.setState({ plotted_data: plotted_dataCopy }, () => {console.log(this.state.plotted_data)})






	}

  componentDidMount() {
    fetch(REST_API_EXAMPLE_URL + "/find_meta_data_fields_and_distinct_entries")
      .then(result => {
        if (result.ok) {
          return result.json();
        }
      })
      .then(data => {
        this.setState({ filter_data: data });
      })
      .catch(err => {
        console.log(
          "Cannot connect to server find_meta_data_fields_and_distinct_entries"
        );
      });

    fetch(REST_API_EXAMPLE_URL + "/find_axis_data_fields")
      .then(result => {
        if (result.ok) {
          return result.json();
        }
      })
      .then(data => {
        const axis_data = [];
        for (var i = 0; i < data.length; i++) {
          axis_data.push({
            value: data[i],
            label: data[i]
          });
        }
        this.setState({ axis_data: axis_data });
      })
      .catch(err => {
        console.log("Cannot connect to server find_axis_data_fields");
      });
  }



  render() {
    console.log("filter data", this.state.filter_data);
    console.log("axis_data", this.state.axis_data);

    const filter_data = this.state.filter_data;
    const axis_data = this.state.axis_data;



    const results_of_db_query = this.state.query_result;



    const data = results_of_db_query;
    const table_key = []
    for (var j = 0; j < data.length; j++) {
      table_key.push(data[j]['_id']['$oid'])
    }
    console.log('table_key',table_key)

    console.log("this.state.query_result",this.state.query_result)

    console.log("selected",this.state.selected)

    const columns = [
      {
        id: "checkbox",
        accessor: "",
        Cell: ({ original }) => {
          return (
            <input
              type="checkbox"
              className="checkbox"
              checked={this.state.selected[original.filename] === true}
              onChange={() => this.toggleRow(original.filename)}
            />
          );
        },
        sortable: false,
        width: 45
      },
    ];



      filter_data.map((x, i) => {
        columns.push({ Header: x["field"][0],
                       accessor: x["field"][0] });
      });



    return (
      <div className="App">
        <Container>
          <Row>
            <Col>
              <h1 className="heading">Materials database</h1>
            </Col>
          </Row>
          <Row>
            <Col md="2" lg="2">
              <LabelsForDropdowns filter_data={filter_data}/>
            </Col>
            <Col md="3" lg="3">
              <FilterDropdowns filter_data={filter_data} event_handler={this.handle_meta_data_dropdown_change_function}/>

              <br/>
              <AxisDropdowns placeholder="Select x axis" axis_data={axis_data} event_handler={this.handle_x_axis_data_dropdown_change_function}/>
              <AxisDropdowns placeholder="Select y axis" axis_data={axis_data}  event_handler={this.handle_y_axis_data_dropdown_change_function}/>

            </Col>
            <Col md="7" lg="7">

              <PlotlyGraph plotted_data={this.state.plotted_data} x_axis_label={this.state.x_axis_label} y_axis_label={this.state.y_axis_label} />
            </Col>
          </Row>

          <Row>
            <Col md="12" lg="12">
              <div>

                <ReactTable
                  key = {table_key}
                  data={data}
                  columns={columns}
                  showPagination={false}
                  defaultPageSize={8}
                />
              </div>
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}

export default App;
