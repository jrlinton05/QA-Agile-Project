from Source.Helpers.database_query_helper import query_database


def delete_user(username):
    query = "SELECT 1 FROM Users WHERE username = ?"
    result, con = query_database(query, params = (username,))
    if result.fetchone() is None:
        print("User does not exist")
        return None
    con.close()

    query = "DELETE FROM Users WHERE username = ?"
    try:
        _, con = query_database(query, params = (username,))
        con.close()
    except Exception as e:
        print(e)
        return False
    else:
        print("Success")
        return True

if __name__ == "__main__":
    delete_user(input("Enter Username to delete\n"))
