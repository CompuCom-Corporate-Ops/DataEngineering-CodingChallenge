# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019 CompuCom, All Rights Reserved
# Created by Luis Fuentes

"""This module contains the forecasting part of the coding challenge."""

from coding_challenge.application_logic import Model, ModelRevision, Object, Tenant, User
from coding_challenge.data_analysis_and_retrieval import _fetch_result_from_database as fetch_results_from_database


def get_forecasted_model_revision_growth_rate(database_file_path, interval_width, forecasting_intervals):
    """This function returns the expected model growth rate of the application.

    The growth rate between two time buckets is defined as

        growth_rate = 1 + ((models_{t2} + revisions_{t2} / (models_t1 + revisions_t1))

    where t1 and t2 represent the number of entities at that time. The expected model growth is an estimate based on
    past values.

    Args:
        database_file_path (str): String containing the path where the SQLite database file can be found.
        interval_with (int): Determines the number of concrete values for t that are put into time bucket for analysis.
            In a real scenario, this could be one day in case the model growth should be forecasted on a daily basis.
        forecasting_intervals (int): Determines, how many intervals should be forecasted.

    Returns:
        list: Returns a list containing the forecasted model growth values. In case two intervals should be forecasted,
            the result could be [1.2, 1.3], with the values depending on the model growth.
    """
    raise NotImplementedError
