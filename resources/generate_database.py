# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019 CompuCom, All Rights Reserved
# Created by Luis Fuentes

"""This helper (re)-generates the database for all parts of the coding challenge."""

import os
import sqlite3.dbapi2 as dbapi
import random
import uuid


_SCALING_FACTOR = 23


def _uuid():
    """"Returns a UUID without any dashes.

    Returns:
        str: Returns a dash-free UUID.
    """
    return str(uuid.uuid4()).replace("-", "")


def _name():
    """Returns a readable name."""
    attributes = list(set([
        "beautiful", "bright", "broken", "clever", "dark", "dusty", "deadly",
        "delicious", "colorful",
        "encouraging", "epic", "fantastic", "fast", "gigantic", "great",
        "heavy", "hidden", "icy", "invisible", "lazy", "light", "magic",
        "monumental", "motivating", "spicy",
        "mystic", "old", "revitalizing", "rusty", "shady", "shiny", "slow",
        "smart", "young", "wild", "domestic", "loud", "silent", "fine", "common",
        "deceptive", "serious", "terrifying", "drowned", "insulting", "foul",
        "shattering", "funky", "legendary", "ultimate", "supreme", "true", "false",
        "frosted", "extraterrestrial"
    ]))

    colors = list(set([
        "aquamarine", "blue", "cyan", "golden", "green", "grey", "iron",
        "ivory", "khaki", "magenta", "olive", "orange", "orchid", "pink",
        "platin", "plum", "purple", "red", "sand", "silver", "turquoise",
        "violet", "white", "yellow"
    ]))

    objects = list(set([
        "alpaca", "antelope", "armor", "axe", "ballista", "boot", "bottle",
        "bow", "burger", "butterfly", "cake", "caravel", "carrot", "cart",
        "cat", "catapult", "charger", "claymore", "clownfish", "club",
        "cobra", "cog", "cow", "crab", "crossbow", "destrier", "dog",
        "dolphin", "dragon", "dwarf", "elephant", "falchion", "falcon",
        "flail", "fox", "frog", "galley", "giant", "giraffe", "glaive",
        "glove", "grizzly", "halbert", "hat", "helmet", "hippo",
        "horse", "impala", "jaguar", "lance", "lemming", "lion",
        "longship", "longsword", "rhinoceros",
        "maul", "monkey", "mortar", "mouse", "musket", "ocelot", "onion",
        "panda", "parrot", "penguin", "pig", "pike", "pillow", "potato",
        "quarterstaff", "rat", "salmon", "seal", "shark", "snail", "snake",
        "soup", "spear", "squirrel", "stag", "steak", "sword", "trebuchet",
        "turtle", "unicorn", "witch", "wolf", "zebra", "zweihander", "pencil",
        "anvil", "cloud", "token", "medal", "amulett", "boot", "wizard", "beer"
    ]))

    return f"{random.choice(attributes)}-{random.choice(colors)}-{random.choice(objects)}"


def get_database_file_path(database_file="magic_database.db"):
    """Returns the complete file path for the given database file.

    Args:
        database_file (str): Name of the database file.

    Returns:
        str: String containing the path of the database file.
    """
    return f"{os.path.dirname(__file__)}/{database_file}"


def recreate_database_file(database_file_path):
    """Generates an empty database. In case the file already exists, it is deleted first.

    Args:
        database_file_path (str): Name of the database file.
    """
    if os.path.isfile(database_file_path):
        print("Database is already present. The database file will be deleted.")
        os.remove(database_file_path)

    print(f"The database file will be stored at {database_file_path}.")
    database = dbapi.connect(database_file_path)
    cursor = database.cursor()
    database.commit()
    cursor.close()


