import torch
from esrgan import ESRGAN  

class ModelLoader:
    def __init__(self):
        self.models = {}
        self.load_models()

    def load_models(self):
        # Load the ESRGAN model
        self.models['esrgan'] = ESRGAN(pretrained=True).eval()
        # Load other models as necessary

    def get_model(self, model_name):
        return self.models.get(model_name, None)

# Usage
model_loader = ModelLoader()
esrgan_model = model_loader.get_model('esrgan')
