from neuro_fuzzy_model import ModelLoader
from utils import get_majority_label
from data_loader import get_main_dataset
from constants import models_dir

def get_prediction_label(company_name):
    #print(company_name)
    dataset, inudstry = get_main_dataset(company_name)
    print(company_name, inudstry)
    model_loader = ModelLoader(f'{models_dir}/{inudstry}.keras')
    model = model_loader.load_model()
    prediction_label = get_majority_label(model, dataset, inudstry)
    return prediction_label