# AI Model Comparison Sheet for Code Generation

#### Models Tested:
- GPT-4o (OpenAI)
- Claude Sonnet (Anthropic)
- Gemini Flash (Google)
- DeepSeek-R1:7B (Ollama – Local)

#### Comparison Criteria:
- Code Quality
- Ease of Use
- Speed / Latency

#### Legend for Ratings:
- ✅ Excellent
- 👍 Good
- ⚠️ Basic or Limited Support
- ❌ Not Supported


## Model-wise Evaluation
Below is a detailed evaluation of each model based on the comparison criteria:

## 1️⃣ Code Quality

**Prompt:**  
Write a Python class called `WeatherService` that fetches current weather data from an external API. The class should have a method `get_weather(city_name)` and handle errors like timeouts or bad responses. Use the `requests` library.

### GPT-4o Output:
```python
import requests

class WeatherService:
    def __init__(self, api_key, base_url="https://api.openweathermap.org/data/2.5/weather"):
        self.api_key = api_key
        self.base_url = base_url

    def get_weather(self, city_name):
        try:
            params = {
                'q': city_name,
                'appid': self.api_key,
                'units': 'metric'  # or 'imperial' for Fahrenheit
            }
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)

            data = response.json()
            weather = {
                'city': data.get('name'),
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
            return weather

        except requests.exceptions.Timeout:
            return {'error': 'Request timed out.'}
        except requests.exceptions.HTTPError as http_err:
            return {'error': f'HTTP error occurred: {http_err}'}
        except requests.exceptions.RequestException as req_err:
            return {'error': f'Request error occurred: {req_err}'}
        except KeyError:
            return {'error': 'Unexpected response format.'}

# Example usage:
# api_key = 'your_api_key_here'
# ws = WeatherService(api_key)
# print(ws.get_weather("London"))
```

### Claude Sonnet Output:
```python
import requests
import json
from typing import Dict, Optional
from requests.exceptions import RequestException, Timeout, ConnectionError, HTTPError


class WeatherServiceError(Exception):
    """Custom exception for weather service errors"""
    pass


class WeatherService:
    """
    A service class for fetching current weather data from an external API.
    
    This example uses OpenWeatherMap API. You'll need to:
    1. Sign up at https://openweathermap.org/api
    2. Get your free API key
    3. Replace 'YOUR_API_KEY' with your actual key
    """
    
    def __init__(self, api_key: str, timeout: int = 10):
        """
        Initialize the weather service.
        
        Args:
            api_key (str): Your API key for the weather service
            timeout (int): Request timeout in seconds (default: 10)
        """
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.timeout = timeout
    
    def get_weather(self, city_name: str) -> Dict:
        """
        Fetch current weather data for a given city.
        
        Args:
            city_name (str): Name of the city to get weather for
            
        Returns:
            Dict: Weather data including temperature, description, humidity, etc.
            
        Raises:
            WeatherServiceError: If there's an error fetching weather data
        """
        if not city_name or not city_name.strip():
            raise WeatherServiceError("City name cannot be empty")
        
        params = {
            'q': city_name.strip(),
            'appid': self.api_key,
            'units': 'metric'  # Use Celsius
        }
        
        try:
            response = requests.get(
                self.base_url, 
                params=params, 
                timeout=self.timeout
            )
            
            # Raise an exception for bad status codes
            response.raise_for_status()
            
            data = response.json()
            
            # Extract and return relevant weather information
            return {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'main': data['weather'][0]['main'],
                'wind_speed': data.get('wind', {}).get('speed', 'N/A'),
                'visibility': data.get('visibility', 'N/A')
            }
            
        except Timeout:
            raise WeatherServiceError(f"Request timed out after {self.timeout} seconds")
        
        except ConnectionError:
            raise WeatherServiceError("Failed to connect to weather service")
        
        except HTTPError as e:
            if e.response.status_code == 401:
                raise WeatherServiceError("Invalid API key")
            elif e.response.status_code == 404:
                raise WeatherServiceError(f"City '{city_name}' not found")
            else:
                raise WeatherServiceError(f"HTTP error {e.response.status_code}: {e.response.reason}")
        
        except json.JSONDecodeError:
            raise WeatherServiceError("Invalid response format from weather service")
        
        except KeyError as e:
            raise WeatherServiceError(f"Unexpected response structure: missing key {e}")
        
        except RequestException as e:
            raise WeatherServiceError(f"Request failed: {str(e)}")


# Example usage
if __name__ == "__main__":
    # Replace with your actual API key
    API_KEY = "YOUR_API_KEY"
    
    weather_service = WeatherService(API_KEY)
    
    try:
        # Test with a city
        weather_data = weather_service.get_weather("London")
        
        print(f"Weather in {weather_data['city']}, {weather_data['country']}:")
        print(f"Temperature: {weather_data['temperature']}°C (feels like {weather_data['feels_like']}°C)")
        print(f"Condition: {weather_data['description'].title()}")
        print(f"Humidity: {weather_data['humidity']}%")
        print(f"Wind Speed: {weather_data['wind_speed']} m/s")
        
    except WeatherServiceError as e:
        print(f"Error getting weather data: {e}")
    
    # Example of handling different types of errors
    cities_to_test = ["London", "InvalidCityName123", ""]
    
    for city in cities_to_test:
        try:
            print(f"\nTesting weather for: '{city}'")
            weather = weather_service.get_weather(city)
            print(f"✓ Success: {weather['temperature']}°C in {weather['city']}")
        except WeatherServiceError as e:
            print(f"✗ Error: {e}")
```

