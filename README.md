# Travelog

### Table of Contents
- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Key Features](#key-features)
- [Key Learning Takeaways](#key-learning-takeaways)
- [Future Improvements](#future-improvements)
- [Links](#links)

### Overview

Travelog is a social travel platform where users can share their travel experiences, document journeys, and discover posts from other travelers.

Built with Django and PostgreSQL, and deployed on DigitalOcean App Platform, this full-stack web app allows users to write blog-style travel posts, interact with others, and explore travel stories from around the world. Working on Travelog gave me hands-on experience in building a full-stack Django application from scratch, deploying it in a production environment, and solving real-world development challenges.


### Tech Stack

| Technology    | Description                           |
|---------------|---------------------------------------|
| Django        | Backend framework for building web apps |
| PostgreSQL    | Relational database management system  |
| Bootstrap     | Frontend framework for responsive design |
| HTML, CSS, JS | Frontend basics for styling and interactivity |
| DigitalOcean  | Hosting platform for production deployment |


### Key features

- User authentication (registration, login, logout)
- Create, edit, and delete travel posts
- Upload images with posts
- Follow other users
- View posts from other users
- Add posts to personal reading list
- Share posts on social media
- Comment on blog posts


###  Key Learning Takeaways
Here are some of the key things I learned while building this project:

User Authentication
- Implemented a complete user authentication system using Django’s built-in authentication framework.
- Created views and templates for user registration, login, logout, password reset, and password change.
  
Custom User Model and Profile
- Followed Django best practices by implementing a custom user model from the beginning.
- Extended the `AbstractUser` model and created a `Profile` model to store profile pictures and additional user information while preserving Django’s built-in authentication functionality.
  
Tagging System with django-taggit
- Integrated the `django-taggit` library to allow users to tag their posts. With the tagging system, users can view posts by tag and discover similar posts based on shared tags.
  
Customising Class-Based Views (CBVs)
- Extended Django’s generic class-based views (CBVs) for greater control over logic and rendering.
- Customised `PostListView` by modifying `get_context_data` to pass tag data to templates.
Implementation:
```python
def get_context_data(self, **kwargs):
	context = super().get_context_data(**kwargs)
	context['tags'] = Tag.objects.all()
	return context

```
  
Database Management with PostgreSQL
- Used PostgreSQL for both local development and production.
- Managed data through Django’s ORM, including foreign key relationships and custom queries.

Deployment on DigitalOcean App Platform
- Deployed the app on DigitalOcean’s App Platform.
- Handled environment variables, static/media file settings, and connected the Django app to a managed PostgreSQL database.

Image Upload & Media Handling
- Enabled users to upload images for both posts and profile pictures using Django’s `ImageField`.
- Configured media storage settings and learned how to serve uploaded files in development and production environments.


### Future Improvements
It is a project that allows me consolidate what I've been learning about Django, Python, on how to configure for production and deployment. I plan to keep improving it by enhancing readability of codes and modularity of the structure, and potentially adding the feature of AI-powered itinary planner. 


### Links
- [GitHub Repository](https://github.com/ellenycc/travelog)
- [Live site](https://www.travelogforall.com/)
