from student import Student
from Data_Source import Courses
from valuator import Validator


student1 = Student("applied_maths&compt.xlsx","failed_agre")
stu_status = Validator(student1,Courses)

print("\n")
stu_status.results()
#stu_status.checker()




