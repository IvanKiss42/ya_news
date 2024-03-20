import pytest
from http import HTTPStatus

from django.urls import reverse
from pytest_lazyfixture import lazy_fixture
from pytest_django.asserts import assertRedirects


# пока не проверена отдельная новость и ред/уд комментария
@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, news_example',
    (
        ('news:home', None),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
        ('news:detail', lazy_fixture('news')))
)
def test_pages_availability_for_anonymous_user(client, name, news_example):
    if news_example is not None:
        url = reverse(name, args=(news_example.id,))
    else:
        url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
def test_comment_pages_availability_for_anonymous_user_(client, name, comment):
    login_url = reverse('users:login')
    url = reverse(name, args=(comment.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
        (lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
def test_pages_availability_for_auth_user(
    parametrized_client, name, comment, expected_status
):
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status
