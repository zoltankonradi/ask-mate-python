import psycopg2
import psycopg2.extras


def get_connection_string():
    # setup connection string
    # to do this, please define these environment variables first
    return 'postgresql://postgres:password@localhost/askmate'
    # user_name = os.environ.get('zoli')
    # password = os.environ.get('zoli')
    # host = os.environ.get('localhost')
    # database_name = os.environ.get('here_comes_your_creative_db_name')
    #
    # env_variables_defined = user_name and password and host and database_name
    #
    # if env_variables_defined:
    #     # this string describes all info for psycopg2 to connect to the database
    #     return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
    #         user_name=user_name,
    #         password=password,
    #         host=host,
    #         database_name=database_name
    #     )
    # else:
    #     raise KeyError('Some necessary environment variable(s) are not defined')


def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a RealDictCursor cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value

    return wrapper