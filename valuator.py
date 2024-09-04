from Data_Source import Courses

class Validator:
    def __init__(self, student,Courses):c
        self.student = student
        self.courses = Courses

    def any_electives(self):
        if len(self.courses[self.student.template_course_code]["Elective modules"]) == 0:
            any_electives_required = False 
        else:
            any_electives_required = True

        return any_electives_required

    def final_mark_validator(self):
        if len(self.student.final_marks) != len(self.student.re_exam_marks) != len(self.student.completed_modules) != len(self.student.completed_module_names):
            raise ValueError("All input lists must have the same length.")

        for i in range(len(self.student.final_marks)):
            if isinstance(self.student.final_marks[i], (int, float)):
              if not 0 <= self.student.final_marks[i] <= 100:
                raise ValueError(f"Final mark at index {i} must be between 0 and 100.")
            if isinstance(self.student.re_exam_marks[i], (int, float)):
              if not 0 <= self.student.re_exam_marks[i] <= 50 :
                raise ValueError(f"There is an unacceptable value in the re-exam ")
        
        results = []
        for final_mark, re_exam_mark in zip(self.student.final_marks, self.student.re_exam_marks):
            if final_mark >= 50:
                results.append((True, "Passed"))
            elif 40 <= final_mark < 50:
                if re_exam_mark == 50:
                    results.append((True, "Re-exam passed"))
                else:
                    results.append((False, "Re-exam failed"))
            elif final_mark == 0:
                results.append((False, "absent"))
            else:
                results.append((False, "Failed"))
            

        return results
    
  
    def aegrotat_exam_validator(self):
        if not hasattr(self.student, 'aegrotat_exam_marks'):
            return []  # No aegrotat exams to validate

        aegrotat_exam_results = []
        
        if len(self.student.aegrotat_exam_marks) != len(self.student.completed_modules) or \
        len(self.student.aegrotat_exam_marks) != len(self.student.completed_module_names):
            raise ValueError("Data mismatch: Length of aegrotat exam marks, module codes, and module names lists must be equal.")

        final_mark_results = self.final_mark_validator()

        for i, module_name in enumerate(self.student.completed_module_names):
            if final_mark_results[i][1] == "absent" and self.student.aegrotat_exam_marks[i] != 0:
                aegrotat_exam_mark = self.student.aegrotat_exam_marks[i]
                if not isinstance(aegrotat_exam_mark, (int, float)):
                    raise ValueError(f"aegrotat exam mark at index {i} must be a number.")
                if not 0 <= aegrotat_exam_mark <= 50:
                    raise ValueError(f"aegrotat exam mark at index {i} must be between 0 and 50.")
                
                if aegrotat_exam_mark < 40:
                    aegrotat_exam_results.append((False, "Failed aegrotat exam"))
                elif 40 <= aegrotat_exam_mark < 50:
                    aegrotat_exam_results.append((True, "Qualified for special exam"))
                else:
                    aegrotat_exam_results.append((True, "Passed aegrotat exam"))

        return aegrotat_exam_results

    def special_exam_results(self):
        module_results = self.final_mark_validator()
        aegrotat_exam_results = self.aegrotat_exam_validator()

        special_exam_results = []

        # Check failed modules for the main exam
        failed_modules = [i for i, result in enumerate(module_results) if not result[0]]

        # Process special exam qualification
        for i in failed_modules:
            
            # check if a student qualified for a  special exam based on the number of modules he/she failed
            if len(failed_modules) <= 2 and  module_results[i][1] == "Failed":
                if self.student.special_result[i] == 50:
                    special_exam_results.append((True, 'Special Exam passed'))
                elif  1 <= self.student.special_result[i] < 50:
                    special_exam_results.append((False, 'Special Exam failed'))


            # Check if the student qualified for special exam based on the re-exam marks
            if module_results[i][1] == "Re-exam failed" and 40 <= self.student.re_exam_marks[i] < 50:
                if self.student.special_result[i] == 50:
                    special_exam_results.append((True, 'Special Exam passed'))
                elif  1 <= self.student.special_result[i] < 50:
                    special_exam_results.append((False, 'Special Exam failed'))

        for  x in range(len(aegrotat_exam_results)):
            # Check if the student qualifies for a special exam based on aegrotat exam results
            if aegrotat_exam_results[x][1] == "Qualified for special exam" and 40 <= self.student.aegrotat_exam_marks[x] < 50:
                if self.student.special_result[x] == 50:
                    special_exam_results.append((True, 'Special Exam passed'))
                elif  1 <= self.student.special_result[x] < 50:
                    special_exam_results.append((False, 'Special Exam failed'))

        return special_exam_results


    def results(self):
        # Retrieve results from validators
        module_results = self.final_mark_validator()
        aegrotat_exam_results = self.aegrotat_exam_validator()
        special_exam_results = self.special_exam_results()

        student_passed = True
        failed_modules = []
        modules_to_check_special_exam = []

        # Check for modules that failed in the main exam
        failed_modules = [i for i, result in enumerate(module_results) if not result[0]]
        
        # Evaluate each failed module
        for index in range(len(failed_modules)):
            final_mark_result = module_results[index]
            re_exam_result = self.student.re_exam_marks[index]
            aegrotat_result = self.student.aegrotat_exam_marks[index]
            
            # Check re-exam results if applicable
            if final_mark_result[1] in ["Failed", "Re-exam failed"] and re_exam_result != 0:
                if 40 <= re_exam_result < 50:
                    # Student qualifies for a special exam
                    modules_to_check_special_exam.append(index)
                else:
                    # Student failed the re-exam
                    student_passed = False
                    failed_modules.append((self.student.completed_modules[index], self.student.completed_module_names[index], "Failed re-exam"))
            
            # Check if student had an aegrotat exam
            if final_mark_result[1] == "absent" and aegrotat_result != 0:
                if 40 <= aegrotat_result < 50:
                    # Student qualifies for a special exam
                    modules_to_check_special_exam.append(index)
                else:
                    # Student failed the aegrotat exam
                    student_passed = False
                    failed_modules.append((self.student.completed_modules[index], self.student.completed_module_names[index], "Failed aegrotat exam"))

            # Check special exam results for modules that failed the main exam
            if index in modules_to_check_special_exam:
                special_exam_result = special_exam_results[index]
                if not special_exam_result[0]:
                    student_passed = False
                    failed_modules.append((self.student.completed_modules[index], self.student.completed_module_names[index], special_exam_result[1]))
                else:
                    # The student passed the special exam
                    continue

        # Final decision
        if student_passed:
            print("Student passed all modules!")
            print("ELIGIBLE FOR GRADUATION!")
        else:
            print("Student failed the following modules:")
            for code, module, reason in failed_modules:
                print(f"{code} : {module}\n Result: {reason}")
    def lists_to_sets(self):
        required_modules_set = set(self.courses[self.student.template_course_code]["Module Names"])
        completed_modules_set = set(self.student.completed_module_names)
        required_modules_electives_set = set(self.courses[self.student.template_course_code]["Elective modules"])
        return required_modules_electives_set, required_modules_set, completed_modules_set

    def outstanding_modules(self):
        required_modules_electives_set, required_modules_set, completed_modules_set = self.lists_to_sets()
        outstanding_modules = required_modules_set - completed_modules_set
        return outstanding_modules

    def elective_modules_requirement(self):
        return len(self.courses[self.student.template_course_code]["Elective modules"]) > 0

    def credit_scores(self):
        # Calculate total credits earned
        passed_modules = 0
        module_results = self.final_mark_validator()

        for result in module_results:
            if result[0]:  # Check if the module is passed
                passed_modules += 1

        total_credits_earned = passed_modules * 16  # Each module is worth 16 credits

        # Compare with course's minimum credit requirement
        if total_credits_earned >= self.courses[self.student.template_course_code]['Total Credits']:
            status = True
        else:
            status = False

        return status,total_credits_earned
    
    def checker(self):
        # Check if student has passed all required modules
        credit_status, earned_credits = self.credit_scores()
        if len(self.outstanding_modules()) == 0:
            if self.elective_modules_requirement():
                required_modules_electives_set, required_modules_set, completed_modules_set = self.lists_to_sets()
                completed_electives = required_modules_electives_set & completed_modules_set
                if len(completed_electives) == 0:
                    print('Not eligible to graduate')
                    print('Reason: You have outstanding elective modules')
                    print("Here are electives to choose from electives:")

                    for elective in self.courses[self.student.template_course_code]['Elective modules']:
                        print(elective)
                        print(" ")
                else:
                    self.results()    
                    '''if credit_status:
                        self.results()
                    else:
                        print('Not eligible to graduate')
                        print(f'Reason: You have not met the minimum credit requirement of  {self.courses[self.student.template_course_code]["Total Credits"]} credits')
                        print(f'You have earned {earned_credits} credits')'''
                        
            else:
                print("THIS COURSE HAS NO ELECTIVES!!")
                self.results()
                '''if credit_status:
                    self.results()
                else:
                    print('Not eligible to graduate')
                    print(f'Reason: You have not met the minimum credit requirement of  {self.courses[self.student.template_course_code]["Total Credits"]} credits')
                    print(f'You have earned {earned_credits} credits')'''
        else:
            print("You have not completed all the required modules for this course")
            print("Here are the outstanding modules: \n" + str(self.outstanding_modules()))

    def student_record(self):
        if len(self.student.completed_modules) != len(self.student.completed_module_names) or \
           len(self.student.completed_modules) != len(self.student.final_marks):
            raise ValueError("Data mismatch: Length of modules, names, and marks lists must be equal.")

        record_str = f"Student initials & Surname: {self.student.student_initials}  Student Number: {self.student.student_number}\n"
        record_str += f"Total Credits: {self.student.total_credits}\n"
        record_str += "Module Code\tModule Name\t\tFinal Mark\n"

        for code, name, mark in zip(self.student.completed_modules, self.student.completed_module_names, self.student.final_marks):
            record_str += f"{code}\t\t{name}\t\t{mark}\n"

        return record_str
