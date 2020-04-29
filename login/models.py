from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class User(models.Model):
    """用户表"""

    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    address = models.CharField(max_length=256, null=True)
    img = models.ImageField(upload_to='img', null=True)
    c_time = models.DateTimeField(auto_now_add=True)

    # __str__帮助人性化显示对象信息
    def __str__(self):
        return self.name

    # 元数据定义用户创建时间的反序排列，最近最先显示
    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


# 文章
class Article(models.Model):
    name = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    likes = models.PositiveIntegerField(default=0)
    introduce = models.CharField(max_length=256)
    place = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    content = models.TextField()
    img = models.ImageField(upload_to='img')
    read_num = models.IntegerField(default=0)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '文章'
        verbose_name_plural = '文章'


# 主题
class Theme(models.Model):
    type = models.CharField(max_length=256)
    content = models.TextField()
    img = models.ImageField(upload_to='img')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type

    class Meta:
        ordering = ['c_time']
        verbose_name = '主题'
        verbose_name_plural = '主题'


# 话题
class Topic(models.Model):
    name = models.CharField(max_length=128)
    content = models.TextField()
    type = models.CharField(max_length=128)
    likes = models.IntegerField(default=0)
    author = models.CharField(max_length=128)
    img = models.ImageField(upload_to='img', null=True)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '话题'
        verbose_name_plural = '话题'


# 景区
class Scenery(models.Model):
    name = models.CharField(max_length=128)
    place = models.CharField(max_length=128)
    content = models.TextField()
    hot = models.IntegerField()
    type = models.CharField(max_length=128)
    introduce = models.CharField(max_length=256)
    rank = models.IntegerField()
    img = models.ImageField(upload_to='img', null=True)
    read_num = models.IntegerField(default=0)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '景区'
        verbose_name_plural = '景区'


# 商品
class Shop(models.Model):
    name = models.CharField(max_length=256)
    price = models.IntegerField()
    type = models.CharField(max_length=128)
    hot = models.IntegerField()
    img = models.ImageField(upload_to='img', null=True)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '商品'
        verbose_name_plural = '商品'


# 用于记录点赞数量的模型
class LikeCount(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # 用于记录点赞数量的字段
    like_num = models.IntegerField(default=0)

    class Meta:
        verbose_name = '点赞数量'
        verbose_name_plural = '点赞数量'


# 用于记录点赞状态的模型
class LikeRecord(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # 记录点赞的用户
    like_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # 记录点赞的时间
    like_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '点赞状态'
        verbose_name_plural = '点赞状态'


# 用来记录用户个性化信息
class Personality(models.Model):
    per_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    problem_one = models.IntegerField()
    problem_two = models.IntegerField()
    problem_three = models.IntegerField()
    c_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '个性化信息'
        verbose_name_plural = '个性化信息'


# 用于记录阅读数量的模型
class ReadCount(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # 用于记录阅读数量的字段
    read_num = models.IntegerField(default=0)

    class Meta:
        verbose_name = '阅读数量'
        verbose_name_plural = '阅读数量'


# 用于记录阅读状态的模型
class ReadRecord(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # 记录阅读的用户
    read_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # 记录阅读的时间
    read_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '阅读记录'
        verbose_name_plural = '阅读记录'
