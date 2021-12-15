from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from ..serializers.blog import BlogSerializer
from ..models.blog import Blog

class BlogsView(APIView):
    def post(self, request):
        # Add the user id as owner
        request.data['author'] = request.user.id
        blog = BlogSerializer(data=request.data)
        if blog.is_valid():
            blog.save()
            return Response(blog.data, status=status.HTTP_201_CREATED)
        else:
            return Response(blog.errors, status=status.HTTP_400_BAD_REQUEST)  

    def get(self, request):
        # filter for mangos with our user id
        blogs = Blog.objects.filter(author=request.user.id)
        data = BlogSerializer(blogs, many=True).data
        return Response(data)

class BlogView(APIView):
    def delete(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        # Check the mango's owner against the user making this request
        if request.user != blog.author:
            raise PermissionDenied('Unauthorized, you are not the owner of this blog post.')
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        if request.user != blog.author:
            raise PermissionDenied('Unauthorized, you are not the owner of this blog post.')
        data = BlogSerializer(blog).data
        return Response(data)
    
    def patch(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        # Check the mango's owner against the user making this request
        if request.user != blog.author:
            raise PermissionDenied('Unauthorized, you are not the owner of this blog post.')
        # Ensure the owner field is set to the current user's ID
        request.data['author'] = request.user.id
        updated_blog = BlogSerializer(blog, data=request.data, partial=True)
        if updated_blog.is_valid():
            updated_blog.save()
            return Response(updated_blog.data)
        return Response(updated_blog.errors, status=status.HTTP_400_BAD_REQUEST)