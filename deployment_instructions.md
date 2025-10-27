# Location Tracker Website Deployment Instructions

## Overview

This document provides comprehensive instructions for deploying the Location Tracker website, a complex web application that tracks visitor locations using IP-based geolocation and stores this information in cookies. The application features both frontend and backend components built with Flask.

## Project Structure

The project follows a standard Flask application structure:

```
location_tracker/
├── requirements.txt      # Python dependencies
├── src/
│   ├── main.py          # Main Flask application entry point
│   ├── models/          # Database models (not actively used in this version)
│   │   └── user.py
│   ├── routes/          # API endpoints
│   │   ├── location.py  # Location tracking endpoints
│   │   └── user.py      # User-related endpoints
│   └── static/          # Frontend assets
│       ├── css/
│       │   └── styles.css
│       ├── js/
│       │   └── main.js
│       └── index.html   # Main HTML page
```

## Features

1. **IP-Based Geolocation**: Uses the ipinfo.io API to determine visitor location based on IP address
2. **Cookie Management**: Stores location data in cookies with a 30-day expiration
3. **Interactive UI**: Allows users to refresh location data or clear stored cookies
4. **Map Placeholder**: Prepared for integration with mapping services in future versions
5. **Responsive Design**: Works on both desktop and mobile devices

## Deployment Options

### Option 1: Local Deployment

1. Ensure Python 3.8+ is installed on your system
2. Clone or download the project files to your local machine
3. Navigate to the project directory in your terminal
4. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Run the application:
   ```bash
   cd src
   python -m main
   ```
7. Access the website at http://localhost:5000

### Option 2: Production Deployment

For production deployment, consider the following options:

1. **Platform as a Service (PaaS)** like Heroku, Render, or PythonAnywhere:
   - Create an account on your preferred platform
   - Follow their specific instructions for deploying Flask applications
   - Ensure environment variables are properly configured

2. **Virtual Private Server (VPS)** like AWS EC2, DigitalOcean, or Linode:
   - Set up a server with Ubuntu or your preferred Linux distribution
   - Install Python, pip, and required dependencies
   - Use Gunicorn or uWSGI as a WSGI server
   - Set up Nginx or Apache as a reverse proxy
   - Configure SSL for secure connections

3. **Docker Deployment**:
   - Create a Dockerfile in the project root
   - Build and run the Docker container
   - Deploy to container orchestration services like Kubernetes or Docker Swarm

## Configuration

### Environment Variables

The application supports the following environment variables:

- `FLASK_ENV`: Set to "production" for production deployment
- `FLASK_SECRET_KEY`: Custom secret key for session management
- `PORT`: Custom port number (default: 5000)

### API Keys

The application uses the free tier of ipinfo.io API. For higher request limits:

1. Register at [ipinfo.io](https://ipinfo.io)
2. Obtain an API key
3. Modify the location.py file to include your API key in requests

## Customization

### Styling

Modify the `src/static/css/styles.css` file to customize the appearance of the website.

### Additional Features

To add more features:

1. Create new route files in the `src/routes/` directory
2. Register new blueprints in `src/main.py`
3. Add frontend components in the `src/static/` directory

## Troubleshooting

### Common Issues

1. **Missing Dependencies**: Ensure all dependencies are installed via `pip install -r requirements.txt`
2. **Port Already in Use**: Change the port number in `src/main.py`
3. **CORS Issues**: If integrating with other services, configure CORS headers in `src/main.py`

### Logs

Check application logs for detailed error information when running the Flask application.

## Security Considerations

1. The application sets cookies with the `httponly` and `samesite='Strict'` flags for security
2. In production, always use HTTPS to protect user data
3. Consider implementing rate limiting for the location tracking API
4. Add proper user consent mechanisms before tracking location in production

## Future Enhancements

1. Integrate with a mapping API (Google Maps, Mapbox, etc.) to display actual maps
2. Add user authentication for personalized tracking
3. Implement a database to store historical location data
4. Add more detailed location information through additional APIs

## Support

For questions or issues, please contact the developer.
