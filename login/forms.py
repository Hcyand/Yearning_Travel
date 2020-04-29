from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput())
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput())
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput())
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput())
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput())
    sex = forms.ChoiceField(label="性别", choices=gender)
    address = forms.CharField(label="地址", max_length=256, widget=forms.TextInput())


class SearchForm(forms.Form):
    title = forms.CharField(label='标题', max_length=128, widget=forms.TextInput())
    body = forms.TextInput()
    picture = forms.ImageField()


class CommentForm(forms.Form):
    name = forms.CharField(label="主题", max_length=128, widget=forms.TextInput())
    content = forms.CharField(label='分享', max_length=256)
    type = forms.CharField(label='类型', max_length=128)


class PersonalityForm(forms.Form):
    problem_one = forms.IntegerField(label="问题一")
    problem_two = forms.IntegerField(label="问题二")
    problem_three = forms.IntegerField(label="问题三")