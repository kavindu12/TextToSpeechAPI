import { Injectable } from '@angular/core';
import {HttpClient,HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ReaderViewService {

  params:any;
  pdfFileName:string
  constructor(private http:HttpClient) { 
    let params = new HttpParams();

  }


  getPDFFlowCharts(fileName:string):Observable<FlowChartData>{
    console.log("came here");
    this.pdfFileName = fileName + ".pdf";
    this.params = new HttpParams().set('filename', this.pdfFileName);

    return this.http.get<FlowChartData>('http://127.0.0.1:5000/pdf_flow_chart_response',{params:this.params})
  }

  getSummarizeText(fileName:string):Observable<SummarizeTextData>{
    console.log("came here");
    this.pdfFileName = fileName + ".pdf";
    this.params = new HttpParams().set('filename', this.pdfFileName);

    return this.http.get<SummarizeTextData>('http://127.0.0.1:5000/summarize_response',{params:this.params})
  }

  getGraphData(fileName:string):Observable<GraphData>{
    console.log("came here");
    this.pdfFileName = fileName + ".pdf";
    this.params = new HttpParams().set('filename', this.pdfFileName);

    return this.http.get<GraphData>('http://127.0.0.1:5000/graph_info',{params:this.params})
  }
}
