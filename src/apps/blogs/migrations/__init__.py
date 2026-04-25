from apps.blogs.data_class.blog import Blog
from apps.blogs.data_class.blog_category import BlogCategory


def init(apps, schema_editor):
    BlogCategory.table_create(apps)
    Blog.table_create(apps)


def init_reverse(apps, schema_editor):
    """
    NOTE: Keep it because it'll complain when you make `make sql-init-test`
    """