### Gemini Flash Output:
```Python
import requests

class WeatherService:
    """
    A service class to fetch current weather data from an external API.
    """

    def __init__(self, api_key: str):
        """
        Initializes the WeatherService with an API key.

        Args:
            api_key (str): Your API key for the weather service (e.g., OpenWeatherMap).
                           Replace with your actual API key.
        """
        self.api_key = api_key
        # Base URL for the weather API.
        # This example uses OpenWeatherMap's current weather endpoint.
        # You would replace this with the actual API endpoint you plan to use.
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city_name: str, timeout: int = 10) -> dict | None:
        """
        Fetches current weather data for a given city.

        Args:
            city_name (str): The name of the city for which to fetch weather data.
            timeout (int): The maximum number of seconds to wait for a response.

        Returns:
            dict | None: A dictionary containing weather data if successful,
                         otherwise None. The dictionary structure will depend
                         on the API response.
        """
        params = {
            "q": city_name,
            "appid": self.api_key,
            "units": "metric"  # Example: Use 'metric' for Celsius, 'imperial' for Fahrenheit
        }

        try:
            # Make the API request with a specified timeout
            response = requests.get(self.base_url, params=params, timeout=timeout)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            # Check if the response content type is JSON
            if 'application/json' in response.headers.get('Content-Type', ''):
                weather_data = response.json()
                print(f"Successfully fetched weather for {city_name}.")
                return weather_data
            else:
                print(f"Error: Received non-JSON response from API for {city_name}.")
                print(f"Response content: {response.text}")
                return None

        except requests.exceptions.HTTPError as e:
            # Handle HTTP errors (e.g., 404 Not Found, 401 Unauthorized, 500 Internal Server Error)
            print(f"HTTP error occurred while fetching weather for {city_name}: {e}")
            if e.response is not None:
                print(f"Status Code: {e.response.status_code}")
                print(f"Response Body: {e.response.text}")
            return None
        except requests.exceptions.ConnectionError as e:
            # Handle network-related errors (e.g., DNS failure, refused connection)
            print(f"Connection error occurred while fetching weather for {city_name}: {e}")
            return None
        except requests.exceptions.Timeout as e:
            # Handle request timeout error
            print(f"Timeout error occurred while fetching weather for {city_name}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            # Handle any other general requests exception
            print(f"An unexpected request error occurred while fetching weather for {city_name}: {e}")
            return None
        except ValueError as e:
            # Handle JSON decoding errors if response.json() fails
            print(f"Error decoding JSON response for {city_name}: {e}")
            return None
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")
            return None

# --- Example Usage ---
if __name__ == "__main__":
    # IMPORTANT: Replace "YOUR_API_KEY" with your actual API key from a weather service.
    # For OpenWeatherMap, you can get a free API key by signing up at:
    # https://openweathermap.org/api
    # It might take a few minutes for a new API key to become active.
    api_key = "YOUR_API_KEY" # Replace with your actual API key

    if api_key == "YOUR_API_KEY":
        print("Please replace 'YOUR_API_KEY' with your actual API key in the script.")
        print("You can get a free API key from OpenWeatherMap (https://openweathermap.org/api).")
    else:
        weather_service = WeatherService(api_key)

        print("\n--- Fetching weather for London ---")
        london_weather = weather_service.get_weather("London")
        if london_weather:
            print(f"City: {london_weather.get('name')}")
            print(f"Temperature: {london_weather['main']['temp']}°C")
            print(f"Description: {london_weather['weather'][0]['description'].capitalize()}")
            print(f"Humidity: {london_weather['main']['humidity']}%")
        else:
            print("Could not retrieve weather for London.")

        print("\n--- Fetching weather for a non-existent city ---")
        non_existent_city_weather = weather_service.get_weather("NonExistentCity12345")
        if non_existent_city_weather is None:
            print("As expected, could not retrieve weather for a non-existent city.")

        print("\n--- Fetching weather for a city with a very short timeout (will likely fail) ---")
        # This is for demonstration of timeout handling
        short_timeout_weather = weather_service.get_weather("Tokyo", timeout=0.001)
        if short_timeout_weather is None:
            print("As expected, request timed out for Tokyo with a very short timeout.")

        print("\n--- Fetching weather for Chennai ---")
        chennai_weather = weather_service.get_weather("Chennai")
        if chennai_weather:
            print(f"City: {chennai_weather.get('name')}")
            print(f"Temperature: {chennai_weather['main']['temp']}°C")
            print(f"Description: {chennai_weather['weather'][0]['description'].capitalize()}")
            print(f"Humidity: {chennai_weather['main']['humidity']}%")
        else:
            print("Could not retrieve weather for Chennai.")
```
### DeepSeek-R1:7B Output:
Thinking...
Okay, I need to write a Python class called WeatherService that fetches current weather data using the requests library. The class should have a method get_weather(city_name) and handle errors like timeouts 
or bad responses.

