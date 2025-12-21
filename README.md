# Ozeri's Blog

A full-featured Flask-based blog application with user authentication, commenting system, and admin functionality.

## Features

### User Management
- User registration and login system
- Secure password hashing with Werkzeug
- User profiles with Gravatar integration
- Session management with Flask-Login

### Blog Posts
- Create, read, update, and delete blog posts (admin only)
- Rich text editor with CKEditor
- Image support for posts
- Post listing with latest 5 posts on homepage
- Individual post pages with full content

### Comments
- Authenticated users can comment on posts
- Comment display with author Gravatar
- Post/Redirect/Get pattern to prevent duplicate submissions

### Additional Features
- Contact form with email notifications
- About page
- Admin-only restrictions for post management
- Responsive design with Bootstrap 5
- SQLAlchemy ORM for database management

## Setup

1. Clone the repository

2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Create a `.env` file in the root directory
   - Add the following variables:
     ```
     SECRET_KEY=your-secret-key-here
     SENDER_EMAIL=your-email@example.com
     PASSWORD=your-email-password
     RECIVER_EMAIL=recipient@example.com
     DB_URI=sqlite:///blog.db
     ```

5. Run the application:
   ```bash
   python main.py
   ```

6. Open browser at `http://127.0.0.1:5000`

7. Register a new user - the first user (ID=1) will have admin privileges

## Project Structure

```
blog/
├── main.py              # Main application routes and logic
├── models.py            # Database models (User, BlogPost, Comment)
├── forms.py             # WTForms definitions
├── utils.py             # Utility functions (email sending)
├── requirements.txt     # Python dependencies
├── templates/           # HTML templates
├── static/              # CSS, JS, and images
└── instance/            # Database file (auto-generated)
```

## Technologies Used

- Flask - Web framework
- Flask-Bootstrap - Bootstrap integration
- Flask-Login - User session management
- Flask-SQLAlchemy - Database ORM
- Flask-CKEditor - Rich text editor
- Flask-Gravatar - User avatars
- WTForms - Form validation
- Werkzeug - Password hashing
- Python-dotenv - Environment variable management

## License

© 2025 Yarin Ozeri. All rights reserved.
