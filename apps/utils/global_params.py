def previous_page(request):
    pre_page = request.META.get('HTTP_REFERER', "/")
    return {'pre_page': pre_page}
