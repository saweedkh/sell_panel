# Customization process
from rest_framework.views import exception_handler
from rest_framework.views import Response
from rest_framework import status


# Whether the exception handler will only be called only for the response generated by the exciting exception. It does not use any response to the view directly returned
# 4 4 5 5 5 5
# Require this exception handling method in Setting, and the Respose object returned by the exception also passes to the renderer class in the JSON of the default, in the DEFAULT_RENDERER_CLASSES in the DRF configuration in Setting
# If there is no declaration, the default mode will be used, as follows
#
# REST_FRAMEWORK = {
#     'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler'
# }
#   below is the already customized process I have configured
# REST_FRAMEWORK = {
# # Globally configure an exception module
#     'EXCEPTION_HANDLER': 'utils.exception.custom_exception_handler',
# # Modify the default returns a class of renderer
#     'DEFAULT_RENDERER_CLASSES': (
#         'utils.rendererresponse.customrenderer',
#     ),
# }
def custom_exception_handler(exc, context):
    # First invoke REST Framework default abnormal processing method to get a standard error response object
    response = exception_handler(exc, context)
    #Print (EXC) # Error Cause You can also do more detailed reasons, by judging the EXC information type
    #Print (Context) # Error message
    # print('1234 = %s - %s - %s' % (context['view'], context['request'].method, exc))
    #print(response)


    # If the response response object is empty, set the value of the MESSAGE, and set the status code to 500
    # If the response response object is not empty, set the value of the message of the message, and will use its own status code
    if response is None:
        return Response({
            'message': f'Server error: {exc}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)

    else:
        # print('123 = %s - %s - %s' % (context['view'], context['request'].method, exc))
        return Response({
            'message': f'Server error: {exc}',
        }, status=response.status_code, exception=True)

    return response