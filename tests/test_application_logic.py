# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019 CompuCom, All Rights Reserved
# Created by Luis Fuentes

"""This module contains all unit tests for the second part of the coding challenge."""

import unittest
import random

from resources.generate_database import get_database_file_path

from coding_challenge.application_logic import DataLoader, Object, Model, Tenant, User, ModelRevision, \
    get_chronological_ordered_model_revisions, get_most_active_user, \
    sort_string_list, get_ordered_list_of_active_model_titles


class TestApplicationLogic(unittest.TestCase):
    """This class encapsulates all predefined unit tests for the application logic part of the coding challenge."""

    @classmethod
    def setUpClass(cls):
        """Initializes the test class."""
        cls.database_file_path = get_database_file_path()
        cls.data_loader = DataLoader(cls.database_file_path)

    def get_random_models(self, model_count):
        """Returns the ids of several models that are used for testing.

        Args:
            model_count (int): Number of models to be tested.

        Returns:
            list: Returns a list of strings, each containing a model id.
        """
        model_ids = self.data_loader._load_data_from_database("SELECT id FROM Models")
        model_ids = [model_id[0] for model_id in model_ids]

        return random.sample(model_ids, model_count)

    def get_ordered_list_of_revisions(self, model_id):
        """Returns a list of ModelRevision instances for the model.

        The list is ordered by creation_date.

        Args:
            model_id (str): id of the model the revisions should be retrieved for.

        Returns:
            list: List of ModelRevision instances, ordered by creation date.
        """
        test_revisions = self.data_loader._load_data_from_database(
            f"SELECT * FROM ModelRevisions WHERE model='{model_id}' ORDER BY creation_date")
        test_revisions = [ModelRevision(*revision) for revision in test_revisions]

        return test_revisions

    def test_get_chronological_ordered_model_revisions_revisions(self):
        """Tests if the ModelRevisions are retrieved."""
        for model in self.get_random_models(10):
            application_revisions = get_chronological_ordered_model_revisions(self.database_file_path, model)
            test_revisions = self.get_ordered_list_of_revisions(model)

            self.assertEqual(len(test_revisions), len(application_revisions))

            for idx in range(len(test_revisions)):
                self.assertEqual(test_revisions[idx], application_revisions[idx])

    def get_random_active_tenant(self, tenant_count):
        """Returns the ids of several tenants that are used for testing.

        Args:
            tenant_count (int): Number of tenants to be tested.

        Returns:
            list: Returns a list of strings, each containing a tenant id.
        """
        tenant_ids = self.data_loader._load_data_from_database(
            "SELECT tenant FROM Objects WHERE object_type='user' AND marked_for_deletion = 0 GROUP BY tenant")
        tenant_ids = [tenant_id[0] for tenant_id in tenant_ids]

        return random.sample(tenant_ids, tenant_count)

    def get_most_active_users_for_tenant(self, tenant_id):
        """Returns a list of most active users for a given tenant.

        Args:
            tenant_id (str): Id of the tenants the users should be retrieved for.

        Returns:
            list: List of User instances representing active users of the given tenant.
        """
        users = self.data_loader._load_data_from_database(f"""
            SELECT users.id, users.first_name, users.last_name
            FROM   ModelRevisions revisions, Objects revision_objects,
                   Users users, Objects user_objects
            WHERE      revisions.id = revision_objects.id
                   AND users.id = user_objects.id
                   AND user_objects.marked_for_deletion = 0
                   AND revisions.author = users.id
                   AND user_objects.tenant = '{tenant_id}'
                   AND revision_objects.tenant = '{tenant_id}'
            GROUP BY
                   users.id, users.first_name, users.last_name
            HAVING COUNT(*) = (
                SELECT MAX(created_revision_counts.created_revisions)
                FROM   (
                           SELECT COUNT(*) AS created_revisions
                           FROM   ModelRevisions revisions, Objects revision_objects,
                                  Objects user_objects
                           WHERE      revisions.id = revision_objects.id
                                  AND revisions.author = user_objects.id
                                  AND user_objects.marked_for_deletion = 0
                                  AND user_objects.object_type = 'user'
                                  AND user_objects.tenant = '{tenant_id}'
                                  AND revision_objects.tenant = '{tenant_id}'
                           GROUP BY user_objects.id
                       ) created_revision_counts
                )
        """)
        users = [User(*user) for user in users]
        return users

    def test_get_most_active_user(self):
        """Tests if the most active users are determined correctly."""
        for tenant in self.get_random_active_tenant(5):
            application_users = get_most_active_user(self.database_file_path, tenant)
            test_users = self.get_most_active_users_for_tenant(tenant)

            self.assertEqual(len(test_users), len(application_users))

            for test_user in test_users:
                self.assertIn(test_user, application_users)

            for application_user in application_users:
                self.assertIn(application_user, test_users)

    def test_case_insensitive_sort(self):
        """Tests if the case insensitive sorting works correctly."""
        strings = ["BaB", "aab", "Aab", "bab"]
        sorted_strings = sort_string_list(strings, False)

        expected_result = ["aab", "aab", "bab", "bab"]
        muted_sorted_strings = [s.lower() for s in sorted_strings]

        self.assertEqual(expected_result, muted_sorted_strings)

    def test_case_sensitive_sort(self):
        """Tests if the case insensitive sorting works correctly."""
        strings = ["BaB", "aab", "Aab", "bab", "BAB"]
        sorted_strings = sort_string_list(strings, True)

        expected_result = ["Aab", "aab", "BAB", "BaB", "bab"]

        self.assertEqual(expected_result, sorted_strings)

    def get_ordered_model_titles(self, tenant_id):
        """Returns a list of undeleted model titles for a specified tenant, ordered in lexical order.

        Args:
            tenant_id (str): Id of the tenants the users should be retrieved for.

        Returns:
            list: List containing the strings of the model names.
        """
        model_titles = self.data_loader._load_data_from_database(f"""
            SELECT models.title
            FROM   Models models, Objects objects
            WHERE      models.id = objects.id
                   AND objects.tenant = "{tenant_id}"
                   AND objects.marked_for_deletion = 0
            ORDER BY
                   LOWER(models.title)
        """)

        model_titles = [title[0] for title in model_titles]
        return model_titles

    def test_get_ordered_list_of_active_model_titles(self):
        """Tests if the list of model titles for a tenant is retrieved correctly."""
        for tenant in self.get_random_active_tenant(5):
            ordered_titles = get_ordered_list_of_active_model_titles(self.database_file_path, tenant)
            expected_titles = self.get_ordered_model_titles(tenant)

            self.assertEqual(ordered_titles, expected_titles)


class TestCustomApplicationLogic(unittest.TestCase):
    """This class encapsulates all user defined unit tests for the application logic part of the coding challenge."""
