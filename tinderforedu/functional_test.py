from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

'''
class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_search_list_and_retrieve_it_later(self):
        # Edith has heard about a cool finding tutor app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:8000/tinderforeduapp/')

        # She notices the page title and header mention Tinder-for-EDU
        self.assertIn('Match-and-Learn', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Match and Learn', header_text)
        welocome_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Welcome, Guest!', welocome_text)


        # She notices login and sign up hyperlink
        login_link = self.browser.find_element_by_link_text('login').text
        self.assertIn('login', login_link)
        signup_link = self.browser.find_element_by_link_text('signup').text
        self.assertIn('login', login_link)


        # She is invited to enter a subjects straight away
        search_text = self.browser.find_element_by_tag_name('p').text
        self.assertIn("search for some one you're looking for" ,search_text)
        inputbox = self.browser.find_element_by_id('subject_find_id')
        self.assertEqual(

        inputbox.get_attribute('placeholder'),
                'Enter a subject'
            )

        # She types "Math2" into a text box
        inputbox.send_keys('Math2')

        # When she hits enter, the page updates, and now
        # the page show lists of people who are good at Math2
        inputbox.send_keys(Keys.ENTER)
        time.sleep(10)
        table = self.browser.find_element_by_id('find_result')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: watcharawut', [row.text for row in rows])




        self.fail('Finish the test!')

        # Satisfied, she goes back to sleep



'''
class signUp(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_sign_up_and_retrieve_it_later(self):
        # Edith wants to be a member so she clicks sign up link
        self.browser.get('http://localhost:8000/tinderforeduapp/signup')

        # She notices the header mention Sign up
        self.assertIn('', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Sign up', header_text)

        # She is invited to enter an Username
        label_username = self.browser.find_element_by_id('id_label_username').text
        self.assertIn('Username:', label_username)
        inputbox_username = self.browser.find_element_by_id('id_username')
        self.assertEqual(
        inputbox_username.get_attribute('type'),
                'text'
            )

        # She is invited to enter a password
        label_password = self.browser.find_element_by_id('id_label_password').text
        self.assertIn('Password:', label_password)
        inputbox_password = self.browser.find_element_by_id('id_password')
        self.assertEqual(
        inputbox_password.get_attribute('type'),
                'password'
            )

        # She is invited to enter a password confirmation
        label_passwordconfirm = self.browser.find_element_by_id('id_label_passwordconfirm').text
        self.assertIn('Password confirmation:', label_passwordconfirm)
        inputbox_passwordconfirm = self.browser.find_element_by_id('id_passwordconfirm')
        self.assertEqual(
        inputbox_passwordconfirm.get_attribute('type'),
                'password'
            )

        # She types "Edith" into Username text box
        inputbox_username.send_keys('Edith')

        # She types "123456" into Password text box
        inputbox_password.send_keys('qwertyuiop[]')

        # She types "123456" again into Password confirmation text box
        inputbox_passwordconfirm.send_keys('qwertyuiop[]')
        input_first_name = self.browser.find_element_by_id("id_first_name")
        input_first_name.send_keys("tu")
        input_last_name = self.browser.find_element_by_id("id_last_name")
        input_last_name.send_keys("pobthorn")
        input_age = self.browser.find_element_by_id("id_age")
        input_age.send_keys('50')
        input_email = self.browser.find_element_by_id("id_email")
        input_email.send_keys("ragr@gmail.com")
        input_college = self.browser.find_element_by_id("id_college")
        # then she notices Sign up button and click it
        input_college.send_keys('kmuntb')
        signup_button = self.browser.find_element_by_id('id_signup')
        self.assertEqual(
        signup_button.get_attribute('type'),
                'submit',
            )

        signup_button.send_keys(Keys.ENTER)
        time.sleep(10)



"""class YourSubject(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('good_subject_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])



    def test_can_add_and_remove_good_subject(self):
        # Pure wants to add his good subject so he clicks good subject link
        self.browser.get('http://127.0.0.1:8000/tinderforeduapp/66/your_subject/')

        # he notices the header mention Enter your good subject
        self.assertIn('', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Enter your good subject', header_text)

        # he notices his name
        name_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('name :pakkapure', name_text)

        # he notices his age
        age_text = self.browser.find_element_by_id('age_id').text
        self.assertIn('age: 18', age_text)

        # he notices his school
        school_text = self.browser.find_element_by_id('school_id').text
        self.assertIn("school: king mongkut's university of technology north bangkok", school_text)

        # he is invited to enter his good subjects
        inputbox = self.browser.find_element_by_id('subject_good_id')
        self.assertEqual(
        inputbox.get_attribute('placeholder'),
                'Enter a subject'
            )

        # he notices add button
        inputbox = self.browser.find_element_by_name('add_button')
        self.assertEqual(
        inputbox.get_attribute('type'),
                'submit'
            )

        # he notices remove button
        inputbox = self.browser.find_element_by_name('remove_button')
        self.assertEqual(
        inputbox.get_attribute('type'),
                'submit'
            )

        # he types "Math2" into a text box
        inputbox = self.browser.find_element_by_id('subject_good_id')
        inputbox.send_keys('Math2')

        # When he hits enter, the page updates, and now
        # the page show lists of his good subject
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Math2')

        # There is still a text box inviting his to add another subject.
        # he enters "Physic"
        inputbox = self.browser.find_element_by_id('subject_good_id')
        inputbox.send_keys('Physic')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both subject on his list
        self.check_for_row_in_list_table('1: Math2')
        self.check_for_row_in_list_table('2: Physic')

        # but he is not good at Physic.
        # he selects Physic checkbox to remove it
        table = self.browser.find_element_by_id('good_subject_table')
        checkbox = table.find_element_by_id('subject_name:2')
        checkbox.click()
        remove_select = self.browser.find_element_by_id("remove_button_id")
        remove_select.send_keys(Keys.ENTER)
        time.sleep(2)



"""
if __name__ == '__main__':
    unittest.main(warnings='ignore')