def generate_tables(database_file_path):
    """Generates all tables for the database.

    Args:
        database_file_path (str): Path to the database file.
    """
    database = dbapi.connect(database_file_path)

    cursor = database.cursor()
    cursor.execute("""
        CREATE TABLE Objects (
            id                  VARCHAR( 32) PRIMARY KEY,
            object_type         VARCHAR(255),
            tenant              VARCHAR( 32),
            marked_for_deletion BOOLEAN      DEFAULT FALSE 
        )""")

    cursor.execute("""
        CREATE TABLE Models (
            id    VARCHAR( 32) REFERENCES Objects(id),
            title VARCHAR(255)
        )""")

    cursor.execute("""
        CREATE TABLE Users (
            id         VARCHAR( 32) REFERENCES Objects(id),
            first_name VARCHAR(255),
            last_name  VARCHAR(255)
        )""")

    cursor.execute("""
        CREATE TABLE ModelRevisions (
            id              VARCHAR(32) REFERENCES Objects(id),
            model           VARCHAR(32) REFERENCES Models(id),
            author          VARCHAR(32) REFERENCES Users(id),
            revision_number INTEGER,
            creation_date   INTEGER
        )""")

    cursor.execute("""
        CREATE TABLE Tenants (
            id   VARCHAR( 32) REFERENCES Objects(id),
            name VARCHAR(255)
        )""")

    database.commit()
    cursor.close()
    database.close()


def generate_tenants(database_file_path):
    """Generates the tenants for the test database.

    Args:
        database_file_path (str): Path to the database file.
    """
    database = dbapi.connect(database_file_path)
    cursor = database.cursor()

    for idx in range(random.randint(_SCALING_FACTOR * 3, _SCALING_FACTOR * 9)):
        id = _uuid()
        cursor.execute(f"INSERT INTO Objects (id, object_type, tenant, marked_for_deletion) "
                       f" VALUES ('{id}','tenant','{id}',{random.randint(0, 50) <= 42})")
        cursor.execute(f"INSERT INTO Tenants (id, name) VALUES ('{id}', '{_name()}')")

    database.commit()
    cursor.close()
    database.close()


def get_random_tenant(database_file_path):
    """Returns the id of a random tenant and if the tenant is marked for deleted.

    Args:
        database_file_path (str): Path to the database file.

    Returns:
        tuple: Returns a tuple of (str, bool) containing a tenant id and if the tenant was deleted.
    """
    database = dbapi.connect(database_file_path)
    cursor = database.cursor()
    cursor.execute("SELECT id, marked_for_deletion FROM Objects WHERE object_type = 'tenant'")
    tenants = cursor.fetchall()
    cursor.close()
    database.close()
    return random.choice(tenants)


def generate_users(database_file_path, scaling_factor=None):
    """Generates the users for the test database.

    Args:
        database_file_path (str): Path to the database file.
        scaling_factor (int): Manual scaling factor.
    """
    database = dbapi.connect(database_file_path)
    cursor = database.cursor()

    if scaling_factor is None:
        scaling_factor = _SCALING_FACTOR

    for idx in range(random.randint(scaling_factor * 50, scaling_factor * 150)):
        id = _uuid()
        tenant = get_random_tenant(database_file_path)
        cursor.execute(f"INSERT INTO Objects (id, object_type, tenant, marked_for_deletion) "
                       f"VALUES ('{id}','user','{tenant[0]}',{random.randint(0, 50) >= 48 or tenant[1] == 1})")
        cursor.execute(f"INSERT INTO Users (id, first_name, last_name) VALUES ('{id}', '{_name()}', '{_name()}')")
        database.commit()

    cursor.close()
    database.close()


def get_random_user(database_file_path , tenant_id=None):
    """Returns the id of a random user, its tenant, and if the tenant is marked for deletion.

    Args:
        database_file_path (str): Path to the database file.
        tenant_id (str): The tenant the user is from.

    Returns:
        tuple: Returns a tuple of (str, str, bool) containing a user id, the users tenant,
            and if the tenant marked for deletion.
    """
    database = dbapi.connect(database_file_path)
    cursor = database.cursor()

    statement = f"""
        SELECT users.id, users.tenant, tenants.marked_for_deletion
        FROM Objects users, Objects tenants
        WHERE     users.object_type = 'user'
              AND users.tenant = tenants.id
    """

    if tenant_id is not None:
        statement += f"""
              AND tenants.id = '{tenant_id}'"""
    cursor.execute(statement)

    users = cursor.fetchall()
    cursor.close()
    database.close()
    return random.choice(users)


