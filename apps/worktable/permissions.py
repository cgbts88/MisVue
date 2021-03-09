from rest_framework import permissions

from django.contrib.auth import get_user_model


User = get_user_model()


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        edp_user_ids = User.objects.filter(department__simple_title='EDP').values('id')
        edp_user_list = []
        for ids in edp_user_ids:
            edp_user_list.append(ids['id'])
        if request.method in permissions.SAFE_METHODS:
            # print("权限1：", request.method)
            return True
        if request.method == 'POST' and request.user.id in edp_user_list:
            # print("权限2：", request.method)
            return True
        # print("验证1：", request.method)
        # print("验证2：", permissions.SAFE_METHODS)
        # print("验证3：", view)
        # print("验证4：", obj)
        # print("验证5：", edp_user_ids)
        return obj.proposer == request.user
