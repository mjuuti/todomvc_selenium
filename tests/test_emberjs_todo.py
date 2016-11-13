"""
Py.Test tests for TODOMVC.com EmberJS page
"""
import pytest
from pageobjects.emberpage import EmberJsPage
from pageobjects.todomvcmainpage import TodoMvcMainPage


@pytest.fixture()
def todo_page() -> EmberJsPage:
    """Fixture to open and return TODO page instance"""
    page = EmberJsPage()
    page.open()
    return page


@pytest.fixture()
def create_todos(todo_page: EmberJsPage, active_todos: int, completed_todos: int):
    """Pre-test fixture to create existing TODO entries"""

    for i in range(active_todos):
        todo_page.add_new_todo_item("active-%i" % i)

    for i in range(completed_todos):
        todo_page.add_new_todo_item("completed-%i" % i)
        element = todo_page.find_todo_by_text("completed-%i" % i)
        todo_page.toggle_active(element)


@pytest.mark.usefixtures("create_todos")
class TestEmberJsTodo:
    """Test class for EmberJS page"""

    @pytest.mark.parametrize(("active_todos", "completed_todos"), [(0, 0)])
    def test_navigate_to_emberjs_page(self):
        """Test navigation from front page to EmberJS page works"""
        main_page = TodoMvcMainPage()
        main_page.open()
        main_page.emberjs_link.click()
        emberjs_page = EmberJsPage()
        assert emberjs_page.is_page_loaded(), "Failed to navigate to Ember JS page"

    @pytest.mark.parametrize(("active_todos", "completed_todos"), [(0, 0)])
    def test_adding_todo_entry(self, todo_page: EmberJsPage):
        """Test adding new TODO entry on empty page works"""
        todo_text = "new todo"
        todo_page.add_new_todo_item(todo_text)
        assert len(todo_page.todo_entries_visible) == 1 and todo_page.todo_entries_visible[0].text == todo_text, \
            "TODO entry with text '%s' was not found" % todo_text

    @pytest.mark.parametrize(("active_todos", "completed_todos"), [(1, 0)])
    def test_edit_todo_content(self, todo_page: EmberJsPage):
        """Test editing content of existing TODO entry works"""
        new_todo_text = "new text"
        todo = todo_page.find_todo_by_text('active-0')
        todo_page.edit_todo(todo, new_todo_text, clear_existing=True)

        assert len(todo_page.todo_entries_visible) == 1 and todo_page.todo_entries_visible[0].text == new_todo_text, \
            "TODO entry with text '%s' was not found" % new_todo_text

    @pytest.mark.parametrize(("active_todos", "completed_todos"), [(1, 0)])
    def test_complete_todo(self, todo_page: EmberJsPage):
        """Test changing active TODO item to completed by clicking the circle works"""
        element = todo_page.find_todo_by_text('active-0')
        todo_page.toggle_active(element)

        count_active = len(todo_page.todo_entries_active)
        count_completed = len(todo_page.todo_entries_completed)
        assert count_active == 0 and count_completed == 1, \
            "Expected to find 0 active and 1 completed entry, got %i and %i" % (count_active, count_completed)

    @pytest.mark.parametrize(("active_todos", "completed_todos"), [(0, 1)])
    def test_reactivate_todo(self, todo_page: EmberJsPage):
        """Test re-activating completed TODO entry by clicking the circle works"""
        element = todo_page.find_todo_by_text('completed-0')
        todo_page.toggle_active(element)

        count_active = len(todo_page.todo_entries_active)
        count_completed = len(todo_page.todo_entries_completed)
        assert count_active == 1 and count_completed == 0, \
            "Expected to find 1 active and 0 completed entries, got %i and %i" % (count_active, count_completed)

    @pytest.mark.parametrize(("active_todos", "completed_todos"), [(1, 0)])
    def test_add_second_todo(self, todo_page: EmberJsPage):
        """Test adding second TODO works"""
        todo_page.add_new_todo_item("new todo")

        assert len(todo_page.todo_entries_visible) == 2, \
            "Expected to find 2 TODO entries, found %i" % len(todo_page.todo_entries_visible)

    @pytest.mark.parametrize(("active_todos", "completed_todos"), [(3, 0)])
    def test_complete_all_active_todos(self, todo_page: EmberJsPage):
        """Test marking all active TODOs completed from down arrow works"""
        todo_page.toggle_all.click()

        assert len(todo_page.todo_entries_active) == 0, "Expected to find all TODO entries completed"

    @pytest.mark.parametrize(("active_todos", "completed_todos"), [(2, 1)])
    def test_filter_visible_todos_by_completed_state(self, todo_page: EmberJsPage):
        """Test completed TODOs can be filtered from view by clicking "Active" link on bottom of the page"""
        todo_page.show_active.click()

        assert len(todo_page.todo_entries_completed) == 0, "Expected to not find completed TODO entries"

    @pytest.mark.parametrize(("active_todos", "completed_todos"), [(2, 1)])
    def test_close_todo(self, todo_page: EmberJsPage):
        """Test closing permanently TODO entry from X icon works"""
        entry_name_to_close = 'active-1'
        element = todo_page.find_todo_by_text(entry_name_to_close)
        todo_page.close_todo(element)

        assert not any([todo.text == entry_name_to_close for todo in todo_page.todo_entries_visible])

    @pytest.mark.parametrize(("active_todos", "completed_todos"), [(1, 2)])
    def test_clear_all_completed_todos(self, todo_page: EmberJsPage):
        """Test all completed TODOs can be permanently closed by clicking "Clear completed" link"""
        todo_page.clear_completed.click()

        assert len(todo_page.todo_entries_completed) == 0, "Expected to not find completed TODO entries"
