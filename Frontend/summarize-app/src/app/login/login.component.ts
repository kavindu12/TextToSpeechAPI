import { Component, OnInit,ViewChild, ElementRef } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import {SpeechrecognitionserviceService} from '../service/speechrecognitionservice.service';
import { first } from 'rxjs/operators';
import { AuthService } from '../auth.service';
import { from } from 'rxjs';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

//   @ViewChild('input2') input: ElementRef;
  @ViewChild ('input2',{static: false}) input2 :ElementRef;
  loginForm: FormGroup;
    loading = false;
    submitted = false;
    returnUrl: string;
   
  speechData: string; 
  nextSpeechWord: string;
  showSearchButton: boolean;

  constructor( private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private speechRecognitionService: SpeechrecognitionserviceService) {
      this.speechData = "";
      this.showSearchButton = true;
      // this.speechRecognitionService.record();
     }

  ngOnInit() {
    console.log("hello")

    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
  });
  this.activateSpeechSearchMovie();
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

      this.speechRecognitionService.record()
          .subscribe(
          //listener
          (value) => {
              this.speechData = value;
              if(this.speechData!=""){
                  this.activateSpeechSearchMovie();
                  this.nextSpeechWord=value;
                  console.log(this.nextSpeechWord);
                  if(this.nextSpeechWord=="yes"){
                    this.input2.nativeElement.focus();
                    console.log('focus');
                  }
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

  activateUserResponse() :void {

    this.speechRecognitionService.userResponse()
    .subscribe(
        //listen user response
        (value) => {
            this.speechData = value;
            if(this.speechData!=""){
                this.activateSpeechSearchMovie();
                this.nextSpeechWord=value;
                console.log(this.nextSpeechWord);
                if(this.nextSpeechWord=="yes"){
                  this.input2.nativeElement.focus();
                  console.log('focus');
                }
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
  // loginUser(event){
  //   event.preventDefault();
  //   const target=event.target;
  //   const username=target.querySelector('#username').value;
  //   const password=target.querySelector('#password').value;

  //   this.Auth.getUserDetails(username,password);
  //   console.log(username,password);;
  // }

}
