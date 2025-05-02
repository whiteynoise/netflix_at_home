from sqlalchemy import text

def users_by_roles():
    return text("""
        SELECT u.username, u.email, u.first_name, u.last_name
        FROM auth.user_roles ur
        JOIN auth.roles r ON ur.role_id = r.role_id
        JOIN auth.users u ON ur.user_id = u.user_id
        WHERE r.title = ANY(:roles)
    """)


def users_by_user_id():
    return text("""
        SELECT u.username, u.email, u.first_name, u.last_name
        FROM auth.users u
        WHERE u.user_id = :user_id
    """)


def get_template_by_id():
    return text("""
        SELECT path
        FROM events_admin.template
        WHERE id = :template_id
    """)
