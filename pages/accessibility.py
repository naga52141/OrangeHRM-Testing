from selenium_axe_python import Axe


def scan(driver):
    axe = Axe(driver)
    axe.inject()
    return axe.run()


def violations_by_impact(results):
    grouped = {}
    for violation in results.get("violations", []):
        grouped.setdefault(violation["impact"], []).append(violation["id"])
    return grouped
