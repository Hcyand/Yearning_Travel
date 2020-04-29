# 基于物品的协同过滤推荐算法实践
import random
import math
from operator import itemgetter
import csv
import pandas as pd


class ItemBaseCF:
    # 初始化参数
    def __init__(self):
        self.n_sim_movies = input('请输入用于推荐的参数的电影数k：')
        self.n_rec_movies = input('请输入对一个用户的推荐数：')

        # 将数据集划分为训练集和测试集
        self.trainSet = {}
        self.testSet = {}

        # 初始化电影相似度矩阵
        self.movies_sim_matrix = {}

        self.movie_popular = {}
        self.movie_count = 0
        # 找到相似的10部电影，为目标用户推荐4部电影
        print("参考电影数为：", self.n_sim_movies)
        print("推荐电影数为：", self.n_rec_movies)

    # 读文件得到“用户-电影”数据，并将数据划分为训练集和数据集
    def get_dataset(self, filename, pivot=0.75):
        trainSet_len = 0
        testSet_len = 0
        for line in self.load_file(filename):
            # rating用户对于物品的兴趣程度
            user, movie, rating, timestamp = line.split(',')
            if random.random() < pivot:
                self.trainSet.setdefault(user, {})
                self.trainSet[user][movie] = rating
                trainSet_len += 1
            else:
                self.testSet.setdefault(user, {})
                self.testSet[user][movie] = rating
                testSet_len += 1
        print("训练集长度：", trainSet_len)
        print(("测试集长度", testSet_len))

    # 读文件，返回文件每一行
    def load_file(self, filename):
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                if i == 0:
                    continue
                yield line.strip('\r\n')
        print("加载 %s 文件成功！" % filename)

    # 计算电影间的相似度
    def calc_movie_sim(self):
        # 建立movies_popular字典
        for user, movies in self.trainSet.items():
            for movie in movies:
                if movies not in self.movie_popular:
                    self.movie_popular[movie] = 0
                else:
                    self.movie_popular[movie] += 1
        self.movie_count = len(self.movie_popular)
        # 建立电影相似矩阵
        for user, movies in self.trainSet.items():
            for m1 in movies:
                for m2 in movies:
                    if m1 == m2:
                        continue
                    self.movies_sim_matrix.setdefault(m1, {})
                    self.movies_sim_matrix[m1].setdefault(m2, 0)
                    self.movies_sim_matrix[m1][m2] += 1
        # 计算电影之间的相似度
        for m1, related_movies in self.movies_sim_matrix.items():
            for m2, count in related_movies.items():
                # 注意0向量的处理，即某电影用户数为0
                if self.movie_popular[m1] == 0 or self.movie_popular[m2] == 0:
                    self.movies_sim_matrix[m1][m2] = 0
                else:
                    self.movies_sim_matrix[m1][m2] = count / math.sqrt(self.movie_popular[m1] * self.movie_popular[m2])

    # 针对目标用户，找出k部相似的电影，并且推荐其中N部
    def recommend(self, user):
        K = int(self.n_sim_movies)
        N = int(self.n_rec_movies)
        rank = {}
        watched_movies = self.trainSet[user]
        for movie, rating in watched_movies.items():
            # 对目标用户每一步看过的电影，从相似电影矩阵中取与这部电影关联最大的前K部电影，若用户之前没有看过，则加入rank
            for related_movie, w in sorted(self.movies_sim_matrix[movie].items(), key=itemgetter(1), reverse=True)[:K]:
                if related_movie in watched_movies:
                    continue
                rank.setdefault(related_movie, 0)
                # 计算推荐度
                rank[related_movie] += w * float(rating)
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[:N]

    # 产生推荐并通过准确率，召回率和覆盖率进行评估
    def evaluate(self):
        N = int(self.n_rec_movies)
        reuserN = input("请输入参与评估的用户数量：")
        reuserN = int(reuserN)
        # 准确率和召回率
        hit = 0
        rec_count = 0
        test_count = 0
        # 覆盖率
        all_rec_movies = set()
        for user, m in list(self.trainSet.items())[:reuserN]:
            test_movies = self.testSet.get(user, {})
            rec_movies = self.recommend(user)
            print("用户 %s 的电影推荐列表为：" % user)
            self.precommend(rec_movies)
            # 注意，这里的w与上面recommend的w不要一样，上面的w是指计算出的相似电影矩阵的权值，而这里是这推荐字典rank对应的推荐度
            for movie, w in rec_movies:
                if movie in test_movies:
                    hit += 1
                all_rec_movies.add(movie)
            rec_count += N
            test_count += len(test_movies)

        precision = hit / (1.0 * rec_count)
        recall = hit / (1.0 * test_count)
        coverage = len(all_rec_movies) / (1.0 * self.movie_count)
        print('准确率=%.4f\t召回率=%.4f\t覆盖率=%.4f' % (precision, recall, coverage))
        print('=' * 100)

    def precommend(self, rec_m):
        csv_file = "movies.csv"
        csv_data = pd.read_csv(csv_file, low_memory=False)
        df = pd.DataFrame(csv_data)
        for movieid, w in rec_m:
            print('电影名称:', df.loc[df['movieId'] == int(movieid), 'title'].values, '推荐度:', w)


if __name__ == '__main__':
    rating_file = "ratings.csv"
    itemCF = ItemBaseCF()
    itemCF.get_dataset(rating_file)
    itemCF.calc_movie_sim()
    itemCF.evaluate()