First, I'll start by outlining what the WeatherService class needs. It should have an __init__ method where I can set up any necessary configurations, like the API endpoint URL and the headers for 
authentication. Since the problem doesn't specify credentials, maybe using basic headers is enough for now.

Next, the get_weather method will take a city_name as input. This method will make a GET request to the API with the city name in the query parameters. I'll use requests.get() for this. 

Handling errors is crucial. I need to think about what exceptions might occur. The main ones are connection errors like timeouts or HTTP errors (e.g., 404, 5xx status codes). I should catch these and return 
appropriate error messages instead of letting exceptions propagate.

I'll also consider using try-except blocks around the request. For HTTP errors, I can check if the response.status_code is not in a successful range (like 200-299) and raise an exception or handle it 
gracefully.

Another thing to think about is encoding the city parameter properly. Since URLs are query strings, using urlencode from urllib.parse would be appropriate here.

I should also include retry logic for transient errors like HTTP timeouts. Using the requests session with retries might help, but since the problem specifies handling errors in general, maybe adding a 
limited number of retries within the method is sufficient.

Wait, but the get_weather method makes a single request. If I use a session, it would require changing the method to accept a session parameter or using a different approach. Maybe for simplicity, I'll handle 
each error within the method without switching to a session unless necessary.

I should also make sure that any exceptions from requests are caught and translated into meaningful messages. For example, if there's a timeout, respond with "Failed to fetch weather data due to network 
issue."

Let me think about potential issues. What if the API requires authentication? Since it wasn't specified, I'll assume basic headers are sufficient.

Now, putting it all together: The class initializes with the base URL and headers. The get_weather method constructs the URL with the city parameter, sends a GET request, handles HTTP errors, catches 
connection exceptions like timeout, and logs any errors that occur during the process.

I should also include logging to track when fetching weather fails. Maybe using try-except inside the method and logging each error case separately for clarity.

So, step by step:

1. Import necessary modules: requests, json, logging, and urllib.parse.
2. Define the WeatherService class with __init__ setting up URL and headers.
3. Implement get_weather method that constructs the query parameters, sends a GET request, handles errors, returns JSON data or error messages.
4. Add try-except blocks to catch HTTP errors, timeouts, etc., and handle them appropriately.

Wait, but how do I determine if it's an HTTP error? Because requests will raise exceptions for bad responses (status codes >= 500) automatically. So in the except block, I can check if it's a timeout or 
another exception type.

I should structure the code like this:

In get_weather:
- Use urlencode to create the query params.
- Make GET request with those params and headers.
- Wrap the request in try-except blocks for specific exceptions.
- If an HTTPError is raised (like status code not 2xx), catch it, log, return appropriate message.
- If a timeout occurs during the request, catch that as well.
- Any other exceptions are caught too, perhaps.

But wait, requests sessions can help with retries. Maybe I should use a session and set retries for transient errors like HTTP timeout or slow connections.

Hmm, but if the user is using get_weather directly, changing it to accept a session might complicate things. Alternatively, within get_weather, I could wrap the request in a retry decorator, but that's not 
standard practice.

Alternatively, perhaps just handle timeouts by setting proxies with retries, but maybe for simplicity, since the problem doesn't specify needing multiple attempts, I'll proceed without.

