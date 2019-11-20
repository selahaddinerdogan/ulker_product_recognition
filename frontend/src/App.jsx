import React, { Component } from 'react';
import './App.css';
import {Route, Switch, BrowserRouter, Redirect} from 'react-router-dom';
import { createStore, applyMiddleware } from "redux";

import Webcam from "react-webcam";
import {DataView, DataViewLayoutOptions} from 'primereact/dataview';
import {Button} from "primereact/button";
import {Dropdown} from "primereact/dropdown";
import {Panel} from 'primereact/panel';
import 'primereact/resources/themes/nova-light/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';
import '@devexpress/dx-react-grid-bootstrap4/dist/dx-react-grid-bootstrap4.css';

class App extends Component {

     constructor() {
        super();
        this.state = {
            image:'no-image.png',
            count : 25,
            products:[],
            first_products:[],
            second_products:[],
            layout: 'list',
            selectedCar: null,
            visible: false,
            sortKey: null,
            sortOrder: null
        };
        this.itemTemplate = this.itemTemplate.bind(this);
        this.onSortChange = this.onSortChange.bind(this);
    }

    setRef = webcam => {
        this.webcam = webcam;
    };

    capture = () => {
        const imageSrc = this.webcam.getScreenshot();
        this.getRequest(imageSrc);
    };

    componentWillMount() {
        this.interval = setInterval(() => {
          this.capture();

        }, 1000);
      }


    getRequest(image){
        const url = '/model/';
        // console.log("*** header: ***",headers);
        let img = image.split('base64,')[1];
        const data = {image: img};
        let body = JSON.stringify(data);
        fetch(url, {
            method: 'POST',
            headers: {
                "Content-type": "application/json; charset=UTF-8",
                "access-control-allow-origin":"*",
                'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,OPTIONS',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
                'Access-Control-Allow-Credentials': 'true'
            },
            body: body

        })
            .then(res => {
                if (res.status < 500) {
                    return res.json().then(data => {
                        return {status: res.status, data};
                    })
                } else {
                    console.log("Server Error!");
                    throw res;
                }
            })
            .then(res => {
                if (res.status === 200) {
                    if (res.data.image !== null)
                    this.setState({
                        image:res.data.image,
                        first_products:res.data.products.filter((pr,index) => index < 9),
                        second_products:res.data.products.filter((pr,index) => index >= 9)
                    });
                    //console.log(res.data.products);

                } else if (res.status === 401 || res.status === 403) {
                    throw res.data;
                }
            })

    }

    onSortChange(event) {
        const value = event.value;

        if (value.indexOf('!') === 0) {
            this.setState({
                sortOrder: -1,
                sortField: value.substring(1, value.length),
                sortKey: value
            });
        }
        else {
            this.setState({
                sortOrder: 1,
                sortField: value,
                sortKey: value
            });
        }
    }

    renderListItem(product) {
        return (
            <div className="p-col-12" style={{padding: '0em', borderBottom: '1px solid #d9d9d9'}}>
                <div className="p-grid p-align-start vertical-container">
                    <div style={{marginTop:'5px'}} className="p-col">
                        <img style={{maxWidth:'80%',maxHeight:'90%'}} src={product.image} />
                    </div>

                    <div style={{marginTop:'5px'}} className="p-col"><b>{product.name}</b></div>

                    <div className="p-col">{product.stock?  <i className="pi pi-check" style={{fontSize: '2.5em',color:'green'}}></i> :
                        <i className="pi pi-times" style={{fontSize: '2.5em',color:'red'}}></i>}</div>

                    </div>
                </div>
        );
    }

    renderGridItem(product) {
        return (
            <div style={{ padding: '.5em' }} className="p-col-12 p-md-3">

            </div>
        );
    }

    itemTemplate(product, layout) {
          if (product !== null) {
              if (!product) {
                  return;
              }

              if (layout === 'list')
                  return this.renderListItem(product);
              else if (layout === 'grid')
                  return this.renderGridItem(product);
          }
          return null;
    }


    render() {

        const videoConstraints = {
            width: 1280,
            height: 720,
            facingMode: "user"
        };


        return (
             <div className="p-fluid">
                    <div className="p-col-12 p-lg-offset-1  p-lg-10 p-justify-center">
                            <div className="p-grid p-dir-col-rev">
                                <Panel header="Ürün Tanıma Modeli"
                                       toggleable={false}
                                       style ={{textAlign:'center'}}
                                >
                                    <div className="p-fluid">
                                        <div className="p-col-12 p-lg-offset-1  p-lg-10 p-justify-center">

                                           <div className="p-grid ">
                                                <div className="p-col" >
                                                        <Webcam
                                                            audio={false}
                                                            height={'50%'}
                                                            minScreenshotWidth={640}
                                                            minScreenshotHeight={480}
                                                            ref={this.setRef}
                                                            screenshotFormat="image/jpeg"
                                                            width={'70%'}

                                                            videoConstraints={videoConstraints}
                                                        />
                                                        <div>
                                                            <img style={{maxWidth:'70%',maxHeight:'50%'}}  src={"/images/"+this.state.image} alt=""></img>
                                                        </div>
                                                </div>

                                                <div className="p-col-12 p-md-6 p-lg-6">
                                                    <div className="p-grid ">
                                                        <div className="p-lg-6">
                                                             <DataView
                                                                style={{marginTop:'27%',fontSize:'12px'}}
                                                                header={"Ürünler"}
                                                                value={this.state.first_products}
                                                                layout={this.state.layout}
                                                                emptyMessage=""
                                                                sortOrder={this.state.sortOrder}
                                                                sortField={this.state.sortField}
                                                                paginatorPosition={'both'}
                                                                itemTemplate={this.itemTemplate}/>
                                                        </div>
                                                        <div className="p-lg-6">
                                                             <DataView
                                                                style={{marginTop:'27%',fontSize:'12px'}}
                                                                header={"Ürünler"}
                                                                value={this.state.second_products}
                                                                layout={this.state.layout}
                                                                emptyMessage=""
                                                                sortOrder={this.state.sortOrder}
                                                                sortField={this.state.sortField}
                                                                paginatorPosition={'both'}
                                                                itemTemplate={this.itemTemplate}/>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </Panel>

                            </div>

                    </div>
             </div>




        );
    }
}

export default App;