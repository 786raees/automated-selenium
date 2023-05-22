"""all the class of this file represent a page like Home Page and Login Page etc
all the class contain all the methods that tells what to do with the driver on certain page
for example:
on login page we will perform login functionality
"""

import contextlib, pyautogui, random, time, math
from typing import List, Union
from selenium.webdriver import Remote
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from automated_selenium.resources.resources import CookieBotResources, Selector


class BasePage:
    """Base class for all the pages
    the subclasses will contain all the methods can be perform on a
    single page

    you can start a new instance of this class as follow

    page = BasePage(driver)
    """
    def __init__(self, driver:Remote) -> None:
        self.driver: Remote = driver
        self.driver.maximize_window()

    def find(self, selector: Selector) -> WebElement:
        """This method will find and return an element from the driver"""
        return self.driver.find_element(selector.ST, selector.SP)

    def find_from_element(self, element: WebElement, selector: Selector) -> WebElement:
        """This method will find and return an element from another element"""
        return element.find_element(selector.ST, selector.SP)

    def find_all(self, selector: Selector) -> List[WebElement]:
        """This method will find and return a list of all available element from the driver"""
        return self.driver.find_elements(selector.ST, selector.SP)

    def wait_until_find(self, selector: Selector, timeout: int = 10, condition=EC.presence_of_element_located) -> WebElement:
        """This method will wait for element to be present in DOM and return an available element from the driver"""
        return WebDriverWait(self.driver, timeout).until(condition((selector.ST, selector.SP)))

    def wait_until_find_all(self, selector: Selector, timeout: int = 10, condition=EC.presence_of_all_elements_located) -> List[WebElement]:
        """This method will wait for elements to be present in DOM and return a list of all available element from the driver"""
        return WebDriverWait(self.driver, timeout).until(condition((selector.ST, selector.SP)))
    
    def click(self, element: WebElement) -> None:
        """Will try to click the given element
        but if it fails it will run script to execute it"""
        if isinstance(element, WebElement):
            try:
                element.click()
            except Exception as e:
                self.driver.execute_script("arguments[0].click();", element)
    
    def click_all(self, elements: List[WebElement] ) -> None:
        for element in elements:
            self.click(element)

    def send_keys(self, element: WebElement, text: str) -> None:
        """This method will help to type text like human

        Args:
            element (WebElement): input element to send keys to
            text (str): text to send
        """
        for letter in text:
            time.sleep(random.uniform(0.01, 0.3))
            element.send_keys(letter)
        
    def random_mouse_movement(self, total_num):
        """
            It will randomly move mouse on the screen for specific number of times.
            Params:
                total_num : Number of times to do this random mouse movement (int)
        """
        # self.circular_mousemovement(random.randint(100, 300))
        for _ in range(total_num):
            width, height = pyautogui.size()

            random_width = random.randint(0, width - 1)
            random_height = random.randint(0, height - 1)
            self.move_mouse_to_coordinates(random_width, random_height)

    @staticmethod
    def move_mouse_to_coordinates(x, y):
        """
            Will move mouse to respective coordinates
            Params:
                x (int value)
                y (int value)
        """
        time_to_move = random.uniform(0.1, 2.0)
        time_to_move = round(time_to_move, 1)

        """ Empty String so that linear mouse movement """
        movements = [pyautogui.easeInQuad, pyautogui.easeOutQuad, pyautogui.easeInOutQuad, pyautogui.easeInBounce, pyautogui.easeInElastic] # type: ignore
        pyautogui.FAILSAFE = False
        try:
            pyautogui.moveTo(x, y, time_to_move, random.choice(movements))
        # except InvalidCoordinatesException as e:
        except Exception as e:
            pyautogui.moveTo(x, y, time_to_move)
            # logging.info("Changing coordinates because of ", type(e))


    def move_mouse_to_element(self, element):
        """
            It will move the mouse cursor to the sepecific element displayed on the screen
            Params:
                driver (selenium webdriver object)
                element (selenium element)
        """
        actions = ActionChains(self.driver)

        panel_height = self.driver.execute_script('return window.outerHeight - window.innerHeight;')
        abs_x = element.location['x']
        y = element.location['y']
        abs_y = y + panel_height
        self.move_mouse_to_coordinates(abs_x, abs_y)
        actions.move_to_element(element)
        with contextlib.suppress(Exception):
            actions.perform()

    def click_random_position_in_element(self, element):
        # sourcery skip: extract-duplicate-method, inline-immediately-returned-variable, move-assign-in-block
        # Get the size and position of the element
        width = element.size['width']
        height = element.size['height']
        x_pos = element.location['x']
        y_pos = element.location['y']

        # Calculate the boundaries of the element
        left_bound = x_pos
        right_bound = x_pos + width
        top_bound = y_pos
        bottom_bound = y_pos + height

        # Generate a random x and y position within the element
        random_x = random.randint(left_bound, right_bound)
        random_y = random.randint(top_bound, bottom_bound)

        self.move_mouse_with_ease(random_x, random_y + 65)

    def find_and_click(self, selector: Selector, timeout: int = 10):
        element = self.scroll_to(selector, timeout)
        self.click(element)
        return element
    
    def scroll_to(self, selector: Selector, timeout: int = 10):
        element = self.wait_until_find(selector, timeout)
        with contextlib.suppress(Exception):
            scroll = ActionChains(self.driver)
            scroll.move_to_element(element).perform()
        return element

    def scroll_to_element(self, element: WebElement, timeout: int = 10):
        with contextlib.suppress(Exception):
            scroll = ActionChains(self.driver)
            scroll.move_to_element(element).perform()
        return element

    def circular_mousemovement(self, radius=300):
        # Radius 
        R = radius
        # measuring screen size
        (x,y) = pyautogui.size()
        # locating center of the screen 
        (X,Y) = pyautogui.position(x/2,y/2) # type: ignore
        # offsetting by radius 
        pyautogui.moveTo(X+R,Y)

        for i in range(230):
            # setting pace with a modulus 
            if i%10 == 0:
                pyautogui.moveTo(X+R*math.cos(math.radians(i)),Y+R*math.sin(math.radians(i)))

    def move_and_click_element_with_ease_in_out(self, element: WebElement) -> None:
        """
        Moves the mouse cursor to a random position within the specified web element, then clicks it with a smooth ease-in/ease-out motion.

        Args:
            element (WebElement): The web element to click.

        Returns:
            None

        Example Usage:
            element = self.driver.find_element_by_xpath("//button[@id='myButton']")
            self.move_and_click_element_with_ease_in_out(element)

        Notes:
            - This function uses PyAutoGUI to move the mouse cursor with an ease-in/ease-out motion, and Selenium's move_to_element_with_offset() and click() functions to click the element at the exact random position.
            - The speed of the mouse movement can be adjusted by dividing the distance by a factor in the "duration" calculation.
            - The easing function used is easeInOutQuad(). You can replace this with your own custom easing function if desired.
            - If the element is not clickable or visible, this function may not work properly.
        """
        action_chains = ActionChains(self.driver)

        # Get the position and size of the element
        x, y = element.location['x'], element.location['y']
        width, height = element.size['width'], element.size['height']

        # Calculate a random position within the element
        rand_x = x + pyautogui.randint(0, width) # type: ignore
        rand_y = y + pyautogui.randint(0, height) # type: ignore

        # Move the mouse to the random position with an ease-in/ease-out motion
        start_x, start_y = pyautogui.position()
        distance = math.sqrt((rand_x - start_x) ** 2 + (rand_y - start_y) ** 2)
        duration = distance / 1000  # adjust the speed by dividing with a factor
        start_time = time.time()

        while (time.time() - start_time) < duration:
            elapsed_time = (time.time() - start_time)
            easing = self.easeInOutQuad(elapsed_time, 0, 1, duration)

            x = int(start_x + (rand_x - start_x) * easing)
            y = int(start_y + (rand_y - start_y) * easing)

            pyautogui.moveTo(x, y)

        # Move the mouse cursor to the exact random position within the element to ensure accuracy
        pyautogui.moveTo(rand_x, rand_y)

        # Click the element at the random position
        action_chains.move_to_element_with_offset(element, rand_x - x, rand_y - y).click().perform()

    @staticmethod
    def easeInOutQuad(t: float, b: float, c: float, d: float) -> float | None:
        """
        An easing function that provides a smooth ease-in/ease-out motion for the mouse cursor.

        Args:
            t (float): The elapsed time.
            b (float): The starting value.
            c (float): The change in value.
            d (float): The duration.

        Returns:
            float: The calculated easing value.

        Notes:
            - This function is used by the move_and_click_element_with_ease_in_out() function to provide an ease-in/ease-out motion for the mouse cursor.
        """
        t /= d / 2
        if t < 1:
            return c

    @staticmethod
    def move_mouse_with_ease(x, y):
        """
        Moves the mouse cursor to the given (x, y) coordinates with an ease-in and ease-out speed.
        
        Args:
            x (int): The x-coordinate to move the mouse cursor to.
            y (int): The y-coordinate to move the mouse cursor to.
        """
        # Get the current mouse position
        current_x, current_y = pyautogui.position()

        # Calculate the distance between the current position and the target position
        distance = ((x - current_x) ** 2 + (y - current_y) ** 2) ** 0.5

        # Set the easing function for the mouse movement
        pyautogui.easeInOutQuad # type: ignore

        # Move the mouse cursor to the target position with ease-in and ease-out speed
        pyautogui.moveTo(x, y, duration=distance/500, tween=pyautogui.easeInOutQuad) # type: ignore

    def scroll_randomly(self, time_to_scroll):
        """
        Scroll randomly up and down on a web page using a Selenium WebDriver.
        time_to_scroll: time to scroll randomly
        """
        # Set the initial scroll position to the top of the page
        scroll_position = 0

        # Define the maximum scroll position (which is the bottom of the page)
        max_scroll_position = pyautogui.size().height

        # Scroll up and down randomly for 10 seconds
        end_time = time.time() + time_to_scroll
        while time.time() < end_time:
            # Randomly choose to scroll up or down
            if random.random() < 0.5:
                # Scroll down by a random amount
                scroll_amount = random.randint(50, 200)
                scroll_position += scroll_amount
                scroll_position = min(scroll_position, max_scroll_position)
                pyautogui.scroll(-scroll_amount)
            else:
                # Scroll up by a random amount
                scroll_amount = random.randint(50, 200)
                scroll_position -= scroll_amount
                scroll_position = max(scroll_position, 0)
                pyautogui.scroll(scroll_amount)

            # Wait for a short time before scrolling again
            time.sleep(random.uniform(0.5, 1.5))

    def search_and_click_random_video(self, keyword: str):
        """
        Searches YouTube for a given keyword, scrolls randomly through the results,
        and clicks on a random video. Then, searches Google for the same keyword,
        and clicks on a random link.

        Args:
            keyword (str): The keyword to search for on YouTube and Google.

        Example Usage:
            self.search_and_click_random_video("cute kittens")  # Search for "cute kittens"

        Notes:
            - This method relies on other methods within the `BasePage` class, such as `scroll_randomly`.
            - The method first navigates to YouTube, searches for the keyword, scrolls randomly, and clicks a random video.
            - After that, the method navigates to Google, searches for the same keyword, and clicks a random link.
        """
        # Navigate to YouTube and search for the keyword
        self.driver.get(CookieBotResources.YoutubeURL)
        search_box = self.wait_until_find(CookieBotResources.YoutubeSearchField)
        self.send_keys(search_box, keyword)
        search_box.submit()

        # Scroll randomly and click a random video
        self.scroll_randomly(5)
        video_elements = self.wait_until_find_all(CookieBotResources.YoutubeVideo)
        video = random.choice(video_elements)
        self.scroll_to_element(video)
        self.click(video)
        time.sleep(30)

        # Navigate to Google and search for the keyword
        self.driver.get(CookieBotResources.GoogleURL)
        search_box = self.wait_until_find(CookieBotResources.GoogleSearchField)
        self.send_keys(search_box, keyword)
        search_box.submit()

        # Scroll randomly, find all link elements, and click a random link
        link_elements = self.wait_until_find_all(CookieBotResources.Googlelink)
        self.scroll_randomly(10)
        link = random.choice(link_elements)
        self.scroll_to_element(link)
        self.click(link)
        time.sleep(3)

        # Scroll randomly on the Google search results page
        self.scroll_randomly(35)
        return self
