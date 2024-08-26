from Data_Source import Courses


class Validator:
    def __init__(self, student,Courses):
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
        for final_mark, module in zip(self.student.final_marks, self.student.template_course_name):
            if final_mark >= 50:
                results.append((True, "Passed",module))
            elif 40 <= final_mark < 50:
                results.append((False,"eligable for re-exam",module))
            elif final_mark == 0:
                results.append((False, "absent",module))
            else:
                results.append((False, "Failed",module))
            
        return results
    

    def re_exam(self):
        main_results =  self.final_mark_validator()
        re_exam_results = []

        if len(self.student.re_exam_marks) != len(self.student.completed_modules):
            raise ValueError("The number of re-exam marks must be equal to the number of completed modules")
        for i in range(len(self.student.re_exam_marks)):
            if isinstance(self.student.re_exam_marks[i], (int, float)):
                if not 0 <= self.student.re_exam_marks[i] <= 50:
                    raise ValueError(f"Re-exam mark at index {i} must be between 0 and 50")
                
        for  i,result  in enumerate(main_results):
            if result[0] == False and result[1] == "eligable for re-exam":
                if self.student.re_exam_marks[i] == 50:
                    re_exam_results.append((True,'re-exam passed',result[2]))
                else:
                    re_exam_results.append((True,'re-exam passed',result[2]))
        return  re_exam_results
                    

  
    def aegrotat_exam_validator(self):
        if not hasattr(self.student, 'aegrotat_exam_marks'):
            return []  # No aegrotat exams to validate

        aegrotat_exam_results = []
        
        if len(self.student.aegrotat_exam_marks) != len(self.student.completed_modules) or \
        len(self.student.aegrotat_exam_marks) != len(self.student.completed_module_names):
            raise ValueError("Data mismatch: Length of aegrotat exam marks, module codes, and module names lists must be equal.")

        main_results = self.final_mark_validator()

        for i, main_result in enumerate(main_results):
            if main_result[1] == "absent" and self.student.aegrotat_exam_marks[i] != 0:
                aegrotat_exam_mark = self.student.aegrotat_exam_marks[i]
                if not isinstance(aegrotat_exam_mark, (int, float)):
                    raise ValueError(f"aegrotat exam mark at index {i} must be a number.")
                if not 0 <= aegrotat_exam_mark <= 50:
                    raise ValueError(f"aegrotat exam mark at index {i} must be between 0 and 50.")
                
                if aegrotat_exam_mark == 50:
                    aegrotat_exam_results.append((True, "Passed aegrotat exam"))
                else:
                    aegrotat_exam_results.append((True, "Failed aegrotat exam"))

        return aegrotat_exam_results

    def special_exam_results(self):
        # Get results from various validators
        main_exam = self.final_mark_validator()
        re_exam = self.re_exam()
        aegrotat_exam = self.aegrotat_exam_validator()

        # Combine all results into a single list
        combined_results = re_exam + aegrotat_exam + main_exam

        special_exam_results = []

        # Identify failed modules
        failed_modules = [i for i, result in enumerate(combined_results) 
                        if not result[0] and (result[1] in ["Failed", "re-exam failed", "Failed aegrotat exam"])]

        # Process special exam qualification
        if len(failed_modules) <= 2:
            for i in failed_modules:
                # Ensure index is within bounds
                if i < len(self.student.special_result):
                    special_exam_mark = self.student.special_result[i]

                    # Validate special exam mark
                    if not isinstance(special_exam_mark, (int, float)):
                        raise ValueError(f"Special exam mark at index {i} must be a number.")
                    
                    # Determine if the student passed or failed the special exam
                    if special_exam_mark == 50:
                        special_exam_results.append((True, 'Special Exam passed'))
                    elif 1 <= special_exam_mark < 50:
                        special_exam_results.append((False, 'Special Exam failed'))
                    else:
                        raise ValueError(f"Special exam mark at index {i} must be between 1 and 50.")
                else:
                    raise IndexError(f"Index {i} is out of bounds for special exam results.")

        return special_exam_results



    def results(self):

        """
        Evaluates a student's results based on final marks, re-exams, aegrotat exams, and special exams.

        Returns:
            bool: True if the student passed all modules, False otherwise.
        """

        # Validate input data
        self.final_mark_validator()
        self.re_exam()
        self.aegrotat_exam_validator()

        # Get results from all functions
        main_results = self.final_mark_validator()
        re_exam_results = self.re_exam()
        aegrotat_exam_results = self.aegrotat_exam_validator()
        special_exam_results = self.special_exam_results()
        passed = True
        # Combine all results
        combined_results = main_results + re_exam_results + aegrotat_exam_results + special_exam_results

        # Check if any result is a failure
        for result in combined_results:
            if not result[0] and result[1] in ["Failed", "re-exam failed", "Failed aegrotat exam", "Special Exam failed"]:
                passed = False

        # Display overall pass/fail status
        print(passed)
        if passed :
            print("The student passed all modules.")
        else:
            print("The student failed some modules.")
        





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
