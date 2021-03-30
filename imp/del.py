from article.models import Article, Viewer
from django.contrib.auth.models import User


article_data_obj = Article.objects.get(url_title='demo')
user_data_obj = User.objects.get(username='ajinkya')
article_instance = Article.objects.get(pk=article_data_obj.id)
user_instance = User.objects.get(pk=user_data_obj.id)


obj, created = Viewer.objects.get_or_create(article_id=article_instance, user_id=user_instance, ip_address="127.0.0.0.1", device_agent='P', is_touch_capable=False, is_bot=False, browser_details="Firefox", os_details="Ubuntu", device_agent_family="unknown")
print(created)
