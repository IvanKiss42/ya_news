import pytest

from django.urls import reverse
from pytest_lazyfixture import lazy_fixture

NO_MORE_NEWS_THAN = 10


def test_main_page_news_amount(client, a_lot_of_news):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    assert len(object_list) <= NO_MORE_NEWS_THAN


def test_main_page_order(client, a_lot_of_news):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comment_order(client, news, a_lot_of_comment):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    news_all = response.context['news']
    all_comments = news_all.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (lazy_fixture('admin_client'), True),
        (lazy_fixture('client'), False)
    ),
)
def test_form_availability_for_auth_user(
    parametrized_client, expected_status, news
):
    url = reverse('news:detail', args=(news.id,))
    response = parametrized_client.get(url)
    assert ('form' in response.context) is expected_status
