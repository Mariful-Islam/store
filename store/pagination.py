from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StorePagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'pages'

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            # "current_pagination_step": self.get_html_context(),
            "current_page": self.page.number,
            "next_page_url": self.get_next_link(),
            "next_page_number": self.get_next_number(),
            "prev_page_link": self.get_previous_link(),
            "prev_page_number": self.get_previous_number(),
            "results": data
        })
    
    def get_previous_number(self):
        if not self.page.has_previous():
            return None
        
        prev_num = self.page.previous_page_number()
        return prev_num if prev_num >= 1 else None
    

    def get_next_number(self):
        if not self.page.has_next():
            return None
        
        next_num = self.page.next_page_number()
        return next_num if next_num >=1 else None
