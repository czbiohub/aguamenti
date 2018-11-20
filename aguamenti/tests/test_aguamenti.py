#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_aguamenti
----------------------------------

Tests for `aguamenti` module.
"""

import pytest


class TestAguamenti(object):

    def test___init__(self, one_hundred):
        assert 100 == one_hundred
