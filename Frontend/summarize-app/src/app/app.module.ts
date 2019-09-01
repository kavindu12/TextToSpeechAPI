import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {PdfViewerModule} from 'ng2-pdf-viewer'
import {HttpClientModule} from '@angular/common/http';
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

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    AdminComponent,
    HomeComponent,
    AlertComponent,
    PdfViewerComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    PdfViewerModule,
    HttpClientModule,
    // Observable,
    // Injectable,
    // NgZone,
    FormsModule,
    ReactiveFormsModule,
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
  bootstrap: [AppComponent]
})
export class AppModule { }
