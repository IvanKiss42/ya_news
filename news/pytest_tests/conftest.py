import pytest
import time

from model_bakery import baker

from news.models import News, Comment


NEWS_FOR_TESTS = 15


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def reader_user(django_user_model):
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def reader_client(reader_user, client):
    client.force_login(reader_user)
    return client


@pytest.fixture
def news(db):
    return News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        text='Текст комментария',
        author=author,
    )


@pytest.fixture
def a_lot_of_news(db):
    return baker.make("news", _quantity=NEWS_FOR_TESTS)


@pytest.fixture
def a_lot_of_comment(news, author):
    comment_list = []
    for index in range(2):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        time.sleep(0.001)
        comment_list.append(comment)
    return comment_list


@pytest.fixture
def form_data():
    return {
        'text': 'Текст',
    }


@pytest.fixture
def new_comment_data():
    return {
        'text': 'Новый текст',
    }
