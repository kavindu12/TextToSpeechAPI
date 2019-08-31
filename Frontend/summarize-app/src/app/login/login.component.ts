import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { SpeechrecognitionserviceService } from '../service/speechrecognitionservice.service';
import { TextToSpeechService } from '../service/text-to-speech.service';
import {Subscription} from 'rxjs'
import { first } from 'rxjs/operators';
import { AuthService } from '../auth.service';
import { from } from 'rxjs';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

    @ViewChild('input2', { static: false }) input2: ElementRef;
    loginForm: FormGroup;
    loading = false;
    submitted = false;
    returnUrl: string;

    speechData: string;
    nextSpeechWord: string;
    nextUserUtterance: string;
    passwordUtterance:string;
    speechWord: string;
    speechUsername: string;
    speechPasswordResponse:string;
    showSearchButton: boolean;
    sub: Subscription;
    sub2:Subscription;


    constructor(private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private speechRecognitionService: SpeechrecognitionserviceService,
        private textToSpeech: TextToSpeechService) {
        this.speechData = "";
        this.speechUsername = "";
        this.showSearchButton = true;
        // this.speechRecognitionService.record();
    }

    ngOnInit() {
        console.log("hello")

        this.loginForm = this.formBuilder.group({
            username: ['', Validators.required],
            password: ['', Validators.required]
        });
        this.activateSpeechSynthesis("Hi welcome to Aspectu currently you are in the login page please say username and password to continue");
        this.activateSpeechSearchMovie();

        //   this.activateSpeechSynthesis();
        this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
    }

    get f() { return this.loginForm.controls; }

    onSubmit() {
        this.submitted = true;

        // stop here if form is invalid
        if (this.loginForm.invalid) {
            return;
        }

        this.loading = true;

    }

    activateSpeechSearchMovie(): void {
        this.showSearchButton = false;

        this.sub=this.speechRecognitionService.record()
            .subscribe(
                //listener
                (value) => {
                    this.speechData = value;
                    //   this.speechUsername=this.speechData;
                    if (this.speechData != "") {
                        //   this.activateSpeechSearchMovie();
                        this.stopSpeechRecording();
                        this.speechWord = "Is the username " + this.speechData + " correct";
                        this.activateSpeechSynthesis(this.speechWord)
                        this.activateSpeechRecord();
                        // console.log(this.nextUserUtterance+"next user utterance");
                        // if (this.nextUserUtterance == "yes") {
                        //     this.input2.nativeElement.focus();
                        //     console.log('focus');
                        // }
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
                    this.showSearchButton = true;
                    console.log("--complete--");
                    this.activateSpeechSearchMovie();
                });
    }

    activateSpeechRecord(): any {
        this.sub2=this.speechRecognitionService.record()
            .subscribe(
                //listener
                (value) => {
                    console.log("speech record activated again");
                    console.log(value);
                    this.nextUserUtterance=value;
                    console.log(this.nextUserUtterance);
                    console.log(this.nextUserUtterance+"next user utterance");
                    if (this.nextUserUtterance == "yes") {
                        this.input2.nativeElement.focus();
                        console.log('focus');
                        this.activateSpeechSynthesis("Please say the password to continue");
                        this.stopSpeechRecordingUtterance();
                        this.activatePasswordUtterance();
                    }
                    else{
                        this.activateSpeechSynthesis("Please say again the username");
                        this.activateSpeechSearchMovie();
                    }
                    return this.nextUserUtterance;
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
                    this.showSearchButton = true;
                    console.log("--complete--");
                    this.activateSpeechSearchMovie();
                });
    }

    stopSpeechRecording(): void {
        this.sub.unsubscribe();
        // this.sub2.unsubscribe();
        this.speechRecognitionService.DestroySpeechObject();
    }

    stopSpeechRecordingUtterance():void{
        this.sub2.unsubscribe();
    }

    activatePasswordResponse():void{
        this.speechRecognitionService.record()
        .subscribe(
            (value)=>{
                this.speechPasswordResponse=value;
                if(this.speechPasswordResponse=="yes"){
                    console.log("Request is send to the server")
                    this.activateSpeechSynthesis("Request is send to the server")
                    this.onSubmit();
                }
                else{
                    this.activateSpeechSynthesis("Please say again the password")
                    this.activatePasswordUtterance();
                }
            }
        )
    }

    activatePasswordUtterance():void{
        this.speechRecognitionService.record()
        .subscribe(
            (value)=>{
                this.passwordUtterance=value;
                this.activateSpeechSynthesis("Is the password "+this.passwordUtterance+" correct");
                this.stopSpeechRecordingUtterance();
                this.activatePasswordResponse();
                
                
                
            }
        )
    }

    activateSpeechSynthesis(input: string): void {

        this.textToSpeech.speak(input);

    }
    // loginUser(event){
    //   event.preventDefault();
    //   const target=event.target;
    //   const username=target.querySelector('#username').value;
    //   const password=target.querySelector('#password').value;

    //   this.Auth.getUserDetails(username,password);
    //   console.log(username,password);;
    // }

}
