import pytest

from pages.app_shell_page import AppShellPage

# Each entry: (nav_label, top_tab, dropdown_item, url_fragment, expected_header)
# top_tab / dropdown_item are None when not applicable for that page.
# Ground truth verified live against the OrangeHRM demo before writing these.

ADMIN_PAGES = [
    ("Admin", "Job", "Job Titles", "admin/viewJobTitleList", "Job Titles"),
    ("Admin", "Job", "Pay Grades", "admin/viewPayGrades", "Pay Grades"),
    ("Admin", "Job", "Employment Status", "admin/employmentStatus", "Employment Status"),
    ("Admin", "Job", "Job Categories", "admin/jobCategory", "Job Categories"),
    ("Admin", "Job", "Work Shifts", "admin/workShift", "Work Shifts"),
    ("Admin", "Organization", "General Information", "admin/viewOrganizationGeneralInformation", "General Information"),
    ("Admin", "Organization", "Locations", "admin/viewLocations", "Organization"),
    ("Admin", "Organization", "Structure", "admin/viewCompanyStructure", "Organization Structure"),
    ("Admin", "Qualifications", "Skills", "admin/viewSkills", "Skills"),
    ("Admin", "Qualifications", "Education", "admin/viewEducation", "Education"),
    ("Admin", "Qualifications", "Licenses", "admin/viewLicenses", "Licenses"),
    ("Admin", "Qualifications", "Languages", "admin/viewLanguages", "Languages"),
    ("Admin", "Qualifications", "Memberships", "admin/membership", "Memberships"),
    ("Admin", "Nationalities", None, "admin/nationality", "Nationalities"),
    ("Admin", "Corporate Branding", None, "admin/addTheme", "Corporate Branding"),
    ("Admin", "Configuration", "Email Configuration", "admin/listMailConfiguration", "Configuration"),
    ("Admin", "Configuration", "Email Subscriptions", "admin/viewEmailNotification", "Email Subscriptions"),
    ("Admin", "Configuration", "Localization", "admin/localization", "Localization"),
    ("Admin", "Configuration", "Language Packages", "admin/languagePackage", "Language Packages"),
    ("Admin", "Configuration", "Modules", "admin/viewModules", "Module Configuration"),
    ("Admin", "Configuration", "Social Media Authentication", "admin/openIdProvider", "Provider List"),
    ("Admin", "Configuration", "Register OAuth Client", "admin/registerOAuthClient", "OAuth Client List"),
    ("Admin", "Configuration", "LDAP Configuration", "admin/ldapConfiguration", "LDAP Configuration"),
]

LEAVE_PAGES = [
    ("Leave", "Apply", None, "leave/applyLeave", "Apply Leave"),
    ("Leave", "My Leave", None, "leave/viewMyLeaveList", "Leave"),
    ("Leave", "Leave List", None, "leave/viewLeaveList", "Leave"),
    ("Leave", "Assign Leave", None, "leave/assignLeave", "Assign Leave"),
    ("Leave", "Entitlements", "Add Entitlements", "leave/addLeaveEntitlement", "Entitlements"),
    ("Leave", "Entitlements", "Employee Entitlements", "leave/viewLeaveEntitlements", "Entitlements"),
    ("Leave", "Entitlements", "My Entitlements", "leave/viewMyLeaveEntitlements", "Entitlements"),
    ("Leave", "Reports", "Leave Entitlements and Usage Report", "leave/viewLeaveBalanceReport", "Reports"),
    ("Leave", "Reports", "My Leave Entitlements and Usage Report", "leave/viewMyLeaveBalanceReport", "Reports"),
    ("Leave", "Configure", "Leave Period", "leave/defineLeavePeriod", "Configure"),
    ("Leave", "Configure", "Leave Types", "leave/leaveTypeList", "Leave Types"),
    ("Leave", "Configure", "Work Week", "leave/defineWorkWeek", "Configure"),
    ("Leave", "Configure", "Holidays", "leave/viewHolidayList", "Configure"),
]

