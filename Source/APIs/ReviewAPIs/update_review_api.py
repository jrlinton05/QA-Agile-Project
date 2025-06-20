from Source.Constants.constants import REVIEW_TABLE_NAME
from Source.Enums.generic_return_codes import GenericReturnCodes
from Source.Enums.update_api_return_codes import UpdateReturnCodes
from Source.Helpers.database_query_helper import query_database


def update_review(review_id, **kwargs):
    fields = []
    params = []

    if 'review_title' in kwargs and kwargs['review_title'] is not None:
        fields.append("review_title = ?")
        params.append(kwargs['review_title'])

    if 'review_body' in kwargs and kwargs['review_body'] is not None:
        fields.append("review_body = ?")
        params.append(kwargs['review_body'])

    if 'review_score' in kwargs and kwargs['review_score'] is not None:
        fields.append("review_score = ?")
        params.append(kwargs['review_score'])

    if 'product_id' in kwargs and kwargs['product_id'] is not None:
        fields.append("product_id = ?")
        params.append(kwargs['product_id'])

    if 'username' in kwargs and kwargs['username'] is not None:
        fields.append("username = ?")
        params.append(kwargs['username'])

    if not fields:
        return UpdateReturnCodes.NO_FIELDS_TO_UPDATE

    query = f'''
    UPDATE {REVIEW_TABLE_NAME}
    SET {", ".join(fields)}
    WHERE review_id = ?
    '''
    params.append(review_id)

    try:
        query_database(query, params=tuple(params))
    except:
        return GenericReturnCodes.ERROR
    else:
        return GenericReturnCodes.SUCCESS
