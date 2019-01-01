class element_has_new_scroll_height(object):
  """An expectation for checking that an element has a new scrollHeight.

  locator       --  used to find the element
  scrollHeight  --  old scrollHeight to be compared to
  
  returns       --  the WebElement once it has a new bigger scrollHeight
  """
  def __init__(self, locator, scrollHeight):
    self.locator = locator
    self.scrollHeight = scrollHeight

  def __call__(self, driver):
    element = driver.find_element(*self.locator)   # Finding the referenced element
    newScrollHeight = driver.execute_script('return arguments[0].scrollHeight', element)
    print(self.scrollHeight, newScrollHeight)
    if newScrollHeight > self.scrollHeight:
        return element
    else:
        return False
