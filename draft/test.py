import pandas as pd
from Data_Source import Courses
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

dataframe= pd.read_excel("student_data.xlsx",sheet_name=0)

   # Storing student data in variables for easy retrieval 
dataframe.loc[0,'Total Credits'] = 416 #Overiding credit score
template_course_code = str(dataframe.loc[0,'Course code'])
template_course_name = dataframe.loc[0,'Course Name']
student_number = dataframe.loc[0,'Student Number']
student_initials = dataframe.loc[0,'Initials & Surname']
total_credits = int(dataframe.loc[0,'Total Credits'])
completed_modules = dataframe.loc[:,'Modules'].to_list()
completed_module_names = dataframe.loc[:,'Module Names'].to_list()
final_marks = dataframe.loc[:,'Final mark'].to_list()
re_exam_marks = dataframe.loc[:,'Re-Exam'].to_list()

    # Taking data from our dict 
print(template_course_code=="4BSC02")
courses_codes = ["4BSC01","4BSC02","4BSC03","4BSC04"]

        
required_modules = Courses["4BSC01"]["Module codes"]
required_modules_names = Courses["4BSC01"]["Module Names"]
required_modules_elective = Courses["4BSC01"]["Elective modules"]
required_modules_elective_codes = Courses["4BSC01"]["Elective codes"]
required_total_credits = Courses["4BSC01"]["Total Credits"]      



    # converting my list to a set
required_modules_set = set(required_modules)
completed_modules_set = set(completed_modules)
required_modules_elective_codes_set = set(required_modules_elective_codes)


    # checking for outstanding modules
outstanding_modules = required_modules_set - completed_modules_set



'''
def elective_modules_requirement():
        
    if len(required_modules_elective_codes) == 0:
        any_electives_required = False 
    elif len(required_modules_elective_codes) != 0:
        any_electives_required = True
    else:
        print("Something is wrong!!")

    return any_electives_required



# method that checks for minimucredit scrore
def check_credit_score():
    if total_credits >= required_total_credits:
        return  "Credit Score Status:",True
    else:
        return "Credit Score Status:",False
    

# method that combine module codes and their corresponding names
def student_record():
    #combine elective modules with required models 
   if len(completed_modules)== len(completed_module_names):
    print("STUDENT RECORD\n")
    print(f"Student initials & Surname: {student_initials}  Student Number: {int(student_number)}\n")

    print("Module codes: Module Names: Final Marks")
    modules_data = zip(completed_modules,completed_module_names,final_marks)
    for code,name,marks in modules_data:
        print(f"{code}: {name}: {marks}")

'''

def final_mark_validator():
    if len(final_marks) != len(re_exam_marks) != len(completed_modules) != len(completed_module_names):
        raise ValueError("All input lists must have the same length.")
    
    for i in range(len(final_marks)):
        if final_marks[i] == "nan" or completed_module_names[i] == "nan":
           raise ValueError("Invalid input: final marks and module names must not be empty.")
        if not isinstance(final_marks[i], (int, float)):
          raise ValueError(f"Final mark at index {i} must be a number.")
        if not 0 <= re_exam_marks[i] and re_exam_marks[i] <= 100:
          raise ValueError(f"Final mark at index {i} must be between 0 and 100.")
        if not isinstance(re_exam_marks[i], (int, float)):
         raise ValueError(f"Re-exam mark at index {i} must be a number.")
        if not 0 <= re_exam_marks[i] and re_exam_marks[i]<= 100:
         raise ValueError(f"Re-exam mark at index {i} must be between 0 and 100.")
        
    results = []
    for final_mark, re_exam_mark in zip(final_marks, re_exam_marks):
        if final_mark >= 50:
            results.append((True, "Passed"))
        elif 40 <= final_mark < 50:
            if re_exam_mark == 50:
                results.append((True, "Re-exam passed"))
            else:
                results.append((False, "Re-exam failed"))
        else:
            results.append((False, "Failed"))
    return results

module_results = final_mark_validator()
student_passed = True
failed_modules = []
for index, result in enumerate(module_results):
    if not result[0]: 
        student_passed = False
        failed_modules.append((completed_module_names[index], result[1]))

if student_passed:
    print("Student passed all modules!")
else:
    print("Student failed the following modules:")
    for module, reason in failed_modules:
        print(f"Module :{module}: {reason}")    


    ''''results = []
    for i in range(len(final_marks)):
        if final_marks[i] >= 50:
         results.append("pass")
        elif 40 <= final_marks[i] <= 49:
            if re_exam_marks[i] >= 50:
                results.append("re-exam passed")
            else:
                results.append("re-exam failed")
        else:
            results.append("failed")

    for x in range(len(final_mark_validator())):
        if results[x] == "re-exam failed"| results[x]== "failed" :
            print(f"Student failed module {completed_modules[x]}")'''


def generate_pq(student_data):
    # Create a new PDF document
    canvas = canvas.Canvas("progress_report.pdf", pagesize=letter)

    # Define font and styles
    font_size = 12
    bold_font = canvas.setFont("Helvetica-Bold", font_size + 2)
    normal_font = canvas.setFont("Helvetica", font_size)

    # Add student details
    canvas.drawString(50, 750, f"Student Name: {student_data['student_name']}")
    canvas.drawString(50, 730, f"Student ID: {student_data['student_id']}")
    canvas.drawString(50, 710, f"Course: {student_data['course']}")

    # Add course performance table (placeholder)
    # ...

    # Add GPA and other summary information
    # ...

    canvas.save()

# Example student data
student_data = {
    "student_name": "John Doe",
    "student_id": "12345678",
    "course": "Computer Science",
    "courses": [
        {"code": "CS101", "name": "Introduction to Programming", "grade": "A"},
        # ... other courses
    ]
}


# SAMPLE CODE!!!






        

      
      







                
                

