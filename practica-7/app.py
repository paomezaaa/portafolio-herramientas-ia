import glob
import os
import time
import gradio as gr
import torch
from transformers import pipeline

# Selecciona GPU si está disponible; de lo contrario usa CPU
device = 0 if torch.cuda.is_available() else -1

# Carga el pipeline de clasificación de imágenes con el modelo solicitado
clasificador = pipeline(
    task="image-classification",
    model="google/mobilenet_v2_1.0_224",
    device=device,
)


def clasificar(imagen):
    """Recibe una imagen y devuelve las 3 etiquetas más probables con su
    porcentaje y el tiempo de inferencia en segundos con dos decimales."""
    if imagen is None:
        return {}, "0.00 s"

    inicio = time.perf_counter()
    predicciones = clasificador(imagen, top_k=3)
    duracion = time.perf_counter() - inicio

    resultados = {
        item["label"]: round(item["score"] * 100, 2)
        for item in predicciones
    }
    tiempo_texto = f"{duracion:.2f} s"

    return resultados, tiempo_texto


# Busca todas las imágenes dentro de la carpeta ejemplos/
extensiones = ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.bmp")
imagenes_ejemplo = []
if os.path.isdir("ejemplos"):
    for ext in extensiones:
        imagenes_ejemplo.extend(glob.glob(os.path.join("ejemplos", ext)))
    imagenes_ejemplo.sort()

demo = gr.Interface(
    fn=clasificar,
    inputs=gr.Image(type="pil", label="Sube o arrastra una imagen"),
    outputs=[
        gr.Label(num_top_classes=3, label="Top 3 predicciones (%)"),
        gr.Textbox(label="Tiempo de respuesta"),
    ],
    title="¿Qué hay en la foto?",
    description="Clasificador de imágenes impulsado por el modelo google/mobilenet_v2_1.0_224.",
    examples=imagenes_ejemplo if imagenes_ejemplo else None,
)

if __name__ == "__main__":
    demo.launch()