from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Initialize the WebDriver with headless options
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode
options.add_argument('--disable-gpu')  # Disable GPU for headless mode
options.add_argument('--window-size=1920x1080')  # Set window size

driver = webdriver.Chrome(options=options)  # Ensure that ChromeDriver is in your PATH

# Open the webpage
driver.get('https://royaleapi.com/players/leaderboard')

# Wait until the page is loaded
wait = WebDriverWait(driver, 10)

try:
    # Step 1: Extract all country options from the "Global" dropdown
    print("Extracting all countries from the 'Global' dropdown...")
    try:
        # Locate the "Global" dropdown button
        country_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.location_modal_button.link.item'))
        )
        # Click the "Global" dropdown button
        driver.execute_script("arguments[0].click();", country_button)
        print("Country dropdown clicked.")

        # Wait for the country options to appear
        country_options = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.location_modal .item'))
        )

        # Get all country names
        all_countries = [option.text.strip() for option in country_options if option.text.strip()]
        print(f"Found {len(all_countries)} countries.")
        print(all_countries)

    except Exception as e:
        print(f"Error extracting countries: {e}")
        driver.quit()

    # Initialize a list to store all data
    all_data = []

    for country_name in all_countries:
        print(f"\nProcessing country: {country_name}")

        # Step 2: Select the country from the dropdown
        print("Step 2: Selecting country from dropdown...")
        try:
            # Locate the "Global" dropdown button
            country_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.location_modal_button.link.item'))
            )
            # Click the "Global" dropdown button
            driver.execute_script("arguments[0].click();", country_button)
            print("Country dropdown clicked.")

            # Wait for the country options to appear
            country_options = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.location_modal .item'))
            )

            # Find the country option and click it
            country_found = False
            for option in country_options:
                if option.text.strip() == country_name:
                    driver.execute_script("arguments[0].click();", option)
                    country_found = True
                    print(f"Selected country: {country_name}")
                    break

            if not country_found:
                print(f"Country '{country_name}' not found in the dropdown options.")
                continue  # Skip to the next country

            # Wait for the table to refresh
            time.sleep(2)

        except Exception as e:
            print(f"Error selecting country '{country_name}': {e}")
            continue  # Skip to the next country

        # Step 3: Set rows per page to 1000
        print("Step 3: Setting rows per page to '1000' after country selection...")
        try:
            # Locate the rows-per-page dropdown
            rows_dropdown = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.ui.pointing.dropdown.link.item'))
            )
            # Use JavaScript to click the dropdown
            driver.execute_script("arguments[0].click();", rows_dropdown)
            print("Rows-per-page dropdown clicked.")

            # Wait for the dropdown options to appear
            row_options = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.menu .rowperpage.item'))
            )

            # Select '1000' from the dropdown
            option_found = False
            for option in row_options:
                if option.text.strip() == '1000':
                    driver.execute_script("arguments[0].click();", option)
                    option_found = True
                    print("Selected '1000' rows per page.")
                    break

            if not option_found:
                print("'1000' option not found in the rows-per-page dropdown.")
                continue  # Skip to the next country

            # Wait for the table to refresh after changing rows per page
            time.sleep(3)

        except Exception as e:
            print(f"Error setting rows per page for country '{country_name}': {e}")
            continue  # Skip to the next country

        # Step 4: Scrape data from the table
        print("Step 4: Scraping data from the table...")
        try:
            # Wait for the table to be present
            wait.until(EC.presence_of_element_located((By.ID, 'roster')))

            # Locate the table
            table = driver.find_element(By.ID, 'roster')

            # Get all rows in the table
            rows = table.find_elements(By.TAG_NAME, 'tr')

            # Check if there are data rows
            if len(rows) <= 1:
                print(f"No data found for country '{country_name}'.")
                continue  # Skip to the next country

            # Iterate over table rows, skipping the header row
            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, 'td')
                if len(cells) >= 4:
                    # Extract row number
                    row_number = cells[0].text.strip()

                    # Extract country name
                    try:
                        country_img = cells[2].find_element(By.TAG_NAME, 'img')
                        country_alt = country_img.get_attribute('alt')
                        country_name_in_row = country_alt.strip().rstrip('}')  # Remove any trailing '}'
                    except Exception:
                        country_name_in_row = country_name  # Fallback to the selected country name

                    # Extract player name and clan
                    cell_text = cells[3].text.strip()
                    player_info = cell_text.split('\n')
                    player_name = player_info[0] if len(player_info) > 0 else ''
                    player_clan = player_info[1] if len(player_info) > 1 else ''

                    # Append data to the list
                    all_data.append([row_number, country_name_in_row, player_name, player_clan])

            print(f"Collected {len(rows) - 1} rows for country '{country_name}'.")

        except Exception as e:
            print(f"Error scraping data for country '{country_name}': {e}")
            continue  # Skip to the next country

        # Optional: Wait before moving to the next country
        time.sleep(1)

    # After the loop, save all_data to a CSV file
    print("\nSaving all data to 'all_countries_data.csv'...")
    with open('all_countries_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Row Number', 'Country', 'Player Name', 'Player Clan'])
        writer.writerows(all_data)

    print("Data scraping completed. Data saved to 'all_countries_data.csv'.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the driver
    driver.quit()
