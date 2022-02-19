# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-runner-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from functools import wraps


def pass_reana_token(f):
    """Decorator to extract a Reana access token from function arguments."""

    @wraps(f)
    def wrapper(execution_id, data, *args, **kwargs):
        try:
            reana_access_token = data.get("reana_access_token")

            if not reana_access_token:
                raise RuntimeError("Invalid `reana_access_token`")
        except:
            raise RuntimeError(
                "Is not possible to load the Execution Tasks and Pipeline records."
            )

        return f(
            execution_id=execution_id,
            reana_access_token=reana_access_token,
            *args,
            **kwargs
        )

    return wrapper
