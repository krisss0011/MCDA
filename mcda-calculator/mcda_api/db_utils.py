from django.db import connection

def truncate_table(model):
    """
    Deletes all records from the model's table and resets the primary key counter in SQLite.
    """
    with connection.cursor() as cursor:
        table_name = model._meta.db_table
        cursor.execute(f"DELETE FROM {table_name};")
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")
        connection.commit()


def reset_auto_increment(model):
    """
    Deletes all records from the model's table and resets the auto-increment ID counter in SQLite.
    This function should only be used when all records are being deleted.
    """
    with connection.cursor() as cursor:
        table_name = model._meta.db_table
        cursor.execute(f"DELETE FROM {table_name};") 
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")  
        connection.commit()