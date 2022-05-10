from domain.model.PostalCode import PostalCode
from domain.repository.PostalCodeRepository import PostalCodeRepository
from adapter.database.postgres import pg_connection


class PostalCodeRepositoryPostgres(PostalCodeRepository):
    def find_all_by_time_frame(self, date_from, date_to) -> [PostalCode]:
        conn = pg_connection()
        with conn.cursor() as cur:
            cur.execute(f'''
                SELECT pc.did, code, geometry, coalesce(SUM(p.amount::FLOAT), 0) FROM postal_codes pc
                LEFT JOIN paystats p ON pc.did = p.postal_code_id AND p_month BETWEEN '{date_from}' AND '{date_to}'
                GROUP BY pc.did, code, geometry
                ORDER BY code ASC
            ''')
            postal_codes = cur.fetchall()
        conn.close()
        return [PostalCode(postal_code[0], postal_code[1], postal_code[2], postal_code[3]) for postal_code in
                postal_codes]

    def find_by_did_and_time_frame(self, did: int, date_from, date_to) -> PostalCode:
        conn = pg_connection()
        with conn.cursor() as cur:
            cur.execute(f'''
                SELECT pc.did, code, geometry, coalesce(SUM(p.amount::FLOAT), 0) FROM postal_codes pc
                LEFT JOIN paystats p ON pc.did = p.postal_code_id AND p_month BETWEEN '{date_from}' AND '{date_to}'
                WHERE pc.did = {did}
                GROUP BY pc.did, code, geometry
            ''')
            postal_code = cur.fetchone()
        conn.close()
        return PostalCode(postal_code[0], postal_code[1], postal_code[2], postal_code[3]) if postal_code is not None else None
