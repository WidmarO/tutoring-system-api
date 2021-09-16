from flask_restful import Resource
from flask import request
from models.tutor import TutorModel
from models.tutoring_program import TutoringProgramModel
from models.teacher import TeacherModel
from Req_Parser import Req_Parser
from flask_jwt_extended import jwt_required, get_jwt


class Tutor(Resource):
    parser = Req_Parser()    
    parser.add_argument('cod_tutor', str, True)
    parser.add_argument('cod_teacher', str, True)
    parser.add_argument('cod_tutoring_program', str, True)
    parser.add_argument('schedule', str)
    parser.add_argument('place')

    def put(self, cod_tutor):
        # Verify if all arguments are correct
        ans, data = TutorList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Verify if tutor exists in database
        tutor = TutorModel.find_by_cod_tutor(cod_tutor)
        if tutor:
            tutor.update_data(**data)
            tutor.save_to_db()
            return tutor.json(), 200

        return {'message': 'Tutor not found.'}, 404

    def get(self, cod_tutor):
        # Return a teacher if found in database
        tutor = TutorModel.find_by_cod_tutor(cod_tutor)
        if tutor:
            return tutor.json(), 200
        return {'message': 'Tutor not found'}, 404

    # @jwt_required()
    def delete(self, cod_tutor):

        # Delete a tutor from database if exist in it
        tutor = TutorModel.find_by_cod_tutor(cod_tutor)
        if tutor:
            tutor.delete_from_db()
            return tutor.json(), 200

        # Return a messagge if not found
        return {'message': 'Teacher not found.'}, 404

class TutorT(Resource):
    parser = Req_Parser()    
    parser.add_argument('phone')
    parser.add_argument('filiation', str, True)
    parser.add_argument('category', str, True)

    @jwt_required()
    def put(self):

        claims = get_jwt()
        if claims['role'] != 'tutor':
            return {'message': 'You are not allowed to do this'}, 401
            
        # Verify if all arguments are correct
        ans, data = TutorT.parser.parse_args(dict(request.json))
        if not ans:
            return data

        email_tutor = claims["sub"]
        
        # Create tutoring program in relation at tutoring program active.
        tutoring_program = TutoringProgramModel.find_tutoring_program_active()
        
        # Create teacher and Verify if teacher exits in database 
        teacher = TeacherModel.find_email_in_tutoring_program(email_tutor, tutoring_program.cod_tutoring_program)
        if not teacher:
            return {"message": "Teacher not found."}, 404
        tutor = TutorModel.find_teacher_in_tutoring_program(tutoring_program.cod_tutoring_program, teacher.cod_teacher)

        # Add student's code to data
        data['cod_teacher'] = teacher.cod_teacher 
        
        # Verify if tutor exists in database
        if tutor:
            teacher.update_data_Tutor(**data)
            teacher.save_to_db()
            return teacher.json(), 200

        return {'message': 'Tutor not found.'}, 404


class TutorList(Resource):
    parser = Req_Parser()    
    parser.add_argument('cod_tutor', str, True)
    parser.add_argument('cod_teacher', str, True)
    parser.add_argument('cod_tutoring_program', str, True)
    parser.add_argument('schedule', str)
    parser.add_argument('place')
    
    # @jwt_required()
    def get(self):
        # Return all teachers in database        
        sort_tutors = [ tutor.json() for tutor in TutorModel.find_all() ]
        sort_tutors = sorted(sort_tutors, key=lambda x: x[list(sort_tutors[0].keys())[0]])
        
        return sort_tutors, 200


    def post(self):

        # Verify if all attributes are in request and are of corrects type
        ans, data = TutorList.parser.parse_args(dict(request.json))
        if not ans:
            return data

        # Verify if teacher already exists in database
        cod_tutor = data['cod_tutor']        
        if TutorModel.find_by_cod_tutor(cod_tutor):
            return {'message': "A tutor with cod_tutor: '{}' already exist".format(cod_tutor)}

        # Create a instance of TeacherModel with the data provided
        tutor = TutorModel(**data)

        # Try to insert the teacher in database
        try:
            tutor.save_to_db()
        except:
            return {'message': "An error ocurred when adding the tutor in DB"}, 500

        # Return the student data with a status code 201
        return tutor.json(), 201

