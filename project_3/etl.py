import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Runs all copy_table_queries
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Runs all insert_table_queries
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Copy data from S3 to staging tables in Redshift and then
    insert data from the staging tables to dimension and fact tables
    ready to be consumed for analytical processes.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
    
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()