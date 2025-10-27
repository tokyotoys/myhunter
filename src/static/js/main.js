// Main JavaScript for Location Tracker Website

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const locationDataElement = document.getElementById('location-data');
    const refreshButton = document.getElementById('refresh-location');
    const clearButton = document.getElementById('clear-location');
    const mapElement = document.getElementById('map');
    
    // Initialize map with default coordinates immediately to ensure container is properly set up
    const defaultCoordinates = "40.7128,-74.0060"; // New York City
    setTimeout(() => {
        console.log("Pre-initializing map container with default view");
        try {
            const [defaultLat, defaultLng] = defaultCoordinates.split(',').map(coord => parseFloat(coord.trim()));
            const defaultMap = L.map(mapElement).setView([defaultLat, defaultLng], 13);
            
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 19
            }).addTo(defaultMap);
            
            // Store map instance globally for later access
            window.locationMap = defaultMap;
            console.log("Default map initialized successfully");
        } catch (e) {
            console.error("Error pre-initializing map:", e);
        }
    }, 100);
    
    // Function to format location data into HTML
    function formatLocationData(data) {
        if (!data || !data.location) {
            return '<p class="error">No location data available.</p>';
        }
        
        const location = data.location;
        
        let html = '<div class="location-info">';
        
        // IP Address
        html += `
            <div class="info-item">
                <h3>IP Address</h3>
                <p>${location.ip || 'Unknown'}</p>
            </div>
        `;
        
        // City
        if (location.city) {
            html += `
                <div class="info-item">
                    <h3>City</h3>
                    <p>${location.city}</p>
                </div>
            `;
        }
        
        // Region
        if (location.region) {
            html += `
                <div class="info-item">
                    <h3>Region</h3>
                    <p>${location.region}</p>
                </div>
            `;
        }
        
        // Country
        if (location.country) {
            html += `
                <div class="info-item">
                    <h3>Country</h3>
                    <p>${location.country}</p>
                </div>
            `;
        }
        
        // Postal Code
        if (location.postal) {
            html += `
                <div class="info-item">
                    <h3>Postal Code</h3>
                    <p>${location.postal}</p>
                </div>
            `;
        }
        
        // Coordinates
        if (location.loc) {
            html += `
                <div class="info-item">
                    <h3>Coordinates</h3>
                    <p>${location.loc}</p>
                </div>
            `;
        }
        
        html += '</div>';
        
        // Add source info
        html += `<p style="margin-top: 15px; font-size: 14px; color: #666;">Source: ${data.cookie_info ? 'cookie' : 'live request'}</p>`;
        
        return html;
    }
    
    // Function to load map based on coordinates
    function loadMap(coordinates) {
        if (!coordinates) {
            mapElement.innerHTML = '<p>No coordinates available to display map.</p>';
            return;
        }
        
        try {
            // Parse coordinates from string (format: "lat,lng")
            const [lat, lng] = coordinates.split(',').map(coord => parseFloat(coord.trim()));
            
            if (isNaN(lat) || isNaN(lng)) {
                console.error("Invalid coordinates:", coordinates);
                mapElement.innerHTML = '<p>Invalid coordinates format. Cannot display map.</p>';
                return;
            }
            
            console.log("Initializing map with coordinates:", lat, lng);
            
            // Clear any existing content
            mapElement.innerHTML = '';
            
            // Use default coordinates if the provided ones seem invalid
            const validLat = (lat >= -90 && lat <= 90) ? lat : 40.7128;
            const validLng = (lng >= -180 && lng <= 180) ? lng : -74.0060;
            
            // Initialize the Leaflet map with a slight delay to ensure DOM is ready
            setTimeout(() => {
                try {
                    // Check if we already have a map instance
                    if (window.locationMap) {
                        // Update existing map view and marker
                        window.locationMap.setView([validLat, validLng], 13);
                        
                        // Remove existing markers
                        window.locationMap.eachLayer(layer => {
                            if (layer instanceof L.Marker) {
                                window.locationMap.removeLayer(layer);
                            }
                        });
                        
                        // Add new marker
                        const marker = L.marker([validLat, validLng]).addTo(window.locationMap);
                        marker.bindPopup(`<b>Your Location</b><br>Latitude: ${validLat}<br>Longitude: ${validLng}`).openPopup();
                        
                        console.log("Updated existing map with new coordinates");
                    } else {
                        // Create new map instance
                        const map = L.map(mapElement, {
                            center: [validLat, validLng],
                            zoom: 13,
                            zoomControl: true
                        });
                        
                        // Add OpenStreetMap tile layer
                        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                            maxZoom: 19
                        }).addTo(map);
                        
                        // Add a marker at the user's location
                        const marker = L.marker([validLat, validLng]).addTo(map);
                        
                        // Add a popup with basic location info
                        marker.bindPopup(`<b>Your Location</b><br>Latitude: ${validLat}<br>Longitude: ${validLng}`).openPopup();
                        
                        // Store map instance globally
                        window.locationMap = map;
                        
                        console.log("New map initialized successfully");
                    }
                    
                    // Fix map display issues by triggering a resize after map is created
                    setTimeout(() => {
                        if (window.locationMap) {
                            window.locationMap.invalidateSize();
                            console.log("Map size invalidated and redrawn");
                        }
                    }, 200);
                } catch (e) {
                    console.error("Error during map initialization:", e);
                    mapElement.innerHTML = '<p>Error initializing map. Please try refreshing the page.</p>';
                }
            }, 100);
        } catch (e) {
            console.error("Error in loadMap function:", e);
            mapElement.innerHTML = '<p>Error processing location data. Please try refreshing the page.</p>';
        }
    }
    
    // Function to fetch location data from API
    async function fetchLocationData() {
        locationDataElement.innerHTML = '<p>Loading location data...</p>';
        locationDataElement.classList.add('loading');
        
        try {
            const response = await fetch('/api/location/track');
            const data = await response.json();
            
            locationDataElement.classList.remove('loading');
            
            if (data.success) {
                locationDataElement.innerHTML = formatLocationData(data);
                
                // Load map if coordinates are available
                if (data.location && data.location.loc) {
                    console.log("Location data received with coordinates:", data.location.loc);
                    
                    // Use default coordinates if real ones aren't available
                    const coordinates = data.location.loc || "40.7128,-74.0060";
                    
                    // Force a small delay to ensure DOM is ready
                    setTimeout(() => {
                        loadMap(coordinates);
                    }, 300);
                } else {
                    console.log("No coordinates in location data, using default");
                    loadMap("40.7128,-74.0060"); // Default to New York City
                }
            } else {
                locationDataElement.innerHTML = `<p class="error">Error: ${data.error || 'Failed to retrieve location data'}</p>`;
                // Load default map on error
                loadMap("40.7128,-74.0060");
            }
        } catch (error) {
            locationDataElement.classList.remove('loading');
            locationDataElement.innerHTML = `<p class="error">Error: ${error.message || 'Failed to connect to the server'}</p>`;
            // Load default map on error
            loadMap("40.7128,-74.0060");
        }
    }
    
    // Function to check for existing location cookie
    async function checkExistingLocation() {
        try {
            const locationCookie = document.cookie
                .split('; ')
                .find(row => row.startsWith('user_location='));
            
            if (locationCookie) {
                const locationData = JSON.parse(decodeURIComponent(locationCookie.split('=')[1]));
                
                locationDataElement.innerHTML = formatLocationData({
                    location: locationData,
                    cookie_info: true
                });
                
                // Load map if coordinates are available
                if (locationData.loc) {
                    loadMap(locationData.loc);
                }
                
                return true;
            }
            
            return false;
        } catch (error) {
            console.error('Error checking location cookie:', error);
            return false;
        }
    }
    
    // Function to clear location cookie
    function clearLocationCookie() {
        document.cookie = 'user_location=; Max-Age=-99999;';
        locationDataElement.innerHTML = '<p>Location data cleared. Refresh to get new location.</p>';
        
        // Reset map to default
        loadMap("40.7128,-74.0060");
    }
    
    // Check for existing location cookie first
    const hasExistingLocation = checkExistingLocation();
    
    // If no existing location, fetch new location data
    if (!hasExistingLocation) {
        fetchLocationData();
    }
    
    // Event listeners
    refreshButton.addEventListener('click', fetchLocationData);
    clearButton.addEventListener('click', clearLocationCookie);
});
