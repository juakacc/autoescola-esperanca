from rolepermissions.roles import AbstractUserRole

class Secretary(AbstractUserRole):
    available_permissions = {
        'secretary': True
    }
