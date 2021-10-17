from wtforms import Form, IntegerField


class Login(Form):
    id = IntegerField()
