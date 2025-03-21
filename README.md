# Travelog

Travelog is a social travel platform for people to share their travelling experiences, document their journeys, and explore posts from other users. It is built with Django and PostgreSQL, and deployed on DigitalOcean App Platform.

### Key features

- User authentication (registration, login, logout)
- Create, edit, and delete travel posts
- Upload images with posts
- Follow other users
- View posts from other users
- Add posts to reading list
- Share posts on social media
- Comment on blog posts

### Tech Stack

- Backend: Django, PostgreSQL
- Frontend: Bootstrap, HTML, CSS, JavaScript
- Deployment: DigitalOcean App Platform, Docker


### Visit The Website
[Travelog](https://django-blog-3a3v3.ondigitalocean.app/)

###  Key Learning Takeaways from Building Travelog
Building Travelog—a Django-based social travel web app—has been an incredible learning experience. Here are some of the key concepts and skills I developed throughout the project:

🛡️ User Authentication
- Implemented a complete user authentication system using Django’s built-in authentication framework.
- Created views and templates for user registration, login, logout, password reset, and password change.
  
👤 Custom User Model & Profile
- Followed Django best practices by implementing a custom user model early in the project.
- Extended the AbstractUser model and created a Profile model to store profile pictures and additional user information while preserving Django’s built-in authentication functionality.
  
🏷️ Tagging System with django-taggit
- Integrated the django-taggit library to allow users to tag their posts. With the tagging system, we can list all posts under a specific tag and display similar posts based on shared tags.
  
🧠 Customising Class-Based Views (CBVs)
- Learned to extend and override Django’s generic class-based views.
- Customised PostListView by modifying get_context_data to include tag data for rendering dynamic links (e.g., filtering posts by city).
Example:
```
def get_context_data(self, **kwargs):
	context = super().get_context_data(**kwargs)
	context['tags'] = Tag.objects.all()
	return context
```
  
🗃️ Database Management with PostgreSQL
- Used PostgreSQL as the primary database for both local development and production.
- Managed data through Django’s ORM, including foreign key relationships and custom queries.

🌐 Deployment on DigitalOcean App Platform
- Deployed the app on DigitalOcean’s App Platform.
- Handled environment variables, static/media file settings, and connected the Django app to a managed PostgreSQL database.

🖼️ Image Upload & Media Handling
- Implemented post images and profile picture uploads using Django’s ImageField.
- Configured media storage settings and learned how to serve uploaded files in development and production environments.

🚀 Query Optimisation
- Used select_related and prefetch_related to optimise database queries involving user profiles and related data.

🛠️ Debugging & Troubleshooting
- Learned to debug Django apps using print statements, Django error messages, and production logs.
- Solved issues related to environment setup, database connections, media handling, and authentication flows.
