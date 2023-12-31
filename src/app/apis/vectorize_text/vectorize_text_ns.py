from http import HTTPStatus
from flask import jsonify
from flask_restx import Namespace, Resource
from src.app.core.sentiment_analyse.vectorize_text import (
	process_convert_tokens_in_seq_of_codes,
	process_vectorize_sequences,
	process_embeddings_vectorization
)

from .dto import vectorization_sequence_model, tokenlist_model, embedding_vectorization_model
from ..utilities.utils import fill_with_default_values

ns = Namespace(
	name='Vectorization Controller',
	description='Tokens vectorization',
	path='/vectorization/',
	validate=True
)


@ns.route('/convert_tokens_in_codes')
class VectorizationAPI(Resource):
	@ns.response(int(HTTPStatus.OK), 'Sequence of codes for given tokens and meta data')
	@ns.expect(tokenlist_model)
	@ns.doc(
		description='Here you can turn tokens into a list of codes. '
					'First, the most common words are selected. '
					'You can limit the list of words using the maxWords parameter. '
					'You will receive a sequence that will define your tokens in the form of a list of codes.'
	)
	def post(self):
		""" Convert tokens in sequence of codes """

		fill_with_default_values(ns.payload, tokenlist_model)
		d = ns.payload

		tokens = d.get('tokens')
		max_words = d.get('maxWords')

		seq, word_to_index, index_to_word = process_convert_tokens_in_seq_of_codes(tokens, max_words)
		response = jsonify({
			'sequence': seq,
			'wordToIndex': word_to_index,
			'indexToWord': index_to_word
		})
		response.status_code = HTTPStatus.OK

		return response


@ns.route('/vectorize_sequences')
class VectorizationSequenceAPI(Resource):
	@ns.response(int(HTTPStatus.OK), 'Vectorized sequences')
	@ns.response(int(HTTPStatus.BAD_REQUEST), 'User entered invalid parameters')
	@ns.expect(vectorization_sequence_model)
	@ns.doc(
		description='A bag of words is a vector that contains as many elements as the words being analyzed. '
					'Each element of the vector corresponds to a specific word, and the value of the vector '
					'is equal to the number of times the word occurs in the text'

	)
	def post(self):
		""" Vectorize sequence using Bag Of Words Algorithm """

		fill_with_default_values(ns.payload, vectorization_sequence_model)
		d = ns.payload

		sequence = d.get('sequences')
		dimension = d.get('dimension')

		if dimension <= 0:
			response = jsonify({
				'error': "'dimension' parameter can't be <= 0."
			})
			response.status_code = HTTPStatus.BAD_REQUEST
			return response

		vectorized_sequences = process_vectorize_sequences(sequence, dimension)
		response = jsonify({
			'vectorizedSequences': vectorized_sequences
		})
		response.status_code = HTTPStatus.OK

		return response


@ns.route('/embedding_vectorize_text')
class EmbeddingVectorizationAPI(Resource):
	@ns.response(int(HTTPStatus.OK), 'Embeddings vectors')
	@ns.expect(embedding_vectorization_model)
	@ns.doc(
		description='Here you can get a list of vector representations of words obtained using the Navec model'
	)
	def post(self):
		""" Get embeddings vectors from tokens """

		d = ns.payload
		tokens = d.get('tokens')
		# max_review_len = d.get('maxReviewLen')
		max_review_len = len(tokens)

		embeddings = process_embeddings_vectorization(tokens, max_review_len)
		embeddings = [[float(num) for num in vect]
					  for vect in embeddings]
		response = jsonify({
			'embeddings': embeddings
		})
		response.status_code = HTTPStatus.OK

		return response
