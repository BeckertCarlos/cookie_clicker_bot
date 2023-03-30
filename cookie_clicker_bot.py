from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
from threading import Thread, Event
import time


class CookieClicker:
    """
       A class that automates cookie clicking and upgrades in the game Cookie Clicker.
    """

    def __init__(self):
        """
            Initializes the driver and starts threads for clicking the cookie, buying upgrades,
            buying products, and clicking golden cookies.
        """

        # Start Driver
        chrome_driver_path = Service(os.environ['DRIVER_PATH'])
        op = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=chrome_driver_path, options=op)
        self.driver.get("https://orteil.dashnet.org/cookieclicker/")

        # Select Language
        time.sleep(5)
        language = self.driver.find_element(by=By.XPATH, value='//*[@id="langSelect-EN"]')
        language.click()

        # Find cookie
        time.sleep(5)
        self.cookie = self.driver.find_element(by=By.XPATH, value='//*[@id="bigCookie"]')

        # Initializing Events
        self.cookie_click_event = Event()
        self.upgrade_event = Event()
        self.products_event = Event()
        self.golden_cookie_event = Event()

        # Initializing Threads
        self.cookie_thread = Thread(target=self.cookie_click, args=(self.cookie_click_event,))
        self.upgrade_thread = Thread(target=self.get_upgrade, args=(self.upgrade_event,))
        self.products_thread = Thread(target=self.get_products, args=(self.products_event,))
        self.golden_cookie_thread = Thread(target=self.get_golden_cookie, args=(self.golden_cookie_event,))

        self.cookie_thread.start()
        self.upgrade_thread.start()
        self.products_thread.start()
        self.golden_cookie_thread.start()

    def __del__(self):
        print("entrou no destrutor")
        cookie.cookie_click_event.clear()
        cookie.upgrade_event.clear()
        cookie.products_event.clear()
        cookie.golden_cookie_event.clear()

        cookie.cookie_thread.join(timeout=0.1)
        cookie.upgrade_thread.join(timeout=0.1)
        cookie.products_thread.join(timeout=0.1)
        cookie.golden_cookie_thread.join(timeout=0.1)

        cookie.driver.close()

    def cookie_click(self, event: Event):
        """
                A thread function that clicks the cookie whenever the event is set.

                Parameters:
                - event (threading.Event): An event that is used to toggle the cookie clicking thread on or off.
        """

        while True:
            event.wait()
            self.cookie.click()

    def get_product_unlocked_enable(self):
        """
                Finds the last unlocked and enabled product on the page.

                Returns:
                - The last unlocked and enabled product as a WebElement, or None if no such product is found.
        """

        try:
            product_unlocked_enabled = self.driver.find_elements(by=By.CSS_SELECTOR, value='.product.unlocked.enabled')
            return product_unlocked_enabled[-1]
        except IndexError as ex:
            pass

    def get_golden_cookie(self, event: Event):
        """
                A thread function that clicks a golden cookie whenever the event is set.

                Parameters:
                - event (threading.Event): An event that is used to toggle the golden cookie clicking thread on or off.
        """

        while True:
            event.wait()
            try:
                golden_cookie = self.driver.find_element(by=By.CSS_SELECTOR, value='.shimmer')
                self.driver.execute_script("arguments[0].click();", golden_cookie)
            except Exception as ex:
                pass

    def get_upgrade(self, event: Event):
        """
               A thread function that buys the first upgrade whenever the event is set.

               Parameters:
               - event (threading.Event): An event that is used to toggle the upgrade buying thread on or off.
        """

        while True:
            event.wait()
            try:
                upgrade = self.driver.find_element(by=By.ID, value='upgrade0')
                self.driver.execute_script("arguments[0].click();", upgrade)
            except Exception as ex:
                pass

    def get_products(self, event: Event):
        """
                A thread function that buys the last unlocked and enabled product whenever the event is set.

                Parameters:
                - event (threading.Event): An event that is used to toggle the product buying thread on or off.
        """

        while True:
            event.wait()
            products = self.get_product_unlocked_enable()
            if products:
                self.driver.execute_script("arguments[0].click();", products)

    @staticmethod
    def toggle_gear(event: Event):
        """
        Toggles the state of the given event object.

        Parameters:
        - event (threading.Event): The event object to toggle.
        """

        if event.is_set():
            event.clear()
        else:
            event.set()

    def toggle(self, selector):
        """
            Toggles the state of the thread associated with the given selector.

            Parameters:
            - selector (str): A string that indicates which thread to toggle. Must be one of 'c', 'g', 'u', or 'p'.
        """

        if selector == 'c':
            self.toggle_gear(self.cookie_click_event)

        elif selector == 'u':
            self.toggle_gear(self.upgrade_event)

        elif selector == 'p':
            self.toggle_gear(self.products_event)

        elif selector == 'g':
            self.toggle_gear(self.golden_cookie_event)


if __name__ == "__main__":

    cookie = CookieClicker()

    while True:
        try:
            user_input = input(f"\nActivate/Deactivate functions:\n\n"
                               f"('c') cookie_click         = "
                               f"{('Activated' if cookie.cookie_click_event.isSet() else 'Deactivated')}\n"
                               f"('g') get_golden_cookie    = "
                               f"{('Activated' if cookie.golden_cookie_event.isSet() else 'Deactivated')}\n"
                               f"('u') get_upgrade          = "
                               f"{('Activated' if cookie.upgrade_event.isSet() else 'Deactivated')}\n"
                               f"('p') get_products         = "
                               f"{('Activated' if cookie.products_event.isSet() else 'Deactivated')}\n"
                               f"('q') QUIT\n\n"
                               f"=> ")

            if user_input in ['c', 'g', 'u', 'p']:
                cookie.toggle(user_input)
            elif user_input == 'q':
                break

        except KeyboardInterrupt:
            break
