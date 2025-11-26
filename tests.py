import sqlite3
import pytest
import transport_app  

class ManagerForTests(transport_app.FreightTransportManager):
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_table()

@pytest.fixture
def manager(tmp_path):
    db_file = tmp_path / "test_transport.db"
    m = ManagerForTests(str(db_file))
    yield m
    m.close()


@pytest.fixture
def msgbox(monkeypatch):
    info_calls = []
    error_calls = []

    def fake_showinfo(title, message):
        info_calls.append((title, message))

    def fake_showerror(title, message):
        error_calls.append((title, message))

    monkeypatch.setattr(transport_app.messagebox, "showinfo", fake_showinfo)
    monkeypatch.setattr(transport_app.messagebox, "showerror", fake_showerror)

    return {"info": info_calls, "error": error_calls}


def test_add_transport(manager, msgbox):
    manager.add_transport("Грузовик", 1000.0, 5.0, 2.0, 2.5)
    assert len(msgbox["info"]) >= 1
    title, msg = msgbox["info"][0]
    assert "Успешно" in title

    manager.cursor.execute(
        "SELECT name, payload_capacity, is_booked, length, width, height "
        "FROM freight_transport")
    rows = manager.cursor.fetchall()
    assert len(rows) == 1

    name, payload_capacity, is_booked, length, width, height = rows[0]
    assert name == "Грузовик"
    assert payload_capacity == 1000.0
    assert is_booked == 0
    assert length == 5.0
    assert width == 2.0
    assert height == 2.5


def test_make_booking(manager, msgbox):
    manager.add_transport("Фура", 2000.0, 8.0, 2.5, 3.0)
    manager.cursor.execute("SELECT id FROM freight_transport WHERE name = ?", ("Фура",))
    transport_id = manager.cursor.fetchone()[0]

    manager.make_booking(transport_id)

    manager.cursor.execute(
        "SELECT is_booked FROM freight_transport WHERE id = ?", (transport_id,)
    )
    is_booked = manager.cursor.fetchone()[0]
    assert is_booked == 1


def test_double_booking(manager, msgbox):
    manager.add_transport("Фургон", 1500.0, 6.0, 2.2, 2.8)

    manager.cursor.execute("SELECT id FROM freight_transport WHERE name = ?", ("Фургон",))
    transport_id = manager.cursor.fetchone()[0]

    manager.make_booking(transport_id)
    msgbox["error"].clear()
    manager.make_booking(transport_id)

    assert len(msgbox["error"]) == 1
    title, msg = msgbox["error"][0]
    assert "Ошибка" in title
    assert "уже забронирован" in msg


def test_cancel_booking(manager, msgbox):
    manager.add_transport("Бортовой", 1200.0, 5.5, 2.1, 2.4)
    manager.cursor.execute("SELECT id FROM freight_transport WHERE name = ?", ("Бортовой",))
    transport_id = manager.cursor.fetchone()[0]

    manager.make_booking(transport_id)

    manager.cursor.execute(
        "SELECT is_booked FROM freight_transport WHERE id = ?", (transport_id,)
    )
    assert manager.cursor.fetchone()[0] == 1

    manager.cancel_booking(transport_id)
    manager.cursor.execute(
        "SELECT is_booked FROM freight_transport WHERE id = ?", (transport_id,)
    )
    assert manager.cursor.fetchone()[0] == 0


def test_view_transport_by_dimensions(manager, msgbox):
    manager.add_transport("Маленький", 500.0, 2.0, 1.5, 1.5)
    manager.add_transport("Средний", 1000.0, 4.0, 2.0, 2.0)
    manager.add_transport("Большой", 3000.0, 10.0, 3.0, 3.5)

    msgbox["info"].clear()
    manager.view_transport_by_dimensions(3.0, 1.8, 1.8)

    assert len(msgbox["info"]) == 1
    title, msg = msgbox["info"][0]
    assert "Маленький" not in msg
    assert "Средний" in msg
    assert "Большой" in msg


if __name__ == "__main__":
    import io
    import contextlib

    print("\nРезультаты интеграционных тестов")

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = pytest.main(["-p", "no:faulthandler", __file__, "-v"])
    output = buffer.getvalue()
    print(output)

    print("Итоговый статус тестов: ")
    if result == 0:
        print("Все тесты пройдены успешно!")
    else:
        print("Есть непрошедшие тесты (код =", result, ")")
    print("================================\n")
