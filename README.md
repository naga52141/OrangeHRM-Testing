# OrangeHRM Selenium Test Suite

Selenium + Python (pytest) automation suite against the [OrangeHRM public demo](https://opensource-demo.orangehrmlive.com), built with the Page Object Model. Covers login, Admin user management (add/search/delete), PIM employee records, data-table search/filter behavior, and full sidebar/topbar navigation.

**Live report:** published automatically to GitHub Pages on every push — see the repo's About section for the link once the first workflow run completes.

## What's covered

- **Login** — valid and invalid credentials
- **Admin > User Management** — add user, search by username, delete, no-match search
- **PIM** — add employee, search by employee ID, no-match search
- **Navigation** — every sidebar module (Admin, PIM, Leave, Time, Recruitment, My Info, Performance, Dashboard, Directory, Maintenance, Claim, Buzz), the Maintenance re-auth gate, the topbar account dropdown, and logout

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
