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
import { Container, Row, Col, Button } from "reactstrap";

import Slider, { createSliderWithTooltip } from 'rc-slider';
import 'rc-slider/assets/index.css';
const style2 = {"white-space":"nowrap"}
const style = { width: 200, margin: 20 };


const marks = {
 '-3': 'micro',
  0: '',
  3: 'kilo',
  6: 'Mega',
  9: 'Giga',
};

const SliderWithTooltip = createSliderWithTooltip(Slider);

const REST_API_EXAMPLE_URL = "http://127.0.0.1:5000";

function QueryResulltsTable(props) {
  if (props.query_Results.length === 0) {
    return <br />;
  }

  const table_key = [];
  for (var j = 0; j < props.query_Results.length; j++) {
    table_key.push(props.query_Results[j]["_id"]["$oid"]);
  }
  console.log("table_key", table_key);
  console.log("props.data query tabe", props.data);
  return (
    <ReactTable
      key={table_key}
      data={props.data}
      columns={[{ Header: "Query results", columns: props.columns }]}
      showPagination={false}
      defaultPageSize={Math.max(3, props.query_Results.length)}
      loading={props.loading}
    />
  );
}

function PlottedResulltsTable(props) {
  if (Object.keys(props.query_Results).length === 0) {
    return <br />;
    console.log("no plotted data so no table");
  }

  const data = [];
  const table_key = [];
  console.log("props.data plotted table", props.data);
  Object.keys(props.data).forEach(function(key) {
    console.log("props.data", key, props.data[key]);
    data.push(props.data[key]);
    table_key.push(props.data[key]["_id"]["$oid"]);
  });

  console.log("props.data data.length", data.length);

  return (
    <ReactTable
      key={table_key}
      data={data}
      columns={[{ Header: "Plotted data", columns: props.columns }]}
      showPagination={false}
      defaultPageSize={data.length}
      loading={props.loading}
    />
  );
}

function LabelsForAxisDropdowns(props) {
  if (props.visible === false) {
    return <br />;
  } else {
    return (
      <div>
        <div className="filter_labels">Select X axis:</div>
        <div className="filter_labels">Select Y axis:</div>
      </div>
    );
  }
}

function LabelsForDropdowns(props) {
  const filter_data = props.filter_data;

  return (
    <div>
      {filter_data.map((x, i) => {
        const field_values = x["field"][0];

        return (
          <div key={i} className="filter_labels">
            {field_values}:
          </div>
        );
      })}
      <hr />
      <br />
    </div>
  );
}

function FilterDropdowns(props) {
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
            value: ""
          },
          label: ""
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
            key={i}
            options={meta_data_dropdown_dict}
            //placeholder={field_values}
            name={field_values}
            //isClearable={true}
            onChange={props.event_handler}
            className="meta_data_dropdown"
          />
        );
      })}
    </div>
  );
}

function AxisDropdowns(props) {
  if (props.visible === false) {
    return <br />;
  }
  var dropdown_id;
  if (props.axis_selection === "") {
    dropdown_id = "axis_data_dropdown_highlighted";
  } else {
    dropdown_id = "axis_data_dropdown";
  }
  return (
    <div id={dropdown_id}>
      <Select
        options={props.axis_data}
        //placeholder={props.placeholder}
        isClearable={false}
        onChange={props.event_handler}
        className="axis_data_dropdown"
        id={dropdown_id}
      />
    </div>
  );
}

function DownloadButton(props) {
  if (Object.keys(props.plotted_data).length === 0) {
    return (<br />)
  }

  var list_of_ids = [];
  Object.keys(props.plotted_data).map(function(key) {
    console.log("Key: ", { key }, "Value: ", props.plotted_data[key]["_id"]["$oid"]);
    list_of_ids.push(props.plotted_data[key]["_id"]["$oid"]);
  });
  var string_of_ids = list_of_ids.join("','");

  string_of_ids = "'" + string_of_ids + "'";

  console.log("string_of_ids", string_of_ids);

  return (
    <a href={REST_API_EXAMPLE_URL + "/download_py3?ids=" + string_of_ids} download="my_cross_sections.txt">
      {" "}
      <Button>Download data</Button>
    </a>
  )
}

