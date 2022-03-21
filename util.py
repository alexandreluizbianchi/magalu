import pandas as pd

def conv_one_hot_enc(dframe, feature_name, is_bool):
    """ Aplica One-Hot_Encoding sobre dados categóricos """
    if is_bool:
        new_features = pd.get_dummies(dframe[feature_name], drop_first=True)
    else:
        new_features = pd.get_dummies(dframe[feature_name])
    dframe = pd.concat([dframe, new_features], axis=1)
    dframe.drop(feature_name, axis=1, inplace=True)
    return dframe


def search_data_by_id(id, train_data, test_data):
    """ Busca carta pelo ID na base de treino e teste """
    data = train_data.loc[train_data['id'] == id]
    if data.empty:
        data = test_data.loc[test_data['id'] == id]
        if data.empty:
            return None
        else:
            return data.drop('id', axis=1)
    else:
        return data.drop(['id', 'strategy'], axis=1)