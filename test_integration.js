// Simple test script to verify backend integration
const API_URL = "http://localhost:8000";

async function testAPI() {
  console.log("🧪 Testing Backend Integration...\n");

  try {
    // Test 1: Health check
    console.log("1. Testing health endpoint...");
    const healthResponse = await fetch(`${API_URL}/health`);
    const healthData = await healthResponse.json();
    console.log("✅ Health check:", healthData.success ? "PASS" : "FAIL");

    // Test 2: Route points
    console.log("\n2. Testing route points endpoint...");
    const routeResponse = await fetch(
      `${API_URL}/route-points?fromCity=Los%20Angeles&toCity=San%20Francisco`
    );
    const routeData = await routeResponse.json();
    console.log("✅ Route points:", routeData.success ? "PASS" : "FAIL");
    if (routeData.success) {
      console.log(
        "   Start:",
        routeData.data.start.city,
        `(${routeData.data.start.lat}, ${routeData.data.start.lng})`
      );
      console.log(
        "   End:",
        routeData.data.end.city,
        `(${routeData.data.end.lat}, ${routeData.data.end.lng})`
      );
    }

    // Test 3: Places along route
    console.log("\n3. Testing places endpoint...");
    const placesResponse = await fetch(
      `${API_URL}/places?fromCity=Los%20Angeles&toCity=San%20Francisco`
    );
    const placesData = await placesResponse.json();
    console.log("✅ Places:", placesData.success ? "PASS" : "FAIL");
    if (placesData.success) {
      console.log(`   Found ${placesData.data.attractions.length} attractions`);
      console.log("   Sample attractions:");
      placesData.data.attractions.slice(0, 3).forEach((attraction, index) => {
        console.log(`   ${index + 1}. ${attraction.name} (${attraction.town})`);
      });
    }

    // Test 4: Route optimization
    console.log("\n4. Testing route optimization...");
    if (placesData.success && placesData.data.attractions.length >= 2) {
      const locationIds = [0, 1]; // Use first two attractions
      const optimizeResponse = await fetch(`${API_URL}/optimize`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ location_ids: locationIds }),
      });
      const optimizeData = await optimizeResponse.json();
      console.log(
        "✅ Route optimization:",
        optimizeData.success ? "PASS" : "FAIL"
      );
      if (optimizeData.success) {
        console.log(
          "   Optimized route:",
          optimizeData.data.optimized_route.location_names
        );
        console.log(
          "   Total distance:",
          optimizeData.data.optimized_route.total_distance
        );
      }
    }

    console.log("\n🎉 All tests completed!");
    console.log("\n📝 Next steps:");
    console.log(
      "1. Make sure the backend is running: cd backend && python3 start_api.py"
    );
    console.log("2. Start the frontend: cd route_optimizer_fe && npm run dev");
    console.log("3. Open http://localhost:5173 in your browser");
    console.log('4. Try searching for "Los Angeles" to "San Francisco"');
  } catch (error) {
    console.error("❌ Test failed:", error.message);
    console.log("\n🔧 Troubleshooting:");
    console.log("1. Make sure the backend is running on port 8000");
    console.log("2. Check if there are any CORS issues");
    console.log("3. Verify the API endpoints are working");
  }
}

// Run the test
testAPI();
