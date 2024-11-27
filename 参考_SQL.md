# SQL

今回使用するModel
```python:models.py
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

class Publisher(models.Model):
    name = models.CharField(max_length=300)
    num_awards = models.IntegerField()

class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    pubdate = models.DateField()
```

### SELECT句
#### 全列抽出
実際は、\*ではなく全列がSELECT句に列挙されますが、スペースの関係上\*で表記しています(以降も同様)。

なお、指定列抽出との比較のために.values()を付けていますが、省略可能です。

    b = Book.objects.all().values()
    #=> 'SELECT * FROM "runner_book"'

#### 指定列抽出
values()の引数に、抽出対象の列名を渡します。

    b = Book.objects.all().values('name')
    #=> SELECT "runner_book"."name" FROM "runner_book"

### WHERE句
通常はfilterを使います。

    b = Book.objects.all().filter(pubdate='2015-10-01')
    #=> 'SELECT * FROM "runner_book" 
    #    WHERE "runner_book"."pubdate" = %s' - PARAMS = ('2015-10-01',)

### NOT
excludeを使います。

    b = Book.objects.all().exclude(pubdate='2015-10-01')
    #=> 'SELECT * FROM "runner_book" 
    #    WHERE NOT ("runner_book"."pubdate" = %s)' - PARAMS = ('2015-10-01',)]

### AND
filterの引数を増やせばANDになります。

    b = Book.objects.all().filter(pubdate='2015-10-01', publisher=1)
    #=> 'SELECT * FROM "runner_book"
    #    WHERE ("runner_book"."publisher_id" = %s 
    #      AND "runner_book"."pubdate" = %s)' - PARAMS = (1, '2015-10-01')

### OR
Qオブジェクトを使います。

    b = Book.objects.all().filter(Q(pubdate='2015-10-01') | Q(publisher=1))
    #=> 'SELECT * FROM "runner_book"
    #    WHERE ("runner_book"."pubdate" = %s 
    #       OR "runner_book"."publisher_id" = %s)' - PARAMS = ('2015-10-01', 1)

### 演算子
主なものは以下にまとめられていました。

    b = Book.objects.all().filter(name__contains='d')
    #=> 'SELECT * FROM "runner_book"
    #    WHERE "runner_book"."name" LIKE %s ESCAPE \'\\\'' - PARAMS = ('%d%',)

### ORDER BY句

昇順

    b = Book.objects.all().order_by('pages')
    #=> SELECT * FROM "runner_book" ORDER BY "runner_book"."pages" ASC - PARAMS = ()

降順
降順キーの先頭に - を付けます。

    b = Book.objects.all().order_by('-pages')
    #=> SELECT * FROM "runner_book" ORDER BY "runner_book"."pages" DESC - PARAMS = ()

### GROUP BY句
#### 全体の集約
    # 集計結果には明示的な名前を付けない
    b1 = Book.objects.all().aggregate(Avg('price'))
    #=> SELECT AVG("runner_book"."price") AS "price__avg" FROM "runner_book"

    # 集計結果に対し、明示的に名前をつける
    b2 = Book.objects.all().aggregate(sum_price=Sum('price'))
    #=> SELECT SUM("runner_book"."price") AS "sum_price" FROM "runner_book"

#### 行の集約
values().annotate()の順で書く
Book.objects.annotate(price_avg=Avg('price')).values('publisher_id') では集約されない
values()にて、集約キーを書く
annotate()にて、新しい集約列を追加

    b = Book.objects.all().values('publisher_id').annotate(price_avg=Avg('price'))
    #=> SELECT "runner_book"."publisher_id", 
    #          AVG("runner_book"."price") AS "price_avg"
    #   FROM "runner_book"
    #   GROUP BY "runner_book"."publisher_id"

### LIMIT句

LIMITのみ

    b = Book.objects.all()[:2]
    #=> SELECT * FROM "runner_book" LIMIT 2

OFFSET付

    # 2-3番目を取り出す
    b = Book.objects.all()[1:3]
    #=> SELECT * FROM "runner_book" LIMIT 2 OFFSET 1

