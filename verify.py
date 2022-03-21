import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

import util
import train
import predict

def main():
    """ Apenas para análise da base de treino e da acurácia do modelo """

    # Leitura dos datasets:
    train_data = pd.read_csv('challenge_train.csv')

    # Análise exploratória mínima (manual): 
    # base ok, sem valores ausentes (apesar de que o XGBoost consegue processá-los)
    # balanceamento de classes ok.    
    print('\nQuinze primeiros elementos:')
    print(train_data.head(15))
    print('\nDatabase info:')
    print(train_data.info())
    print('\nDescritivo da base:')
    print(train_data.describe())
    print('\nVerificação de NA:')
    print(train_data.isna().mean(axis=0))
    print('\nBalanceamento das classes:')
    print(train_data.strategy.value_counts())
    
    # Remoção do que não é feature:
    train_data.drop(['id', 'name'], axis=1, inplace=True)

    # Transformação dos dados categóricos (qualitativos) 
    # para dados numéricos (quantitativos):
    # One-hot-encoding reduzido: strategy --> late (0 ou 1)
    train_data = util.conv_one_hot_enc(train_data, 'strategy', is_bool=True)
    # One-hot-encoding normal
    train_data = util.conv_one_hot_enc(train_data, 'type', is_bool=False)
    train_data = util.conv_one_hot_enc(train_data, 'god', is_bool=False)

    # Separação das labels (y) para o treino supervisionado:
    X = train_data.drop('late', axis=1)
    y = train_data.late

    print('\nDez primeiros atributos de treino:')
    print(X.head(10))
    print('\nDez primeiros labels de treino:')
    print(y.head(10))
    
    # Treinamento e geração do modelo completo, em arquivo:
    train.run(X, y, 'full_model.json')

    # Opção: separar dados de treino em: 
    # 80% para treino e 20% para teste (check de acurácia):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42)

    # Treinamento e geração do modelo de validação, em arquivo:
    train.run(X_train, y_train, 'valid_model.json')

    # Predição utilizando o modelo salvo em arquivo
    predict.load('valid_model.json')
    y_pred = predict.run_from_dframe(X_test,)
    
    # Converte y_true para categorico...
    y_test = predict.conv_class(y_test)
        
    accuracy = accuracy_score(y_test, y_pred)
    print("\n\nAccuracy: %.2f%%" % (accuracy * 100.0))


if __name__ == '__main__':
    main()
