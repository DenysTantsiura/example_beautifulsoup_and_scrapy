from mongoengine import Document
from mongoengine.fields import (
    ListField, 
    StringField, 
    ReferenceField
)


class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField()
    author = ReferenceField(Author)  # не рядком, а Reference fields полем, де зберігається ObjectID з колекції authors
    quote = StringField()
