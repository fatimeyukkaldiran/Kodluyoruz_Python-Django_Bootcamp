from django import forms

class LoginForm(forms.Form):
    username = forms.EmailField(
        label='User Name', max_length=100, 
        help_text="Please Enter Email",
    )
    password = forms.CharField(
        label="Enter Password",
        max_length=100,
        help_text="Enter Password Again",
        widget=forms.PasswordInput()
    )
    # tcno = forms.IntegerField(
    #     label="Tc No Gir",
    #     min_value=10000000000,
    #     max_value=99999999999
    # )
    
    