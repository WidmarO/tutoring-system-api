from flask_restful import Resource
from flask import request
from models.student import StudentModel
from models.user import UserModel
from models.tutoring_program import TutoringProgramModel
from Req_Parser import Req_Parser


class Create_Student_Accounts(Resource):

    parser = Req_Parser()    
    parser.add_argument('student_list', list, True)

    def put(self):
        # Return a teacher if found in database
        # ans, data = Filter_Tutors_from_Teachers.parser.parse_args(dict(request.json))
        # if not ans:
        #     return data

        data = dict(request.json)

        for student in data['student_list']:
            student_user = UserModel.find_by_username(student['email'])
            if not student_user:
                student_user  = UserModel(student['email'], student['email'], 'student')
                # student_user  = UserModel(student['email'], self.create_password_student, 'student')
                try:
                    student_user.save_to_db()
                except:
                    return {'message': 'An error ocurred while trying add User in DB'} , 500
        student_account_list = [ student_user.json() for student_user in UserModel.find_by_role('student')]
        student_account_list = sorted(student_account_list, key=lambda x: x[list(student_account_list[0].keys())[0]])
    
        return student_account_list, 200

    def create_password_student(self):
        list_student_accounts = UserModel.find_by_role('student')
        list_student_accounts = [ student_account.json() for student_account in list_student_accounts]
        list_student_accounts = sorted(list_student_accounts, key=lambda x: x[list(list_student_accounts[0].keys())[0]])
        if len(list_student_accounts) == 0 :
            return 'S000001'
        string = list_student_accounts[-1]['username']
        string = string[:6]
        code = str(string)
        new_code = '{:>00}'.format(str('S')) + code
        return new_code