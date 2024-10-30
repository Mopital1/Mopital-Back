from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from mopito_project.utils.paginations import CustomPagination

# from .utils.paginations import CustomPagination


class BaseModelViewSet(GenericViewSet):
    pagination_class = CustomPagination

    def destroy(self, request, *args, **kwargs):
        """
        Disable the instance in the database.
        """
        instance = self.get_object()
        # if hasattr(instance, "code"):
        #     instance.code += f"_{instance.id}"
        instance.is_active = False

        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["put"])
    def soft_delete(self, request, *args, **kwargs):
        """
        Disable the instance in the database.
        """
        instance = self.get_object()
        # if hasattr(instance, "code"):
        #     instance.code += f"_{instance.id}"
        instance.is_active = False

        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)



