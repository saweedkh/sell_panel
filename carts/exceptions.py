class CartException(Exception):
    def __init__(self, msg='Cart Exception Error', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
