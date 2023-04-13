from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import BookReviewSerializer
from book.models import Book, BookReview


# class BookReviewViewSet(ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = BookReview.objects.all().order_by('id')
#     serializer_class = BookReviewSerializer
#     lookup_field = 'id'


class BookListReviewApiView(APIView):
    def get(self, request):
        bookreviews = BookReview.objects.all().order_by('-id')
        paginator = PageNumberPagination()
        pagination = paginator.paginate_queryset(bookreviews, request)
        serializer = BookReviewSerializer(pagination, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, reqeust):
        serializer = BookReviewSerializer(data=reqeust.data)
        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookReviewDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        review = BookReview.objects.get(id=id)
        serializer = BookReviewSerializer(review)

        return Response(data=serializer.data)

    def put(self, request, id):
        review = BookReview.objects.get(id=id)
        serializer = BookReviewSerializer(instance=review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        review = BookReview.objects.get(id=id)
        serializer = BookReviewSerializer(instance=review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        review = BookReview.objects.get(id=id)
        review.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