function AxisScaleRadioButton(props) {


  if (
    Object.keys(props.plotted_data).length === 0 ||
    Object.keys(props.selected).length === 0 ||
    props.x_axis_label === undefined ||
    props.y_axis_label === undefined
  ) {
    console.log("nothing plotted");
    return <br />;
}
  return (
    <label>
      {props.title}
      <input type="radio" value={props.label} checked={props.event_handler === props.label} onChange={props.onChange} />
      {props.label} {"\u00A0"}
    </label>
  );
}

function ScaleSlider(props){
  if (
    Object.keys(props.plotted_data).length === 0 ||
    Object.keys(props.selected).length === 0 ||
    props.x_axis_label === undefined ||
    props.y_axis_label === undefined
  ) {
    console.log("nothing plotted");
    return <br />;
}

    return (
    <span style={style2}>
      X axis units <label style={style}>
    <SliderWithTooltip dots min={-3} max={9} marks={marks} step={1} tipFormatter={percentFormatter} onChange={props.onChange} defaultValue={0} />
    </label>
    </span>
    )
}


function PlotlyGraph(props) {
  console.log("props.plotted_data", props.plotted_data);
  console.log("props.selected", Object.keys(props.selected).length);
  console.log("props.plotted_data.length", Object.keys(props.plotted_data).length);
  console.log("props.x_axis_label", props.x_axis_label);
  console.log("props.y_axis_label", props.y_axis_label);
  console.log("props.x_axis_scale", props.x_axis_scale);
  console.log("props.y_axis_scale", props.y_axis_scale);
  console.log("props.x_axis_mutliplier", props.x_axis_mutliplier);
  console.log("props.y_axis_mutliplier", props.y_axis_mutliplier);
  const list_of_data_dictionaries = [];
  if (
    Object.keys(props.plotted_data).length === 0 ||
    Object.keys(props.selected).length === 0 ||
    props.x_axis_label === undefined ||
    props.y_axis_label === undefined
  ) {
    console.log("nothing to plot");
    return <br />;

  } else {

    console.log('x_axis_label',props.x_axis_label)

    for (var key in props.plotted_data) {

        var multiplied_x_axis = props.plotted_data[key][props.x_axis_label].map(function(entry) {
            return entry*Math.pow(10, -1*props.x_axis_mutliplier);
        });

        var multiplied_y_axis = props.plotted_data[key][props.y_axis_label].map(function(entry) {
            return entry*Math.pow(10, -1*props.y_axis_mutliplier);
            
        });


      list_of_data_dictionaries.push({
        x: multiplied_x_axis,
        y: multiplied_y_axis,
        type: "scatter",
        mode: "lines+points",
        name: props.plotted_data[key]["filename"]
      });
    }
  }

  const base_units = ' unknown units'
  var units = '('+base_units+')'
  if (props.x_axis_mutliplier === -3){
    units = ' (m'+base_units+')'
  }
  if (props.x_axis_mutliplier === -2 || 
      props.x_axis_mutliplier === -1 || 
      props.x_axis_mutliplier === 1 ||
      props.x_axis_mutliplier === 2 ||
      props.x_axis_mutliplier === 4 ||
      props.x_axis_mutliplier === 5 ||
      props.x_axis_mutliplier === 7 ||
      props.x_axis_mutliplier === 8 
      ){
    units = ' (10 <sup>'+props.x_axis_mutliplier+'</sup> '+base_units+')'
  }  
  if (props.x_axis_mutliplier === 3){
    units = ' (k'+base_units+')'
  }
  if (props.x_axis_mutliplier === 6){
    units = ' (M'+base_units+')'
  }  
  if (props.x_axis_mutliplier === 9){
    units = ' (G'+base_units+')'
  }  
        

  const x_axis_title = props.x_axis_label + ' ' + units

  return (
    <Plot
      data={list_of_data_dictionaries}
      layout={{
        xaxis: {
          title: x_axis_title,
          type: props.x_axis_scale
        },
        yaxis: {
          title: props.y_axis_label,
          type: props.y_axis_scale
        },
        margin: {
          r: 0,
          t: 1,
          pad: 1
        },
        legend: {
          x: 0,
          y: 1
        }
      }}
    />
  );
}


