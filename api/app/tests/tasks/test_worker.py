from app.tasks.worker import save_to_db


def test_one():

    assert save_to_db.delay('a').get(timeout=1) == None