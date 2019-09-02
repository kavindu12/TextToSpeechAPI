import { Component, OnInit, Input } from '@angular/core';
import {ReaderViewService} from '../service/reader-view.service'
import { TextToSpeechService } from '../service/text-to-speech.service';

import { from } from 'rxjs';

@Component({
  selector: 'app-reader-view',
  templateUrl: './reader-view.component.html',
  styleUrls: ['./reader-view.component.css']
})
export class ReaderViewComponent implements OnInit {

  @Input() childMessage:string;
  flowChartData:string;
  summarizeText:string;
  loadOnce:boolean=true;

  constructor(private readerViewService:ReaderViewService,
    private textToSpeech: TextToSpeechService,) {
    this.childMessage="";
   }

  ngOnInit() {
    // this.getFileName(this.childMessage);

  }

  ngAfterViewChecked(){
    if(this.childMessage!=undefined && this.loadOnce==true){
      console.log("File name is "+this.childMessage)
      this.getFileName(this.childMessage)
      this.getSummarizeText(this.childMessage)
      this.loadOnce=false;
    }
  }	


  getFileName(fileName:string){
    console.log(fileName)
    this.readerViewService.getPDFFlowCharts(fileName).subscribe(
      data=>{
        this.flowChartData=data.flowChartText;
        console.log(this.flowChartData);
        this.activateSpeechSynthesis("Reading the Flow Chart Information of the Research Paper"+this.flowChartData);
      }
    )
  }

  getSummarizeText(fileName:string){
    this.readerViewService.getSummarizeText(fileName).subscribe(
      data=>{
        this.summarizeText=data.SummarizeText;
        console.log(this.summarizeText);
        this.activateSpeechSynthesis("Reading the Summarize Text Of the Research Paper"+this.summarizeText);
      }
    )
  }

  activateSpeechSynthesis(input: string): void {

    this.textToSpeech.speak(input);

  }

}
