from student import Student
from Data_Source import Courses
from Validator import validator


student1 = Student("student_data.xlsx",0)
stu_status = validator(student1,Courses)
print(stu_status.student_record())
print("\n")
stu_status.checker()




