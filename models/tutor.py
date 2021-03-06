from db import db

class TutorModel(db.Model):
    __tablename__ = 'tutors'
    
    # -- Attributes --
    cod_tutor = db.Column(db.String(6), primary_key=True)
    cod_teacher = db.Column(db.String(6), db.ForeignKey('teachers.cod_teacher'), primary_key=True)
    cod_tutoring_program = db.Column(db.String(6), db.ForeignKey('tutoring_programs.cod_tutoring_program'), primary_key=True)
    schedule = db.Column(db.String(250))
    place = db.Column(db.String(100)) 

    # -- Relations --
    appointment = db.relationship('AppointmentModel')
    student_helper_tutor = db.relationship('StudentHelperTutorModel') 
    tutor_student = db.relationship('TutorStudentModel')

    def __init__(self, cod_tutor, cod_teacher, cod_tutoring_program, schedule, place):
        self.cod_tutor = cod_tutor
        self.cod_teacher = cod_teacher
        self.cod_tutoring_program = cod_tutoring_program
        self.schedule = schedule
        self.place = place


    def json(self):
        return {'cod_tutor': self.cod_tutor,
                'cod_teacher': self.cod_teacher,
                'cod_tutoring_program': self.cod_tutoring_program,
                'schedule': self.schedule,
                'place': self.place
                }

    def update_data(self, cod_tutor, cod_teacher, cod_tutoring_program, schedule, place):
        self.cod_tutor = cod_tutor
        self.cod_teacher = cod_teacher
        self.cod_tutoring_program = cod_tutoring_program
        self.schedule = schedule
        self.place = place

    @classmethod
    def find_by_cod_tutor(cls, _cod_tutor):
        # -> SELECT * FROM items where cod_coordinator=cod_coordinator LIMIT 1
        return cls.query.filter_by(cod_tutor=_cod_tutor).first()

    @classmethod
    def find_teacher_in_tutoring_program(cls, _cod_tutoring_program, _cod_teacher):
        # -> SELECT * FROM items where cod_tutoring_program=cod_tutoring_program LIMIT 1
        return cls.query.filter_by(cod_tutoring_program=_cod_tutoring_program).filter_by(cod_teacher=_cod_teacher).first()

    @classmethod
    def find_by_cod_tutoring_program(cls, _cod_tutoring_program):
        # -> SELECT * FROM items where dni=dni LIMIT 1
        return cls.query.filter_by(cod_tutoring_program=_cod_tutoring_program)

    @classmethod
    def find_all(cls):
        # -> SELECT * FROM items
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()