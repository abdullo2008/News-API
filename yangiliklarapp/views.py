from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import NewsModel, Category
from .serializers import NewsSerializer, CategorySerializer


# class NewsAPIView(generics.ListAPIView):
#     queryset = NewsModel.objects.all()
#     serializer_class = NewsSerializer


class NewsAPIView(APIView):
    def get(self, request):
        news = NewsModel.objects.all()
        serializers_data = NewsSerializer(news, many=True).data
        data = {
            'status': True,
            'request': f'Returned {len(serializers_data)} news',
            'news': serializers_data
        }

        return Response(data)


# class NewsRetrieveView(generics.RetrieveAPIView):
#     queryset = NewsModel.objects.all()
#     serializer_class = NewsSerializer


class NewsRetrieveView(APIView):
    def get(self, request, pk):
        try:
            news = NewsModel.objects.filter(id=pk)
            serializer_data = NewsSerializer(news)
            if serializer_data.is_valid():
                data = {
                    'status': True,
                    'news': serializer_data.data
                }
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                return Response(data='Invalid data', status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(data={'status': False,
                                  'message': 'News is not found'}, status=status.HTTP_404_NOT_FOUND)


# class NewsCreateAPIView(generics.CreateAPIView):
#     queryset = NewsModel.objects.all()
#     serializer_class = NewsSerializer


class NewsCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Create a new news",
        request_body=NewsSerializer,
        responses={201: NewsSerializer()}
    )
    def post(self, request):
        request_data = request.data
        serializer = NewsSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'status': True,
                'message': f'{len(request_data)} new/news saved to the database',
                'new': request_data
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'status': False,
                'message': serializer.error_messages
            }, status=status.HTTP_400_BAD_REQUEST)


# class NewsUpdateAPIView(generics.UpdateAPIView):
#     queryset = NewsModel.objects.all()
#     serializer_class = NewsSerializer


class NewsUpdateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Update a news item",
        request_body=NewsSerializer,
        responses={200: NewsSerializer()},
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description="ID of the news item to update",
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def put(self, request, pk):
        try:
            news = NewsModel.objects.get(id=pk)
        except NewsModel.DoesNotExist:
            return Response(
                data={'status': False, 'message': 'News item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = NewsSerializer(news, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'status': True,
            'message': f"{len(serializer.data)} new updated",
            'new': serializer.data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Partially update a news item",
        request_body=NewsSerializer,
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description="ID of the news item to partially update",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={200: NewsSerializer()}
    )
    def patch(self, request, pk):
        try:
            news = NewsModel.objects.get(id=pk)
        except NewsModel.DoesNotExist:
            return Response(
                data={'status': False, 'message': 'News item not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = NewsSerializer(news, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            data = {
                'status': True,
                'message': "News item partially updated",
                'new': request.data
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(
                data={'status': False, 'message': None, 'not found': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk):
        try:
            news = NewsModel.objects.get(id=pk)
            news.delete()
            return Response(
                data={'status': True, 'message': 'News item deleted'},
                status=status.HTTP_204_NO_CONTENT
            )
        except NewsModel.DoesNotExist:
            return Response(
                data={'status': False, 'message': 'News item not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class NewsDeleteAPIView(generics.DestroyAPIView):
    queryset = NewsModel.objects.all()
    serializer_class = NewsSerializer


# class NewsDeleteAPIView(APIView):
#     def delete(self):


# class CategoryAPIView(generics.ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


class CategoryListCreateAPIView(APIView):
    def get(self, request):
        category = Category.objects.all()
        serializers_data = CategorySerializer(category, many=True).data
        data = {
            'status': True,
            'request': f'Returned {len(serializers_data)} news',
            'category': serializers_data
        }

        return Response(data)

    @swagger_auto_schema(
        operation_description="Create a new category",
        request_body=CategorySerializer,
        responses={201: CategorySerializer()}
    )
    def post(self, request):
        request_data = request.data
        serializer = CategorySerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'status': True,
                'message': f'{len(request_data)} category saved to the database',
                'category': request_data
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'status': False,
                'message': serializer.error_messages
            }, status=status.HTTP_400_BAD_REQUEST)


# class CategoryCreateAPIView(generics.ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


# class CategoryUpdateAPIView(generics.UpdateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
#
# class CategoryDeleteAPIView(generics.DestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


class CategoryUpdateDeleteAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Update a category",
        request_body=CategorySerializer,
        responses={200: CategorySerializer()},
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description="ID of the category to update",
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def put(self, request, pk):
        try:
            category = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            return Response(
                data={'status': False, 'message': 'Category item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'status': True,
            'message': f"{len(serializer.data)} category updated",
            'category': serializer.data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    # @swagger_auto_schema(
    #     operation_description="Partially update a category item",
    #     request_body=CategorySerializer,
    #     manual_parameters=[
    #         openapi.Parameter(
    #             name='id',
    #             in_=openapi.IN_PATH,
    #             description="ID of the category to partially update",
    #             type=openapi.TYPE_INTEGER
    #         )
    #     ],
    #     responses={200: CategorySerializer()}
    # )
    # def patch(self, request, pk):
    #     try:
    #         category = Category.objects.get(id=pk)
    #     except Category.DoesNotExist:
    #         return Response(
    #             data={'status': False, 'message': 'Category not found'},
    #             status=status.HTTP_404_NOT_FOUND
    #         )
    #
    #     serializer = CategorySerializer(category, data=request.data, partial=True)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         data = {
    #             'status': True,
    #             'message': "Category partially updated",
    #             'category': request.data
    #         }
    #         return Response(data=data, status=status.HTTP_200_OK)
    #     else:
    #         return Response(
    #             data={'status': False, 'message': None, 'not found': serializer.errors},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    def delete(self, request, pk):
        try:
            category = Category.objects.get(id=pk)
            category.delete()
            return Response(
                data={'status': True, 'message': 'Category deleted'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Category.DoesNotExist:
            return Response(
                data={'status': False, 'message': 'Category not found'},
                status=status.HTTP_404_NOT_FOUND
            )