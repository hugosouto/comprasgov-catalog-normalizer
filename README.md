# comprasgov-catalog-normalizer

This script reads data from a postgres database, encodes categorical columns to numeric values, and writes the resulting dataframe to a postgres database.

The script is intended to encode the Materials Catalog of the Federal Government of Brazil for machine learning. The Materials Catalog is a hierarchical catalogue of materials used by the Federal Government of Brazil to standardize the procurement process. The catalogue is available at https://www.gov.br/compras/pt-br/acesso-a-informacao/consulta-detalhada/consulta-detalhada and downloaded at https://www.gov.br/compras/pt-br/acesso-a-informacao/consulta-detalhada/planilha-catmat-catser/catmat.xlsx.
