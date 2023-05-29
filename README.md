# Automated-Selenium

Automated-Selenium is a Python library that provides a base page class designed to facilitate the implementation of the Page Object Model (POM) structure in Selenium-based test or process automation projects.

## Introduction

The Automated-Selenium library aims to simplify the development and maintenance of Selenium test automation frameworks by offering a reusable and extensible base page class. This base class encapsulates common functionality and provides essential methods for interacting with web elements, managing page navigation, and handling common automation tasks.

## Key Features

- **Page Object Model (POM) Support**: Automated-Selenium promotes the use of the Page Object Model design pattern, allowing you to organize your code into reusable and maintainable components.
- **Web Element Interaction**: The library provides a comprehensive set of methods for interacting with web elements, such as clicking, typing, selecting options, and verifying element properties.
- **Page Navigation**: With Automated-Selenium, you can easily navigate between pages, handle redirects, and manage browser windows or tabs.
- **Customizable and Extensible**: The base page class can be extended and customized to suit the specific needs of your project. You can add additional methods or override existing ones to accommodate your application's unique behaviors.
- **Integration with Selenium**: Automated-Selenium seamlessly integrates with the Selenium WebDriver, enabling you to harness the full power of Selenium for browser automation.

## Installation

To use Automated-Selenium in your Python project, follow these steps:

1. Make sure you have Python 3.x installed on your system.
2. Install the required dependencies by running the following command:

   ```
   pip install automated-selenium
   ```

3. Import the library into your Python code:

   ```python
   from automated_selenium import BasePage
   ```

## Getting Started

To get started with Automated-Selenium, you can follow these steps:

1. Create a new Python module for your page objects or navigate to an existing one.
Note: Your element selector should be an instance of Selector class as follow.
   ```python
   # your resources or locator file
   from automated_selenium import Selector
   from selenium.webdriver.common.by import By

   class LoginResources:
      # your resources as follow
      username_field = Selector(By.XPATH, "//input[@id='username']")
      password_field = Selector(By.XPATH, "//input[@id='password']")
      submit_button = Selector(By.XPATH, "//input[@id='submit_btn']")
   ```
2. Import required functions and classes:

   ```python
   from automated_selenium import BasePage

   # Import your resources
   from .resources import LoginResources
   ```

3. Create a new class for your page object, inherit from `BasePage` and add your own methods:

   ```python
   class MyPage(BasePage):
       logged_in = False
       url = 'https://example.com'

       def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         # call your web url here
         self.driver.get(self.url)
         
       # Add your custom methods and properties here
       def check_login(self):
         # check if the user is logged in
         # perform some task to check login
         # if user is logged in make self.logged_in = True
         self.logged_in = True

       def login(self, username: str, password: str):
         # check if user is already logged in
         self.check_login()
         if self.logged_in:
            # Find username field
            username_field = self.find(LoginResources.username_field)
            # Type username like human
            self.send_keys(username_field, username)

            # Find password field
            password_field = self.find(LoginResources.password_field)
            # Type password like human
            self.send_keys(password_field, password)

            # Find submit button
            submit_button = self.find(LoginResources.submit_button)
            # click on submit button
            self.click(submit_button)
            # check if you are logged in successfully
            self.check_login()
            # Return self if you want to chain your actions as follow.
            # login_page = LoginPage(driver)
            # login_page.check_login()\
            #           .login()\
            return self
      ```
4. Now use this page object to login in your `main.py`.
   ```python
   from automated_selenium import get_undetected_chrome_browser
   from your_pages import MyPage

   def main():
      # A profile to use by browser it will create new one if it do not have already
      # the profile will store cookies and other user data for the next run.
      profile_name = 'my_profile'
      # Create a new driver instance
      driver = get_undetected_chrome_browser(profile_name)
      my_page = MyPage(driver)
      # Perform some task here

      my_page.login(username='admin', password='automated_selenium')

   if __name__ == '__main__':
      main()
   ```
   
