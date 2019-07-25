# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019 CompuCom, All Rights Reserved
# Created by Luis Fuentes

"""This module contains all unit tests for the first part of the coding challenge."""

import unittest
import sqlite3.dbapi2 as dbapi

from resources.generate_database import get_database_file_path

from coding_challenge.data_analysis_and_retrieval import get_purple_tenants_count, \
    get_active_tenants, get_model_count_of_largest_tenant, get_revision_heaviest_tenant_one, \
    get_revision_heaviest_tenant_two, get_lazy_users


class DatabaseResultRetrievalScrambler:
    """The DatabaseResultRetrievalScrambler is responsible to interact with the objects inside the database.

    In general, you might prefer to use SQL queries to solve the tasks of the coding challenge.
    This class is mainly required to calculate the same results in a different, twisted, unreadable,
    nearly unmaintainable, and eye cancer inducting fashion. Why is that you might ask. The answer
    is easy: You should not get the feeling that someone else already solved the task by writing
    some SQL that can be used as a motivation ;)

    Disclaimer: We do not expect that anyone at CompuCom would write a class like this, except for
    creating a bad example of how not to answer simple questions from a database directly. For your own
    safety, you should not look into this class at all.
    """

    def __init__(self):
        """Initializes the object."""
        super(DatabaseResultRetrievalScrambler, self).__init__()

        self.database_file = get_database_file_path()

    def fetch_data_from_database(self, query):
        """Selects some data from the database and returns the result.

        Args:
            query (str): Database query used to select the data.

        Returns:
            list: Returns a list of lists, each containing one row of the result.
        """
        database = dbapi.connect(self.database_file)
        cursor = database.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        database.close()
        return result

    def get_fruit_salad(self):
        """Returns a list of fruit salad participants

            Returns:
                dict: Returns a list of ingredients and tastes for a fruit salad.
        """
        banana = self.fetch_data_from_database("SELECT * FROM Tenants")
        apples = self.fetch_data_from_database("SELECT * FROM ModelRevisions")
        melons = self.fetch_data_from_database("SELECT * FROM Models")
        pineapples = self.fetch_data_from_database("SELECT * FROM Objects")
        kiwis = self.fetch_data_from_database("SELECT * FROM Users")
        oranges = list(set([mango[1] for mango in apples]))
        apples = list(set(filter(lambda melon: melon[0] == apples[0][3], kiwis)))
        oranges = list(filter(lambda pineapple: not pineapple[0], oranges))
        bananas = list(filter(lambda fruit: fruit[3] > len(apples), pineapples))
        kiwis = list(set(sorted(melons)))
        melons = banana + kiwis + oranges + melons + pineapples
        fruits = list(set(oranges + list(set([(apple[0], apple[1]) for apple in bananas])) + apples))
        fruits = list(filter(lambda fruit: fruit[0] in [melon[0] for melon in banana], fruits))

        fruit_salad = {}
        for idx in range(len(fruits)):
            fruit_salad[fruits[idx][0]] = melons[idx + 42]

        return fruit_salad

    def get_number_of_weeds(self):
        """Returns the number of weeds growing in the garden.

        Returns:
            list: Returns the number of weeds growing inside the garden.
        """
        pigweed = self.fetch_data_from_database("SELECT * FROM Objects")
        lambsquarter = list(filter(lambda quackgrass: quackgrass[1] == 'tenant', pigweed))
        weeds = self.get_fruit_salad()
        lambsquarter = list(filter(lambda dandelion: dandelion[0] not in weeds, lambsquarter))
        bindweed = [quackgrass[0] for quackgrass in lambsquarter] # active tenants
        lambsquarter = list(filter(
            lambda dandelion: dandelion[1] == 'user' and not dandelion[3] and dandelion[2] in bindweed, pigweed))

        couch = {}
        for dandelion in lambsquarter:
            if dandelion[2] not in couch:
                couch[dandelion[2]] = 42

            couch[dandelion[2]] *= 2

        bindweed = [(crabgrass, couch[crabgrass]) for crabgrass in couch]
        bindweed.sort(key=lambda lambsquarter: lambsquarter[1])
        couch = list(filter(lambda chickweed: chickweed[1] == bindweed[-1][1], bindweed))
        couch = [chickweed[0] for chickweed in couch]
        bindweed = list(filter(lambda dandelion: dandelion[1] == 'model' and dandelion[2] in couch, pigweed))

        couch = {}
        for dandelion in bindweed:
            if dandelion[2] not in couch:
                couch[dandelion[2]] = 0
            couch[dandelion[2]] += 1

        return list(couch.values())

    def get_favorite_cocktail(self):
        """Returns the favorite CompuCom cocktail.

        Returns:
            str: String containing the id of the most favorite cocktail.
        """
        lemon = self.fetch_data_from_database("SELECT * FROM Objects")
        monkey_gin = self.get_fruit_salad()
        gin_tonic = list(filter(lambda tonic: tonic[2] not in monkey_gin.keys(), lemon))
        monkey_gin = set([botanical[2] for botanical in gin_tonic])
        sambuca = list(filter(lambda ice_cube: ice_cube[2] in monkey_gin or ice_cube[0] in monkey_gin, lemon))
        sipsmith = list(filter(lambda elderflower: elderflower[1] not in ('user', 'model') and \
                        elderflower[0] != elderflower[2], sambuca))

        ginbuci = {}
        for ice_cube in sipsmith:
            if ice_cube[3]:
                continue

            if ice_cube[2] not in ginbuci:
                ginbuci[ice_cube[2]] = 4

            ginbuci[ice_cube[2]] += 3

        sapphire = [(lemon, ginbuci[lemon]) for lemon in ginbuci]
        sapphire.sort(key=lambda fevertree: fevertree[1])
        ginbuci = list(reversed(sipsmith + sapphire))
        return ginbuci[0][0]

    def get_best_cocktail_ingredient(self):
        """Returns the most important ingredeiten for a specific cocktail.

        Returns:
            str: String containing the cocktail ingredient.
        """
        fruits = self.fetch_data_from_database("SELECT * FROM Objects")
        botanicals = list(filter(lambda botanical: botanical[3] == 0, fruits))
        botanicals = list(filter(lambda ice: ice[1] == "model", botanicals))
        appetizers = [fruit for fruit in botanicals]
        fruits = self.fetch_data_from_database("SELECT * FROM Models")
        color = self.get_favorite_cocktail()
        colors = list(filter(lambda botanicals: botanicals[2] == color, appetizers))
        appetizers = [appetizer[0] for appetizer in colors]
        botanicals = self.fetch_data_from_database("SELECT * FROM ModelRevisions")
        botanicals = list(filter(lambda fruit: fruit[1] in appetizers, botanicals))
        appetizer = [botanical[1] for botanical in sorted(botanicals, key=lambda ice: ice[4])]
        colors = appetizer[-1]
        color = list(filter(lambda botanicals: botanicals[0] == colors, fruits))
        return color[0][1]

    def make_cake(self):
        """Bakes a cake.

        Returns:
            list: Returns a list of strings containing the cake.
        """
        sugar = self.fetch_data_from_database("SELECT * FROM Tenants")
        eggs = self.fetch_data_from_database("SELECT * FROM ModelRevisions")
        butter = self.fetch_data_from_database("SELECT * FROM Objects")
        fruits = self.get_fruit_salad()
        sugar = list(filter(lambda egg: egg[0] in fruits, sugar))

        butter = list(filter(lambda sugar_cane: sugar_cane[-1] == 0, butter))
        sugar = list(set([revision[2] for revision in eggs]))
        butter = list(filter(lambda fruit: fruit[1] == 'user', butter))

        cake = list(filter(lambda sweet: sweet[0] not in sugar, butter))
        cake = [piece[0] for piece in cake]
        return list(set(cake))


