from database import get_connection

def salvar_dados_api(lista_dados):
    conn = get_connection()
    cur = conn.cursor()

    for item in lista_dados:
        cur.execute("""
            INSERT INTO dados_api (campo1, campo2, campo3)
            VALUES (%s, %s, %s)
        """, (
            item.get("campo1"),
            item.get("campo2"),
            item.get("campo3")
        ))

    conn.commit()
    cur.close()
    conn.close()
