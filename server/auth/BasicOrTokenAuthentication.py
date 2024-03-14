from rest_framework.authentication import BasicAuthentication, BaseAuthentication, TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from node.models import Node
from base64 import b64decode


class BasicOrTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Check if basic authentication credentials are provided
        basic_auth = request.headers.get('Authorization')
        sender_host = request.META.get('HTTP_HOST', '')
        sender_host = "http://" + sender_host + "/"
        # print(basic_auth)
        # print(sender_host)
        if basic_auth:
            print("Basic auth provided")
            # Parse basic auth header
            try:
                auth_type, auth_string = basic_auth.split()
                if auth_type.lower() == 'basic':
                    username, password = b64decode(auth_string.encode()).decode().split(':')
                    # print("Basic auth found", sender_host, username, password)
                    # check if the user exists in the database
                    node = Node.objects.get(host=sender_host, username=username, password=password, isActive=True)
                    # if authentication is successful, return success response
                    if node:
                        print("Basic auth successful")
                        return (node, None)
                    else:
                        # If the user does not exist, return failure response
                        print("Basic auth failed")
                        return None
                        
            except:
                pass  # If parsing fails or credentials are incorrect, proceed to token authentication
        
        # If basic authentication fails or is not provided, try token authentication
        token_auth = TokenAuthentication()
        try:
            user, token = token_auth.authenticate(request)
            if user is None:
                raise AuthenticationFailed('Unauthorized')  # Return unauthorized response
            return user, token
        except:
            raise AuthenticationFailed('Unauthorized')