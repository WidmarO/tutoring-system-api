from db import db

class PrincipalsModel(db.Model):
    _tablename_ = 'principals'
    
    # cod_principal varchar(6),
	# cod_teacher varchar(6),
	# cod_tutoring_program varchar(6),
	# primary Key(cod_principal),
	# foreign key(cod_teacher) references teachers(cod_teacher),
	# foreign key(cod_tutoring_program) references tutoring_programs(cod_tutoring_program)

    cod_principal = db.Column(db.String(6), primary_key=True)
    cod_teacher = db.Column(db.String(6), db.ForeignKey('teacher.cod_teacher'))
    cod_tutoring_program = db.Column(db.String(6), db.ForeignKey('tutoring_programs.cod_tutoring_program'))

    #relation
    
    #cod_coordinator = db.relationship('Tutoring_ProgramModel')

    def _init_(self, cod_principal, cod_teacher, cod_tutoring_program):
        self.cod_principal = cod_principal
        self.cod_teacher = cod_teacher
        self.cod_tutoring_program = cod_tutoring_program


    def json(self):
        return {'cod_principal': self.cod_principal,
                'cod_teacher': self.cod_teacher,
                'cod_tutoring_program': self.cod_tutoring_program,
                }

    def update_data(self, cod_principal, cod_teacher, cod_tutoring_program):
        self.cod_principal = cod_principal
        self.cod_teacher = cod_teacher
        self.cod_tutoring_program = cod_tutoring_program

    @classmethod
    def find_by_cod_principal(cls, _cod_principal):
        # -> SELECT * FROM items where cod_coordinator=cod_coordinator LIMIT 1
        return cls.query.filter_by(cod_principal=_cod_principal).first()
    
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