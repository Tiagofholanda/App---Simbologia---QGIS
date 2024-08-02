import streamlit as st
import os
import tempfile
from PIL import Image
import base64
import svgwrite

def convert_png_to_svg(input_file, output_file):
    # Abre a imagem PNG e obtém suas dimensões
    image = Image.open(input_file)
    width, height = image.size
    
    # Converte a imagem para base64
    with open(input_file, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Cria um arquivo SVG com a imagem PNG embutida
    dwg = svgwrite.Drawing(output_file, profile='full', size=(width, height))
    dwg.add(dwg.image(href=f'data:image/png;base64,{image_data}', insert=(0, 0), size=(width, height)))
    dwg.save()

st.title("Conversor de PNG para SVG")

uploaded_file = st.file_uploader("Escolha uma imagem PNG", type="png")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    # Exibir a imagem PNG
    image = Image.open(tmp_file_path)
    st.image(image, caption='Imagem PNG Carregada', use_column_width=True)

    # Converter para SVG
    output_svg_path = tmp_file_path.replace(".png", ".svg")
    convert_png_to_svg(tmp_file_path, output_svg_path)

    # Ler o arquivo SVG convertido
    with open(output_svg_path, "rb") as svg_file:
        svg_data = svg_file.read()

    st.download_button(
        label="Baixar imagem SVG",
        data=svg_data,
        file_name="imagem_convertida.svg",
        mime="image/svg+xml"
    )

    # Remover arquivos temporários
    os.remove(tmp_file_path)
    os.remove(output_svg_path)
