"""Factory for Azure OpenAI models behind APIM using LangChain."""

from __future__ import annotations

import os
from typing import Optional

from langchain_openai import AzureChatOpenAI


ENV_ENDPOINT = "AZURE_OPENAI_ENDPOINT"
ENV_API_VERSION = "AZURE_OPENAI_API_VERSION"
ENV_DEPLOYMENT = "AZURE_OPENAI_DEPLOYMENT"
ENV_API_KEY = "AZURE_OPENAI_API_KEY"
ENV_APIM_SUBSCRIPTION_KEY = "AZURE_APIM_SUBSCRIPTION_KEY"


def build_azure_apim_chat_model(temperature: float = 0.0) -> Optional[AzureChatOpenAI]:
    """Build AzureChatOpenAI configured for an APIM gateway.

    Returns None when mandatory environment variables are missing.
    """

    endpoint = os.getenv(ENV_ENDPOINT)
    api_version = os.getenv(ENV_API_VERSION)
    deployment = os.getenv(ENV_DEPLOYMENT)
    api_key = os.getenv(ENV_API_KEY)
    apim_subscription_key = os.getenv(ENV_APIM_SUBSCRIPTION_KEY)

    if not endpoint or not api_version or not deployment:
        return None

    default_headers = {}
    if apim_subscription_key:
        default_headers["Ocp-Apim-Subscription-Key"] = apim_subscription_key

    kwargs = {
        "azure_endpoint": endpoint,
        "api_version": api_version,
        "azure_deployment": deployment,
        "temperature": temperature,
        "default_headers": default_headers,
    }

    if api_key:
        kwargs["api_key"] = api_key

    return AzureChatOpenAI(**kwargs)