TIME_PAGES = [
    ("Time", "Attendance", "My Records", "attendance/viewMyAttendanceRecord", "Attendance"),
    ("Time", "Attendance", "Punch In/Out", "attendance/punchIn", "Punch In"),
    ("Time", "Attendance", "Employee Records", "attendance/viewAttendanceRecord", "Attendance"),
    ("Time", "Attendance", "Configuration", "attendance/configure", "Attendance Configuration"),
    ("Time", "Reports", "Project Reports", "time/displayProjectReportCriteria", "Reports"),
    ("Time", "Reports", "Employee Reports", "time/displayEmployeeReportCriteria", "Reports"),
    ("Time", "Reports", "Attendance Summary", "time/displayAttendanceSummaryReportCriteria", "Reports"),
]

RECRUITMENT_PAGES = [
    ("Recruitment", "Candidates", None, "recruitment/viewCandidates", "Recruitment"),
    ("Recruitment", "Vacancies", None, "recruitment/viewJobVacancy", "Recruitment"),
]

PERFORMANCE_PAGES = [
    ("Performance", "Manage Reviews", None, "performance/searchEvaluatePerformanceReview", "Manage Reviews"),
    ("Performance", "My Trackers", None, "performance/viewMyPerformanceTrackerList", "My Performance Trackers"),
    ("Performance", "Employee Trackers", None, "performance/viewEmployeePerformanceTrackerList", "Performance"),
    ("Performance", "Configure", "KPIs", "performance/searchKpi", "Configure"),
    ("Performance", "Configure", "Trackers", "performance/viewPerformanceTracker", "Configure"),
]

CLAIM_PAGES = [
    ("Claim", "Submit Claim", None, "claim/submitClaim", "Create Claim Request"),
    ("Claim", "My Claims", None, "claim/viewClaim", "Claim"),
    ("Claim", "Assign Claim", None, "claim/assignClaim", "Create Claim Request"),
    ("Claim", "Configuration", "Events", "claim/viewEvents", "Configuration"),
    ("Claim", "Configuration", "Expense Types", "claim/viewExpense", "Configuration"),
]

ALL_MODULE_PAGES = (
    ADMIN_PAGES + LEAVE_PAGES + TIME_PAGES + RECRUITMENT_PAGES + PERFORMANCE_PAGES + CLAIM_PAGES
)

# My Info tabs all live on the same PIM employee-profile page and swap content
# in place, so URL fragment alone is the reliable signal (verified live).
MY_INFO_TABS = [
    ("Personal Details", "pim/viewPersonalDetails"),
    ("Contact Details", "pim/contactDetails"),
    ("Emergency Contacts", "pim/viewEmergencyContacts"),
    ("Dependents", "pim/viewDependents"),
    ("Immigration", "pim/viewImmigration"),
    ("Job", "pim/viewJobDetails"),
    ("Salary", "pim/viewSalaryList"),
    ("Report-to", "pim/viewReportToDetails"),
    ("Qualifications", "pim/viewQualifications"),
    ("Memberships", "pim/viewMemberships"),
]


@pytest.mark.parametrize("nav_label, top_tab, dropdown_item, url_fragment, expected_header", ALL_MODULE_PAGES)
def test_module_page_loads(logged_in_driver, nav_label, top_tab, dropdown_item, url_fragment, expected_header):
    page = AppShellPage(logged_in_driver)
    page.open_module_page(nav_label, top_tab=top_tab, dropdown_item=dropdown_item)
    page.wait.until(lambda d: url_fragment in d.current_url)
    assert expected_header in page.get_page_headers()


@pytest.mark.parametrize("tab_label, url_fragment", MY_INFO_TABS)
def test_my_info_tab_loads(logged_in_driver, tab_label, url_fragment):
    page = AppShellPage(logged_in_driver)
    page.click_nav_item("My Info")
    page.click_dropdown_item(tab_label)
    page.wait.until(lambda d: url_fragment in d.current_url)
