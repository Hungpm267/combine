# apps/api/exception_handler.py

from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    """
    tùy chỉnh cho mọi lỗi API trc khi đư a đén client
    """
    
    # 1. Lấy response lỗi tiêu chuẩn của DRF (ví dụ: {"detail": "Not found."})
    response = exception_handler(exc, context)

    # 2. Nếu response là None (thường là lỗi 500 Server Error)
    if response is None:
        # Bạn có thể log lỗi 'exc' và 'context' ở đây để debug
        # print(f"LỖI NGHIÊM TRỌNG: {exc}") 
        
        return Response(
            {
                "status_code": 500,
                "message": "Đã có lỗi hệ thống xảy ra, vui lòng thử lại sau."
                # "details": str(exc) # Chỉ bật 'details' khi debug
            },
            status=500
        )

    # 3. Nếu là lỗi đã biết (4xx), chúng ta re-format nó
    
    error_message = "Đã có lỗi xảy ra." # Thông báo chung
    
    # Cố gắng lấy thông báo lỗi chi tiết hơn từ data của DRF
    if isinstance(response.data, dict):
        if 'detail' in response.data:
            error_message = response.data['detail']
        elif 'notify' in response.data:
            error_message = response.data['notify']
        elif 'error' in response.data:
            error_message = response.data['error']
        else:
            # Xử lý lỗi validation (ví dụ: {"name": ["This field is required."]})
            try:
                first_key = next(iter(response.data)) # Lấy key đầu tiên (vd: "name")
                first_error_list = response.data[first_key]
                if isinstance(first_error_list, list):
                    error_message = f"{first_key}: {first_error_list[0]}"
                else:
                    error_message = f"{first_key}: {first_error_list}"
            except StopIteration:
                pass # Giữ message chung

    elif isinstance(response.data, list):
        error_message = response.data[0] # Lấy lỗi đầu tiên trong list

    # 4. Xây dựng format response mới theo ý 
    custom_response_data = {
        'status_code': response.status_code,
        'message': error_message
    }

    # Gán dữ liệu đã re-format vào response và trả về
    response.data = custom_response_data
    
    return response