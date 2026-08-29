# OrangeHRM Selenium Test Suite

Selenium + Python (pytest) automation suite against the [OrangeHRM public demo](https://opensource-demo.orangehrmlive.com), built with the Page Object Model. 89 tests covering login, every module in the app (top-level pages down to second-level sub-tabs), and real CRUD/interaction flows including a custom JS calendar date picker.

**Live Allure report:** https://naga52141.github.io/OrangeHRM-Testing/
**Live pytest-html report:** https://naga52141.github.io/OrangeHRM-Testing/pytest-html-report.html

Both are republished automatically on every push to `main`.

## What's covered

- **Login** — valid and invalid credentials
- **Admin > User Management** — add user, search by username, delete, no-match search
- **PIM** — add employee, search by employee ID, no-match search, all 10 personal-details tabs (Contact Details, Emergency Contacts, Dependents, Immigration, Job, Salary, Report-to, Qualifications, Memberships)
- **Navigation** — every sidebar module (Admin, PIM, Leave, Time, Recruitment, My Info, Performance, Dashboard, Directory, Maintenance, Claim, Buzz), the Maintenance re-auth gate, the topbar account dropdown, and logout
- **Full module sweep** — every sub-page across Admin (Job, Organization, Qualifications, Nationalities, Corporate Branding, Configuration — 23 pages), Leave (Apply, My Leave, Entitlements, Reports, Configure, Leave List, Assign Leave — 13 pages), Time (Attendance, Reports — 7 pages), Recruitment (Candidates, Vacancies), Performance (Manage/My/Employee Trackers, Configure — 5 pages), and Claim (Submit/My/Assign Claim, Configuration — 5 pages)
- **Leave** — Assign Leave end-to-end through a real custom JS calendar widget (open picker, click a working day, submit, confirm the balance dialog)
- **Dashboard** — key widgets present (Time at Work, My Actions, Quick Launch, Buzz Latest Posts, etc.)
- **Directory** — employee search returns result cards
- **Buzz** — create a post and confirm it appears in the live feed

## Running locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v
```

Tests run headless by default. To watch them in a real browser window:

```bash
HEADLESS=false pytest tests/ -v
```

## Reports

Every run produces:
- A self-contained HTML report at `reports/report.html`
- Raw Allure results in `allure-results/`

To view the Allure report locally (requires the [Allure commandline](https://allurereport.org/docs/install/)):

```bash
allure serve allure-results
```

## CI/CD

`.github/workflows/tests.yml` runs the suite headless on every push to `main`, then publishes both the Allure report and the pytest-html report to the `gh-pages` branch.