But to be thorough, perhaps using a session is better. So in the __init__, create an requests.Session(), and then use it in get_weather. That way, each request can have retries configured.

Wait, but the code provided earlier didn't do that. Let me check again.

In the initial code I wrote, get_weather uses requests.get() directly without a session. But if I switch to using a session with retries, perhaps via urllib.parse's request function or using sessions in a 
more structured way, it might be better for handling multiple issues like timeouts and transient errors.

But given time constraints, maybe just handle the timeout exception by catching it in try-except.

Putting all together:

Import logging.

In __init__: store the base URL (like 'http://api.openweathermap.org/data/2.5/weather'), headers with your API key if needed, but since it's not specified, perhaps use empty or placeholder.

In get_weather: create a query params string with city_name, encode it, send GET request, catch exceptions like requests.exceptions.RequestException which covers timeouts, HTTP errors except 4xx (since some 
status codes are allowed), and return appropriate messages.

Wait, but in the code example I provided earlier, there's a try-except for json decoding error. That might not be necessary if we handle all possible exceptions first.

So perhaps reorganize: first attempt to send request, catch any RequestException which includes timeouts, then check if response is okay, parse JSON, else return error message.

Wait, but the code I wrote before had:

try:
    response = requests.get(url)
except requests.exceptions.Timeout:
    print("Failed due to timeout")
except Exception as e:
    # Handle other errors
But that's not covering all possible exceptions. Using a general except could catch too much, so it's better to specifically handle the RequestException which includes timeouts.

Alternatively, in the except block after sending the request, check if response is None or raised an exception during get().

Wait, perhaps:

try:
    response = requests.get(url, params=params)
except requests.exceptions.RequestException as e:
    logging.error(f"Failed to fetch weather: {e}")
    return "Failed to fetch weather data. Please try again later."

But then we also need to handle the case where response.status_code is not 200-299. So maybe:

In the get_weather method, after making the request, check if it's successful.

So perhaps:

try:
    response = requests.get(url, params=params)
except requests.exceptions.RequestException as e:
    # Handle network issues
    logging.error(f"Request failed: {e}")
    return f"Failed to fetch weather data. Connection error."

Then, after getting the response, check if it's OK.

If not, handle HTTP errors:

if response.status_code >= 400:
    logging.error(f"HTTP Error: {response.status_code}. Response: {response.text}")
    return f"WeaponError occurred. Status code {response.status_code}."

Alternatively, perhaps combine these steps into a single try-except block that catches all possible exceptions.

But in the initial example, it was more specific with handling json decoding error and timeout separately. Maybe to be precise, handle each type of exception accordingly.

In any case, I'll proceed to write the code with try-except blocks for different types of errors: timeout, JSON parsing failure, generic HTTP errors, etc.

So in summary:

The class will have an __init__ that sets up the base URL and headers. The get_weather method constructs the query parameters, sends a GET request, handles exceptions like timeouts and HTTP errors, returns 
appropriate messages or JSON data on success.

I'll also make sure to log any errors so users can see what's going wrong.
...done thinking.

To solve this problem, we need to create a Python class called `WeatherService` that fetches current weather data from an external API. The class should handle various potential issues such as timeouts and 
invalid responses, providing appropriate error messages for each scenario.

### Approach
1. **Class Initialization**: The `WeatherService` class is initialized with the base URL of the API endpoint and a dictionary of headers required for authentication.
2. **Method Implementation**: The `get_weather` method takes a city name as input and constructs the API request to fetch weather data.
3. **Error Handling**: The method uses try-except blocks to handle different types of exceptions:
   - **Timeout Errors**: Explicitly caught and handled with an appropriate error message.
   - **JSON Parsing Failures**: Catched after requesting JSON-formatted responses and converted into meaningful messages.
   - **HTTP Errors**: Handled by checking the HTTP status code, providing specific error messages for non-successful responses.

### Solution Code

```python
import logging
import requests
from urllib.parse import urlencode

class WeatherService:
    def __init__(self, base_url: str, headers: dict):
        self.base_url = base_url
        self.headers = headers.copy()
    
    def get_weather(self, city_name: str) -> str:
        params = urlencode({'q': city_name})
        url = f"{self.base_url}?{params}"
        
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"Unexpected HTTP status code {response.status_code} received from API")
                return f"WeaponError occurred. Status code {response.status_code}."
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed for city: {city_name}. Exception message: {str(e)}")
            return f"Failed to fetch weather data for city '{city_name}'. Please try again later."
```

