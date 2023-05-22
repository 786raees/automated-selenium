"""This File contains all the locators all the elements of different pages
If in futur the UI of the website will change we can change the locators from here
"""
from selenium.webdriver.common.by import By
from dataclasses import dataclass

@dataclass
class Selector:
    """class to create objects for selecting or targetting a certain element
        on the page

        Args:
            ST (str): Selector Type: ie XPATH or CSSSelector
            SP (str): Path of the element according to selector type
    """
    ST: str
    SP: str


class CookieBotResources:
    """This class contains all the locators and urls for cookie bot"""

    # URLs for YouTube and Google
    YoutubeURL = "https://youtube.com/"
    GoogleURL = "https://google.com/"

    # Locators for YouTube search field and video elements
    YoutubeSearchField = Selector(By.XPATH, "//input[@id='search']")
    YoutubeVideo = Selector(By.XPATH, "//a[@id='video-title']")

    # Locators for Google search field and link elements
    GoogleSearchField = Selector(By.XPATH, "//*[@name='q']")
    Googlelink = Selector(By.XPATH, '//a[./h3[contains(@class,"DKV0Md")]]')