function percentFormatter(v) {
  return `${v}`;
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
      x_axis_scale: "lin",
      y_axis_scale: "lin",
      columns: [],
      data: [],
      loading: false,
      selected: {},
      loading_graph: false,
      requires_axis_selection: true,
      requires_checkbox_selection: true,
      x_axis_mutliplier:0, 
      y_axis_mutliplier:0 
    };

    this.handle_y_axis_data_dropdown_change_function = this.handle_y_axis_data_dropdown_change_function.bind(this);

    this.handle_x_axis_data_dropdown_change_function = this.handle_x_axis_data_dropdown_change_function.bind(this);

    this.handle_meta_data_dropdown_change_function = this.handle_meta_data_dropdown_change_function.bind(this);

    this.handle_xaxis_scale_change = this.handle_xaxis_scale_change.bind(this);

    this.handle_yaxis_scale_change = this.handle_yaxis_scale_change.bind(this);

    this.handle_xaxis_units_change = this.handle_xaxis_units_change.bind(this);

    this.handle_yaxis_units_change = this.handle_yaxis_units_change.bind(this);    

    this.toggleRow = this.toggleRow.bind(this);

    this.handle_clearplot_button_press = this.handle_clearplot_button_press.bind(this);
  }

  handle_clearplot_button_press(event) {
    console.log("clearing plotted data");
    this.setState({
      plotted_data: {}
    });
    this.setState({
      selected: {}
    });
  }

  make_clear_button() {
    console.log("this.state.selected", Object.keys(this.state.selected).length);
    if (Object.keys(this.state.selected).length === 0 || Object.keys(this.state.plotted_data).length === 0) {
      return "";
    } else {
      return <Button onClick={this.handle_clearplot_button_press}>Clear selection</Button>;
    }
  }

  handle_xaxis_scale_change(event) {
    console.log("event.target.value", event.target.value);
    this.setState({
      x_axis_scale: event.target.value
    });
    console.log("x_axis_scale", this.state.x_axis_scale);
  }

  handle_yaxis_scale_change(event) {
    console.log("event.target.value", event.target.value);
    this.setState({
      y_axis_scale: event.target.value
    });
    console.log("y_axis_scale", this.state.y_axis_scale);
  }

  handle_xaxis_units_change(value) {
    console.log("value", value);
    this.setState({
      x_axis_mutliplier: value
    });

  }

  handle_yaxis_units_change(value) {
    console.log("value", value);
    this.setState({
      y_axis_mutliplier: value
    });

  }

  handle_meta_data_dropdown_change_function(optionSelected) {
    this.setState({ loading: true });
    console.log("new metadata field selected", optionSelected.value);

    console.log("new metadata field selected", optionSelected.placeholder);
    let queryCopy = JSON.parse(JSON.stringify(this.state.query));
    console.log(queryCopy);

    if (optionSelected.value["value"] === "") {
      delete queryCopy[optionSelected.value["field"]];
      console.log("deleting field from query", optionSelected.value["field"]);
    } else {
      queryCopy[optionSelected.value["field"]] = optionSelected.value["value"];
    }

    this.setState({ query: queryCopy }, () => {
      console.log("state =", this.state);
      console.log("JSON.stringify(this.state.query)=", JSON.stringify(this.state.query));
      console.log(REST_API_EXAMPLE_URL + "/get_matching_entrys?query=" + JSON.stringify(this.state.query));

      var meta_data_fields_string = "";

      for (var i = 0; i < this.state.axis_data.length; i++) {
        meta_data_fields_string = meta_data_fields_string + ',"' + this.state.axis_data[i]["value"] + '":0';
      }

      meta_data_fields_string = meta_data_fields_string.replace(",", "{");
      meta_data_fields_string = meta_data_fields_string + "}";

      console.log("meta_data_fields_string", meta_data_fields_string);

      console.log(
        REST_API_EXAMPLE_URL +
          "/get_matching_entrys_limited_fields?query=" +
          JSON.stringify(this.state.query) +
          "&fields=" +
          meta_data_fields_string
      );
      //fetch(REST_API_EXAMPLE_URL + "/get_matching_entrys?query=" + JSON.stringify(this.state.query))

      fetch(
        REST_API_EXAMPLE_URL +
          "/get_matching_entrys_limited_fields?query=" +
          JSON.stringify(this.state.query) +
          "&fields=" +
          meta_data_fields_string
      )
        .then(result => {
          if (result.ok) {
            return result.json();
          }
        })
        .then(data => {
          this.setState({ query_result: data });
          this.setState({ loading: false });
          console.log("state =", this.state);
        })
        .catch(err => {
          console.log(
            "Cannot connect to server " +
              REST_API_EXAMPLE_URL +
              "get_matching_entrys?query=" +
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

  ReturnColumns(check_box_class) {
    const columns = [
      {
        id: "checkbox",
        accessor: "",
        Cell: ({ original }) => {
          return (
            <input
              type="checkbox"
              className={check_box_class}
              checked={this.state.selected[original.filename] === true}
              onChange={() => this.toggleRow(original.filename)}
            />
          );
        },
        sortable: false,
        width: 45
      }
    ];
    this.state.filter_data.map((x, i) => {
      columns.push({
        Header: x["field"][0],
        accessor: x["field"][0]
      });
    });

    return columns;
  }

  toggleRow(filename) {
    this.setState({ loading: true });
    this.setState({ loading_graph: false });
    const newSelected = Object.assign({}, this.state.selected);
    newSelected[filename] = !this.state.selected[filename];
    console.log("check box clicked", filename, "state=", newSelected[filename]);
    this.setState({ selected: newSelected });

    const select_dic = this.state.selected;
    console.log("values");
    console.log(Object.values(select_dic));

    let plotted_dataCopy = JSON.parse(JSON.stringify(this.state.plotted_data));
    if (newSelected[filename] === true) {
      // this.setState({requires_checkbox_selection: false,});
      console.log(REST_API_EXAMPLE_URL + "/get_matching_entry?query={'filename':" + filename + "}");
      fetch(REST_API_EXAMPLE_URL + "/get_matching_entry?query={'filename':" + filename + "}")
        .then(result => {
          if (result.ok) {
            return result.json();
          }
        })
        .then(data => {
          plotted_dataCopy[filename] = data;
          this.setState({ plotted_data: plotted_dataCopy });
          this.setState({ loading_graph: false });
          this.setState({ loading: false });
          console.log("state =", this.state);
        })
        .catch(err => {
          console.log(
            "Cannot connect to server " +
              REST_API_EXAMPLE_URL +
              "/get_matching_entry?query={'filename':" +
              filename +
              "}"
          );
        });
    } else {
      delete plotted_dataCopy[filename];
      this.setState({ loading: false });
    }

    console.log("plotted_dataCopy", plotted_dataCopy);
    this.setState({ plotted_data: plotted_dataCopy }, () => {
      console.log(this.state.plotted_data);
    });
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

        const meta_data_fields_local = [];
        data.map((x, i) => {
          console.log("meta_data_field", x["field"][0]);
          meta_data_fields_local.push(x["field"][0]);
        });
        this.setState({ meta_data_fields: meta_data_fields_local });
      })
      .catch(err => {
        console.log("Cannot connect to server find_meta_data_fields_and_distinct_entries");
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

    console.log("this.state.query_result", this.state.query_result);

    console.log("selected", this.state.selected);

    const selected = this.state.selected;

    var check_box_class;
    if (
      Object.keys(selected).length === 0 ||
      Object.keys(selected).every(function(k) {
        return selected[k] === false;
      })
    ) {
      check_box_class = "checkbox_highlighted";
    } else {
      check_box_class = "checkbox";
    }
    console.log("check_box_class", check_box_class);
    console.log(
      "check_box_class",
      Object.keys(selected).every(function(k) {
        return selected[k] === false;
      })
    );
    console.log("check_box_class", this.state.selected);

    const columns = this.ReturnColumns(check_box_class);

    var visible_axis_dropdowns;
    if (Object.keys(this.state.query_result).length === 0) {
      visible_axis_dropdowns = false;
    } else {
      visible_axis_dropdowns = true;
    }

    return (
      <div className="App">
        <Container>
          <Row>
            <Col>
              <h1 className="heading">Database GUI</h1>
            </Col>
          </Row>
          <Row>
            <Col md="2" lg="2">
              <LabelsForDropdowns filter_data={filter_data} />
              <LabelsForAxisDropdowns visible={visible_axis_dropdowns} />
            </Col>
            <Col md="3" lg="3">
              <FilterDropdowns
                filter_data={filter_data}
                event_handler={this.handle_meta_data_dropdown_change_function}
              />
              <hr />
              <br />

              <AxisDropdowns
                placeholder="Select x axis"
                axis_data={axis_data}
                axis_selection={this.state.x_axis_label}
                event_handler={this.handle_x_axis_data_dropdown_change_function}
                visible={visible_axis_dropdowns}
              />

              <AxisDropdowns
                placeholder="Select y axis"
                axis_data={axis_data}
                axis_selection={this.state.y_axis_label}
                event_handler={this.handle_y_axis_data_dropdown_change_function}
                visible={visible_axis_dropdowns}
              />
            </Col>
            <Col md="7" lg="7">
              <PlotlyGraph
                selected={this.state.selected}
                plotted_data={this.state.plotted_data}
                x_axis_label={this.state.x_axis_label}
                y_axis_label={this.state.y_axis_label}
                x_axis_scale={this.state.x_axis_scale}
                y_axis_scale={this.state.y_axis_scale}
                x_axis_mutliplier={this.state.x_axis_mutliplier}
                y_axis_mutliplier={this.state.y_axis_mutliplier}
              />

              {this.make_clear_button()}

              <DownloadButton plotted_data={this.state.plotted_data} />
              <br />
              <br />

              <AxisScaleRadioButton
                plotted_data={this.state.plotted_data}
                event_handler={this.state.x_axis_scale}
                onChange={this.handle_xaxis_scale_change}
                label={"log"}
                title="X axis scale "
                x_axis_label={this.state.x_axis_label}
                y_axis_label={this.state.y_axis_label}  
                selected={this.state.selected}              
              />
              <AxisScaleRadioButton
                plotted_data={this.state.plotted_data}
                event_handler={this.state.x_axis_scale}
                onChange={this.handle_xaxis_scale_change}
                label={"lin"}
                title=""
                x_axis_label={this.state.x_axis_label}
                y_axis_label={this.state.y_axis_label} 
                selected={this.state.selected}               
              />

              <br />

              <AxisScaleRadioButton
                plotted_data={this.state.plotted_data}
                event_handler={this.state.y_axis_scale}
                onChange={this.handle_yaxis_scale_change}
                label={"log"}
                title="Y axis scale "
                x_axis_label={this.state.x_axis_label}
                y_axis_label={this.state.y_axis_label} 
                selected={this.state.selected}               
              />
              <AxisScaleRadioButton
                event_handler={this.state.y_axis_scale}
                onChange={this.handle_yaxis_scale_change}
                label={"lin"}
                title=""
                plotted_data={this.state.plotted_data}
                x_axis_label={this.state.x_axis_label}
                y_axis_label={this.state.y_axis_label}  
                selected={this.state.selected}              
              />

              <br/>

              <ScaleSlider 
                onChange={this.handle_xaxis_units_change}
                plotted_data={this.state.plotted_data}
                x_axis_label={this.state.x_axis_label}
                y_axis_label={this.state.y_axis_label}  
                selected={this.state.selected}   
                />



            </Col>
          </Row>

          <Row>
            <Col md="12" lg="12">
              <div>
                <br />

                <QueryResulltsTable
                  query_Results={this.state.query_result}
                  data={results_of_db_query}
                  columns={columns}
                  loading={this.state.loading}
                />

                <br />
                <PlottedResulltsTable
                  query_Results={this.state.plotted_data}
                  data={this.state.plotted_data}
                  columns={columns}
                  loading={this.state.loading}
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
