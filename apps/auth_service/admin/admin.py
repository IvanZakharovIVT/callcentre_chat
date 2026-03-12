from starlette.requests import Request
from starlette_admin import PasswordField
from starlette_admin.contrib.sqla import ModelView


class UserAdmin(ModelView):
    column_list = ['uuid', 'username', 'email', 'role',]

    column_searchable_list = ['username', 'email', 'uuid']

    exclude_fields = ['password_hash']
    exclude_fields_from_list = ['password_hash']
    exclude_fields_from_detail = ['password_hash']
    exclude_fields_from_create = ['password_hash']
    exclude_fields_from_edit = ['password_hash']

    form_columns = ['uuid', 'username', 'email', 'password', 'role']

    column_labels = {
        'username': 'Username',
        'email': 'Email Address',
        'uuid': 'UUID',
        'role': 'Role',
        'password': 'Password',
    }

    def get_fields(self, request: Request):
        fields = super().get_fields(request)

        # Find and replace the password field with PasswordField
        for i, field in enumerate(fields):
            if field.name == 'password':
                fields[i] = PasswordField('Password', required=True)
                break

        return fields

