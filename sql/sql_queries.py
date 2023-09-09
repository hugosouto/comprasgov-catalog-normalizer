sql_query = """
SELECT 
     it_co_orgao_superior
    ,it_no_orgao_superior
    ,it_co_orgao_vinculado
    ,it_no_orgao_vinculado
    ,it_co_unidade_gestora
    ,it_no_unidade_gestora
FROM estrutura.siasg_uasgs_orgaos
WHERE 1=1
ORDER BY it_co_orgao_superior, it_co_orgao_vinculado, it_co_unidade_gestora;
"""
