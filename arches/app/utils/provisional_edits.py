from django.db import connection


def user_has_provisional_edits(userid):

    query = f"select tiledata = (provisionaledits-> '{userid}') -> 'value' from tiles where provisionaledits-> '{userid}' is not null;"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return len(result) > 0


def approve_all_provisional_edits_for_user(userid):

    queries = [
        f"update tiles set tiledata = (provisionaledits-> '{userid}') -> 'value' where provisionaledits-> '{userid}' is not null;",
        f"update tiles set provisionaledits = provisionaledits - '{userid}' where provisionaledits-> '{userid}' is not null;",
        "select * from refresh_geojson_geometries();",
    ]
    with connection.cursor() as cursor:
        for query in queries:
            cursor.execute(query)
        result = cursor.fetchall()
    return len(result) > 0
