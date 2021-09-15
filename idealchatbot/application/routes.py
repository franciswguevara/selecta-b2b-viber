from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]

class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)

    label_columns = {'contact_group':'Contacts Group'}
    list_columns = ['name','personal_cellphone','birthday','contact_group']

    show_fieldsets = [
        (
            'Summary',
            {'fields': ['name', 'address', 'contact_group']}
        ),
        (
            'Personal Info',
            {'fields': ['birthday', 'personal_phone', 'personal_cellphone'], 'expanded': False}
        ),
    ]

db.create_all()

appbuilder.add_view(
    GroupModelView,
    "List Groups",
    icon = "fa-folder-open-o",
    category = "Contacts",
    category_icon = "fa-envelope"
)

appbuilder.add_view(
    ContactModelView,
    "List Contacts",
    icon = "fa-envelope",
    category = "Contacts"
)