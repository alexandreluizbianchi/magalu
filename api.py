from flask_restplus import Api, fields, Resource
from flask import Flask, Blueprint
from flask_cors import CORS
import pandas as pd
import json

import util
import predict

""" Transforma datasets em dataframes pré-processados """
# Leitura dos datasets:
train_data = pd.read_csv('challenge_train.csv')
train_data.drop('name', axis=1, inplace=True)
train_data = util.conv_one_hot_enc(train_data, 'type', is_bool=False)
train_data = util.conv_one_hot_enc(train_data, 'god', is_bool=False)

test_data = pd.read_csv('challenge_test.csv')
test_data.drop('name', axis=1, inplace=True)
test_data = util.conv_one_hot_enc(test_data, 'type', is_bool=False)
test_data = util.conv_one_hot_enc(test_data, 'god', is_bool=False)

# Carrega modelo completo para predições, previamente criado:
predict.load('full_model.json')


api = Api(
    version="1.0",
    title="Classificador de Cartas",
    description="Classifica uma carta como 'early' ou 'late'"
)

@api.errorhandler
def default_error_handler(e):
	print('An unhandled exception ocurred.')

ns = api.namespace('id', description='Esta rota faz a predição de uma carta')

@ns.route('/<int:id>')
class IdRoute(Resource):
    @api.doc(responses={ 200: 'Sucesso', 204: 'Não encontrado', 400: 'Solicitação Inválida'})
    def get(self, id):
        """
        Retorna uma previsão pelo id da carta
        """
        try:
            df = util.search_data_by_id(id, train_data, test_data)
            if df is None:
                return '', 204
            else:
                pred = predict.run_from_dframe(df)
                if len(pred) == 1:
                    return pred[0], 200
                return '', 204
        except Exception as e:
            return {'error':str(e)}, 400


app = Flask(__name__)
CORS(app)

app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
app.config['RESTPLUS_VALIDATE'] = True
app.config['RESTPLUS_MASK_SWAGGER'] = False
app.config['ERROR_404_HELP'] = False
app.config['JSON_AS_ASCII'] = False

blueprint = Blueprint('api', __name__, url_prefix='/api')
api.init_app(blueprint)
api.add_namespace(ns)

app.register_blueprint(blueprint)

# remover esta linha
app.run(host = "0.0.0.0", port=5017, debug=False)
