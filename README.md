# Location Tracker Website with Admin Dashboard

A web application that tracks visitor locations using IP-based geolocation and provides an admin dashboard to view all visitor locations on a map.

## Features

- **Visitor Location Tracking**: Tracks visitor location using IP-based geolocation
- **Permanent Cookies**: Stores visitor information in cookies that remain on the visitor's device permanently
- **Interactive Map**: Displays visitor location on a Leaflet map with OpenStreetMap tiles
- **Admin Dashboard**: Secure admin area to view all visitor locations
- **Visitor Analytics**: Collects and displays browser type, operating system, and device model information

## Admin Access

- **URL**: `/admin`
- **Username**: sinner
- **Password**: Cetemiri?7

## Requirements

- Python 3.6+
- Flask 2.0.1
- Werkzeug 2.0.1
- Flask-SQLAlchemy 2.5.1
- Requests 2.28.2
- Additional dependencies in requirements.txt

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/location-tracker.git
cd location-tracker
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python src/main.py
```

5. Access the application at `http://localhost:5000`

## Deployment Options

### Heroku Deployment

1. Create a Heroku account and install the Heroku CLI
2. Login to Heroku:
```bash
heroku login
```

3. Create a new Heroku app:
```bash
heroku create your-app-name
```

4. Add a Procfile (already included in the repository):
```
web: gunicorn wsgi:app
```

5. Deploy to Heroku:
```bash
git push heroku main
```

### Railway Deployment

1. Create a Railway account and connect it to your GitHub
2. Create a new project from your GitHub repository
3. Railway will automatically detect the Python project and deploy it
4. Add the following environment variables:
   - `FLASK_APP=wsgi.py`
   - `FLASK_ENV=production`

### Vercel Deployment

1. Create a Vercel account and connect it to your GitHub
2. Import your GitHub repository
3. Configure the build settings:
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: `src`
   - Install Command: `pip install -r requirements.txt`
4. Add a `vercel.json` file:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "wsgi.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "wsgi.py"
    }
  ]
}
```

## Project Structure

```
location-tracker/
├── src/
│   ├── main.py              # Main Flask application
│   ├── routes/
│   │   ├── admin.py         # Admin routes and authentication
│   │   └── location.py      # Location tracking endpoints
│   ├── models/
│   │   └── user.py          # User/visitor data model
│   └── static/
│       ├── admin/
│       │   ├── dashboard.html  # Admin dashboard
│       │   └── login.html      # Admin login page
│       ├── css/
│       │   └── styles.css      # Application styles
│       ├── js/
│       │   └── main.js         # Frontend JavaScript
│       └── index.html          # Main application page
├── requirements.txt         # Python dependencies
├── Procfile                # For Heroku/Railway deployment
├── wsgi.py                 # WSGI entry point
└── .gitignore              # Git ignore file
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