Pythonのstep付

    # 始まり1、終わり3、step2
    b = Book.objects.all()[:3:2]
    #=> SELECT * FROM "runner_book" LIMIT 3

### JOIN

#### INNER JOIN
状況に応じて、filterやselect_relatedを使います。
```
# INNER JOINするけど、SELECT句にはpublisherの列は無い
b1 = Book.objects.filter(publisher__num_awards=5)
#=> SELECT "runner_book"."id", "runner_book"."name", "runner_book"."pages", 
#          "runner_book"."price", "runner_book"."rating", 
#          "runner_book"."publisher_id", "runner_book"."pubdate"
#   FROM "runner_book"
#   INNER JOIN "runner_publisher" 
#       ON ( "runner_book"."publisher_id" = "runner_publisher"."id" )
#   WHERE "runner_publisher"."num_awards" = %s
#   LIMIT 21 - PARAMS = (5,)
```

```
# INNER JOINし、SELECT句にもpublisherの列がある
b2 = Book.objects.select_related().all()
#=> SELECT "runner_book"."id", "runner_book"."name", "runner_book"."pages",
#          "runner_book"."price", "runner_book"."rating", 
#          "runner_book"."publisher_id", "runner_book"."pubdate",
#          "runner_publisher"."id", "runner_publisher"."name", 
#          "runner_publisher"."num_awards"
#   FROM "runner_book"
#   INNER JOIN "runner_publisher"
#       ON ( "runner_book"."publisher_id" = "runner_publisher"."id" )
#   LIMIT 21 - PARAMS = ()
```

```
# INNER JOINとWHEREを使って、全列出す
b3 = Book.objects.filter(publisher__num_awards=5).select_related().all()
#=> SELECT "runner_book"."id", "runner_book"."name", "runner_book"."pages", 
#          "runner_book"."price", "runner_book"."rating", 
#          "runner_book"."publisher_id", "runner_book"."pubdate",
#          "runner_publisher"."id", "runner_publisher"."name", 
#          "runner_publisher"."num_awards"
#   FROM "runner_book"
#   INNER JOIN "runner_publisher" 
#       ON ( "runner_book"."publisher_id" = "runner_publisher"."id" )
#   WHERE "runner_publisher"."num_awards" = %s
#   LIMIT 21 - PARAMS = (5,)
```

### LEFT JOIN

とりあえず分かっている範囲のLEFT JOINは以下のとおりです。

```
# id IS NULL
p1 = Publisher.objects.filter(book__isnull=True)
#=> SELECT *
#   FROM "runner_publisher"
#   LEFT OUTER JOIN "runner_book" 
#       ON ( "runner_publisher"."id" = "runner_book"."publisher_id" )
#   WHERE "runner_book"."id" IS NULL
```

```
# publisher_id IS NULL
p2 = Publisher.objects.filter(book__publisher__isnull=True)
#=> SELECT *
#   FROM "runner_publisher"
#   LEFT OUTER JOIN "runner_book"
#      ON ( "runner_publisher"."id" = "runner_book"."publisher_id" )
#   WHERE "runner_book"."publisher_id" IS NULL
```

### 逆方向のJOIN
外部キーの設定先から外部キーの設定元へたぐります。

```
# p = Author.objects.filter(age__gt=5)や
# p = Author.objects.all() だと逆引きできない

a = Author.objects.get(pk=1).book_set.all()
#=> SELECT "runner_book"."id", "runner_book"."name", "runner_book"."pages", 
#          "runner_book"."price", "runner_book"."rating", 
#          "runner_book"."publisher_id", "runner_book"."pubdate"
#   FROM "runner_book"
#   INNER JOIN "runner_book_authors" 
#       ON ( "runner_book"."id" = "runner_book_authors"."book_id" )
#   WHERE "runner_book_authors"."author_id" = %s
#   LIMIT 21 - PARAMS = (1,)
```

### 複数のJOIN
<table_name>__<table_name>__<column_name>で複数テーブルをまたがってJOINします。

