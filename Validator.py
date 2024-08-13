class validator:
    def __init__(self,student,courses):
        self.student = student
        self.courses = courses

    def any_electives(self):
        if len(self.courses[self.student.template_course_code]["Elective codes"]) == 0:
            any_electives_required = False 
        elif len(self.courses[self.student.template_course_code]["Elective codes"]) != 0:
            any_electives_required = True
        else:
            print("Something is wrong!!")

        return any_electives_required
    
    def final_mark_validator(self):
        if len(self.student.final_marks) != len(self.student.re_exam_marks) != len(self.student.completed_modules) != len(self.student.completed_module_names):
            raise ValueError("All input lists must have the same length.")
    
        for i in range(len(self.student.final_marks)):
            if self.student.final_marks[i] == "nan" or self.student.completed_module_names[i] == "nan":
                raise ValueError("Invalid input: final marks and module names must not be empty.")
            if not isinstance(self.student.final_marks[i], (int, float)):
                raise ValueError(f"Final mark at index {i} must be a number.")
            if not 0 <= self.student.re_exam_marks[i] and self.student.re_exam_marks[i] <= 100:
                raise ValueError(f"Final mark at index {i} must be between 0 and 100.")
            if not isinstance(self.student.re_exam_marks[i], (int, float)):
                raise ValueError(f"Re-exam mark at index {i} must be a number.")
            if not 0 <= self.student.re_exam_marks[i] and self.student.re_exam_marks[i]<= 100:
                raise ValueError(f"Re-exam mark at index {i} must be between 0 and 100.")
        
        results = []
        for self.student.final_mark, self.student.re_exam_mark in zip(self.student.final_marks, self.student.re_exam_marks):
            if self.student.final_mark >= 50:
                results.append((True, "Passed"))
            elif 40 <= self.student.final_mark < 50:
                if self.student.re_exam_mark == 50:
                    results.append((True, "Re-exam passed"))
                else:
                    results.append((False, "Re-exam failed"))
            else:
                results.append((False, "Failed"))
        return results
    
    def results(self):
        module_results = self.final_mark_validator()
        student_passed = True
        failed_modules = []
        for index, result in enumerate(module_results):
            if not result[0]: 
                student_passed = False
                failed_modules.append((self.student.completed_modules[index],self.student.completed_module_names[index], result[1]))

        if student_passed:
            print("Student passed all modules!")
            print("ELIGABLE FOR GRADUATION !")
        else:
            print("Student failed the following modules:")
            for code, module, reason in failed_modules:
                print(f"{code} :{module}\n Result: {reason}")    
    
    def lists_to_sets(self):
        required_modules_set = set(self.courses[self.student.template_course_code]["Module Names"])
        completed_modules_set = set(self.student.completed_module_names)
        required_modules_electives_set = set(self.courses[self.student.template_course_code]["Elective modules"])
        return required_modules_electives_set,required_modules_set,completed_modules_set

    def outstanding_modules(self):
        required_modules_electives_set,required_modules_set,completed_modules_set = self.lists_to_sets()
        outstanding_modules = required_modules_set - completed_modules_set
        return outstanding_modules

    def elective_modules_requirement(self):

        return len(self.courses[self.student.template_course_code]["Elective modules"]) > 0
    

    def checker(self):
        if len(self.outstanding_modules()) ==0:

            if self.elective_modules_requirement() == True:
                required_modules_electives_set,required_modules_set,completed_modules_set = self.lists_to_sets()
                completed_electives = required_modules_electives_set & completed_modules_set
                if len(completed_electives) ==0:
                    print("ELECTIVE MODULES NOT COMPLITED")
                else:
                    
                    print("Here are completed electives:")
                    for elective in completed_electives:
                        print(elective)
                    print(" ")
                    self.results()
            else:
                print("THIS COURSE HAS NO ELECTIVES!!")
                self.results()

        else:
            print("You have not completed all the required modules for this course")
            print("Here are the outstanding modules: \n"+str(self.outstanding_modules()))

    def student_record(self):
        if len(self.student.completed_modules) != len(self.student.completed_module_names) or \
         len(self.student.completed_modules) != len(self.student.final_marks):
            raise ValueError("Data mismatch: Length of modules, names, and marks lists must be equal.")

        record_str = f"Student initials & Surname: {self.student.student_initials}  Student Number: {self.student.student_number}\n"
        record_str += f"Total Credits: {self.student.total_credits}\n"
        record_str += "Module Code\tModule Name\t\tFinal Mark\n"

        for code, name, mark in zip(self.student.completed_modules, self.student.completed_module_names, self.student.final_marks):
            record_str += f"{code}\t\t{name}\t\t{mark}\n"

        return record_str





