# Jsupa DIY Blog
Do It Yourself Blog written in django by johnrmremi

This web application creates an very basic blog site using Django. The site allows blog administators to register new users and assign them to the groups as bloggers(blogger can add, edit and delete their own blog posts) or normal_users(who can create, edit and delete thier comments). Normal users can only comment when they are logged in but only bloggers can create blogs and comments. Any user can list all bloggers, all blogs, and detail for bloggers and blogs (including comments for each blog).

# Quick Start
To get this project up and running locally on your computer:

    1. Set up the Python development environment. We recommend using a Python virtual environment.
    2. Assuming you have Python setup, run the following commands (if you're on Windows you may use py or py -3 instead of python3 to start Python):
        pip3 install -r requirements.txt
        python3 manage.py makemigrations
        python3 manage.py migrate
        python3 manage.py collectstatic
        python3 manage.py test # Run the standard tests. These should all pass.
        python3 manage.py createsuperuser # Create a superuser
        # Then in the admin interface, create two groups
            # 1. bloggers
              # then assign it the permission: blog|blog|View blogs as blogger
           # 2. normal_users
               # this group does not have any permission
        # Then create few users and assign them to these groups.
        python3 manage.py runserver
Open a browser to http://127.0.0.1:8000/admin/ to open the admin site
Create a few test objects of each type.
Open tab to http://127.0.0.1:8000 to see the main site, with your new objects.
>>>>>>> deployment
