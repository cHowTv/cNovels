from .documentation import XcodeAutoSchema # change it to your desire import path


class ProductXcodeAutoSchema(XcodeAutoSchema):
    curl_template = 'swagger/product/curl_sample.md'
    

class InvoiceXcodeAutoSchema(XcodeAutoSchema):
    # python_template = 'swagger/invoice/python_sample.html'
    curl_template = 'swagger/invoice/curl_sample.md'
