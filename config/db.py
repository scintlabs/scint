import os
from uuid import uuid4

import psycopg2
from util.logging import logger

from base.persistence.env import envar


def init_sql_connection():
    logger.info(f"Opening database connection.")
    try:
        connection = psycopg2.connect(
            database=envar("SCINT_SQL_DB"),
            user=envar("SCINT_SQL_USER"),
            password=envar("SCINT_SQL_PASS"),
            host="localhost",
            port="5432",
        )

        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        record = cursor.fetchone()

        return connection

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error connecting to the database: {error}")
        return None


def insert_message(role, content, response_id):
    connection = init_sql_connection()

    if not connection:
        logger.error("Failed to connect to the database.")
        return None

    cursor = connection.cursor()
    message_id = str(uuid4())

    insert_query = """
    INSERT INTO messages (message_id, role, content, timestamp, response_id)
    VALUES (%s, %s, %s, NOW(), %s);
    """

    logger.info(f"Inserting message into database.")
    cursor.execute(insert_query, (message_id, role, content, response_id))
    connection.commit()
    cursor.close()
    connection.close()

    return message_id
