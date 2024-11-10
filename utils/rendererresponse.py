'''
 Custom return processing
'''

# Import the class of the JSON format returned
from rest_framework.renderers import JSONRenderer


class customrenderer(JSONRenderer):
    # Reconstruct the render method
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:

            # print(renderer_context)
            # print(renderer_context["response"].status_code)

            #      , success, and wrong are this
            # Successful and exception response information, exception information has been processed as {'Message': 'Error'} in the previous custom exception processing
            # print(data)

            # If the returned DATA is a dictionary
            if isinstance(data, dict):
                # Response Information There are two keys in Message and Code, get Message and Code in the response information, and delete these two keys in the original DATA, put them in custom response information.
                # In response information, the MSG content is changed to the status code that requests success code changed to request.
                msg = data.pop('message', 'Request success')
                code = data.pop('code', renderer_context["response"].status_code)
            # If it is not a dictionary, change the MSG content to request success code to change the status code for request.
            else:
                msg = 'Request success'
                code = renderer_context["response"].status_code

            # Custom returned format
            ret = {
                'msg': msg,
                'code': code,
                'data': data,
            }
            # Return JSON data
            return super().render(ret, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
