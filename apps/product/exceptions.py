from rest_framework.exceptions import APIException


class InsufficientFundsException(APIException):
    status_code = 400
    default_detail = "Insufficient funds."
    default_code = "insufficient_funds"


class ProductNotAvailableException(APIException):
    status_code = 400
    default_detail = "The product out of stock."
    default_code = "not_available"
