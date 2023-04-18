from book.models import Book, BookReview


def context_function(request):
    pass
    # reviews = BookReview.objects.get(user=request.user)
    #
    # context = {'my_books_reviews': reviews}
    #
    # return context

