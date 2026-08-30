import uuid

from pages.recruitment_page import RecruitmentPage


def test_add_candidate_appears_in_search(logged_in_driver):
    page = RecruitmentPage(logged_in_driver)
    last_name = f"QA{uuid.uuid4().hex[:6]}"

    page.navigate()
    page.add_candidate(first_name="Automated", last_name=last_name, email=f"{last_name.lower()}@example.com")

    page.navigate()
    page.search_by_name(last_name)
    assert page.get_records_found_count() == 1


def test_candidate_search_with_no_match_shows_no_records(logged_in_driver):
    page = RecruitmentPage(logged_in_driver)
    page.navigate()
    page.search_by_keyword(f"zzz_nonexistent_{uuid.uuid4().hex[:6]}")
    assert page.has_no_records()
