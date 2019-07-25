# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019 CompuCom, All Rights Reserved
# Created by Luis Fuentes

"""This module contains all unit tests for the first part of the coding challenge."""

import unittest

from resources.generate_database import get_database_file_path

from coding_challenge.forecasting import get_forecasted_model_revision_growth_rate


class TestForecasting(unittest.TestCase):
    """This class encapsulates all predefined unit tests for the forecasting part of the coding challenge."""

    def test_get_forecasted_model_revision_growth_rate(self):
        """Tests if the forecast is calculated correctly."""
        forecast = get_forecasted_model_revision_growth_rate(get_database_file_path(), 50, 3)

        self.assertEqual(3, len(forecast))


class TestCustomApplicationLogic(unittest.TestCase):
    """This class encapsulates all user defined unit tests for the application logic part of the coding challenge."""
