def remover_segunda_virgula(s):
    # Encontrar a posição da primeira vírgula
    primeira_virgula = s.find(',')
    
    # Encontrar a posição da segunda vírgula a partir da posição da primeira vírgula
    segunda_virgula = s.find(',', primeira_virgula + 1)
    
    # Se encontrar a segunda vírgula, criar uma nova string excluindo-a
    if segunda_virgula != -1:
        nova_string = s[:segunda_virgula] + s[segunda_virgula+1:]
        return nova_string
    else:
        # Se não houver segunda vírgula, retornar a string original
        return s

# Exemplo de uso
minha_string = "1,2,3,4,5"
nova_string = remover_segunda_virgula(minha_string)
print(nova_string)