### Explanation
- **Initialization**: The `__init__` method sets up the base URL and headers required for accessing the API. This includes placeholders for any necessary authentication details.
- **Constructing the Request**: In the `get_weather` method, we construct a query parameter dictionary with the city name to fetch weather data. We then encode this into a string that is appended as a 
parameter in the API URL.
- **Handling Requests**: The method attempts to send a GET request. If successful and returns a 200 status code, it parses and returns the JSON response.
- **Error Handling**: The try-except block catches any network-related exceptions (like timeouts) and handles them with specific error messages. It also checks for non-200 HTTP status codes to handle API 
errors appropriately.

This approach ensures that the `WeatherService` class robustly handles various potential issues, providing clear and informative error messages while maintaining a clean and efficient code structure.

# Evaluation of Code Quality
### GPT-4o
##### Pros
- Simple and short
- Returns basic weather info
- Basic error handling (Timeout, HTTPError, etc.)
##### Cons:
- No custom exceptions
- Limited documentation
- Doesn’t differentiate HTTP status codes
- Not very scalable (no visibility, feels_like, etc.)

### Claude Sonnet
##### Pros
- Custom exception (WeatherServiceError)
- Detailed error handling (401, 404, etc.)
- Includes feels_like, visibility, pressure
- Clear docstrings, type hints
- Great for production-level code
##### Cons:
- Slightly verbose
- Doesn’t return None, always raises (could be debated as good practice)

### Gemini Flash
##### Pros
- Works out of the box
- Graceful fallback (returns None)
- Example usage tests different cities and errors
##### Cons:
- No custom exceptions
- Mixes business logic and I/O (print statements)
- Less reusable in larger apps or services
- Returns raw API response, not structured

### DeepSeek-R1:7B
##### Pros:
- Uses logging for errors
- Configurable headers
- Uses urlencode safely
##### Cons:
- Doesn’t handle specific HTTP errors (401, 404)
- No structured output (return str or raw json)
- Error message contains typo: "WeaponError" (!)
- Limited to generic RequestException
- Logging without fallback or clear user feedback

## 2️⃣ Ease of Use

**Prompt:**  
How can I write a function in JavaScript that checks if a string is a valid email? Explain it to a beginner with code and comments.

### GPT-4o Output:
**✅ What is a valid email?**
A valid email generally looks like:
`something@example.com`
Where:
something is the local part (username)
example.com is the domain name
There are more complex rules, but we'll start simple.

