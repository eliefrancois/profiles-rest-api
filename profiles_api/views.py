from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status # This returns HTTP status codes from API, will use this in post function handler
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from profiles_api import serializers # Will use this to tell API what data to exect when making a POST PUT PATCH request to API
from profiles_api import models
from profiles_api import permissions


class HelloAPiView(APIView): 
    """Test API View"""
    serializer_class =serializers.HelloSerializer # Configures the API view to the serializer class

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methds as function (get, post, patch, put, delete)',
            'Is simiular to tranditional Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs',

        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self,request):
        """Create a hello message with user name"""

        # self.serializer_class is retriving the configured serializer for the view
        serializer= self.serializer_class(data=request.data) 

        # Serializers have the capability to assure the data passed in is valid based on the parameters set in specific serializer, in this case we will check that the data passed in is less than 10 characters
        if serializer.is_valid():
            name = serializer.validated_data.get('name') # This will return the name passed in by user if it is valid
            message =f'Hello {name}'
            return Response({'message': message})
        
        # If the data entered is incorrect then an eror code will be 
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
                )

    def put(self,request, pk=None):  # Pk is primary 
        """Update an exsiting object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Partially update an exsiting object"""
        return Response({'method': 'PATCH'})

    
    def delete(self, request, pk=None):
        """Delete an exsiting object"""
        return Response({'method': 'DELETE'})
 

class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer

    def list(self,request):
        """Return a hello message"""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLS using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message."""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""

        return Response({'http_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating, creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes =(permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'email', )


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class PatientInfoViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating patient info objects"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.PatientInfoSerializer # This points to the
    queryset = models.PatientInfo.objects.all()
    permission_classes = (permissions.UpdateOwnReading, IsAuthenticated,) # Validates that a user is authenticated to read or modify objects
    

    def perform_create(self, serializer): # overridijg this function so that when a user tries to create an object they are validated as the current user
        """Sets the patient profile to the logged in user"""
        serializer.save(user_profile=self.request.user) # This sets the user profile to the current user from the serializer passed in 
