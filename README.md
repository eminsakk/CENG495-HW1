# URL
- buyin.onrender.com

# About Programming Language and Framework Choice
- Python has a rich standart library. Some operations are much easier to implement  I used Python extensively in CENG111 class.After that I did not use it again. Because I know that Python is used a lot field like in deep learning, I thought python is a good choice for me. 
- Another reason why I choose Python is that Python has mature and versatile web frameworks such as Django and Flask. And these packages are easy to install and easy to manage them thanks to pip package installer. 
- Firstly,I am a bit familiar with Django thanks to the my senior year project. So I had started to develop the web site with it. However I have some issues about poetry versions and MongoDB Django connector Djongo. I spent 5 days to solve on these. When I succeed I could not deploy the project on the render. So I changed my mind and continued with Flask for backend development and PyMongo for MongoDB database operations. With these frameworks, deploying a web project on render much easier compared to Django and Djongo in my opinion.

# Notes on BuyIn Implementation
- First of all we have 2 types of user, admin and regular user. You can use same login page for admin authentication or regular user athentication. 
- Regular users also can register the site using register route in the code. This is basic register page that creates regular user by taking username and 
password. If there will be an error with similarity of the passwords error message is shown in the same page.
- Uses can filter items according to their needs.
- There is an ambiguity of the add users to the system using admin panel because of the password authentication of the users. I think that only username and is admin checkbox is sufficient to create users. Providing passwords is nonsense for me in this panel. So every created newly user by admin panel just writes its username and press the login. I have handled the situation by setting every password of the users by empty string in admin panel registration.
- I assume that reviews and ratings are united aspects of the e-commerce system. If only user gives rating and submit the button content of the review is empty,
and I save it as it is. Users can see these ratings and empty comments.
- There is a bug that I can not fix it yet. It is basically when user logout the account it is successfully directed to login page of the system.
However If she/he uses the back button in the top left of the browser, user logged in again secretively. I think that this bug is because of the unproper 
implementation of the POST and GET forms of the routes however I could not fix it. This bug also occurs in comment. After sending rating and review, when I hit the browser back button, my review and rating come to the screen. After second hit, it works properly
- app.py file mainly includes routes and Flask based implementations. database_utils.py file mainly includes PyMongo usage.