**✅ JavaScript Function to Check Email**
```Javascript
function isValidEmail(email) {
    // Regular Expression to test the email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // Test the email string against the regex
    return emailRegex.test(email);
}
```
**🧠 Explanation (Line-by-Line):**
```
function isValidEmail(email) {
```
- This defines a function called isValidEmail.
- It takes one parameter: email (a string you want to check).
```
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
```
We use a regular expression (also called regex) to define the pattern of a valid email.
Here's what this means:
- ^ and $ mean: start and end of the string.
- [^\s@]+ means: one or more characters that are not a space (\s) or @.
- @ is the required symbol in an email.
- \\. is the dot before the domain (we escape . with \ because it's special in regex).
- The second [^\s@]+ ensures the domain name is valid (e.g., com, org).
```
return emailRegex.test(email);
```
- .test(email) checks if the input string matches the regex pattern.
- Returns true if it's a valid email, false otherwise.

**✅ Example Usage**
```
console.log(isValidEmail("ayushi@example.com")); // true
console.log(isValidEmail("not-an-email"));       // false
console.log(isValidEmail("hello@world"));        // false (missing .com or domain extension)
```

**🔍 Optional: More Strict Email Validation**
If you want stricter checks, you can use a more complex regex. But for most cases, the one above is good and readable.

### Claude Sonnet Output:
```Javascript
// Simple email validation function
function isValidEmail(email) {
    // First, check if the email is a string and not empty
    if (typeof email !== 'string' || email.trim() === '') {
        return false;
    }
    
    // Remove any extra whitespace
    email = email.trim();
    
    // Basic checks for email structure
    // Must contain exactly one @ symbol
    const atCount = email.split('@').length - 1;
    if (atCount !== 1) {
        return false;
    }
    
    // Split the email into local part (before @) and domain part (after @)
    const parts = email.split('@');
    const localPart = parts[0];
    const domainPart = parts[1];
    
    // Check if both parts exist and aren't empty
    if (!localPart || !domainPart) {
        return false;
    }
    
    // Local part (before @) validation
    // Should be 1-64 characters long
    if (localPart.length < 1 || localPart.length > 64) {
        return false;
    }
    
    // Domain part (after @) validation
    // Should be 1-253 characters long
    if (domainPart.length < 1 || domainPart.length > 253) {
        return false;
    }
    
    // Domain must contain at least one dot
    if (!domainPart.includes('.')) {
        return false;
    }
    
    // Domain shouldn't start or end with a dot or hyphen
    if (domainPart.startsWith('.') || domainPart.endsWith('.') || 
        domainPart.startsWith('-') || domainPart.endsWith('-')) {
        return false;
    }
    
    // Check for valid characters using a simple regex
    // This allows letters, numbers, dots, hyphens, and underscores
    const validCharsRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    
    return validCharsRegex.test(email);
}

// More advanced version using a comprehensive regex pattern
function isValidEmailRegex(email) {
    // Check if email is a string
    if (typeof email !== 'string') {
        return false;
    }
    
    // Comprehensive email regex pattern
    // This pattern covers most common email formats
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    
    return emailRegex.test(email.trim());
}

// Test the functions with examples
console.log('=== Testing Basic Function ===');
console.log(isValidEmail('test@example.com'));        // true
console.log(isValidEmail('user.name@domain.co.uk'));  // true
console.log(isValidEmail('invalid-email'));           // false
console.log(isValidEmail('test@'));                   // false
console.log(isValidEmail('@domain.com'));             // false
console.log(isValidEmail('test@domain'));             // false
console.log(isValidEmail(''));                        // false

console.log('\n=== Testing Regex Function ===');
console.log(isValidEmailRegex('test@example.com'));        // true
console.log(isValidEmailRegex('user.name@domain.co.uk'));  // true
console.log(isValidEmailRegex('invalid-email'));           // false
console.log(isValidEmailRegex('test@'));                   // false
console.log(isValidEmailRegex('@domain.com'));             // false

// Example of how to use it in a real application
function validateUserEmail() {
    const userInput = 'user@example.com'; // This would come from a form input
    
    if (isValidEmail(userInput)) {
        console.log('✅ Email is valid!');
        // Proceed with form submission or other logic
    } else {
        console.log('❌ Please enter a valid email address');
        // Show error message to user
    }
}

// Run the example
validateUserEmail();
```
### Gemini Flash Output:
```Javascript
/**
 * Checks if a given string is a valid email address using a regular expression.
 * This function is designed to be beginner-friendly with extensive comments.
 *
 * @param {string} email - The string to be validated as an email address.
 * @returns {boolean} - True if the string is a valid email, false otherwise.
 */
function isValidEmail(email) {
  // --- Step 1: Basic Checks ---
  // First, let's make sure the input `email` is actually a string.
  // If it's not a string, it can't be a valid email.
  if (typeof email !== 'string') {
    console.error("Input must be a string. Received type:", typeof email);
    return false;
  }

  // If the string is empty, it's definitely not a valid email.
  if (email.trim() === '') {
    return false;
  }

  // --- Step 2: Understanding Regular Expressions (Regex) ---
  // A regular expression is a sequence of characters that defines a search pattern.
  // We use it here to define what a "valid email format" looks like.

  // The regex pattern for email validation:
  // This is a common pattern used to validate emails. Let's break it down:
  // ^                       - Asserts position at the start of the string.
  // [^\s@]+                 - Matches one or more characters that are NOT a whitespace (\s) or '@'.
  //                           This covers the "username" part before the @.
  // @                       - Matches the literal '@' character.
  // [^\s@]+                 - Matches one or more characters that are NOT a whitespace (\s) or '@'.
  //                           This covers the "domain name" part after the @ (e.g., "example").
  // \.                      - Matches the literal '.' character. We use '\.' because '.'
  //                           has a special meaning in regex (any character) so we escape it.
  // [^\s@]+                 - Matches one or more characters that are NOT a whitespace (\s) or '@'.
  //                           This covers the "top-level domain" part after the last dot (e.g., "com", "org").
  // $                       - Asserts position at the end of the string.

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  // --- Step 3: Testing the Email with the Regex ---
  // The `test()` method of a RegExp object executes a search for a match
  // between a regular expression and a specified string. Returns `true` or `false`.
  return emailRegex.test(email);
}

// --- Step 4: Examples of Usage ---

console.log("--- Email Validation Examples ---");

// Valid emails
console.log("test@example.com:", isValidEmail("test@example.com"));     // Should be true
console.log("john.doe@sub.domain.co.uk:", isValidEmail("john.doe@sub.domain.co.uk")); // Should be true
console.log("user123@mail.net:", isValidEmail("user123@mail.net"));     // Should be true

// Invalid emails
console.log("invalid-email:", isValidEmail("invalid-email"));         // Should be false (missing @ and domain)
console.log("user@.com:", isValidEmail("user@.com"));             // Should be false (missing domain part after @)
console.log("@domain.com:", isValidEmail("@domain.com"));         // Should be false (missing username)
console.log("user@domain:", isValidEmail("user@domain"));         // Should be false (missing top-level domain)
console.log("user@domain.c:", isValidEmail("user@domain.c"));       // Should be false (too short, but regex allows) - this regex is simple
console.log("user domain.com:", isValidEmail("user domain.com"));     // Should be false (contains space)
console.log("user@domain..com:", isValidEmail("user@domain..com"));   // Should be false (double dot)
console.log("", isValidEmail(""));                             // Should be false (empty string)
console.log(null, isValidEmail(null));                         // Should be false (not a string)
console.log(undefined, isValidEmail(undefined));               // Should be false (not a string)
console.log(123, isValidEmail(123));                           // Should be false (not a string)
```
This function isValidEmail takes a string and uses a regular expression to determine if it matches a typical email format. The comments inside the code explain what each part of the regular expression does, helping you understand how it checks for the "username@domain.tld" structure.

Keep in mind that email validation can be very complex due to the vast number of valid email formats. This regex is a good, commonly used starting point for most applications, but it's not exhaustive for every possible edge case allowed by RFCs.

### DeepSeek-R1:7B Output:
Thinking...
Okay, so the user previously asked about cleaning something vague, but then they started talking about writing a JavaScript function to check if a string is a valid email. Hmm, wait, looking back at their 
initial query, they just said "clean" without much context. Maybe they got confused when I listed options earlier.

Now, they’re asking for help with a specific problem: creating a JavaScript function to validate emails. They also want it explained like talking to a beginner, including code and comments. Alright, so first, 
I need to break down what makes an email valid.

I should start by outlining the basic rules of emails. Things like having a local part (the username) before the @ symbol, followed by a domain name after. Then, mention the dots between parts and ensure 
there's only one dot in certain places.

Next, think about possible edge cases—like invalid characters or missing parts. For example, an email without a domain wouldn’t be valid. Also, special characters like / or spaces might cause issues.

Then, I should explain that implementing all these rules manually would be complicated, so maybe using a regex is better. Wait, but regex for emails can get really long and might not cover everything 
reliably. Oh well, it's common to use regex for email validation even if it’s not perfect.

So, outline the steps of the function: checking each part against specific patterns. Maybe write pseudo-code first to make it clear before converting to actual JavaScript.

In the code, I'll include comments explaining each step. For example, checking the local part with a regex that allows letters, numbers, and some special characters but no spaces or dots. Then do the same for 
the domain name, making sure there's at least one number after the @ symbol before the TLD.

I should also handle case sensitivity by converting the email to lowercase in the function.

Finally, test the function with various examples to show how it works and highlight possible issues like invalid characters or missing parts.
...done thinking.

Sure! Let's write a JavaScript function that checks if a string is a valid email. Email validation involves checking the format of both the local part (before the `@` symbol) and the domain part (after the 
`@` symbol).

