import { Component, OnInit } from '@angular/core';
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

  loginForm: FormGroup;
    loading = false;
    submitted = false;
    returnUrl: string;
   
  speechData: string; 
  showSearchButton: boolean;

  constructor( private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private speechRecognitionService: SpeechrecognitionserviceService) {
      this.speechData = "";
      this.showSearchButton = true;
     }

  ngOnInit() {
    console.log("hello")

    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
  });
  

  // reset login status
  // this.authenticationService.logout();

  // get return url from route parameters or default to '/'
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
