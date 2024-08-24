


from operator import truediv
from Data_Source import Courses


class validator:
    def __init__(self,student,courses):
        self.student = student
        self.courses = courses

    def any_electives(self):
        if len(self.courses[self.student.template_course_code]["Elective codes"]) == 0:
            any_electives_required = False 
        else:
            any_electives_required = True

        return any_electives_required
    
    def final_mark_validator(self):
        if len(self.student.final_marks) != len(self.student.re_exam_marks) != len(self.student.completed_modules) != len(self.student.completed_module_names):
            raise ValueError("All input lists must have the same length.")
    
        for i in range(len(self.student.final_marks)):
            if self.student.final_marks[i] is None or self.student.completed_module_names[i] is None:
                raise ValueError("Invalid input: final marks and module names must not be empty.")
            if not isinstance(self.student.final_marks[i], (int, float)):
                raise ValueError(f"Final mark at index {i} must be a number.")
            if not 0 <= self.student.final_marks[i] <= 100:
                raise ValueError(f"Final mark at index {i} must be between 0 and 100.")
            if not isinstance(self.student.re_exam_marks[i], (int, float)):
                raise ValueError(f"Re-exam mark at index {i} must be a number.")
            if not 0 <= self.student.re_exam_marks[i] <= 50 :
                raise ValueError(f"Re-exam mark at index {i} must be between 0 and 50.")
        
        results = []
        for final_mark, re_exam_mark in zip(self.student.final_marks, self.student.re_exam_marks):
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
    
    def aggregate_exam_validator(self):
        if not hasattr(self.student, 'aggregate_exam_marks'):
            return []  # No aggregate exams to validate

        aggregate_exam_results = []
        
        # Validate that the lengths match
        if len(self.student.aggregate_exam_marks) != len(self.student.completed_modules) or \
           len(self.student.aggregate_exam_marks) != len(self.student.completed_module_names):
            raise ValueError("Data mismatch: Length of aggregate exam marks, module codes, and module names lists must be equal.")

        for i, module_name in enumerate(self.student.completed_module_names):
            # Check if the final exam was missed and aggregate exam was taken
            if self.student.final_marks[i] == "missed" and self.student.aggregate_exam_marks[i] != "missed":
                aggregate_exam_mark = self.student.aggregate_exam_marks[i]
                if not isinstance(aggregate_exam_mark, (int, float)):
                    raise ValueError(f"Aggregate exam mark at index {i} must be a number.")
                if not 0 <= aggregate_exam_mark <= 50 or self.student.re_exam_marks[i] is None:
                    raise ValueError(f"Aggregate exam mark at index {i} must be between 0 and 50.")
                
                if aggregate_exam_mark < 50:
                    aggregate_exam_results.append((False, "Failed aggregate exam"))
                else:
                    aggregate_exam_results.append((True, "Passed aggregate exam"))

        return aggregate_exam_results
    
    def special_exam_results(self):
        module_results = self.final_mark_validator()
        aggregate_exam_results = self.aggregate_exam_validator()

        
        special_exam_results = []

        if not hasattr(self.student, 'aggregate_exam_marks'):
            aggregate_exam_results = []  # No aggregate exams to validate

        # Check the final and aggregate exam results to determine if special exams was written
        for i, result in enumerate(module_results):
            #final_mark = self.student.final_marks[i]
            results = self.final_mark_validator()
            #module_name = self.student.completed_module_names[i]
            
        if len(aggregate_exam_results) > 0:
                aggregate_exam_result = aggregate_exam_results[i]
                if aggregate_exam_result[1] == "Failed aggregate exam":
                    if self.special_result[i] == 50:
                        special_exam_results.append((True,'Special Exam passed'))
                    elif self.special_result[i] < 50:
                        special_exam_results.append((False,'Special Exam failed'))
        
        if len(results) > 0:
            if results[i] == "Re-exam failed":
                if self.special_result[i] == 50:
                    special_exam_results.append((True,'pecial Exam passed'))
                elif self.special_result[i] < 50:
                    special_exam_results.append((False,'Special Exam failed'))            
        

        return special_exam_results


    def results(self):
        module_results = self.final_mark_validator()
        aggregate_exam_results = self.aggregate_exam_validator()
        special_exam_results = self.special_exam_validator()

        student_passed = True
        failed_modules = []
        
        for index, result in enumerate(module_results):
            if not result[0]: 
                student_passed = False
                failed_modules.append((self.student.completed_modules[index], self.student.completed_module_names[index], result[1]))

        for index, result in enumerate(aggregate_exam_results):
            if not result[0]: 
                student_passed = False
                failed_modules.append((self.student.completed_modules[index], self.student.completed_module_names[index], result[1]))

        for index, result in enumerate(special_exam_results):
            if not result[0]:
                student_passed = False
                failed_modules.append((self.student.completed_modules[index], self.student.completed_module_names[index], result[1]))

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
    
    
    def credit_scores(self):
        
        if self.total_credits >= Courses[self.student.template_course_code]['Total Credits']:
            status = True
        else:
            status = False
        return status
        

    def checker(self):
        if len(self.outstanding_modules()) ==0:

            if self.elective_modules_requirement() is True:
                required_modules_electives_set,required_modules_set,completed_modules_set = self.lists_to_sets()
                completed_electives = required_modules_electives_set & completed_modules_set
                if len(completed_electives) ==0:
                    print('Not eligable to graduate')
                    print('Reason : You have outstanding elective modules')
                    print("Here are electives to choose from electives:")

                    for elective in Courses[self.student.template_course_code]['Elective module']:
                        print(elective)
                        print(" ")

                else:    
                    self.results()
            else:
                print("THIS COURSE HAS NO ELECTIVES!!")
                if self.credit_scores() is True:
                    self.results()
                else:
                    print('Not eligable to graduate')
                    print('Reason : You do not meet the minimum credit score')

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
    







