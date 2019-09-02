import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import { Observable } from 'rxjs';



@Injectable({
  providedIn: 'root'
})
export class PdfServiceService {

  private pdfText:string;
  constructor(private http:HttpClient) { 
    this.pdfText=""
  }

  getPDF():string{
    return '/assets/demo.pdf';
  }

  getPDFText():Observable<UserResponse>{

    return this.http.get<UserResponse>('http://127.0.0.1:5000/researchPaperText');

  }

  getAllFiles():Observable<string[]>{

    return this.http.get<string[]>('http://127.0.0.1:5000/getAllFiles');
  }
}
