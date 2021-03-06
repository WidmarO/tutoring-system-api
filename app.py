import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
import time

from datetime import datetime, timedelta, timezone

# from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
# from flask_jwt_extended import get_jwt
# from flask_jwt_extended import get_jwt_identity
# from flask_jwt_extended import set_access_cookies
# from flask_jwt_extended import unset_jwt_cookies
# from flask_jwt_extended import jwt_required

from models.role import RoleModel
from models.user import UserModel


from models.coordinator import CoordinatorModel
from models.tutoring_program import TutoringProgramModel
from models.new import NewModel
from models.teacher import TeacherModel
from models.principal import PrincipalModel
from models.tutor import TutorModel
from models.student import StudentModel
from models.tutor_student import TutorStudentModel
from models.appointment import AppointmentModel
from models.student_helper import StudentHelperModel
from models.workshop import WorkshopModel
from models.workshop_student import WorkshopStudentModel
from models.student_helper_tutor import StudentHelperTutorModel
from models.workshop_attendance import WorkshopAttendanceModel
from models.curricular_advancement import CurricularAdvancementModel
from models.description_workshop_attendance import DescriptionWorkshopAttendanceModel


# from security import authenticate, identity

from resources.student import StudentList, Student, StudentListTutoringProgram, StudentS, AddStudents, StudentListPrincipal
from resources.coordinator import CoordinatorList, Coordinator
from resources.tutoring_program import TutoringProgramList, TutoringProgram
# from resources.workshop import Workshop, WorkshopList
from resources.documentation import Documentation, Documentation_coordinator,Documentation_principal,Documentation_teacher,Documentation_student,Documentation_tutor
from resources.authenticate import Login, UpdateCredentials, Admin
from resources.teacher import TeacherList, Teacher, AddTeachers, TeacherListTutoringProgram, TeacherListPrincipal
from resources.tutor import TutorList, Tutor, TutorT, TutorListTutoringProgram
from resources.distribute_student import DistributeStudent
from resources.tutor_student import TutorStudentList, TutorStudentT, TutorStudentC
from resources.appointment import AppointmentList, Appointment, AppointmentListTutoringProgram, AppointmentTutor, AppointmentListCoordinator
from resources.filter_teachers_for_tutors import Filter_Tutors_from_Teachers
from resources.principal import Principal, PrincipalList, PrincipalC, PrincipalP
from resources.create_student_accounts import Create_Student_Accounts
from resources.create_tutor_accounts import Create_Tutor_Accounts
from resources.user import User
from resources.update_credentials_coordinator import UpdateCredentialsCoordinator
from resources.user_in_tutoring_program import UserTutoringProgram
from resources.new import New, NewList, NewListCoordinator, NewListTutoringProgram
from resources.user_in_tutoring_program import UserTutoringProgram

app = Flask(__name__)
CORS(app)

# -- Configurations for security

# app.config["JWT_COOKIE_SECURE"] = False
# app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_SECRET_KEY"] = "widmaro"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=45)

jwt = JWTManager(app)

# @app.after_request
# def refresh_expiring_jwts(response):
#     try:
#         claims = get_jwt()
#         exp_timestamp = claims["exp"]
#         now = datetime.now(timezone.utc)
#         target_timestamp = datetime.timestamp(now + timedelta(minutes=4))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(claims['sub'], 
#                                             additional_claims={'role': claims['role'],
#                                                                  'id': claims['id']})
#             set_access_cookies(response, access_token)
#         return response
#     except (RuntimeError, KeyError):
#         # Case where there is not a valid JWT. Just return the original respone
#         return response


# ----------------------------- LOCAL DATABASE
# type_database = 'mysql'
# user_database = 'root'
# pass_database = 'toor' # for wid is toor
# url_database = '127.0.0.1' # for wid is 127.0.0.1  #localhost:3307
# name_database = 'tutoring-system-bd'
# ---------------------------- CLEVER CLOUD DATABASE
type_database = 'mysql'
user_database = 'udwsw0hbqah0nikx'
pass_database = '6eaqlxBNvKWNGUuRR32M'
url_database = 'b0du4ayviyfhrlbnjckc-mysql.services.clever-cloud.com'
name_database = 'b0du4ayviyfhrlbnjckc'

