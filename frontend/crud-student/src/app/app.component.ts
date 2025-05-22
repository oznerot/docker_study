import { Component } from '@angular/core';
import { StudentComponent } from './student/student.component';

@Component({
  selector: 'app-root',
  imports: [StudentComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'crud-student';
}
