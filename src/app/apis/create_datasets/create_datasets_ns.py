from http import HTTPStatus
from flask import jsonify
from flask_restx import Namespace, Resource

from .dto import sportmaster_parser_info_reqparser
from src.app.core.create_datasets.create_datasets_logic import create_sportmaster_dataset

ns = Namespace(
	name='Create Dataset Controller',
	description='Создание датасета',
	path='/create_dataset/',
	validate=True
)


@ns.route('/sportmaster')
class CreateSportmasterDataset(Resource):
	@ns.response(int(HTTPStatus.OK), 'Task created successfully')
	@ns.expect(sportmaster_parser_info_reqparser)
	def post(self):
		"""Create task of getting dataset from sportmaster"""

		request_body = sportmaster_parser_info_reqparser.parse_args()
		catalog_url: str = request_body.get('catalog_url')
		pages: int = request_body.get('pages')
		# cookies: dict = request_body.get('cookies')
		# headers: dict = request_body.get('headers')

		result = create_sportmaster_dataset.delay(catalog_url, pages)
		response = jsonify({
			'result_id': result.id,
			'message': 'task created successfully'
		})
		response.status_code = HTTPStatus.OK

		return response