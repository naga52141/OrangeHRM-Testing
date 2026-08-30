import uuid

from pages.recruitment_page import RecruitmentPage


def test_add_search_delete_candidate(logged_in_driver):
    page = RecruitmentPage(logged_in_driver)
    last_name = f"QA{uuid.uuid4().hex[:6]}"

    page.navigate()
    page.add_candidate(first_name="Automated", last_name=last_name, email=f"{last_name.lower()}@example.com")

    page.navigate()
    page.search_by_name(last_name)
    assert page.get_records_found_count() == 1

    toast_text = page.delete_first_result()
    assert "Success" in toast_text
    # The already-filtered list updates in place; re-searching by name would
    # fail since the deleted candidate no longer has an autocomplete match.
    assert page.has_no_records()


def test_candidate_search_with_no_match_shows_no_records(logged_in_driver):
    page = RecruitmentPage(logged_in_driver)
    page.navigate()
    page.search_by_keyword(f"zzz_nonexistent_{uuid.uuid4().hex[:6]}")
    assert page.has_no_records()
