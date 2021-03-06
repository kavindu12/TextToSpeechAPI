import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {PdfViewerModule} from 'ng2-pdf-viewer'
import {HttpClientModule} from '@angular/common/http';
import {MatButtonModule} from '@angular/material'
// import { Injectable,NgZone } from '@angular/core';
// import { Observable } from 'rxjs';
// import * as _ from "lodash";

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { AdminComponent } from './admin/admin.component';
import { HomeComponent } from './home/home.component';
import { RouterModule } from '@angular/router';
import { from } from 'rxjs';
import { AlertComponent } from './alert/alert.component';
import { PdfViewerComponent } from './pdf-viewer/pdf-viewer.component';
import { ReaderViewComponent } from './reader-view/reader-view.component';
import {WebcamModule} from 'ngx-webcam'

const MaterialComponents =[
  MatButtonModule
];

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    AdminComponent,
    HomeComponent,
    AlertComponent,
    PdfViewerComponent,
    ReaderViewComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MaterialComponents,
    PdfViewerModule,
    HttpClientModule,
    // Observable,
    // Injectable,
    // NgZone,
    FormsModule,
    ReactiveFormsModule,
    WebcamModule,
    RouterModule.forRoot([
      {
        path:'',
        component: HomeComponent
      },
      {
        path:'login',
        component:LoginComponent
      },
      {
        path:'admin',
        component:AdminComponent
      },
      {
        path:'researchPaperViewer',
        component:PdfViewerComponent
      }
    ])
  ],
  providers: [],
  exports:[MaterialComponents],
  bootstrap: [AppComponent]
})
export class AppModule { }
