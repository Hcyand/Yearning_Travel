from ..models import Article, Scenery, LikeCount, LikeRecord, Topic
from django.contrib.contenttypes.models import ContentType


# 首页文章推荐
def get_hot_articles(content_type, num):
    res = []
    content_type = ContentType.objects.get(model=content_type)
    hot_likes = LikeCount.objects.filter(content_type=content_type).order_by('-like_num').values()
    for like in hot_likes[:num]:
        like_id = like['object_id']
        res.append(Article.objects.get(id=like_id))
    return res


# 首页景点top10
def get_hot_scenery(num):
    hot_scenery = Scenery.objects.all().order_by('rank')
    return hot_scenery[:num]


# 个人页面喜欢的文章
def get_user_like_article(content_type, user):
    res = []
    content_type = ContentType.objects.get(model=content_type)
    user_likes = LikeRecord.objects.values().filter(content_type=content_type, like_user=user)
    for like in user_likes:
        like_id = like['object_id']
        res.append(Article.objects.get(id=like_id))
    return res


# 个人页面喜欢景点
def get_user_like_scenery(content_type, user):
    res = []
    content_type = ContentType.objects.get(model=content_type)
    user_likes = LikeRecord.objects.values().filter(content_type=content_type, like_user=user)
    for like in user_likes:
        like_id = like['object_id']
        res.append(Scenery.objects.get(id=like_id))
    return res


# 个人页面喜欢话题
def get_user_like_topic(content_type, user):
    res = []
    content_type = ContentType.objects.get(model=content_type)
    user_likes = LikeRecord.objects.values().filter(content_type=content_type, like_user=user)
    for like in user_likes:
        like_id = like['object_id']
        res.append(Topic.objects.get(id=like_id))
    return res
