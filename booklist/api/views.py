from rest_framework import generics, mixins, filters
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Book
from .serializers import BookModelSerializer
# from rest_framework.decorators import api_view



# RetrieveAPIView
# RetrieveAPIView




class BookAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    # lookup_field = 'pk'
    serializer_class = BookModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, ]
    permission_classes = []
    filterset_fields = ['id', 'title', 'authors_name', 'language_book', ]
    search_fields = ['id', 'title', 'authors_name', 'language_book', ]
    ordering_fields = ['id', 'title', 'authors_name', 'language_book', ]

    def get_queryset(self):
        return Book.objects.all()

    # def get_queryset(self):
    #     qs = Book.objects.all()
    #     query = self.request.GET.get("query")
    #     if query is not None:
    #         qs = qs.filter(
    #             Q(title__icontains=query) |
    #             Q(language_book__icontains=query)|
    #             Q(authors_name__icontains=query)
    #         ).distinct()
    #     return qs


    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

    # def get_queryset(self):
    #     qs = Book.objects.all()
    #     query = self.request.GET.get("q")
    #     if query is not None:
    #         qs = qs.filter(
    #             Q(title__icontains=query) |
    #             Q(content__icontains=query)
    #         ).distinct()
    #     return qs

    # def get_object(self):
    #     id = self.kwargs.get("id")
    #     return Book.objects.get(pk=id)


class BookRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = BookModelSerializer

    def get_queryset(self):
        return Book.objects.all()

    # def get_object(self):
    #     id = self.kwargs.get("id")
    #     return Book.objects.get(pk=id)


# class BooklistRudView(generics.RetrieveUpdateDestroyAPIView):
#     pass
#     lookup_field = 'pk'


#
#








# class BookModelViewSet(viewsets.ModelViewSet):
# 	# queryset = Book.objects.all()
#
# 	serializer_class = BookSerializer
# 	filter_backends = [DjangoFilterBackend]
# 	filterset_fields = ['author', 'year', 'num_of_pages']