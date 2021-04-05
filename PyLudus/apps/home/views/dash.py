import logging

import dateparser

from PyLudus.apps.home.views import get_login_url, is_user_login_ok
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from fusionauth.fusionauth_client import FusionAuthClient

logger = logging.getLogger(__name__)


class DashView(View):
    """The main landing page for the website."""

    def get(self, request: WSGIRequest) -> HttpResponse:
        """HTTP GET: Return the view template."""
        login_url = get_login_url(request)
        user_id = is_user_login_ok(request)

        if not user_id:
            return redirect(login_url)

        birthday = None
        user = None

        try:
            client = FusionAuthClient(
                settings.FUSION_AUTH_API_KEY, settings.FUSION_AUTH_INTERNAL_API_URL
            )
            logger.info(f"{user_id=}")
            r = client.retrieve_user(user_id)
            if r.was_successful():
                user = r.success_response["user"]
                logger.info(f"{user=}")
                birthday = r.success_response["user"].get("birthDate", None)
                logger.info(f"{birthday=}")
            else:
                logger.info("couldn't get user")
                logger.info(r.error_response)
            logger.info(f"render dashboard with {user_id}")
        except Exception as e:
            logger.error(f"Error occurred while communicating with Fusion API: {e}")
            return redirect(login_url)

        return render(request, "home/dash.html", {"user": user, "birthday": birthday})

    def post(self, request: HttpRequest) -> HttpResponse:
        """HTTP POST: Set user birthdate."""
        birthday = request.POST.get("birthday")
        user_id = request.POST.get("user_id")
        normalised_birthday = None
        logger.info(f"{birthday=}")
        logger.info(f"{user_id=}")

        try:
            dt = dateparser.parse(birthday)
            normalised_birthday = dt.strftime("%Y-%m-%d")
        except Exception as e:
            logger.error(f"Couldn't parse birthday: {e}")

        if not normalised_birthday:
            return render(
                request,
                "home/dash.html",
                {
                    "message": "Couldn't parse birthday. Please use YYYY-MM-DD",
                    "user_id": user_id,
                },
            )

        try:
            client = FusionAuthClient(
                settings.FUSION_AUTH_API_KEY, settings.FUSION_AUTH_INTERNAL_API_URL
            )
            r = client.patch_user(user_id, {"user": {"birthDate": normalised_birthday}})
            if r.was_successful():
                logger.info(r.success_response)
                return render(
                    request,
                    "home/dash.html",
                    {
                        "message": "Your birthday has been set",
                        "birthday": normalised_birthday,
                        "user": r.success_response["user"],
                    },
                )
            else:
                logger.error(r.error_response)
                return render(
                    request,
                    "home/dash.html",
                    {
                        "message": "Something went wrong",
                        "user": r.error_response["user"],
                    },
                )
        except Exception as e:
            logger.critical(e)
            return render(
                request,
                "home/dash.html",
                {"message": "Something went wrong"},
            )
