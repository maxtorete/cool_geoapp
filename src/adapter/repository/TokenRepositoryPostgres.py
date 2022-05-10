from adapter.database.postgres import pg_connection


class TokenRepositoryPostgres():
    def find_one_by_username(self, username: str):
        conn = pg_connection()
        with conn.cursor() as cur:
            cur.execute(f"SELECT username, password, salt FROM users WHERE username LIKE '{username}'")
            user = cur.fetchone()
        conn.close()
        return {'username': user[0], 'password': user[1], 'salt': user[2]}