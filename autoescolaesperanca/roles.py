from rolepermissions.roles import AbstractUserRole

class Admin(AbstractUserRole):
    available_permissions = {
        'admin': True,
        'secretary': True,
        'instructor': True,
        'student': True
    }

class Secretary(AbstractUserRole):
    available_permissions = {
        'secretary': True,
        'instructor': True,
        'student': True
    }

class Instructor(AbstractUserRole):
    available_permissions = {
        'instructor': True,
        'student': True
    }

class Student(AbstractUserRole):
    available_permissions = {
        'student': True
    }
