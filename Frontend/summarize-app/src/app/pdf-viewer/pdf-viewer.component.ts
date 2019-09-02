import { Component, OnInit } from '@angular/core';
import { PdfServiceService } from '../service/pdf-service.service'
import { TextToSpeechService } from '../service/text-to-speech.service';
import { SpeechrecognitionserviceService } from '../service/speechrecognitionservice.service';
import { Subscription } from 'rxjs'


import { ViewEncapsulation } from '@angular/core'

import { from } from 'rxjs';

@Component({
  selector: 'app-pdf-viewer',
  templateUrl: './pdf-viewer.component.html',
  styleUrls: ['./pdf-viewer.component.css'],
  // encapsulation: ViewEncapsulation.None
})
export class PdfViewerComponent implements OnInit {

  speechData: string;
  page: number = 1;
  pdfSrc: string = '';
  pdfText: string = '';
  speechWord: string = '';
  nextUserUtterance: string = '';
  fileNameArray: string[];
  sub: Subscription;
  sub2:Subscription;
  isFileName:boolean=false;
  fileName:string='';
  selectedFileName:string;


  constructor(private pdfService: PdfServiceService,
    private textToSpeech: TextToSpeechService,
    private speechRecognitionService: SpeechrecognitionserviceService) { }

  ngOnInit() {
    this.pdfSrc = this.pdfService.getPDF();
    // this.pdfText=this.pdfService.getPDFText();
    console.log(this.pdfText);
    this.getPdfText();
    this.getFileNames();
    // this.activateSpeechSearchMovie();
  }

  getPdfText() {

    this.pdfService.getPDFText().subscribe(
      data => {
        this.pdfText = data.text;
        // console.log(this.pdfText);
        // this.activateSpeechSynthesis(this.pdfText);
      }
    )
  }

  activateSpeechSynthesis(input: string): void {

    this.textToSpeech.speak(input);

  }

  getFileNames() {
    this.pdfService.getAllFiles().subscribe(
      data => {
        this.fileNameArray = data;
        this.activateSpeechSynthesis("Please Say one of the file names to read ")
        this.fileNameArray.forEach(file => {
          this.activateSpeechSynthesis(file);
        })
        this.activateSpeechSearchMovie();
        console.log(this.fileNameArray);
      }
    )
  }

  activateSpeechSearchMovie(): void {

    // this.getFileNames();
    this.sub = this.speechRecognitionService.record()
      .subscribe(
        //listener
        (value) => {
          this.speechData = value;
          if (this.speechData != "") {
            this.stopSpeechRecording();
            this.speechWord = "Is the file name " + this.speechData + " correct";
            this.activateSpeechSynthesis(this.speechWord)
            this.activateSpeechRecord(this.speechData);

          }
          console.log(value);
        },
        //errror
        (err) => {
          console.log(err);
          if (err.error == "no-speech") {
            console.log("--restatring service--");
            this.activateSpeechSearchMovie();
          }
        },
        //completion
        () => {
          // this.showSearchButton = true;
          console.log("--complete--");
          this.activateSpeechSearchMovie();
        });
  }

  stopSpeechRecording(): void {
    this.sub.unsubscribe();
    // this.sub2.unsubscribe();
    this.speechRecognitionService.DestroySpeechObject();
  }

  activateSpeechRecord(fileName:string): any {
    this.sub2 = this.speechRecognitionService.record()
      .subscribe(
        //listener
        (value) => {
          console.log("speech record activated again");
          console.log(value);
          this.nextUserUtterance = value;
          console.log(this.nextUserUtterance);
          this.fileNameArray.forEach(file => {
            if(file==fileName){
              this.selectedFileName=file;
              this.isFileName=true;
            }
          })
          if (this.isFileName==true && this.nextUserUtterance=="yes") {
            this.isFileName=false
            this.activateSpeechSynthesis("Correct File Name");
            this.stopSpeechRecordingUtterance();
          }
          else {
            this.activateSpeechSynthesis("Incorrect file name please tell the exact file name");
            this.stopSpeechRecordingUtterance();
            this.activateSpeechSearchMovie();
            this.activateSpeechSynthesis("Please Say one of the file names to read ")
            this.fileNameArray.forEach(file => {
              this.activateSpeechSynthesis(file);
            })

          }
          // return this.nextUserUtterance;
          console.log(value);
        },
        //errror
        (err) => {
          console.log(err);
          if (err.error == "no-speech") {
            console.log("--restatring service--");
            this.activateSpeechSearchMovie();
          }
        },
        //completion
        () => {
          console.log("--complete--");
          this.activateSpeechSearchMovie();
        });
  }

  stopSpeechRecordingUtterance(): void {
    this.sub2.unsubscribe();
  }

}
