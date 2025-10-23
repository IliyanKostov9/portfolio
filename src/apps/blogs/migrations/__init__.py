from apps.blogs.data_class.blog import Blog
from apps.blogs.data_class.blog_category import BlogCategory


def init(apps, _):
    BlogCategory.table_create(apps)
    Blog.table_create(apps)


def init_reverse():
    """
    NOTE: Keep it because it'll complain when you make `make sql-init-test`
    """
