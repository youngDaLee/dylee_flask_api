from flask import Blueprint, request

from utils.response import response
from database import query

bp = Blueprint('health', __name__, url_prefix='/health')


@bp.route('/stats', methods=['GET'])
def stats():
    """
    환자와 방문 테이블들 간단한 통계를 제공하는 API
    """
    is_suc, data = query.stats_data_select({})
    if is_suc:
        return response(200, data)
    else:
        return response(500)


@bp.route('/concept-id', methods=['GET'])
def concept_id():
    """
    concept db에 대한 데이터 조회, 검색, 페이지네이션 제공 api
    """
    try:
        offset = request.args.get('offset', 0)
        limit = request.args.get('offset', 10)
        category = request.args.get('category', None)
        search_keyword = request.args.get('search_keyword', None)

    except KeyError:
        return response(400)

    args = {
        'offset': offset,
        'limit': limit,
        'category': category,
        'search_keyword': search_keyword,
    }

    is_suc, data = query.concept_id_select(args)
    if is_suc:
        return response(200, data)
    else:
        return response(500)


@bp.route('/row', methods=['GET'])
def row():
    try:
        # concept_id = request.args['concept_id']

        offset = request.args.get('offset', 0)
        limit = request.args.get('offset', 10)

        category = request.args.get('category', None)
        search_keyword = request.args.get('search_keyword', None)

    except KeyError:
        return response(400)

    args = {
        # 'concept_id': concept_id,
        'offset': offset,
        'limit': limit,
        'category': category,
        'search_keyword': search_keyword,
    }

    is_suc, data = query.table_select(args)
    if is_suc:
        return response(200, data)
    else:
        return response(500)
