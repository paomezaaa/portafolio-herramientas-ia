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
    """Recibe una imagen (PIL.Image o numpy array) y devuelve las 3 etiquetas
    más probables con su porcentaje (0.0 a 100.0) en un diccionario."""
    if imagen is None:
        return {}

    predicciones = clasificador(imagen, top_k=3)

    return {
        item["label"]: round(item["score"] * 100, 2)
        for item in predicciones
    }


demo = gr.Interface(
    fn=clasificar,
    inputs=gr.Image(type="pil", label="Sube o arrastra una imagen"),
    outputs=gr.Label(num_top_classes=3, label="Top 3 predicciones (%)"),
    title="Clasificador de imágenes con MobileNetV2",
    description="Sube una imagen para obtener las 3 etiquetas más probables y su porcentaje de confianza.",
)

if __name__ == "__main__":
    demo.launch()