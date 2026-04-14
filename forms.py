from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

# Форма для статей
class ArticleForm(FlaskForm):
    title = StringField("Название статьи", validators=[DataRequired(), Length(max=100)])
    intro = StringField("Краткое описание", validators=[DataRequired(), Length(max=300)])
    text = TextAreaField("Полный текст", validators=[DataRequired()])
    submit = SubmitField("Опубликовать")

# Форма для входа
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")

# Форма для регистрации
class RegisterForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField("Повтор пароля", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Зарегистрироваться")
