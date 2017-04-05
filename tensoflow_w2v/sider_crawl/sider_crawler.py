from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import re


# css selector for sider to get side effects and indications
TABLE_SELECTOR = '#drugInfoTable'
TERM_SELECOTR = "table tr td a[href^='/se']"
MULTIPLE_OP = "div ul li a[href^='drugs/']"


def get_med_names():
    """
    read the 100 medicine names from file
    """
    names = list()
    # with open('missing_meds.txt', 'r') as f:
    with open('generic_medlist.txt', 'r') as f:
        for line in f:
            names.append(line.strip().lower())
    return names

def get_terms_cids(table):
    terms_cid = dict()
    for term in table.find_elements_by_css_selector(TERM_SELECOTR):
        url = term.get_attribute("href")
        clean_term_text = clean_text(term.text)
        terms_cid[clean_term_text] = url.rsplit('/', 2)[-2]
    return terms_cid

def get_terms(table):
    """
    extract side effects terms and indication terms from the table element
    """
    terms = list()
    for term in table.find_elements_by_css_selector(TERM_SELECOTR):
        terms.append(term.text)
    return terms

def clean_text(s):
    s_cl = re.sub(r"[^\w\s]", '_', s).lower()
    s_cl = re.sub(r"\s+", '_', s_cl)
    s_cl = re.sub('[_]+', '_', s_cl)
    return s_cl

med_names = get_med_names()
driver = webdriver.Chrome()
final_results = {}

# search every medicine name as keyword
med_not_found = []
print("Generic Medicine:")
for name in med_names:
    print(name)
    driver.get("http://sideeffects.embl.de/")
    # locate to the search box
    elem = driver.find_element_by_name("q")
    elem.clear()
    # put the medicine name in the search box
    elem.send_keys(name)
    elem.send_keys(Keys.RETURN)
    # Check if autoselect page.
    auto_comp_option = driver.find_elements_by_css_selector(MULTIPLE_OP)
    if auto_comp_option:
        for options in auto_comp_option:
            if options.text == name:
                options.click()
                break

    driver.implicitly_wait(10)  # wait until the site is fully rendered
    # there are two tables, one for side effects and one for indications
    se_tables = driver.find_elements_by_css_selector(TABLE_SELECTOR)
    if se_tables:
        #side_effects = get_terms(se_tables[0])
        side_effects = get_terms_cids(se_tables[0])
        #indications = get_terms(se_tables[1])
        indications = get_terms_cids(se_tables[1])
        side_effects_cl = []
        indications_cl = []
        '''
        if indications:
            for ind in indications:
                ind = clean_text(ind)
                indications_cl.append(ind)
        if side_effects:
            for se in side_effects:
                se = clean_text(se)
                side_effects_cl.append(se)
        '''
        med_name_cl = clean_text(name)
        final_results[med_name_cl] = {
            'side_effects': side_effects, 'indications': indications}
    else:
        med_not_found.append(name)

driver.close()
print("Generic Medicine not in SIDER")
print(med_not_found)
# write result into json file
with open('only_effs_v1.json', 'w') as f:
    json.dump(final_results, f, indent=2)
