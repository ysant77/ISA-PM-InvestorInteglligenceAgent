from Neuro_Fuzzy.neuro_fuzzy_model import ModelLoader
from Neuro_Fuzzy.utils import get_majority_label
from Neuro_Fuzzy.data_loader import get_main_dataset
from Neuro_Fuzzy.constants import models_dir

def get_prediction_label(company_name):
    #print(company_name)
    dataset, inudstry = get_main_dataset(company_name)
    print(company_name, inudstry)
    model_loader = ModelLoader(f'{models_dir}/{inudstry}.keras')
    model = model_loader.load_model()
    prediction_label = get_majority_label(model, dataset, inudstry)
    return prediction_label