### Step-by-Step Explanation:
1. **Basic Structure**: A valid email has two main parts separated by an `@` symbol:
   - `[Local Part]@[Domain Part]`
2. **Local Part**:
   - Must contain only letters, numbers, dots, and certain special characters.
   - Cannot be empty.
3. **Domain Part**:
   - Also must contain only letters, numbers, dots, and certain special characters.
4. **Special Characters**:
   - The `@` symbol is used to separate the local part from the domain part.
   - The dot `.` can appear in both parts but cannot be the first or last character (e.g., `.example.com` or `example.com.`).
5. **Case Insensitivity**: Emails are case-insensitive, so we'll convert the input to lowercase for easier checking.

### Code with Comments:
```javascript
function isEmailValid(email) {
    // Convert email to lowercase for uniformity
    const lowerEmail = email.toLowerCase();
    
    // Check if local part and domain parts exist (are not empty)
    let isValid = true;
    isValid = isValid && lowerEmail.includes('@'); // Must have '@'
    
    // Split the email into local and domain parts
    let splitIndex = lowerEmail.indexOf('@');
    let localPart = lowerEmail.substring(0, splitIndex);
    let domainPart = lowerEmail.substring(splitIndex + 1);
    
    // Check if both parts are not empty
    isValid = isValid && localPart.length > 0 && domainPart.length > 0;
    
    // Regular expressions for validation
    // Local part pattern: allows letters, numbers, dots, and some special chars
    const localRegex = /^[a-z\d+-_\.]+$/;
    isValid = isValid && localRegex.test(localPart);
    
    // Domain part pattern: similar to local part but with additional checks
    const domainRegex = /^[a-z\d+-_.]+(\.[a-z\d+-_.]+)+$/;
    isValid = isValid && domainRegex.test(domainPart);
    
    return isValid;
}
```

