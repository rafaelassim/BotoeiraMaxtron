import qrcode
import os

# Lista de strings para gerar QR Codes
strings = ["aabastece","adescarte","babastece","bdescarte","cabastece","cdescarte","gabastece","gvazio","gdescarte"]
#strings = ["tipoa","tipob"]
# Diretório onde os QR Codes serão salvos
output_dir = "qrcodes/"

# Crie o diretório se não existir
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for string in strings:
    # Crie o QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(string)
    qr.make(fit=True)

    # Crie a imagem do QR Code
    img = qr.make_image(fill='black', back_color='white')

    # Substitui caracteres inválidos para nomes de arquivo
    filename = "".join(c for c in string if c.isalnum() or c in (' ', '.', '_')).rstrip()

    # Salve a imagem com o nome correspondente
    img.save(os.path.join(output_dir, f"{filename}.png"))

print("QR Codes gerados e salvos com sucesso!")