# 名字：Pains
# 时间：2024/6/27 15:23
def get_responder(request):
    user = request.user

    if user.department.leader.uid == user.uid:
        if user.department.name == '董事会':
            responder = None
        else:
            responder = user.department.manager
    else:
        responder = user.department.leader

    return responder