### Explanation:
1. **Convert to Lowercase**: The email is converted to lowercase to handle case insensitivity.
2. **Check for '@' Symbol**: The email must contain an `@` symbol; otherwise, it's invalid.
3. **Split into Parts**: The email is split into the local part (before `@`) and domain part (after `@`).
4. **Local Part Validation**: Uses a regular expression to check if the local part contains only valid characters (letters, numbers, dots, underscores, hyphens, or periods).
5. **Domain Part Validation**: Uses another regular expression to validate the domain part, ensuring it follows similar rules and has at least one additional segment after the first.

### Example:
```javascript
console.log(isEmailValid("john@example.com")); // true
console.log(isEmailValid("john@exam@ple.com")); // false (multiple @ symbols)
console.log(isEmailValid("john.doe@example.co.uk")); // true
console.log(isEmailValid("john@examplecomuk")); // false (no dot in domain part)
```

### Edge Cases:
- `"@example.com"` → Invalid (empty local part)
- `"john@.com"` → Invalid (dot as first character of domain part)
- `"john@exmple.co.uk"` → Valid
- `"John@Doe@example.com"` → Valid

This function provides a basic validation, but real-world email rules are more complex. You might want to expand the regex patterns or add additional checks based on specific requirements.

# Evaluation of Ease of Use
### GPT-4o
##### Pros
- Very beginner-friendly: breaks down the regex simply.
- Easy to copy-paste and use.
- Highlights both practical use and learning.
- Visual format (✅, 🧠, 🔍) helps readability.
##### Cons:
- A bit simplistic: doesn’t handle edge cases like empty strings, null, etc.
- Regex explained, but not deeply.

### Claude Sonnet
##### Pros
- Strong coverage of edge cases (e.g., length checks, split validation).
- Explains structure-based logic, not just regex.
- Beginner-safe with minimal surprises.
##### Cons:
- Long and a bit overwhelming for beginners.
- Some checks might seem redundant with the regex that follows.
- Slightly mixes “simple” and “advanced” ideas in the same function.

### Gemini Flash
##### Pros
- Very thoughtful explanation of regex (e.g., ^, $, \s).
- Examples clearly show what passes and fails.
- Handles type checking (e.g., typeof email !== 'string').
##### Cons:
- Slightly verbose—comments may be overkill for casual learners.

### DeepSeek-R1:7B
##### Pros:
- Attempts a step-by-step beginner explanation.
- Covers both logic and regex.
- Includes lowercase conversion, which is nice.
##### Cons:
- Cluttered intro (leftover "thinking..." notes).
- Regex used in domain check is less standard ((\.[a-z\d+-_.]+)+ might confuse beginners).
- Misses some beginner-friendly real-world guidance.

## 3️⃣ Speed / Latency

**Prompt:**  
Create a function in Java that reverses a string.

### Response Time Comparison

| Model           | Response Time |
|----------------|----------------|
| GPT-4o          | 6 seconds   |
| Gemini Flash    | 7 seconds   |
| Claude Sonnet   | 14 seconds  |
| DeepSeek-R1:7B  | 56 seconds  |

**Comments:**
- **GPT-4o** and **Gemini Flash** responded fastest, making them great for real-time interaction.
- **Claude Sonnet** was moderately slower but still acceptable.
- **DeepSeek-R1:7B** had the slowest response due to local inference limitations, which is expected for open-source models run on limited hardware.

# AI Model Comparison Summary

| Model         | Code Quality        | Ease of Use         | Speed/Latency       | Time   | Comments                                                                 |
|---------------|---------------------|----------------------|----------------------|--------|--------------------------------------------------------------------------|
| GPT-4o        | 👍 Good             | ✅ Excellent         | ✅ Excellent         | 6 sec  | Simple, clean, great for beginners; Fastest model                        |
| Claude Sonnet | ✅ Excellent        | ⚠️ Basic             | ⚠️ Basic             | 14 sec | Well-structured, production-ready, but slightly overwhelming             |
| Gemini        | 👍 Good             | 👍 Good              | 👍 Good              | 7 sec  | Good for learning, not reusable; Good speed                              |
| DeepSeek-R1   | ⚠️ Basic            | ⚠️ Basic             | ❌ Not Supported     | 56 sec | Buggy design, cluttered output; Very slow                                |
