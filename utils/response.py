from flask import jsonify

MESSAGE_TABLE = {
    200: "success",
    400: "missig_params",
    412: "invalid_data",
    500: "internel_server_error",
}


def response(status_code, data=None, message=''):
    """
    return jsonify response

    :param status_code: ``int`` status_code
    :param data: ``Optional`` 
    :param message: ``Optional`` ``str``

    >> response(200)
    {
        'status_code': 200,
        'message': 'success',
        'data': None
    }
    """

    if not message:
        try:
            message = MESSAGE_TABLE[status_code]
        except:
            pass

    return jsonify({
        'status_code': status_code,
        'message': message,
        'data': data
    })
