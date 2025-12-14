import random
import time
from playwright.sync_api import sync_playwright

def delete_friends():
    with sync_playwright() as p:
        # Launch browser in headed mode so user can see and interact
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to Facebook...")
        page.goto("https://www.facebook.com/")

        print("Please log in to Facebook manually in the browser window.")
        print("IMPORTANT: Navigate to your profile -> Friends -> 'All Friends'.")
        print("The URL should look like: https://www.facebook.com/username/friends_all")
        print("Press Enter in this terminal when you are on the 'All Friends' page...")
        input()

        print("Starting deletion process...")
        
        while True:
            try:
                # User feedback: The "Friends" button opens mutual friends.
                # We need to click the "..." menu which has aria-label="More".
                
                # Find all 'Three dots' buttons with aria-label="More"
                # These are usually the action menus for each friend card.
                more_buttons = page.locator('div[aria-label="More"]').all()
                
                if not more_buttons:
                    print("No 'More' buttons found. Please make sure you are on the 'All Friends' page.")
                    break

                print(f"Found {len(more_buttons)} 'More' buttons visible.")

                processed_count = 0
                for button in more_buttons:
                    try:
                        # Scroll into view
                        button.scroll_into_view_if_needed()
                        
                        # Click the "More" button to open menu
                        button.click()
                        time.sleep(random.uniform(1.0, 2.0))
                        
                        # Now look for "Unfriend" option in the menu
                        # It can be a span or a div with text "Unfriend"
                        # Sometimes it is nested.
                        unfriend_option = page.locator('div[role="menuitem"]:has-text("Unfriend")')
                        if not unfriend_option.is_visible():
                             unfriend_option = page.locator('span:text-is("Unfriend")')
                        
                        if unfriend_option.is_visible():
                            unfriend_option.click()
                            time.sleep(random.uniform(1.0, 2.0))
                            
                            # Confirm unfriend if a modal pops up
                            confirm_button = page.locator('div[aria-label="Confirm"]')
                            if confirm_button.is_visible():
                                confirm_button.click()
                                print("Unfriended one person.")
                                processed_count += 1
                            else:
                                # Sometimes it's a generic "OK" or "Unfriend" button in the dialog
                                confirm_button_alt = page.locator('div[role="dialog"] div[role="button"]:has-text("Confirm")')
                                if confirm_button_alt.is_visible():
                                    confirm_button_alt.click()
                                    print("Unfriended one person (alt confirm).")
                                    processed_count += 1
                                else:
                                    print("Confirmation dialog not found or not needed.")
                                
                            # Wait random time to avoid detection
                            wait_time = random.uniform(3.0, 7.0)
                            print(f"Waiting {wait_time:.2f} seconds...")
                            time.sleep(wait_time)
                        else:
                            print("Unfriend option not found in menu. Closing menu.")
                            # Click body to close menu
                            page.mouse.click(0, 0)
                            
                    except Exception as e:
                        print(f"Error processing a friend: {e}")
                        continue
                
                if processed_count == 0:
                    print("Could not process any friends in this batch. Trying to scroll...")
                
                # Scroll down to load more
                page.keyboard.press("End")
                time.sleep(3)
                
            except Exception as e:
                print(f"Loop error: {e}")
                break

        print("Finished.")
        browser.close()

if __name__ == "__main__":
    delete_friends()