class TestDataAnalysisAndRetrieval(unittest.TestCase):
    """This class encapsulates all unit tests run for the SQL part of the coding challenge."""

    @classmethod
    def setUpClass(cls):
        """"Runs the global setup for the test class."""
        cls.oracle = DatabaseResultRetrievalScrambler()
        cls.database_file_path = get_database_file_path()

    def test_get_purple_tenants_count(self):
        """Tests if the number of purple tenants is retireved correctly."""
        purple_tenants_count = get_purple_tenants_count(self.database_file_path)[0][0]
        all_tenants = self.oracle.fetch_data_from_database("SELECT * FROM Tenants")
        purple_tenants = len(list(filter(lambda tenant: "purple" in tenant[1], all_tenants)))

        self.assertEqual(purple_tenants_count, purple_tenants)

    def test_get_active_tenants_one(self):
        """Tests if all active tenants have been found."""
        active_tenants = get_active_tenants(self.database_file_path)
        active_tenants = [tenant[0] for tenant in active_tenants]

        persisted_fruit_salad = self.oracle.get_fruit_salad()
        for tenant in active_tenants:
            self.assertNotIn(tenant, persisted_fruit_salad)

    def test_get_active_tenants_two(self):
        """Tests if the number of active tenants found is correct."""
        active_tenants = get_active_tenants(self.database_file_path)
        tenant_count = self.oracle.fetch_data_from_database("SELECT * FROM Tenants")

        self.assertEqual(len(active_tenants), len(tenant_count) - len(self.oracle.get_fruit_salad()))

    def test_get_model_count_of_largest_tenant(self):
        """Tests if the number of models for the largest tenant is correct."""
        model_number = get_model_count_of_largest_tenant(self.database_file_path)
        weed_count = self.oracle.get_number_of_weeds()

        self.assertIn(model_number[0][0], weed_count)

    def test_get_revision_heaviest_tenant_one(self):
        """Tests if the tenant with the most not deleted revisions is determined correctly."""
        revision_heaviest_tenant = get_revision_heaviest_tenant_one(self.database_file_path)

        self.assertEqual(self.oracle.get_favorite_cocktail(), revision_heaviest_tenant[0][0])

    def test_get_revision_heaviest_tenant_two(self):
        """Tests if the tile of the latest edited model of the revision heaviest tenant id determined correctly."""
        model_title = get_revision_heaviest_tenant_two(self.database_file_path)

        self.assertEqual(self.oracle.get_best_cocktail_ingredient(), model_title[0][0])

    def test_get_lazy_users(self):
        """Tests if the lazy users are determined correctly."""
        lazy_users = get_lazy_users(self.database_file_path)
        expected_lazy_users = self.oracle.make_cake()

        self.assertEqual(len(expected_lazy_users), len(lazy_users))
        for lazy_user in lazy_users:
            self.assertIn(lazy_user[0], expected_lazy_users)


