from xgboost import XGBClassifier

def run(X_train, y_train, model_name):
    """ Treina e salva um modelo """    
    # Treino com hiperparâmetros padrões, 
    # sem utilizar métodos de tuning (para simplificar):
    model = XGBClassifier(objective='binary:logistic', use_label_encoder=False)
    model.fit(X_train, y_train)
    model.save_model(model_name)
