from django import forms
    

"""
Form for the user to enter a coupon code
""" 
class CouponApplyForm(forms.Form):
    code = forms.CharField()