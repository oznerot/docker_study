import { Component, OnInit } from '@angular/core';
import { StudentService } from '../services/student.service';
import { Student } from '../models/student.model';
import { FormsModule } from '@angular/forms'; // Import FormsModule here
import { CommonModule } from '@angular/common';// Usually needed for *ngIf, *ngFor

@Component({
  selector: 'app-student',
  templateUrl: './student.component.html',
  styleUrls: ['./student.component.scss'],
  imports: [FormsModule, CommonModule]
})
export class StudentComponent implements OnInit{
  selectedStudent: Student | null = null;
  newStudent: Student = {id: '', name: '', age: 0};
  students: Student[] = []

  constructor (private studentService: StudentService) {}
  ngOnInit(): void {
    this.getStudents();
  }

  get studentForm(): Student {
    return this.selectedStudent ?? this.newStudent;
  }
  createStudent(): void{
    if (!this.newStudent.name || this.newStudent.age <= 0) return;
    this.studentService.createStudent(this.newStudent).subscribe(
      (createdStudent) => {
        this.students.push(createdStudent);
        this.newStudent = { id: '', name: '', age: 0 };
      },
      (error) => console.error(error)
    );
  };

  getStudents(): void {
    this.studentService.getStudents().subscribe(
      (data) => (this.students = data),
      (error) => console.error(error)
    );
  }
  updateStudent(): void{
    if (!this.selectedStudent) return;
    this.studentService.updateStudent(this.selectedStudent.id, this.selectedStudent).subscribe(
      () => {
        const index = this.students.findIndex(s => s.id === this.selectedStudent!.id);
        if (index !== -1) this.students[index] = this.selectedStudent!;
        this.selectedStudent = null;
      },
      (error) => console.error(error)
    );
  };
  selectStudent(student: Student): void {
    this.selectedStudent = { ...student };
  }
  deleteStudent(id:string): void{
    this.studentService.deleteStudent(id).subscribe(
      () => {
        this.students = this.students.filter(s => s.id !== id);
        if (this.selectedStudent?.id === id) this.selectedStudent = null;
      },
      (error) => console.error(error)
    );
  };
  cancelEdit(): void {
    this.selectedStudent = null;
  };

}