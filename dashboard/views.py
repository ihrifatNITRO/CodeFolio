from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
import re, time

# --- New Imports for Selenium ---
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
# --- End of New Imports ---


def clean_stat(stat_text):
    """Safely extracts the number, handling cases where it's a dash."""
    cleaned_text = stat_text.strip().split('/')[0].strip()
    return 0 if cleaned_text == '-' else int(cleaned_text)


@login_required
def dashboard_view(request):
    context = {}
    driver = None  # Initialize driver to None

    if request.method == 'POST':
        leetcode_handle = request.POST.get('leetcode')
        codeforces_handle = request.POST.get('codeforces')
        codechef_handle = request.POST.get('codechef')

        if leetcode_handle:
            try:
                # Setup Chrome options for headless mode
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument("window-size=1280,720")
                options.add_argument(
                    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
                options.add_argument("--disable-gpu")

                # Initialize the Chrome driver
                driver = webdriver.Chrome(service=ChromeService(
                    ChromeDriverManager().install()), options=options)

                url = f"https://leetcode.com/{leetcode_handle}/"
                driver.get(url)

                # Wait 10s to ensure the stats are loaded
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".text-sd-easy")))
                

                '''find all 'Show more' clickable'''
                show_more_clickables = driver.find_elements(
                    By.XPATH, "//*[contains(text(), 'Show more')]")
                for clickable in show_more_clickables:
                    try:
                        # Use a JavaScript click, which is more reliable for elements
                        # that might be tricky to interact with.
                        driver.execute_script("arguments[0].click();", clickable)
                        # Wait a moment for the new content to load
                        time.sleep(0.7)
                    except Exception as e:
                        print(
                            f"Warning: Could not click a 'Show more' button. {e}")


                '''start web scraping'''
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')


                '''Find the number of problem solved'''
                # Find each stat by its specific label class
                easy_label = soup.find('div', class_='text-sd-easy')
                medium_label = soup.find('div', class_='text-sd-medium')
                hard_label = soup.find('div', class_='text-sd-hard')

                if easy_label and medium_label and hard_label:
                    # Find the next sibling div which contains the numbers
                    easy_stat_div = easy_label.find_next_sibling('div')
                    medium_stat_div = medium_label.find_next_sibling('div')
                    hard_stat_div = hard_label.find_next_sibling('div')

                    easy = clean_stat(easy_stat_div.text)
                    medium = clean_stat(medium_stat_div.text)
                    hard = clean_stat(hard_stat_div.text)
                    total = easy + medium + hard

                    context['leetcode_stats'] = {
                        'easy': easy, 'medium': medium, 'hard': hard, 'total': total}
                else:
                    context['error'] = 'Could not find stats. LeetCode page structure may have changed.'


                '''Find the languages are used in LeetCode'''
                # Get all div with prog. languages
                language_stats = []
                language_containers = soup.select(
                    'div.flex.items-center.justify-between.text-xs')
                
                for container in language_containers:
                    language_span = container.find('span', class_='notranslate')
                    count_span = container.find('span', class_='font-medium')

                    if language_span and count_span:
                        language_name = language_span.text.strip()
                        solved_count = int(count_span.text.strip())
                        language_stats.append([language_name, solved_count])

                if language_stats:
                    context['language_stats'] = language_stats

                
                '''Tags of the problems'''
                skill_stats = []
                skill_containers = soup.select(
                    'div.mb-3.mr-4.inline-block.text-xs')
                
                for container in skill_containers:
                    skill_span = container.find('a')
                    count_span = container.find('span', class_='pl-1')

                    if skill_span and count_span:
                        skill_name = skill_span.find('span').text.strip()
                        solved_count = count_span.text.strip()
                        skill_stats.append([skill_name, solved_count])
                
                if skill_stats:
                    context['skill_stats'] = skill_stats


                '''yearly reports'''
                yearly_stats = []
                # get no of total last 1yr submissions
                last_year_submission = soup.find(
                    'span', class_='mr-[5px]').text.strip()
                yearly_stats.append(last_year_submission)
                # find "Total active days" label and get its value using regex
                active_days_label = soup.find(
                    'span', string=re.compile('Total active days'))
                active_days_value = active_days_label.find_next_sibling('span')
                yearly_stats.append(active_days_value.text.strip())

                # find "Max streak" label and get its value using regex
                max_streak_label = soup.find(
                    'span', string=re.compile('Max streak'))
                max_streak_value = max_streak_label.find_next_sibling('span')
                yearly_stats.append(max_streak_value.text.strip())
                
                if yearly_stats:
                    context['yearly_stats'] = yearly_stats
                


            except Exception as e:
                context['error'] = f"An error occurred: {str(e)}"
            finally:
                # close the browser
                if driver:
                    driver.quit()

        context['leetcode_handle'] = leetcode_handle
        context['codeforces_handle'] = codeforces_handle
        context['codechef_handle'] = codechef_handle

    response = render(request, 'dashboard/dashboard.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response
