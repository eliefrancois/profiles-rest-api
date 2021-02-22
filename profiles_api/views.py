from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status # This returns HTTP status codes from API, will use this in post function handler

from profiles_api import serializers # WIll use this to tell API what data to exect when making a POST PUT PATCH request to API

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
 