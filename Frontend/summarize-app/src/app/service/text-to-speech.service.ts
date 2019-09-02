import { Injectable,NgZone } from '@angular/core';
import { Observable } from 'rxjs';


interface IWindow extends Window{
  SpeechSynthesisUtterance: any;
  SpeechSynthesis: any;
}

@Injectable({
  providedIn: 'root'
})
export class TextToSpeechService {

  constructor(private zone:NgZone) {
      if ('speechSynthesis' in window) {
          console.log('Your browser supports speech synthesis.');
      // speak('hi');
      } else {
          alert('Sorry your browser does not support speech synthesis. Try this in <a href="https://www.google.com/chrome/browser/desktop/index.html">Google Chrome</a>.');
      }

   }

   speak(input:string){

      // return Observable.create(observer=>{
        const {SpeechSynthesisUtterance}: IWindow = <IWindow>window;
    const {SpeechSynthesis}: IWindow = <IWindow>window;

    // Create a new instance of SpeechSynthesisUtterance.
    var msg = new SpeechSynthesisUtterance();
    // Set the text.
    msg.text =input;
    // Set the attributes.
    msg.lang = 'en-US';
    // msg.voice = 'Google US English'; //  'Google UK English Female' 
    // msg.voice = 'Google US English' 
    msg.volume = 1;
    msg.rate = 1;
    msg.pitch = 1;
    //  msg.onend = function(event) { console.log('Speech complete'); }
    // Queue this utterance.
    // var talk = new SpeechSynthesis();
    (<any>window).speechSynthesis.speak(msg);

    

   }
   

}