```
a = Author.objects.filter(book__publisher__name='Pub2')
#=> SELECT "runner_author"."id", "runner_author"."name", "runner_author"."age"
#   FROM "runner_author"
#   INNER JOIN "runner_book_authors"
#       ON ( "runner_author"."id" = "runner_book_authors"."author_id" )
#       INNER JOIN "runner_book" 
#           ON ( "runner_book_authors"."book_id" = "runner_book"."id" )
#           INNER JOIN "runner_publisher"
#               ON ( "runner_book"."publisher_id" = "runner_publisher"."id" )
#   WHERE "runner_publisher"."name" = %s
#   LIMIT 21 - PARAMS = ('Pub2',)
```

### データベース関数の利用
```
b = Book.objects.all()\
                .extra(select={'month': "strftime('%m', pubdate)"})\
                .values('month')\
                .annotate(sum_price=Sum('price'))
#=> SELECT (strftime(\'%m\', pubdate)) AS "month", 
#          SUM("runner_book"."price") AS "sum_price"
#   FROM "runner_book"
#   GROUP BY (strftime(\'%m\', pubdate))
```

strftime()の結果を、文字列から数値へとキャストする方法は以下の通りです。

```
b = Book.objects.all()\
                .extra(select={'month': "cast(strftime('%m', pubdate) AS integer)"})\
                .values('month')\
                .annotate(max_price=Max('price'))
#=> SELECT (cast(strftime(\'%m\', pubdate) AS integer)) AS "month", 
#          MAX("runner_book"."price") AS "max_price"
#   FROM "runner_book"
#   GROUP BY (cast(strftime(\'%m\', pubdate) AS integer))
```

### CASE式
Django1.8よりCASE式にも対応しているようです。

```
# name列とcase式で作成したimpression列を表示
b = Book.objects.annotate(
    impression=Case(
        When(pages=10, then=Value('short')),
        When(pages=20, then=Value('short')),
        When(pages=30, then=Value('good')),
        When(pages=40, then=Value('long')),
        default=Value('nothing'),
        output_field=CharField()
    )
).values('name', 'impression')
#=> SELECT "runner_book"."name",
#   CASE WHEN "runner_book"."pages" = %s THEN %s
#        WHEN "runner_book"."pages" = %s THEN %s
#        WHEN "runner_book"."pages" = %s THEN %s
#        WHEN "runner_book"."pages" = %s THEN %s
#        ELSE %s END AS "impression"
#   FROM "runner_book"
#   LIMIT 21' - PARAMS = (10, 'short', 20, 'short', 30, 'good', 40, 'long', 'nothing')
```

```
b = Book.objects.values('rating').filter(rating__gt=3).annotate(
# defalutがあるので、then=0はいらないけど、見栄え上残しておく
b = Book.objects.values('rating').filter(rating__gt=3).annotate(
    # defalutがあるので、then=0はいらないけど、見栄え上残しておく
    pub1=Sum(Case(
        When(rating=5, then=1),
        When(rating=4, then=0),
        default=Value(0),
        output_field=IntegerField()
    )),
    pub2=Sum(Case(
        When(rating=5, then=0),
        When(rating=4, then=1),
        default=Value(0),
        output_field=IntegerField()
    ))
)
#=> SELECT "runner_book"."rating",
#          SUM(CASE
#              WHEN "runner_book"."rating" = %s THEN %s
#              WHEN "runner_book"."rating" = %s THEN %s 
#              ELSE %s END) AS "pub2",
#          SUM(CASE 
#              WHEN "runner_book"."rating" = %s THEN %s
#              WHEN "runner_book"."rating" = %s THEN %s
#              ELSE %s END) AS "pub1"
#   FROM "runner_book"
#   WHERE "runner_book"."rating" > %s
#   GROUP BY "runner_book"."rating"
#   LIMIT 21' - PARAMS = (5.0, 0, 4.0, 1, 0, 5.0, 1, 4.0, 0, 0, 3.0)
```