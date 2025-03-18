# Bookly 📚

Bookly is a RESTful API service for managing book reviews, authentication, and tagging functionality. It is built using **FastAPI** and follows modern API design principles.

## Features
- 📖 **Books Management**: CRUD operations on books.
- 🔐 **Authentication**: User registration, login, email verification, and token-based authentication.
- ⭐ **Reviews**: Users can add, retrieve, and delete reviews for books.
- 🏷 **Tags**: Books can be tagged with multiple categories for better organization.

## Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL (or any preferred database)

### Clone the Repository
```bash
git clone https://github.com/cyxabima/bookly.git
cd bookly
```

### Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Books 📚
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/v1/books/` | Get all books |
| POST | `/api/v1/books/` | Create a new book |
| GET | `/api/v1/books/{book_uid}` | Get details of a book |
| PATCH | `/api/v1/books/{book_uid}` | Update a book |
| DELETE | `/api/v1/books/{book_uid}` | Delete a book |

### Authentication 🔑
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/api/v1/auth/signup` | Create a new user |
| POST | `/api/v1/auth/login` | User login |
| GET | `/api/v1/auth/verify/{token}` | Verify user email |
| GET | `/api/v1/auth/me` | Get authenticated user details |
| POST | `/api/v1/auth/reset-password-email` | Request password reset email |
| POST | `/api/v1/auth/reset-password/{token}` | Reset password |

### Reviews ⭐
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/v1/review/` | Get all reviews |
| GET | `/api/v1/review/{review_uid}` | Get review details |
| DELETE | `/api/v1/review/{review_uid}` | Delete a review |
| POST | `/api/v1/review/book/{book_uid}` | Add a review to a book |

### Tags 🏷
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/v1/tags/` | Get all tags |
| POST | `/api/v1/tags/` | Create a new tag |
| POST | `/api/v1/tags/book/{book_uid}/tags` | Assign tags to a book |
| PUT | `/api/v1/tags/{tag_uid}` | Update a tag |
| DELETE | `/api/v1/tags/{tag_uid}` | Delete a tag |



## API Documentation 📄
Once the server is running, the API docs can be accessed at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Pdf Documentation 📄
- [pdf of Documentation](Bookly%20-%20Swagger%20UI.pdf)

- [Comprehensive Documentation](Bookly%20-%20ReDoc.pdf)

## [PostMen Collections 🔄 ](Bookly.postman_collection.json)



## License 📜
This project is licensed under the MIT License. [(view)](license.md)


## 📂 Project Structure
```
└── src
    ├── books
    │   ├── __init__.py
    │   ├── routes.py
    │   ├── schemas.py
    │   └── service.py
    ├── config.py
    ├── db
    │   ├── __init__.py
    │   ├── main.py
    │   ├── models.py
    │   └── redis.py
    ├── email.py
    ├── errors.py
    ├── __init__.py
    ├── middleware.py
    ├── myTyping.py
    ├── reviews
    │   ├── __init__.py
    │   ├── routes.py
    │   ├── schemas.py
    │   └── service.py
    ├── tags
    │   ├── __init__.py
    │   ├── routes.py
    │   ├── schemas.py
    │   └── service.py
    ├── templates
    └── users
        ├── dependency.py
        ├── __init__.py
        ├── routes.py
        ├── schemas.py
        ├── service.py
        └── utils.py
```

## Contributors 👨‍💻
- ### **[Ukasha Anwer @ Cyxabima](https://github.com/cyxabima)** - Developer & Maintainer  

---
💡 **Contributions are welcome!** If you find any issues or want to enhance Bookly, feel free to submit a pull request!

