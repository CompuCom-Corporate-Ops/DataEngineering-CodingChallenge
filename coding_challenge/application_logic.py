# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019 CompuCom, All Rights Reserved
# Created by Luis Fuentes

import sqlite3.dbapi2 as dbapi
from dataclasses import dataclass


@dataclass
class Object:
    """Represents an object instance of the application."""
    id: str
    object_type: str
    tenant: str
    marked_for_deletion: int

    def __init__(self, id: str, object_type: str, tenant: str, marked_for_deletion: int):
        """Initializes the Object.

        Args:
            id (str): UUID containing the id of the object.
            object_type (str): Type of object, this entry belongs to.
            tenant (str): The tenant the object belongs to.
            marked_for_deletion (int): 0 if the Object is active, 1 in case it can be deleted.
        """
        super(Object, self).__init__()

        self.id = id
        self.object_type = object_type
        self.tenant = tenant
        self.marked_for_deletion = marked_for_deletion


@dataclass
class Model:
    """Class representing a model of the application."""
    id: str
    name: str

    def __init__(self, id: str, title: str,):
        """Initializes the Model.

        Args:
            id (str): UUID containing the id of the model.
            title (str): The title of the model.
        """
        super(Model, self).__init__()

        self.id = id
        self.title = title


@dataclass
class ModelRevision:
    """Class representing a model revision."""
    id: str
    model: str
    author: str
    revision_number: int
    creation_date: int

    def __init__(self, id: str, model: str, author: str, revision_number:int, creation_date: int):
        """Initializes the ModelRevision.

        Args:
            id (str): UUID containing the id of the model revision.
            model (str): UUID containing the model the revision is part of.
            author (str): UUID containing the id of the user creating the revision.
            revision_number (int): Revision number of the revision, starting at 1.
            creation_date (int): Integer representing the creation date of the revision.
        """
        super(ModelRevision, self).__init__()

        self.id = id
        self.model = model
        self.author = author
        self.revision_number = revision_number
        self.creation_date = creation_date


@dataclass
class User:
    """Class representing a user of the application."""
    id: str
    first_name: str
    last_name: str

    def __init__(self, id: str, first_name: str, last_name: str,):
        """Initializes the User.

        Args:
            id (str): UUID containing the id of the user.
            first_name (str): First name of the user.
            last_name (str): Last name of the user.
        """
        super(User, self).__init__()

        self.id = id
        self.first_name = first_name
        self.last_name = last_name


@dataclass
class Tenant:
    """Class representing a tenant of the application."""
    id: str
    name: str

    def __init__(self, id: str, name: str,):
        """Initializes the Tenant.

        Args:
            id (str): UUID containing the id of the tenant.
            name (str): The name of the tenant.
        """
        super(Tenant, self).__init__()

        self.id = id
        self.name = name


class DataLoader:
    """The DataLoader is responsible to load all entities from the database. """

    def __init__(self, database_file_path):
        """Initializes the DataLoader.

        Args:
            database_file_path (str): String containing the path where the SQLite database file can be found.
        """
        super(DataLoader, self).__init__()
        self.database_file = database_file_path

    def _load_data_from_database(self, query):
        """Loads the requested data from the database.

        This method is private and should therefore not be called directly!

        Args:
            query (str): Query to be executed.

        Returns:
            list: List containing tuples, each representing one row of the query result.
        """
        database = dbapi.connect(self.database_file)
        cursor = database.cursor()
        cursor.execute(query)

        result = cursor.fetchall()

        cursor.close()
        database.close()

        return result

    def get_model_revisions(self):
        """Loads all ModelRevisions from the database.

        Returns:
            list: Returns a list of ModelRevision instances, each containing the data of one tuple of the
                ModelRevisions table.
        """
        revisions = self._load_data_from_database("SELECT * FROM ModelRevisions")
        revisions = [ModelRevision(*row) for row in revisions]
        return revisions

    def get_users(self):
        """Returns the users of the application.

        Returns:
            list: List containing all users of the application.
        """
        users = self._load_data_from_database("SELECT * FROM Users")
        users = [User(*row) for row in users]
        return users

    def get_objects(self):
        """Returns the objects of the application.

        Returns:
            list: List containing all objects of the application.
        """
        objects = self._load_data_from_database("SELECT * FROM Objects")
        objects = [Object(*row) for row in objects]
        return objects

    def get_tenants(self):
        """Returns the tenants of the application.

        Returns:
            list: List containing all tenants of the application.
        """
        tenants = self._load_data_from_database("SELECT * FROM Tenants")
        tenants = [Tenant(*row) for row in tenants]
        return tenants

    def get_models(self):
        """Returns the tenants of the application.

        Returns:
            list: List containing all tenants of the application.
        """
        models = self._load_data_from_database("SELECT * FROM Models")
        models = [Model(*row) for row in models]
        return models


def get_chronological_ordered_model_revisions(database_file_path, model_id):
    """This function returns an ordered list of model revisions for any given model.

    Args:
        database_file_path (str): String containing the path where the SQLite database file can be found.
        model_id (str): The id of the model for which the revisions should be retrieved.

    Returns:
        list: Returns a list of model revisions, ordered by the creation date.
    """
    data_loader = DataLoader(database_file_path)
    model_revisions = data_loader.get_model_revisions()

    # remove the line below in case you have implemented a solution
    raise NotImplementedError

    return model_revisions


def get_most_active_user(database_file_path, tenant_id):
    """Returns a list of the most active user(s) for a specific tenant.

    The activity state of a user is defined by the number of revisions the user created. For the case
    that multiple users created the same number of revisions and are still not marked for deletion, all
    users are returned.

    Args:
        database_file_path (str): String containing the path where the SQLite database file can be found.
        tenant_id (str): The id of the users that created the most revisions within the tenant.

    Returns:
        list: Returns a list of User instances representing the most active users of the tenant.
    """
    data_loader = DataLoader(database_file_path)
    most_active_users = []

    # remove the line below in case you have implemented a solution
    raise NotImplementedError

    return most_active_users


def sort_string_list(string_list, case_sensitive):
    """Retrieves a list of strings and returns it sorted, either case sensitive or case insensitive.

    Please implement the sorting of the strings within this function.

    Args:
        string_list (list): List of strings to be sorted.
        case_sensitive (bool): Determines if the list should be sorted case sensitive or case insensitive.
            If this is True, the list is sorted case sensitive, where capital letters come before small letters but
            preserving alphabetical order. In case the parameter is False, the list is sorted case insensitive.

    Returns:
        list: List containing the sorted strings.
    """
    sorted_strings = string_list.copy()

    # remove the line below in case you have implemented a solution
    raise NotImplementedError

    return sorted_strings


def get_ordered_list_of_active_model_titles(database_file_path, tenant_id, case_sensitive=False):
    """Returns a list of all active model titles of a specific tenant.

    The list is either sorted case-sensitive or case-insensitive.

    Args:
        database_file_path (str): String containing the path where the SQLite database file can be found.
        tenant_id (str): The id of the users that created the most revisions within the tenant.
        case_sensitive (bool): Determines if the titles should  be sorted case sensitive or not.

    Returns:
        list: Returns a list of strings containing the sorted model names.
    """
    data_loader = DataLoader(database_file_path)

    # remove the line below in case you have implemented a solution
    raise NotImplementedError

    return sort_string_list(titles, case_sensitive)
