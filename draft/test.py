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
    for index in failed_modules:
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