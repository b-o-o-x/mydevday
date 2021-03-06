from flask import Flask, Blueprint, render_template, jsonify, request  # Flask 서버 객체 import
from _system import db  # mongodb 정보

devday = Blueprint('devday', __name__)


# time
import time


##############################
# main
##############################

# 메인 화면
@devday.route('/')
def main():
    # mongo test
    ip_addr = request.remote_addr;
    url = request.url;
    user_agent = request.user_agent.string;
    current_time = time.strftime('%y-%m-%d %H:%M:%S');
    doc = {'ip_addr': ip_addr, 'url': url, 'user_agent': user_agent, 'connect_time': current_time}
    db.log.insert_one(doc)

    return render_template('DevDay/index.html')
    return jsonify({
        'result': {
            'success': 'true',
            'message': '3팀 전국구 MyDevDay.'
        },
        'row_count': 1,
        'row': [
            {
                'name': 'Andy',
                'tel': '010-3292-3892',
                'email': 'booxboox@naver.com'
            },
        ]
    })


# test page
@devday.route('/test')
def test():
    return render_template('DevDay/index_test.html')


# 공개된 전체 데이터 요청 API
@devday.route('/devday', methods=['POST'])
def devday_list():
    print('devday_list')

    per_page = 6;
    page = max(0, int(request.form['page']) - 1)

    datas = list(db.post.find({}, {}).limit(per_page).skip(per_page * page).sort('date', -1))

    if len(datas) <= 0:
        return jsonify({
            'result': {
                'success': 'false',
                'message': 'devday 목록이 없습니다',
                'row_count': 0,
                'row': [],
            }
        })

    ret_datas = [];
    for d in datas:
        likedata = list(db.devday_like.find({'dev_id': str(d['_id'])}))
        commentdata = list(db.devday_comment.find({'dev_id': str(d['_id'])}))

        ret_datas.append({
            'user_id': d['writer'],
            'dev_id': str(d['_id']),
            'subject': d['title'],
            'content': '',
            'category': d['category'],
            'memo1': d['goal'],
            'memo2': d['todayLearned'],
            'memo3': d['todo'],
            'memo4': '',
            'memo5': '',
            'feeling': d['feeling'],
            'emoticon': d['emoticon'],
            'date': d['date'][0:10],
            'like_count': len(likedata),  # 임시
            'comment_count': len(commentdata),  # 임시
        })


    if len(datas) >= 1:
        return jsonify({
            'result': {
                'success': 'true',
                'message': 'devday 목록 가져오기 성공',
                'row_count': len(datas),
                'row': ret_datas,
            }
        })
