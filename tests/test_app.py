import json
import os
import tempfile

import pytest

from app import app, filter_memos, get_all_tags, sorted_memos, validate_memo_input


@pytest.fixture
def client():
    """Flask test client fixture."""
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client


@pytest.fixture
def temp_data(monkeypatch):
    """Use a temporary directory for data files during tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "memos.json")
        backup_file = os.path.join(tmpdir, "memos.json.bak")
        lock_file = os.path.join(tmpdir, "memos.lock")
        secret_file = os.path.join(tmpdir, ".secret_key")

        monkeypatch.setattr("app.DATA_FILE", data_file)
        monkeypatch.setattr("app.BACKUP_FILE", backup_file)
        monkeypatch.setattr("app.LOCK_FILE", lock_file)
        monkeypatch.setattr("app.SECRET_KEY_FILE", secret_file)

        # Create empty data file
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump([], f)

        yield tmpdir


class TestValidateMemoInput:
    def test_empty_title(self):
        assert validate_memo_input("", "content") == "标题和内容都不能为空！"

    def test_empty_content(self):
        assert validate_memo_input("title", "") == "标题和内容都不能为空！"

    def test_title_too_long(self):
        assert validate_memo_input("x" * 201, "content") == "标题不能超过200字符！"

    def test_content_too_long(self):
        assert validate_memo_input("title", "x" * 50001) == "内容不能超过50000字符！"

    def test_valid(self):
        assert validate_memo_input("title", "content") is None


class TestSortedMemos:
    def test_pinned_first(self):
        memos = [
            {"title": "B", "pinned": False, "created_at": "2026-04-20 10:00:00"},
            {"title": "A", "pinned": True, "created_at": "2026-04-20 09:00:00"},
        ]
        result = sorted_memos(memos)
        assert result[0]["title"] == "A"
        assert result[1]["title"] == "B"

    def test_newer_first_same_pinned(self):
        memos = [
            {"title": "Old", "pinned": False, "created_at": "2026-04-20 09:00:00"},
            {"title": "New", "pinned": False, "created_at": "2026-04-20 10:00:00"},
        ]
        result = sorted_memos(memos)
        assert result[0]["title"] == "New"
        assert result[1]["title"] == "Old"


class TestFilterMemos:
    def test_search_by_title(self):
        memos = [
            {"title": "Hello World", "content": "foo"},
            {"title": "Goodbye", "content": "bar"},
        ]
        result = filter_memos(memos, q="hello")
        assert len(result) == 1
        assert result[0]["title"] == "Hello World"

    def test_filter_by_tag(self):
        memos = [
            {"title": "A", "tags": ["work"]},
            {"title": "B", "tags": ["life"]},
        ]
        result = filter_memos(memos, tag="work")
        assert len(result) == 1
        assert result[0]["title"] == "A"


class TestGetAllTags:
    def test_collects_all_unique_tags(self):
        memos = [
            {"title": "A", "tags": ["work", "idea"]},
            {"title": "B", "tags": ["work", "life"]},
        ]
        result = get_all_tags(memos)
        assert result == ["idea", "life", "work"]


class TestRoutes:
    def test_index_page(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "我的备忘录".encode() in response.data

    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "healthy"

    def test_add_memo(self, client, temp_data):
        response = client.post(
            "/add",
            data={"title": "Test Note", "content": "Test content", "tags": "work, idea"},
            follow_redirects=True,
        )
        assert response.status_code == 200

    def test_add_memo_empty_title(self, client, temp_data):
        response = client.post(
            "/add",
            data={"title": "", "content": "Test content", "tags": ""},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert "标题和内容都不能为空" in response.data.decode("utf-8")

    def test_delete_nonexistent_memo(self, client, temp_data):
        response = client.post(
            "/delete/nonexistent-id",
            follow_redirects=True,
        )
        assert response.status_code == 200
