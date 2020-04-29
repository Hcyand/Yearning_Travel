"""
旅游推荐系统，基于物品的协同过滤算法实现
"""
import math
from operator import itemgetter
from ..models import LikeRecord, Scenery, ReadRecord, Personality, Article
from django.contrib.contenttypes.models import ContentType


# 推荐景区
def recommend_scenery(user_now, N):
    # N表示推荐数量
    # 数据集
    data = {}
    rating = 1
    content_type = ContentType.objects.get(model="scenery")
    for scenery in LikeRecord.objects.filter(content_type=content_type):
        user = scenery.like_user.id
        read_rating = 0.1
        if ReadRecord.objects.filter(content_type=content_type, object_id=scenery.id, read_user=scenery.like_user):
            num = 0
            read_record = ReadRecord.objects.get(content_type=content_type, object_id=scenery.id,
                                                 read_user=scenery.like_user)
            for i in read_record:
                num += 1
            read_rating = 0.1 * (2 ** num)
        x = 1
        if Personality.objects.filter(per_user=user):
            person = Personality.objects.get(per_user=user)
            scenery_type = Scenery.objects.get(id=scenery.object_id).type
            if scenery_type == "城市":
                if person.problem_one == 1:
                    x = x * 1.1
                if person.problem_two == 1:
                    x = x * 1.1
                if person.problem_three == 1:
                    x = x * 1.1
            else:
                if person.problem_one == 2:
                    x = x * 1.1
                if person.problem_two == 2:
                    x = x * 1.1
                if person.problem_three == 2:
                    x = x * 1.1
        data.setdefault(user, {})
        data[user][scenery.object_id] = (rating + read_rating) * x
    # 初始化景区相似度矩阵
    scenery_sim_matrix = {}
    # 受欢迎的景区
    scenery_popular = {}

    # 计算景区间相似度
    # 建立scenery_popular字典
    for user, scenerys in data.items():
        for scenery in scenerys:
            if scenery not in scenery_popular:
                scenery_popular[scenery] = 0
            else:
                scenery_popular[scenery] += 1
    # 建立景区间的相似度
    for user, scenerys in data.items():
        for s1 in scenerys:
            for s2 in scenerys:
                if s1 == s2:
                    continue
                scenery_sim_matrix.setdefault(s1, {})
                scenery_sim_matrix[s1].setdefault(s2, 0)
                scenery_sim_matrix[s1][s2] += 1 / math.log(1 + len(scenerys))  # 惩罚活跃用户
    # 计算景区之间的相似度
    for s1, related_scenerys in scenery_sim_matrix.items():
        for s2, count in related_scenerys.items():
            if scenery_popular[s1] == 0 or scenery_popular[s2] == 0:
                scenery_sim_matrix[s1][s2] = 0
            else:
                scenery_sim_matrix[s1][s2] = count / math.sqrt(scenery_popular[s1] * scenery_popular[s2])

    # 针对目标用户，推荐其中N个
    rank = {}
    watched_scenerys = data[user_now.id]
    for scenery, rating in watched_scenerys.items():
        for related_scenery, w in sorted(scenery_sim_matrix[scenery].items(), key=itemgetter(1), reverse=True):
            if related_scenery in watched_scenerys:
                continue
            rank.setdefault(related_scenery, 0)
            # 计算推荐度
            rank[related_scenery] += w * float(rating)
    rem = sorted(rank.items(), key=itemgetter(1), reverse=True)[:N]
    res = []
    for i in rem:
        res.append([Scenery.objects.get(id=i[0]), i[1]])
    return res


# 推荐文章
def recommend_article(user_now, N):
    # N 表示推荐数量
    # 数据集
    data = {}
    rating = 1
    content_type = ContentType.objects.get(model="article")
    for article in LikeRecord.objects.filter(content_type=content_type):
        user = article.like_user.id
        read_rating = 0.1
        if ReadRecord.objects.filter(content_type=content_type, object_id=article.id, read_user=article.like_user):
            num = 0
            read_record = ReadRecord.objects.get(content_type=content_type, object_id=article.id,
                                                 read_user=article.like_user)
            for i in read_record:
                num += 1
            read_rating = 0.1 * (2 ** num)
        data.setdefault(user, {})
        data[user][article.object_id] = rating + read_rating
    # 初始化文章相似度矩阵
    article_sim_matrix = {}
    # 受欢迎的文章
    article_popular = {}

    # 计算文章间相似度
    # 建立article_popular字典
    for user, articles in data.items():
        for article in articles:
            if article not in article_popular:
                article_popular[article] = 0
            else:
                article_popular[article] += 1
    # 建立文章间相似度
    for user, articles in data.items():
        for a1 in articles:
            for a2 in articles:
                if a1 == a2:
                    continue
                article_sim_matrix.setdefault(a1, {})
                article_sim_matrix[a1].setdefault(a2, 0)
                article_sim_matrix[a1][a2] += 1 / math.log(1 + len(articles))  # 惩罚活跃用户
    # 计算文章之间相似度
    for a1, related_articles in article_sim_matrix.items():
        for a2, count in related_articles.items():
            if article_popular[a1] == 0 or article_popular[a2] == 0:
                article_sim_matrix[a1][a2] = 0
            else:
                article_sim_matrix[a1][a2] = count / math.sqrt(article_popular[a1] * article_popular[a2])
    # 针对目标用户，推荐其中N个
    rank = {}
    watched_articles = data[user_now.id]
    for article, rating in watched_articles.items():
        for related_article, w in sorted(article_sim_matrix[article].items(), key=itemgetter(1), reverse=True):
            if related_article in watched_articles:
                continue
            rank.setdefault(related_article, 0)
            # 计算推荐度
            rank[related_article] += w * float(rating)
    rem = sorted(rank.items(), key=itemgetter(1), reverse=True)[:N]
    res = []
    for i in rem:
        res.append([Article.objects.get(id=i[0]), i[1]])
    return res
