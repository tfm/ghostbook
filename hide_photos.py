import random
import time
from playwright.sync_api import sync_playwright

def hide_photos():
    with sync_playwright() as p:
        # Launch browser in headed mode
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to Facebook...")
        page.goto("https://www.facebook.com/")

        print("Please log in to Facebook manually.")
        print("IMPORTANT: Navigate to Profile -> Photos -> 'Your Photos'.")
        print("Then CLICK ON THE FIRST PHOTO to open it in full screen (theater mode).")
        print("Press Enter in this terminal when the first photo is open...")
        input()

        print("Starting privacy update process...")
        
        while True:
            try:
                # 1. Find and click the "..." (More) button
                # In theater mode, it's often "Actions for this post" or just "More"
                # Use .first to avoid strict mode violation if multiple exist (e.g. background feed)
                more_button = page.locator('div[aria-label="Actions for this post"]').first
                if not more_button.is_visible():
                    more_button = page.locator('div[aria-label="More"]').first
                
                if more_button.is_visible():
                    more_button.click()
                    time.sleep(random.uniform(1.0, 2.0))
                    
                    # 2. Find "Edit audience" or "Edit privacy"
                    edit_audience = page.locator('div[role="menuitem"]:has-text("Edit audience")')
                    if not edit_audience.is_visible():
                        edit_audience = page.locator('div[role="menuitem"]:has-text("Edit privacy")')
                        
                    if edit_audience.is_visible():
                        edit_audience.click()
                        time.sleep(random.uniform(2.0, 3.0))
                        
                        # 3. Select "Only me"
                        # Try multiple selectors
                        only_me = page.locator('div[role="radio"]:has-text("Only me")').first
                        if not only_me.is_visible():
                             only_me = page.locator('span:text-is("Only me")').first
                        if not only_me.is_visible():
                             only_me = page.locator('div[aria-label="Only me"]').first
                        
                        # Check if hidden under "See more"
                        if not only_me.is_visible():
                            see_more = page.locator('div[role="button"]:has-text("See more")').first
                            if see_more.is_visible():
                                print("Clicking 'See more'...")
                                see_more.click()
                                time.sleep(1.0)
                                # Try selectors again after expansion
                                only_me = page.locator('div[role="radio"]:has-text("Only me")').first
                                if not only_me.is_visible():
                                     only_me = page.locator('span:text-is("Only me")').first
                        
                        if only_me.is_visible():
                            print("Found 'Only me' option.")
                            # Check if already set
                            # aria-checked might be on the radio div or a parent/child
                            is_checked = only_me.get_attribute("aria-checked") == "true"
                            if not is_checked:
                                # Check parent just in case
                                try:
                                    parent = only_me.locator('..')
                                    if parent.get_attribute("aria-checked") == "true":
                                        is_checked = True
                                except:
                                    pass

                            if is_checked:
                                print("Already set to 'Only me'.")
                                page.keyboard.press("Escape") # Close modal
                                time.sleep(1.0)
                                # Ensure menu is closed
                                page.mouse.click(0, 0) 
                            else:
                                only_me.click()
                                time.sleep(random.uniform(1.0, 2.0))
                                
                                # Click Save/Done
                                save_btn = page.locator('div[aria-label="Save"]')
                                if not save_btn.is_visible():
                                    save_btn = page.locator('div[aria-label="Done"]')
                                
                                if save_btn.is_visible():
                                    save_btn.click()
                                    print("Updated photo to 'Only me'.")
                                    time.sleep(random.uniform(2.0, 3.0)) # Wait for save
                                else:
                                    print("Save button not found.")
                                    page.keyboard.press("Escape")
                        else:
                            print("'Only me' option not found.")
                            page.keyboard.press("Escape")
                    else:
                        print("'Edit audience' not found in menu. (Might be a cover photo or uneditable?)")
                        # Close menu
                        page.keyboard.press("Escape")
                        
                else:
                    print("'More' button (...) not found.")
                
                # 4. Go to next photo
                next_button = page.locator('div[aria-label="Next photo"]')
                if not next_button.is_visible():
                    next_button = page.locator('div[aria-label="Next"]')
                
                if next_button.is_visible():
                    next_button.click()
                    print("Moved to next photo.")
                    time.sleep(random.uniform(2.0, 4.0))
                else:
                    print("No 'Next' button found. End of album?")
                    break
                    
            except Exception as e:
                print(f"Error processing photo: {e}")
                # Try to recover
                page.keyboard.press("Escape")
                time.sleep(1)
                # Try to move next anyway
                try:
                    page.locator('div[aria-label="Next photo"]').click()
                except:
                    break
                
        print("Finished.")
        browser.close()

if __name__ == "__main__":
    hide_photos()