def generate_models(database_file_path):
    """Generates the models for the test database.

    Args:
        database_file_path (str): Path to the database file.
    """
    database = dbapi.connect(database_file_path)
    cursor = database.cursor()

    for idx in range(random.randint(_SCALING_FACTOR * 100, _SCALING_FACTOR * 300)):
        id = _uuid()
        user = get_random_user(database_file_path)
        cursor.execute(f"INSERT INTO Objects (id, object_type, tenant, marked_for_deletion) "
                       f"VALUES ('{id}','model','{user[1]}',{random.randint(0, 50) >= 36 or user[2] == 1})")
        cursor.execute(f"INSERT INTO Models (id, title) VALUES ('{id}', '{_name()}')")
        database.commit()

    cursor.close()
    database.close()


def get_models(database_file_path):
    """"Returns a list of Models stored in the database.

    Args:
        database_file_path (str): Path to the database file.

    Returns:
        list: List containing tuples of with the relevant model information: (id, tenant, marked_for_deletion).
    """
    database = dbapi.connect(database_file_path)
    cursor = database.cursor()
    cursor.execute("""
        SELECT id, tenant, marked_for_deletion
        FROM Objects
        WHERE object_type = 'model'
    """)
    models = cursor.fetchall()
    cursor.close()
    database.close()
    return models


def generate_revisions(database_file_path):
    """Generates the tenants for the test database.

    Args:
        database_file_path (str): Path to the database file.
    """
    database = dbapi.connect(database_file_path)
    cursor = database.cursor()

    models = get_models(database_file_path)

    for model in models:
        for revision in range(random.randint(3, 12)):
            id = _uuid()
            author = get_random_user(database_file_path, model[1])

            start_date = random.randint(21414, 352145)

            cursor.execute(f"INSERT INTO Objects (id, object_type, tenant, marked_for_deletion) "
                           f"VALUES ('{id}','revision','{model[1]}',{random.randint(0, 50) >= 49 or model[2] == 1})")

            statement = f"""
                INSERT INTO ModelRevisions (id, model, author, revision_number, creation_date) 
                VALUES ('{id}', '{model[0]}', '{author[0]}', {revision}, 
                {random.randint(1,72) + (revision * 73) + start_date})
            """
            try:
                cursor.execute(statement)
            except Exception as e:
                print(statement)
                raise e

        database.commit()

    cursor.close()
    database.close()

def optimize_database(database_file_path):
    """Reorders the objects in the database for better query performance.

    Args:
        database_file_path (str): Path to the database file.
    """
    database = dbapi.connect(database_file_path)

    cursor = database.cursor()
    cursor.execute("SELECT * FROM Objects ORDER BY id ASC")
    objects = cursor.fetchall()
    cursor.close()

    cursor = database.cursor()
    for database_object in objects:
        cursor.execute(f"DELETE FROM Objects WHERE id='{database_object[0]}'")
        cursor.execute(f"""
            INSERT INTO Objects (id, object_type, tenant, marked_for_deletion)
            VALUES ('{database_object[0]}','{database_object[1]}', '{database_object[2]}', {database_object[3]})
        """)

    database.commit()
    cursor.close()

    cursor = database.cursor()
    cursor.execute("SELECT * FROM ModelRevisions ORDER BY id ASC")
    revisions = cursor.fetchall()
    cursor.close()

    cursor = database.cursor()
    for revision in revisions:
        cursor.execute(f"DELETE FROM ModelRevisions WHERE id='{revision[0]}'")
        cursor.execute(f"""
                INSERT INTO ModelRevisions (id, model, author, revision_number, creation_date)
                VALUES ('{revision[0]}','{revision[1]}', '{revision[2]}', {revision[3]}, {revision[4]})
            """)

    database.commit()
    cursor.close()

    database.close()


def populate_database(database_file_path):
    """Populates the database with actual data.

    Args:
        database_file_path (str): Path to the database file.
    """
    generate_tenants(database_file_path)
    generate_users(database_file_path)
    generate_models(database_file_path)
    generate_revisions(database_file_path)
    generate_users(database_file_path, 2)


# this part is executed if the script is called directly
if __name__ == "__main__":

    database_file_path = get_database_file_path()
    recreate_database_file(database_file_path)
    generate_tables(database_file_path)
    print("Populating database. This might take a while.")
    populate_database(database_file_path)
    print("Optimizing database")
    optimize_database(database_file_path)
