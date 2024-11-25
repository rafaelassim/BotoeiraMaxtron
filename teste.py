def reduzir_string(texto):
    # Remove quebras de linha e espaços extras
    texto = texto.replace("\n", " ").replace("\r", " ").strip()
    # Trunca para 50 caracteres com reticências, se necessário
    return texto[:47] + "..." if len(texto) > 50 else texto

# Exemplo de uso
texto = """Esta é uma string muito longa
que precisa ser reduzida para se ajustar
ao limite de 50 caracteres."""
texto_reduzido = reduzir_string(texto)
print(texto_reduzido)