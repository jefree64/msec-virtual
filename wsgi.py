from backend import create_app
from backend.models import Student, User
import config


app = create_app(config.Config)


def db():
    with app.app_context():
        student = [
            Student(register_number=9115021205302, name="hisbullah", department='it', email="aidenxhisbullah@gmail.com"),
            Student(register_number=9115021205305, name="hesbullah", department='it', email="mohamed.hisbullah.com@gmail.com"),
            Student(register_number=9115021205304, name="hasbullah", department='it', email="hisbullah2002k@gmail.com")
        ]
        for i in student:
            i.save()


print('Start')

if __name__ == "__main__":
    app.run()