import re

# Compilar la expresión regular
p = re.compile('ab*')

# Texto a buscar
texto = 'cab abc abbc ac ab'

# Usar finditer para obtener posiciones
posiciones = [(match.start(), match.end()) for match in p.finditer(texto)]

# Imprimir las posiciones
print(posiciones)
