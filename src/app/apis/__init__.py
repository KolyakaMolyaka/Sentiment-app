from flask_restx import Api

api = Api(
	prefix='/api/',
	title='Приложение для анализа тональности текста',
	description= \
		'Описание...',
	version='1.0',
)

from .create_datasets.create_datasets_ns import ns as create_datasets_ns
api.add_namespace(create_datasets_ns)

from .get_datasets_results.get_datasets_results_ns import ns as get_datasets_results_ns
api.add_namespace(get_datasets_results_ns)