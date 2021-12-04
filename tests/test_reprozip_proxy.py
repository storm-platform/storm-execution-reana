# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# reprozip-proxy is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Module tests."""

from flask import Flask

from reprozip_proxy import ReproZipProxy


def test_version():
    """Test version import."""
    from reprozip_proxy import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = ReproZipProxy(app)
    assert 'reprozip-proxy' in app.extensions

    app = Flask('testapp')
    ext = ReproZipProxy()
    assert 'reprozip-proxy' not in app.extensions
    ext.init_app(app)
    assert 'reprozip-proxy' in app.extensions


def test_view(base_client):
    """Test view."""
    res = base_client.get("/")
    assert res.status_code == 200
    assert 'Welcome to reprozip-proxy' in str(res.data)
