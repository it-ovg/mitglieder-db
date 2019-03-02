class CORSMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.META)
        
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["mein-heDDader"] = "bipo"
        print("aha, middleware also")

        return response