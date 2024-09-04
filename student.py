import pandas as pd

class Student:
    def __init__(self,file_name,file_path):
        self.file_name = file_name
        self.file_path = file_path
        self.dataframe  = pd.read_excel(self.file_name,sheet_name = self.file_path)

        columns_to_fill = ['Final mark', 'Re-Exam', 'aggregate_exam_marks', 'special_results']
        # Replace NaN values with 0 in the specified columns
        for column in columns_to_fill:
            if column in self.dataframe.columns:
                self.dataframe[column] = self.dataframe[column].fillna(0)
            else:
                print(f"Column {column} not found in the dataframe.")

        self.template_course_code = str(self.dataframe.loc[0,'Course code'])
        self.template_course_name = self.dataframe.loc[0,'Course Name']
        self.student_number = self.dataframe.loc[0,'Student Number']
        self.student_initials = self.dataframe.loc[0,'Initials & Surname']
        self.total_credits = int(self.dataframe.loc[0,'Total Credits'])
        self.special_result = self.dataframe.loc[:,'special_results']
        self.aegrotat_exam_marks = self.dataframe.loc[:,'aggregate_exam_marks']
        self.completed_modules = self.dataframe.loc[:,'Modules'].to_list()
        self.completed_module_names = self.dataframe.loc[:,'Module Names'].to_list()
        self.final_marks = self.dataframe.loc[:,'Final mark'].to_list()
        self.re_exam_marks = self.dataframe.loc[:,'Re-Exam'].to_list()

        columns_to_fill = ['Final mark', 'Re-Exam', 'aggregate_exam_marks', 'special_results']
        # Replace NaN values with 0 in the specified columns
        for column in columns_to_fill:
            if column in self.dataframe.columns:
                self.dataframe[column] = self.dataframe[column].fillna(0)
            else:
                print(f"Column {column} not found in the dataframe.")