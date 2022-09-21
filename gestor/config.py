#para eviatr la pérdida de datos del csv
# cada vez que ejecutamos una prueba

import sys
DATABASE_PATH = 'clientes.csv'

if 'pytest' in sys.argv[0]:
    DATABASE_PATH = 'tests/clientes_test.csv'
