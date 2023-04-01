from django import forms
from book.models import BookReview


class BookReviewForm(forms.ModelForm):
    RATING_CHOICES = (
        ('5', '5 stars'),
        ('4', '4 stars'),
        ('3', '3 stars'),
        ('2', '2 stars'),
        ('1', '1 stars'),
    )

    stars = forms.ChoiceField(choices=RATING_CHOICES)

    class Meta:
        model = BookReview
        fields = ('stars', 'comment')
