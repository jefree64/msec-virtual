from sqlalchemy import Column, String, Integer, ForeignKey, Time, Date, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from flask_bcrypt import generate_password_hash, check_password_hash
import pyexcel
from sqlalchemy.exc import IntegrityError



db = SQLAlchemy()

Model = db.Model

db.session.add_all()

class base:
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def loadFromFile(cls):
        ...
        

    
@dataclass
class Department(Model, base):
    id = Column(Integer, primary_key = True)
    name: str = Column(Integer, unique=True)
    classes = relationship('Class')

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
    
    @classmethod
    def get_name(cls, id):
        return cls.query.get(id).name or None
    
    @classmethod
    def get_class(cls, dept_id, year):
        return Class.query.filter_by(dept_id = dept_id).filter_by(year = year).first()
        
@dataclass
class Class(Model, base):
    id = Column(Integer, primary_key = True)
    year: int = Column(Integer, nullable=False)
    sem: int = Column(Integer)
    dept_id  = Column(Integer, ForeignKey('department.id'))
    dept_name: str = Column(String, nullable=False)
    subjects = relationship('Subject')
    

    def __init__(self, year, dept_id: int, dept_name: str) -> None:
        super().__init__()
        self.year = year
        self.dept_id = dept_id
        self.dept_name = dept_name

    def add_student(self, student: 'Student') :
        ClassStudents(self.id, student.id).save()
        ...    

    @property
    def students(self):
        studs_id = [cls.stud_id for cls in ClassStudents.query.filter_by(class_id = self.id).all()]
        students = list()
        for id in studs_id:
            stud = Student.query.get(id)
            if stud is not None:
                students.append(stud)
        return students




@dataclass
class Subject(Model, base):
    id = Column(Integer, primary_key=True)
    code: str = Column(String, nullable=False)
    name: str = Column(String)
    class_id = Column(Integer, ForeignKey('class.id'))
    
    def __init__(self, code: str, name: str, class_id: int) :
        self.code = code
        self.name = name
        self.class_id = class_id



@dataclass
class Hod(Model, base): 
    id = Column(Integer, primary_key=True)
    name: str = Column(String)
    email = Column(String, unique=True)
    dept_id = Column(Integer, ForeignKey('department.id'))
    dept_name: str = Column(String)
    dept = relationship('Department', uselist=False)

    def __init__(self, name: str, email: str, dept_id: int, dept_name: str) -> None:
        super().__init__()
        self.name = name
        self.email = email
        self.dept_id = dept_id
        self.dept_name = dept_name
    

@dataclass
class Student(Model, base):
    id = Column(Integer, primary_key=True)
    register_number: int = Column(Integer, unique=True)
    name: str = Column(String)
    dept_id = Column(Integer, ForeignKey('department.id'))
    department: str = Column(String)
    email: str = Column(String)
    mobile_number: str = Column(String)
    
    
    def __init__(self, register_number: int, name: str,dept_id: int, dept_name: str, email: str, mobile_number: str = None) -> None:
        self.register_number = register_number
        self.name = name
        self.email = email
        self.dept_id = dept_id
        self.department = dept_name
        self.mobile_number = mobile_number

    
    

@dataclass
class User(Model, base) :
    id = Column(Integer, primary_key=True)
    password = Column(String)
    role: str = Column('role', String, nullable=False)
    role_id: int = Column('role_id', Integer)
    dept_id = Column(Integer, ForeignKey('department.id'))
    

    def __init__(self, role: str, role_id: str, dept_id: int, password: str | None = None) -> None:
        self.role = role
        self.role_id = role_id
        self.password = generate_password_hash(password) if password else password
        self.dept_id = dept_id

    def verify_password(self, pwd: str) -> bool:
        return True if check_password_hash(self.password, pwd) else False

    def change_password(self, pwd: str) -> None:
        self.password = generate_password_hash(pwd)

    @classmethod
    def get(cls, role: str, role_id: str):
        return cls.query.filter_by(role = role).filter_by(role_id = role_id).first()
    


