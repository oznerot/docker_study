import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, map, Observable, of } from 'rxjs';
import { Student } from '../models/student.model';
import { environment } from '../../environments/environment'

@Injectable({
    providedIn: 'root',
})
export class StudentService {
    //private apiUrl = environment.apiUrl
    private apiUrl = environment.apiUrl
    
    constructor(private http:HttpClient) {}

  getStudents(): Observable<Student[]> {
    return this.http.
      get<{ students: Student[]}>(`${this.apiUrl}/students`)
      .pipe(map(response => response.students)); // GET /students (we'll add this in API)
  }

  getStudent(id: string): Observable<Student> {
    return this.http
      .get<Student>(`${this.apiUrl}/students/${id}`);
  }

  createStudent(student: Student): Observable<any> {
    return this.http
      .post<{inserted_id: string, student: Student}>(`${this.apiUrl}/student`, student)
      .pipe(map(response => response.student));
  }

  updateStudent(id: string, student: Partial<Student>): Observable<any> {
    return this.http.put(`${this.apiUrl}/student/${id}`, student);
  }

  deleteStudent(id: string): Observable<any> {
    return this.http
      .delete(`${this.apiUrl}/student/${id}`)
      .pipe(map(()=>true),
        catchError((error) => {
          console.log(error);
          return of(false)
        }));
  }
}