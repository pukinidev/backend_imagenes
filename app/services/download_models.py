import os
import shutil
import kagglehub


def download_models():
    path = kagglehub.model_download("valetyc/imagenes/keras/default", force_download=True)
    target_dir = "app/ml_models"

    for filename in os.listdir(path):
        src = os.path.join(path, filename)
        dst = os.path.join(target_dir, filename)
        shutil.move(src, dst)
        