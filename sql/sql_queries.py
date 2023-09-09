sql_query = """
SELECT *
FROM catalogo.item_material
WHERE 1=1
ORDER BY codigo_grupo, codigo_classe, codigo_pdm, codigo_item
"""
