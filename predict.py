import pandas as pd
from xgboost import XGBClassifier
import util


loaded_model = XGBClassifier()

def load(model_name):
    """ Tenta carregar um modelo pelo nome """
    try:
        loaded_model.load_model(model_name)
    except Exception as e:
        print('Erro ao carregar modelo', model_name,':',e)


def conv_class(preds):
    """ Retorna o(s) nome(s) da(s) classe(s) """
    ret = []
    for pred in preds:
        if pred == 0:
            ret.append('early')
        elif pred == 1:
            ret.append('late')
    return ret


def run_from_file(fname):
    """ Faz o pré-tratamento do conteúdo do arquivo antes da predição """
    try:
        X_test = pd.read_csv(fname)
        X_test = X_test.drop(['id', 'name'], axis=1)
        X_test = util.conv_one_hot_enc(X_test, 'type', is_bool=False)
        X_test = util.conv_one_hot_enc(X_test, 'god', is_bool=False)
        preds = loaded_model.predict(X_test)
        return conv_class(preds)
    except Exception as e:
        print('Erro durante a previsão:',e)


def run_from_dframe(dframe):
    """ Faz a predição supondo que o dataframe já está tratado! """
    try:
        if dframe is not None:
            preds = loaded_model.predict(dframe)
            return conv_class(preds)
    except Exception as e:
        print('Erro durante a previsão:',e)
