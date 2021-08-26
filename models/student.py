from db import db

class StudentModel(db.Model):
    __tablename__ = 'students'
    
    cod_student = db.Column(db.String(6), primary_key=True, unique = True)
    name = db.Column(db.String(60), nullable=False)
    f_lastname = db.Column(db.String(40))
    m_lastname = db.Column(db.String(40))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    reference_person = db.Column(db.String(200))
    phone_reference_person = db.Column(db.String(20))
    cod_tutoring_program = db.Column(db.String(6), db.ForeignKey('tutoring_programs.cod_tutoring_program'))

    def __init__(self, cod_student, name, f_lastname, m_lastname, phone, email, reference_person, phone_reference_person, cod_tutoring_program):
        self.cod_student = cod_student
        self.name = name
        self.f_lastname = f_lastname
        self.m_lastname = m_lastname
        self.phone = phone
        self.email = email
        self.reference_person = reference_person
        self.phone_reference_person = phone_reference_person
        self.cod_tutoring_program = cod_tutoring_program

    def json(self):
        return {'cod_student': self.cod_student,
                'name': self.name,
                'f_lastname': self.f_lastname,
                'm_lastname': self.m_lastname,
                'phone': self.phone,
                'email': self.email,
                'reference_person' : self.reference_person,
                'phone_reference_person' : self.phone_reference_person,
                'cod_tutoring_program' : self.cod_tutoring_program
                }

    def update_data(self, cod_student, name, f_lastname, m_lastname, phone, email, reference_person, phone_reference_person, cod_tutoring_program):
        self.cod_student = cod_student
        self.name = name
        self.f_lastname = f_lastname
        self.m_lastname = m_lastname
        self.phone = phone
        self.email = email
        self.reference_person = reference_person
        self.phone_reference_person = phone_reference_person
        self.cod_tutoring_program = cod_tutoring_program

    @classmethod
    def find_by_cod_student(cls, _cod_student):
        # -> SELECT * FROM items where cod_student=cod_student LIMIT 1
        return cls.query.filter_by(cod_student=_cod_student).first()


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
