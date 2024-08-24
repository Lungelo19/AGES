import pandas as pd

class Student:
    def __init__(self,file_name,file_path):
        dataframe  = pd.read_excel(file_name,file_path)
        self.template_course_code = str(dataframe.loc[0,'Course code'])
        self.template_course_name = dataframe.loc[0,'Course Name']
        self.student_number = dataframe.loc[0,'Student Number']
        self.student_initials = dataframe.loc[0,'Initials & Surname']
        self.total_credits = int(dataframe.loc[0,'Total Credits'])
        self.special_result = dataframe.loc[:,'special_results']
        self.aggregate_exam_marks = dataframe.loc[:,'aggregate_exam_marks']
        self.completed_modules = dataframe.loc[:,'Modules'].to_list()
        self.completed_module_names = dataframe.loc[:,'Module Names'].to_list()
        self.final_marks = dataframe.loc[:,'Final mark'].to_list()
        self.re_exam_marks = dataframe.loc[:,'Re-Exam'].to_list()