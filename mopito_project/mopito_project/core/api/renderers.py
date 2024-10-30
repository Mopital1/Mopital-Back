import json

from rest_framework import status
from rest_framework.renderers import JSONRenderer


class BaseRenderer(JSONRenderer):
    """
    Overrides the default JSONRenderer to update the response structure.
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return b''
        success_codes = [
            status.HTTP_200_OK,
            status.HTTP_204_NO_CONTENT,
            status.HTTP_201_CREATED
        ]
        error_codes = [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        ]
        view = renderer_context.get("view", None)
        response = renderer_context.get("response", None)
        msg = ""
        success = True
        if response is not None:
            if response.status_code in success_codes:
                msg = "MsgUtils.OK"
                success = True
            if response.status_code in error_codes:
                msg = "MsgUtils.OPERATION_FAILED"
                success = False

        if hasattr(view, "action") and view.action == "list":
            total = len(data)
        else:
            total = 1

        custom_data = {
            "data": data,
            "total": total,
            "msg": msg,
            "success": success
        }

        return super().render(custom_data, accepted_media_type, renderer_context)
