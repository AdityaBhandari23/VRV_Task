from rest_framework.permissions import BasePermission

# class HasRole(BasePermission):
#     def has_permission(self, request, view):
#         required_role = getattr(view, 'required_role', None)
#         if required_role:
#             return request.user.user_roles.filter(role__name=required_role)
#         return False

ROLE_HIERARCHY = {
    'director': 3,
    'hod': 2,
    'student': 1,
}

class RolePermission(BasePermission):
    def has_permission(self, request, view):
        # Get required role for the view
        required_role = getattr(view, 'required_role', None)
        if not required_role:
            return True  # No role restriction on this view

        # Check if the user has sufficient role privilege
        user_roles = request.user.user_roles.all()
        user_highest_role = max(
            [ROLE_HIERARCHY.get(role.role.name, 0) for role in user_roles],
            default=0
        )
        return user_highest_role >= ROLE_HIERARCHY.get(required_role, 0)