5. Implement your page-specific methods and use the provided base methods to interact with web elements, handle navigation, and perform other automation tasks.
6. Instantiate your page object class in your test code and start automating!

## BasePage Class

The `BasePage` class is the base class for all the pages in the project. Subclasses will contain methods that can be performed on a single page. 

To create a new instance of this class, use the following code:

```python
page = MyPage(driver)
```

### Methods

- **`__init__(self, driver: Remote) -> None`**: Initializes the `BasePage` class with a `driver` object and maximizes the window.

- **`find(self, selector: Selector) -> WebElement`**: Finds and returns an element from the driver.

- **`find_from_element(self, element: WebElement, selector: Selector) -> WebElement`**: Finds and returns an element from another element.

- **`find_all(self, selector: Selector) -> List[WebElement]`**: Finds and returns a list of all available elements from the driver.

- **`wait_until_find(self, selector: Selector, timeout: int = 10, condition=EC.presence_of_element_located) -> WebElement`**: Waits for an element to be present in the DOM and returns an available element from the driver.

- **`wait_until_find_all(self, selector: Selector, timeout: int = 10, condition=EC.presence_of_all_elements_located) -> List[WebElement]`**: Waits for elements to be present in the DOM and returns a list of all available elements from the driver.

- **`click(self, element: WebElement) -> None`**: Tries to click the given element. If it fails, it executes a script to click it.

- **`click_all(self, elements: List[WebElement]) -> None`**: Clicks all elements in the given list.

- **`send_keys(self, element: WebElement, text: str) -> None`**: Helps to type text like a human into the input element.

- **`random_mouse_movement(self, total_num)`**: Randomly moves the mouse on the screen for a specific number of times.

- **`move_mouse_to_coordinates(x, y)`**: Moves the mouse to the specified coordinates.

- **`move_mouse_to_element(self, element)`**: Moves the mouse cursor to the specific element displayed on the screen.

- **`click_random_position_in_element(self, element)`**: Clicks a random position within the specified element.

- **`find_and_click(self, selector: Selector, timeout: int = 10)`**: Finds and clicks the element specified by the selector.

- **`scroll_to(self, selector: Selector, timeout: int = 10)`**: Scrolls to the element specified by the selector.

- **`scroll_to_element(self, element: WebElement, timeout: int = 10)`**: Scrolls to the specified element.

- **`circular_mousemovement(self, radius=300)`**: Performs a circular mouse movement with the specified radius.

- **`move_and_click_element_with_ease_in_out(self, element: WebElement) -> None`**: Moves the mouse cursor to a random position within the specified web element, then clicks it with a smooth ease-in/ease-out motion.

- **`easeInOutQuad(t: float, b: float, c: float, d: float) -> float | None`**: An easing function that provides a smooth ease-in/ease-out motion for the mouse cursor.

- **`move_mouse_with_ease(x, y)`**: Moves the mouse cursor to the given (x, y) coordinates with an ease-in and ease-out speed.

- **`scroll_randomly(self, time_to_scroll)`**: Scrolls randomly up and down on a web page using a Selenium WebDriver.

- **`search_and_click_random_video(self, keyword: str)`**: Searches YouTube for a

For more detailed documentation and examples, please refer to the [Automated-Selenium GitHub repository](https://github.com/786raees/automated-selenium).

## Contributing

Contributions to the Automated-Selenium library are welcome! If you encounter any issues, have suggestions for improvements, or would like to contribute code, please feel free to submit a pull request on the [GitHub repository](https://github.com/786raees/automated-selenium).

## License

Automated-Selenium is released under the [MIT License](https://github.com/786raees/automated-selenium/blob/main/LICENSE). Please review the license file for more details.

## Acknowledgments

We would like to express our gratitude to the open-source community for their contributions, as well as the authors of the libraries and tools that have made Automated-Selenium possible.

## Contact

For any questions or inquiries, please contact the project maintainers at [waqarkhan1252617@gmail.com](mailto:waqarkhan1252617@gmail.com).