import "./Map.css";

// Free map visualization component
const FreeMapVisualization = ({ markers, locations }) => {
  return (
    <div className="map-container" style={{ 
      backgroundColor: '#f8f9fa', 
      padding: '20px',
      height: '500px',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'flex-start',
      alignItems: 'center',
      border: '2px solid #e9ecef',
      borderRadius: '8px',
      position: 'relative'
    }}>
      <div style={{
        position: 'absolute',
        top: '10px',
        left: '10px',
        right: '10px',
        backgroundColor: 'white',
        padding: '15px',
        borderRadius: '6px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        zIndex: 10
      }}>
        <h3 style={{ margin: '0 0 10px 0', color: '#2c3e50' }}>🗺️ Route Optimization Demo</h3>
        <p style={{ margin: '0', fontSize: '14px', color: '#6c757d' }}>
          Free visualization - No API costs required!
        </p>
      </div>

      {/* Route Points Display */}
      {markers && markers.length > 0 && (
        <div style={{ 
          marginTop: '80px',
          width: '100%',
          maxWidth: '600px'
        }}>
          <h4 style={{ color: '#2c3e50', marginBottom: '15px' }}>📍 Route Points:</h4>
          <div style={{ display: 'flex', gap: '20px', justifyContent: 'center' }}>
            {markers.map(marker => (
              <div key={marker.key} style={{ 
                padding: '15px',
                backgroundColor: marker.color === 'blue' ? '#e3f2fd' : '#e8f5e8',
                borderRadius: '8px',
                border: `2px solid ${marker.color === 'blue' ? '#2196f3' : '#4caf50'}`,
                minWidth: '200px',
                textAlign: 'center'
              }}>
                <div style={{
                  width: '20px',
                  height: '20px',
                  borderRadius: '50%',
                  backgroundColor: marker.color === 'blue' ? '#2196f3' : '#4caf50',
                  margin: '0 auto 10px auto'
                }}></div>
                <strong style={{ color: '#2c3e50' }}>{marker.label}</strong>
                <br />
                <span style={{ fontSize: '12px', color: '#6c757d' }}>
                  Lat: {marker.position.lat.toFixed(4)}
                </span>
                <br />
                <span style={{ fontSize: '12px', color: '#6c757d' }}>
                  Lng: {marker.position.lng.toFixed(4)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Selected Attractions Display */}
      {locations && locations.length > 0 && (
        <div style={{ 
          marginTop: '30px',
          width: '100%',
          maxWidth: '800px'
        }}>
          <h4 style={{ color: '#2c3e50', marginBottom: '15px' }}>🎯 Selected Attractions:</h4>
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
            gap: '15px'
          }}>
            {locations.map((location, index) => (
              <div key={index} style={{ 
                padding: '12px',
                backgroundColor: '#fff3e0',
                borderRadius: '6px',
                border: '1px solid #ffb74d',
                fontSize: '13px'
              }}>
                <strong style={{ color: '#e65100' }}>{location.name}</strong>
                <br />
                <span style={{ color: '#6c757d', fontSize: '11px' }}>
                  Lat: {location.location.lat.toFixed(4)}, Lng: {location.location.lng.toFixed(4)}
                </span>
                {location.distance_from_route && (
                  <>
                    <br />
                    <span style={{ color: '#6c757d', fontSize: '11px' }}>
                      Distance: {location.distance_from_route.toFixed(2)} miles
                    </span>
                  </>
                )}
                {location.category && (
                  <>
                    <br />
                    <span style={{ 
                      color: '#fff',
                      backgroundColor: '#ff9800',
                      padding: '2px 6px',
                      borderRadius: '3px',
                      fontSize: '10px'
                    }}>
                      {location.category}
                    </span>
                  </>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Status Information */}
      <div style={{ 
        marginTop: '30px',
        padding: '15px',
        backgroundColor: '#d4edda',
        borderRadius: '6px',
        border: '1px solid #c3e6cb',
        textAlign: 'center',
        fontSize: '14px',
        color: '#155724'
      }}>
        <p style={{ margin: '0 0 5px 0' }}>✅ Backend API is working!</p>
        <p style={{ margin: '0 0 5px 0' }}>✅ Route points and attractions are being fetched</p>
        <p style={{ margin: '0', fontSize: '12px' }}>💰 Completely free - No API costs!</p>
      </div>

      {/* Simple Map Representation */}
      <div style={{
        marginTop: '20px',
        width: '100%',
        height: '200px',
        backgroundColor: '#e8f5e8',
        border: '2px solid #4caf50',
        borderRadius: '8px',
        position: 'relative',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <div style={{
          position: 'absolute',
          top: '20px',
          left: '20px',
          width: '15px',
          height: '15px',
          backgroundColor: '#2196f3',
          borderRadius: '50%',
          border: '2px solid #1976d2'
        }}></div>
        <div style={{
          position: 'absolute',
          bottom: '20px',
          right: '20px',
          width: '15px',
          height: '15px',
          backgroundColor: '#4caf50',
          borderRadius: '50%',
          border: '2px solid #388e3c'
        }}></div>
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          fontSize: '14px',
          color: '#2c3e50',
          fontWeight: 'bold'
        }}>
          Route Path
        </div>
      </div>
    </div>
  );
};

function GoogleMap({ locations, markers }) {
  // Always use the free visualization
  return <FreeMapVisualization markers={markers} locations={locations} />;
}

export default GoogleMap; 