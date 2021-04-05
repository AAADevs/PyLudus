import urllib
from typing import Any, Optional

import pkce
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from fusionauth.fusionauth_client import FusionAuthClient
import logging

logger = logging.getLogger(__name__)


def get_or_create_user(user_id: int, request: HttpRequest) -> Any:
    """
    Look up an object with the given kwargs, creating one if necessary.

    Return User object.
    """
    user = User.objects.filter(username=user_id).first()

    if not user:
        user = User(username=user_id)
        user.save()

    return user


def get_login_url(request: HttpRequest) -> str:
    """Returns redirect response for a user login."""
    # redirect_url = request.build_absolute_uri(reverse("dash"))
    # redirect_url = urllib.parse.quote(redirect_url)
    if ("pkce_verifier" in request.session) is False or (
        "code_challenge" in request.session
    ) is False:
        code_verifier = pkce.generate_code_verifier(length=128)
        code_challenge = pkce.get_code_challenge(code_verifier)
        request.session["pkce_verifier"] = code_verifier
        request.session["code_challenge"] = code_challenge
    redirect_url = urllib.parse.quote(settings.LOGIN_REDIRECT_URL)
    login_url = (
        f"{settings.FUSION_AUTH_BASE_URL}/oauth2/authorize"
        f"?client_id={settings.FUSION_AUTH_APP_ID}&redirect_uri={redirect_url}&response_type=code"
        f"&code_challenge={request.session['code_challenge']}&code_challenge_method=S256"
    )
    return login_url


def is_user_login_ok(request: HttpRequest) -> Optional[str]:
    """Checks if the user is login was successful or not."""
    logger.debug("starting login")
    client = FusionAuthClient(
        settings.FUSION_AUTH_API_KEY, settings.FUSION_AUTH_INTERNAL_API_URL
    )

    code = request.GET.get("code")
    logger.debug(f"{code=}")

    if not code:
        logger.debug("no code")
        return False

    try:
        # redirect_url = request.build_absolute_uri(reverse("dash"))
        redirect_url = settings.LOGIN_REDIRECT_URL
        logger.info(f"{redirect_url=}")
        # if you are using version 1.19.x of the python library or later, use this
        r = client.exchange_o_auth_code_for_access_token_using_pkce(
            code,
            redirect_url,
            request.session["pkce_verifier"],
            client_id=settings.FUSION_AUTH_APP_ID,
            client_secret=settings.FUSION_AUTH_CLIENT_SECRET,
        )
        was_successful = r.was_successful()
        logger.info(f"{was_successful=}")
        if was_successful:
            # access_token = r.success_response["access_token"]
            user_id = r.success_response["userId"]
            get_or_create_user(user_id, request)
            return user_id
        else:
            logger.error(r.error_response)
            return False

    except Exception as exc:
        logger.critical(f"{exc=}")
