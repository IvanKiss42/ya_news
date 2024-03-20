import pytest

from django.urls import reverse
from pytest_lazyfixture import lazy_fixture
from pytest_django.asserts import assertFormError

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (lazy_fixture('client'), False),
        (lazy_fixture('author_client'), True)
    ),
)
def test_comment_post(parametrized_client, expected_status, news, form_data):
    url = reverse('news:detail', args=(news.id,))
    parametrized_client.post(url, data=form_data)
    assert (Comment.objects.count() == 1) is expected_status


def test_bad_words(author_client, news):
    url = reverse('news:detail', args=(news.id,))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}'}
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (lazy_fixture('reader_client'), False),
        (lazy_fixture('author_client'), True)
    ),
)
def test_edit_availability_for_users(
    parametrized_client, new_comment_data, comment, expected_status
):
    url = reverse('news:edit', args=(comment.id,))
    parametrized_client.post(url, data=new_comment_data)
    comment.refresh_from_db()
    assert (comment.text == new_comment_data['text']) == expected_status


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (lazy_fixture('reader_client'), False),
        (lazy_fixture('author_client'), True)
    ),
)
def test_delete_availability_for_users(
    parametrized_client, comment, expected_status
):
    url = reverse('news:delete', args=(comment.id,))
    parametrized_client.post(url)
    assert (Comment.objects.count() == 0) == expected_status
