from Data_Source import Courses
import pandas as pd


dataframe = pd.read_excel("student_data.xlsx",sheet_name=1)

# Storing STUDENT DATA in variables for easy retrieval 

course_code = str(dataframe.loc[0,'Course code'])
course_name = dataframe.loc[0,'Course Name']
student_number = dataframe.loc[0,'Student Number']
student_initials = dataframe.loc[0,'Initials & Surname']
total_credits = int(dataframe.loc[0,'Total Credits'])
completed_modules = dataframe.loc[:,'Modules'].to_list()
completed_module_names = dataframe.loc[:,'Module Names'].to_list()
final_marks = dataframe.loc[:,'Final mark'].to_list()
re_exam_marks = dataframe.loc[:,'Re-Exam'].to_list()



    # Taking data from our dict 
required_modules = Courses["4BSC01"]["Modules codes"]
required_modules_names = Courses["4BSC01"]["Modules Names"]
required_modules_elective = Courses["4BSC01"]["Elective module"]
required_modules_elective_codes = Courses["4BSC01"]["Elective codes"]
required_total_credits = Courses["4BSC01"]["Total Credits"]

    # converting my list to a set
required_modules_set = set(required_modules)
required_modules_names_set = set(required_modules_names)
completed_modules_set = set(completed_modules)
completed_module_names_set = set(completed_module_names)
required_modules_elective_codes_set = set(required_modules_elective_codes)
required_modules_elective_set = set(required_modules_elective)



def elective_modules_requirement():

    if len(required_modules_elective_codes) == 0:
            any_electives_required = False 
    elif len(required_modules_elective_codes) != 0:
            any_electives_required = True
    else:
            print("Something is wrong!!")
    return any_electives_required


def validator():
    # checking for outstanding modules
    outstanding_modules = required_modules_names_set - completed_module_names_set

    if len(outstanding_modules) ==0:
         #checking if the course does not have any electives
        if elective_modules_requirement() == True:
            completed_elective_modules = completed_module_names_set & required_modules_elective_set
            #checking if you have completed the elective modules
            if len(completed_elective_modules) == 0:
                print("ELECTIVE MODULES NOT COMPLITED")
            else:
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

        else:
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
    else:
        print("You have not completed all the required modules for this course")
        print("Here are the outstanding modules: \n"+str(outstanding_modules))


def student_record():
    #combine elective modules with required models 
    if len(completed_modules)== len(completed_module_names):
        print("~~STUDENT RECORD~~\n")
        print(f"Student initials & Surname: {student_initials}  Student Number: {int(student_number)}\n")
        print("Total Credits: "+str(total_credits))
        print("Module codes: Module Names: Final Marks")
        modules_data = zip(completed_modules,completed_module_names,final_marks,)
        for code,name,marks in modules_data:
            print(f"{code}: {name}: {marks}")


def final_mark_validator():
    if len(final_marks) != len(re_exam_marks) != len(completed_modules) != len(completed_module_names):
        raise ValueError("All input lists must have the same length.")
    
    for i in range(len(final_marks)):
        if final_marks[i] == "nan" or completed_module_names[i] == "nan":
           raise ValueError("Invalid input: final marks and module names must not be empty.")
        if not isinstance(final_marks[i], (int, float)):
          raise ValueError(f"Final mark at index {i} must be a number.")
        if not 0 <= final_marks[i] and final_marks[i] <= 100:
          raise ValueError(f"Final mark at index {i} must be between 0 and 100.")
        if not isinstance(re_exam_marks[i], (int, float)):
         raise ValueError(f"Re-exam mark at index {i} must be a number.")
        if not 0 <= re_exam_marks[i] and re_exam_marks[i]<= 50:
         raise ValueError(f"Re-exam mark at index {i} must be between 0 and 50.")
        
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

validator()  



        

        
    