def logger_middleware(get_response):
    print("\033[0;32mload middleware...\033[0m")

    def wrapper(request):
        print("\033[0;32mbefore request.\033[0m")
        response = get_response(request)
        print("\033[0;32mafter request.\033[0m")
        return response

    return wrapper