# -- Set de BD configurations for conection
sqlalchemy_database_uri = type_database + '://' + user_database + \
    ':' + pass_database + '@' + url_database + '/' + name_database
app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

# -- RESOURCES OF THE APPLICATION
api.add_resource(Documentation, '/')
api.add_resource(Admin, '/admin')
api.add_resource(Documentation_coordinator, '/documentation_coordinator')
api.add_resource(Documentation_teacher, '/documentation_teacher')
api.add_resource(Documentation_principal, '/documentation_principal')
api.add_resource(Documentation_student, '/documentation_student')
api.add_resource(Documentation_tutor, '/documentation_tutor')
api.add_resource(Student, '/student/<string:cod_student>')
api.add_resource(StudentList, '/student')
api.add_resource(StudentListPrincipal, '/student_list_principal')
api.add_resource(AddStudents, '/addstudents')
api.add_resource(StudentListTutoringProgram, '/student_list/<string:cod_tutoring_program>')
api.add_resource(Teacher, '/teacher/<string:cod_teacher>')
api.add_resource(TeacherList, '/teachers')
api.add_resource(AddTeachers, '/addteachers')
api.add_resource(TeacherListPrincipal, '/teacher_list_principal')
api.add_resource(TeacherListTutoringProgram, '/teacher_list/<string:cod_tutoring_program>')
api.add_resource(Tutor, '/tutor/<string:cod_tutor>')
api.add_resource(TutorList, '/tutors')
api.add_resource(Coordinator, '/coordinator/<string:cod_coordinator>')
api.add_resource(CoordinatorList, '/coordinators')
api.add_resource(TutoringProgram, '/tutoring_program/<string:cod_tutoring_program>')
api.add_resource(TutoringProgramList, '/tutoring_programs')
# api.add_resource(UserRegister, '/register')
api.add_resource(Login, '/login')
api.add_resource(TutorStudentT, '/students')
api.add_resource(TutorStudentC, '/tutor_student/<string:cod_tutor>/<string:cod_tutoring_program>/<string:cod_student>')
api.add_resource(TutorStudentList, '/tutor_students')
api.add_resource(DistributeStudent, '/distribute_students')
api.add_resource(Appointment, '/appointment/<string:cod_appointment>')
api.add_resource(AppointmentList, '/appointments/<string:cod_student>')
api.add_resource(AppointmentTutor, '/student_appointment_list/<string:cod_student>/<string:cod_tutoring_program>')
api.add_resource(AppointmentListTutoringProgram, '/appointment_list/<string:cod_tutoring_program>')
api.add_resource(AppointmentListCoordinator, '/appointment_list_coordinator')
api.add_resource(Filter_Tutors_from_Teachers, '/filter_tutors_from_teachers')
api.add_resource(Principal, '/principal/<string:cod_principal>')
api.add_resource(PrincipalList, '/principals')
api.add_resource(PrincipalC, '/principalC')
api.add_resource(PrincipalP, '/principalP')
api.add_resource(Create_Student_Accounts, '/create_student_accounts')
api.add_resource(Create_Tutor_Accounts, '/create_tutor_accounts')
api.add_resource(StudentS, '/students_update')
api.add_resource(TutorT, '/tutorT')
api.add_resource(User, '/authenticate_user')
api.add_resource(UpdateCredentials, '/update_credentials')
api.add_resource(UpdateCredentialsCoordinator, '/update_credentials_coordinator')
api.add_resource(UserTutoringProgram, '/user_tutoring_program')
api.add_resource(New, '/new/<string:cod_new>')
api.add_resource(NewList, '/news')
api.add_resource(NewListTutoringProgram, '/new_tutoring_program/<string:cod_tutoring_program>')
api.add_resource(NewListCoordinator, '/new_list_coordinator')

# -- Module that create the tables in the BD
# @app.before_first_request
# def create_tables():
#     db.create_all()

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)