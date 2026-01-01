# Delivery App - Frontend Testing Dashboard

A simple HTML/JavaScript frontend for testing all microservices through the API Gateway.

## How to Use

1. **Open the HTML file:**
   - Simply open `index.html` in your web browser
   - Or use a local server (recommended):
     ```bash
     # Using Python
     python -m http.server 3000
     
     # Using Node.js (if you have http-server installed)
     npx http-server -p 3000
     ```
   - Then visit: `http://localhost:3000`

2. **Configure Gateway URL:**
   - The default gateway URL is `http://localhost:8089`
   - You can change it in the input field at the top if your gateway runs on a different port

3. **Test Services:**
   - **User Service**: Get all users or get a user by ID
   - **Restaurant Service**: Get all restaurants, get restaurant by ID, or get menu items
   - **Order Service**: Create orders, get order by ID, or get orders by user
   - **Delivery Service**: Create deliveries or get delivery by ID

## Features

- ✅ Clean, modern UI with gradient design
- ✅ Real-time API testing
- ✅ JSON response viewer
- ✅ Error handling and display
- ✅ Loading indicators
- ✅ Responsive design

## Testing Workflow

1. **Start all services** (Eureka, User Service, Restaurant Service, Order Service, Gateway)
2. **Open the frontend** in your browser
3. **Test in order:**
   - Get all users to see available user IDs
   - Get all restaurants to see available restaurant IDs
   - Create an order using valid user_id and restaurant_id
   - Create a delivery for the order
   - View enriched data in responses (user details, restaurant details, order details)

## Notes

- Make sure CORS is enabled in Django (already configured)
- All requests go through the Gateway at port 8089
- Responses show enriched data from inter-service communication
- Error messages will appear in red if something goes wrong

