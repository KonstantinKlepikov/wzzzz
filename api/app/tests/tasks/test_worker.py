from app.tasks.worker import get_vacancy


def test_get_vacancy():

    assert get_vacancy(api_url='a', params={'b': 'c'}) == 'Abcdz', 'wrong result'
