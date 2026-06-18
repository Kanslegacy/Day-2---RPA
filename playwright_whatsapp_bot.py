from playwright.sync_api import sync_playwright
import time
import os

# ====================== CONFIG ======================
CONTACT_NAME = "Kannan"          # ← Change if needed
MESSAGE = "Hi there! 👋 How are you?"

PROFILE_DIR = r"E:\Gen_AI\whatsapp_profile"
# ===================================================

def main():
    os.makedirs(PROFILE_DIR, exist_ok=True)
    
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=False,
            args=[
                '--start-maximized',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-blink-features=AutomationControlled'
            ],
            viewport={'width': 1280, 'height': 900}
        )

        page = context.pages[0] if context.pages else context.new_page()
        
        print("🚀 Opening WhatsApp Web...")
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded")

        print("⏳ Waiting for WhatsApp to load...")
        try:
            page.wait_for_selector('[data-testid="chat-list"]', timeout=60000)
            print("✅ WhatsApp loaded!")
        except:
            print("Timeout waiting for load.")
            input("Press Enter after WhatsApp is ready...")
            page.reload()

        # Close "What's New" popup
        try:
            page.locator('button[aria-label="Close"]').click(timeout=5000)
            print("✅ Closed popup")
        except:
            pass
        time.sleep(2)

        # === SEARCH CONTACT (Multiple fallback methods) ===
        print(f"🔍 Searching for: {CONTACT_NAME}")
        try:
            # Try multiple possible search box selectors
            search_selectors = [
                'div[contenteditable="true"][data-tab="3"]',
                '[data-testid="chat-search-input"]',
                'input[placeholder*="Search"]',
                '//div[contains(@class, "selectable-text") and @contenteditable="true"]'
            ]
            
            search_box = None
            for selector in search_selectors:
                try:
                    search_box = page.wait_for_selector(selector, timeout=5000)
                    if search_box:
                        print(f"✅ Found search box using: {selector}")
                        break
                except:
                    continue

            if not search_box:
                raise Exception("Search box not found")

            search_box.click()
            search_box.fill(CONTACT_NAME)
            time.sleep(2.5)

            # Click on contact (more reliable)
            contact_selectors = [
                f'span[title="{CONTACT_NAME}"]',
                f'div[role="listitem"] span:has-text("{CONTACT_NAME}")',
                f'//span[contains(text(), "{CONTACT_NAME}")]'
            ]
            
            for sel in contact_selectors:
                try:
                    contact = page.wait_for_selector(sel, timeout=8000)
                    if contact:
                        contact.click()
                        print(f"✅ Opened chat with {CONTACT_NAME}")
                        break
                except:
                    continue
            else:
                raise Exception("Contact not found")

            time.sleep(2)

        except Exception as e:
            print(f"❌ Error finding contact: {e}")
            print("Tip: Make sure the contact name is exact as shown in WhatsApp")
            input("Press Enter to exit...")
            context.close()
            return

        # Send message
        try:
            # Multiple selectors for message input
            msg_selectors = [
                'div[contenteditable="true"][data-tab="10"]',
                '[data-testid="conversation-compose-box-input"]',
                'div[role="textbox"][data-tab="10"]'
            ]
            
            msg_box = None
            for sel in msg_selectors:
                try:
                    msg_box = page.wait_for_selector(sel, timeout=5000)
                    if msg_box:
                        break
                except:
                    continue

            if msg_box:
                msg_box.click()
                msg_box.fill(MESSAGE)
                page.keyboard.press("Enter")
                print(f"✅ Message sent: {MESSAGE}")
            else:
                print("❌ Message box not found")
        except Exception as e:
            print(f"❌ Failed to send message: {e}")

        print("\n🎉 Done! Browser staying open...")
        time.sleep(15)


if __name__ == "__main__":
    main()
    