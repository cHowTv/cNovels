from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from drf_yasg.inspectors import SwaggerAutoSchema

schema_view = get_schema_view(
   openapi.Info(
      title="cBooks",
      default_version='v1',
      description="cBooks API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="proflamyt@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


class CreatedResponseSerializer(serializers.Serializer):
    """ This is a sample serializer for showing my intent """
    id = serializers.CharField(
        help_text=_("This is the `id` of created object.")
    )
class OKResponseSerializer(serializers.Serializer):
    """ This is a sample serializer for showing my intent """
    id = serializers.CharField(
        help_text=_("This is the `id` of created object.")
    )


class XcodeAutoSchema(SwaggerAutoSchema):
    # python_template = None
    curl_template = None

    def get_operation(self, operation_keys=None):
        # assert self.python_template, "All SwaggerAutoSchema class must define python_template filed in it"
        assert self.curl_template, "All SwaggerAutoSchema class must define curl_template filed in it"
        
        operation = super().get_operation(operation_keys)

        # Using django templates to generate the code
        template_context = {
            "request_url": self.request._request.build_absolute_uri(self.path),
        }

        operation.update({
            'x-code-samples': [
                {
                    "lang": "curl",
                    "source": render_to_string(self.curl_template, template_context)
                }
            ]
        })
        return operation

    @classmethod
    def responses(cls):
        return {
            201: CreatedResponseSerializer(),
            200: OKResponseSerializer(),
            400: "bad request.", # you can use your own text or serializer
            401: "anauthorized request." # you can use your own text or serializer as well
        }