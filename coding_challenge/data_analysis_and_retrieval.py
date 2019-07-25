# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019 CompuCom, All Rights Reserved
# Created by Luis Fuentes

"""This module contains all queries that are required to pass the challenge described in Section 4.

Please implement your queries in the functions named get_<name_of_the_query>. An example implementation for the query
**purple_tenants_count** can be found in **get_purple_tenants_count**.
"""

import sqlite3.dbapi2 as dbapi


def _fetch_result_from_database(query, database_file_path):
    """"Executes the query and returns the result.

    Args:
        query (str): String containing the executable SQL query.
        database_file_path (str): Path to the database file.

    Returns:
        list: Returns a list of lists, each containing one row of the requested result.
    """
    database = dbapi.connect(database_file_path)
    cursor = database.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    database.close()
    return result


def get_purple_tenants_count(database_file_path):
    """This function retrieves the number of tenants that have the color purple in their name.

    Args:
        database_file_path (str): String containing the path where the SQLite database file can be found.

    Returns:
        list: Returns a list containing the results of the query. In this specific case, the list should only
            contain a single entry.
    """
    query = """
        SELECT COUNT(*)
        FROM   Tenants
        WHERE  name LIKE '%purple%'
    """

    return _fetch_result_from_database(query, database_file_path)


def get_active_tenants(database_file_path):
    """This function retrieves active tenants.

    A tenant is active, in case users exist that are not marked for deletion.

    Args:
        database_file_path (str): String containing the path where the SQLite database file can be found.

    Returns:
        list: Returns a list containing the results of the query. In this specific case, the list contains tuples
            with the id of an active tenant. In case the tenants with the ids "a", "b", and "c" are active, the
            result is [("a",), ("b",), ("c",)].
    """
    # remove the line below in case you have implemented the query.
    raise NotImplementedError

    query = """
    """

    return _fetch_result_from_database(query, database_file_path)


def get_model_count_of_largest_tenant(database_file_path):
    """This function returns the number of models of the largest tenant.

    The size of a tenant in this case is determined by the number of active users.

    Args:
        database_file_path (str): String containing the path where the SQLite database file can be found.

    Returns:
        list: Returns a list containing the result of the query. In this specific case, the list contains a
            single tuple with one element. In case the largest tenant has 300 models, the result is [(300,)].
    """
    # remove the line below in case you have implemented the query.
    raise NotImplementedError

    query = """
    """

    return _fetch_result_from_database(query, database_file_path)


def get_revision_heaviest_tenant_one(database_file_path):
    """This function returns the tenant with the most not deleted model revisions.

    Args:
        database_file_path (str): String containing the path where the SQLite database file can be found.

    Returns:
        list: Returns a list containing the result of the query. In this specific case, the list contains a
            single tuple with one element. In case the largest tenant has the id 42, the result is [(42,)].
    """
    # remove the line below in case you have implemented the query.
    raise NotImplementedError

    query = """
    """

    return _fetch_result_from_database(query, database_file_path)


def get_revision_heaviest_tenant_two(database_file_path):
    """This function returns the title of the latest model of the tenant that has the most revisions.

    For this query, maintainability and modularisation can be more important then performance.

    Args:
        database_file_path (str): String containing the path where the SQLite database file can be found.

    Returns:
        list: Returns a list containing the results of the query. In this specific case, the list contains a
            single tuple with one element. In case the latest model of the largest tenant is called 'master-process',
            the result is [("master-process",)].
    """
    # remove the line below in case you have implemented the query.
    raise NotImplementedError

    query = """
    """

    return _fetch_result_from_database(query, database_file_path)


def get_lazy_users(database_file_path):
    """This function returns the ids of all users that are neither marked for deletion, nor edited any model.

    Args:
        database_file_path (str): String containing the path where the SQLite database file can be found.

    Returns:
        list: Returns a list containing the results of the query. In this specific case, the list contains
            tuples, each containing the id of an active user that never edited a model. In case the lazy
            users have the ids "a", "b", and "c", the result is [("a",), ("b",), ("c",)].
    """
    # remove the line below in case you have implemented the query.
    raise NotImplementedError

    query = """
    """

    return _fetch_result_from_database(query, database_file_path)
