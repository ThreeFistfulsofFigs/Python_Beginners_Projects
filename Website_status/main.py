# ============================================================================
# WEBSITE STATUS CHECKER TOOL
# ============================================================================
# A comprehensive tool for monitoring website availability and performance.
# Provides detailed HTTP response analysis including status codes, headers,
# server information, and response times for website health monitoring
# and troubleshooting purposes.
# ============================================================================

# Import required libraries
import requests  # For HTTP requests and web communication
from requests import Response, RequestException  # For type hints and exception handling
from requests.structures import CaseInsensitiveDict  # For header data structure
from typing import Dict, List, Optional, Tuple, Any  # For type annotations
import time  # For timestamp and timing operations
from urllib.parse import urlparse  # For URL validation and parsing

# ============================================================================
# CONFIGURATION CONSTANTS
# ============================================================================
# HTTP request configuration
DEFAULT_TIMEOUT = 30  # Default request timeout in seconds
DEFAULT_USER_AGENT = "Website-Status-Checker/1.0"  # Custom user agent string
MAX_REDIRECTS = 5  # Maximum number of redirects to follow

# Display formatting constants
SEPARATOR_LINE = "-" * 60
SECTION_HEADER = "=" * 70
SUCCESS_INDICATOR = "✓"
ERROR_INDICATOR = "✗"
WARNING_INDICATOR = "⚠"

# Status code categories for classification
STATUS_CODE_CATEGORIES = {
    'informational': range(100, 200),
    'success': range(200, 300),
    'redirection': range(300, 400),
    'client_error': range(400, 500),
    'server_error': range(500, 600)
}


# ============================================================================
# URL VALIDATION AND PREPROCESSING
# ============================================================================
def validate_url(url: str) -> bool:
    """
    Validates if the provided string is a properly formatted URL.

    Args:
        url (str): The URL string to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    try:
        # URL PARSING AND VALIDATION
        # Parse the URL to check its components
        parsed_url = urlparse(url.strip())

        # SCHEME VALIDATION
        # Ensure URL has proper HTTP/HTTPS scheme
        if not parsed_url.scheme or parsed_url.scheme not in ['http', 'https']:
            return False

        # NETLOC VALIDATION
        # Ensure URL has a valid network location (domain)
        if not parsed_url.netloc:
            return False

        return True

    except Exception:
        return False


def normalize_url(url: str) -> str:
    """
    Normalizes and cleans the URL for consistent processing.

    Args:
        url (str): The URL to normalize.

    Returns:
        str: The normalized URL string.
    """
    # URL CLEANING
    # Remove leading/trailing whitespace
    cleaned_url = url.strip()

    # SCHEME ADDITION
    # Add HTTP scheme if missing (assuming HTTP for basic connectivity test)
    if not cleaned_url.startswith(('http://', 'https://')):
        cleaned_url = 'https://' + cleaned_url

    return cleaned_url


# ============================================================================
# STATUS CODE ANALYSIS
# ============================================================================
def analyze_status_code(status_code: int) -> Tuple[str, str, str]:
    """
    Analyzes HTTP status code and provides category, description, and indicator.

    Args:
        status_code (int): The HTTP response status code.

    Returns:
        Tuple[str, str, str]: Category, description, and visual indicator.
    """
    # STATUS CODE CATEGORIZATION
    for category, code_range in STATUS_CODE_CATEGORIES.items():
        if status_code in code_range:
            # CATEGORY-SPECIFIC ANALYSIS
            if category == 'success':
                return category, "Request successful", SUCCESS_INDICATOR
            elif category == 'redirection':
                return category, "Redirection required", WARNING_INDICATOR
            elif category == 'client_error':
                return category, "Client error occurred", ERROR_INDICATOR
            elif category == 'server_error':
                return category, "Server error occurred", ERROR_INDICATOR
            elif category == 'informational':
                return category, "Informational response", WARNING_INDICATOR

    # UNKNOWN STATUS CODE
    return "unknown", "Unknown status code", ERROR_INDICATOR


# ============================================================================
# HEADER ANALYSIS AND EXTRACTION
# ============================================================================
def extract_server_info(headers: CaseInsensitiveDict) -> Dict[str, str]:
    """
    Extracts relevant server and response information from HTTP headers.

    Args:
        headers (CaseInsensitiveDict): HTTP response headers.

    Returns:
        Dict[str, str]: Dictionary containing extracted server information.
    """
    # SERVER INFORMATION EXTRACTION
    server_info = {
        'server': headers.get('Server', 'Unknown'),
        'content_type': headers.get('Content-Type', 'Unknown'),
        'content_length': headers.get('Content-Length', 'Unknown'),
        'last_modified': headers.get('Last-Modified', 'Unknown'),
        'cache_control': headers.get('Cache-Control', 'Unknown'),
        'connection': headers.get('Connection', 'Unknown'),
        'encoding': headers.get('Content-Encoding', 'Unknown')
    }

    return server_info


def analyze_security_headers(headers: CaseInsensitiveDict) -> Dict[str, bool]:
    """
    Analyzes the presence of important security headers.

    Args:
        headers (CaseInsensitiveDict): HTTP response headers.

    Returns:
        Dict[str, bool]: Dictionary indicating presence of security headers.
    """
    # SECURITY HEADER CHECKLIST
    security_headers = {
        'X-Frame-Options': 'X-Frame-Options' in headers,
        'X-Content-Type-Options': 'X-Content-Type-Options' in headers,
        'X-XSS-Protection': 'X-XSS-Protection' in headers,
        'Strict-Transport-Security': 'Strict-Transport-Security' in headers,
        'Content-Security-Policy': 'Content-Security-Policy' in headers,
        'Referrer-Policy': 'Referrer-Policy' in headers
    }

    return security_headers


# ============================================================================
# HTTP REQUEST EXECUTION
# ============================================================================
def perform_http_request(url: str) -> Optional[Response]:
    """
    Performs HTTP GET request with comprehensive error handling and configuration.

    Args:
        url (str): The URL to send the request to.

    Returns:
        Optional[Response]: Response object if successful, None if failed.

    Raises:
        RequestException: Various HTTP-related exceptions.
    """
    try:
        # REQUEST CONFIGURATION
        # Set up request parameters for optimal performance and compatibility
        request_config = {
            'timeout': DEFAULT_TIMEOUT,
            'allow_redirects': True,
            'headers': {
                'User-Agent': DEFAULT_USER_AGENT,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
        }

        # HTTP REQUEST EXECUTION
        # Perform GET request with configured parameters
        response = requests.get(url, **request_config)

        return response

    # SPECIFIC ERROR HANDLING
    except requests.exceptions.Timeout:
        print(f"{ERROR_INDICATOR} Request timeout after {DEFAULT_TIMEOUT} seconds")
        return None
    except requests.exceptions.ConnectionError:
        print(f"{ERROR_INDICATOR} Connection error - Unable to reach server")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"{ERROR_INDICATOR} HTTP error occurred: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"{ERROR_INDICATOR} Request exception: {e}")
        return None
    except Exception as e:
        print(f"{ERROR_INDICATOR} Unexpected error during request: {e}")
        return None


# ============================================================================
# RESPONSE ANALYSIS AND DISPLAY
# ============================================================================
def display_basic_info(url: str, response: Response) -> None:
    """
    Displays basic website status information.

    Args:
        url (str): The URL that was checked.
        response (Response): The HTTP response object.
    """
    # BASIC INFORMATION EXTRACTION
    status_code = response.status_code
    response_time = response.elapsed.total_seconds()

    # STATUS CODE ANALYSIS
    category, description, indicator = analyze_status_code(status_code)

    # BASIC INFO DISPLAY
    print(f"\n{SECTION_HEADER}")
    print(f"WEBSITE STATUS CHECK RESULTS")
    print(f"{SECTION_HEADER}")
    print(f"URL                : {url}")
    print(f"Status Code        : {status_code} {indicator} ({description})")
    print(f"Response Time      : {response_time:.3f} seconds")
    print(f"Status Category    : {category.title()}")


def display_server_info(response: Response) -> None:
    """
    Displays detailed server and content information.

    Args:
        response (Response): The HTTP response object.
    """
    # SERVER INFORMATION EXTRACTION
    headers = response.headers
    server_info = extract_server_info(headers)

    # SERVER INFO DISPLAY
    print(f"\n{SEPARATOR_LINE}")
    print("SERVER INFORMATION")
    print(f"{SEPARATOR_LINE}")

    for key, value in server_info.items():
        display_key = key.replace('_', ' ').title()
        print(f"{display_key:18}: {value}")


def display_security_analysis(response: Response) -> None:
    """
    Displays security header analysis.

    Args:
        response (Response): The HTTP response object.
    """
    # SECURITY ANALYSIS
    security_headers = analyze_security_headers(response.headers)
    present_headers = sum(security_headers.values())
    total_headers = len(security_headers)

    # SECURITY INFO DISPLAY
    print(f"\n{SEPARATOR_LINE}")
    print(f"SECURITY HEADERS ANALYSIS ({present_headers}/{total_headers} present)")
    print(f"{SEPARATOR_LINE}")

    for header, present in security_headers.items():
        indicator = SUCCESS_INDICATOR if present else ERROR_INDICATOR
        status = "Present" if present else "Missing"
        print(f"{indicator} {header:25}: {status}")


# ============================================================================
# COMPREHENSIVE STATUS CHECK
# ============================================================================
def check_status(url: str) -> Optional[Dict[str, Any]]:
    """
    Performs comprehensive website status check with detailed analysis.

    Args:
        url (str): The URL to check for status and performance.

    Returns:
        Optional[Dict[str, Any]]: Dictionary containing all check results, None if failed.
    """
    # URL VALIDATION AND NORMALIZATION
    if not validate_url(url):
        print(f"{ERROR_INDICATOR} Invalid URL format: {url}")
        return None

    normalized_url = normalize_url(url)

    # HTTP REQUEST EXECUTION
    print(f"Checking website status for: {normalized_url}")
    start_time = time.time()

    response = perform_http_request(normalized_url)

    if response is None:
        print(f"{ERROR_INDICATOR} Failed to get response from: {normalized_url}")
        return None

    # COMPREHENSIVE ANALYSIS
    try:
        # BASIC INFORMATION DISPLAY
        display_basic_info(normalized_url, response)

        # SERVER INFORMATION DISPLAY
        display_server_info(response)

        # SECURITY ANALYSIS DISPLAY
        display_security_analysis(response)

        # RESULTS COMPILATION
        # Compile all results into a structured format for programmatic use
        results = {
            'url': normalized_url,
            'status_code': response.status_code,
            'response_time': response.elapsed.total_seconds(),
            'server_info': extract_server_info(response.headers),
            'security_headers': analyze_security_headers(response.headers),
            'headers': dict(response.headers),
            'success': 200 <= response.status_code < 300
        }

        print(f"\n{SEPARATOR_LINE}")
        print(f"{SUCCESS_INDICATOR} Status check completed successfully")
        print(f"{SEPARATOR_LINE}")

        return results

    except Exception as e:
        print(f"{ERROR_INDICATOR} Error during response analysis: {e}")
        return None


# ============================================================================
# BATCH PROCESSING FUNCTIONALITY
# ============================================================================
def check_multiple_urls(urls: List[str]) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Performs status checks on multiple URLs with batch processing.

    Args:
        urls (List[str]): List of URLs to check.

    Returns:
        Dict[str, Optional[Dict[str, Any]]]: Results for each URL.
    """
    results = {}

    print(f"\n{SECTION_HEADER}")
    print(f"BATCH STATUS CHECK - PROCESSING {len(urls)} URLs")
    print(f"{SECTION_HEADER}")

    for index, url in enumerate(urls, 1):
        print(f"\n[{index}/{len(urls)}] Processing: {url}")
        results[url] = check_status(url)

        # BRIEF PAUSE BETWEEN REQUESTS
        # Avoid overwhelming target servers
        if index < len(urls):
            time.sleep(1)

    # BATCH SUMMARY
    successful_checks = sum(1 for result in results.values() if result is not None)
    print(f"\n{SECTION_HEADER}")
    print(f"BATCH PROCESSING COMPLETE")
    print(f"Successful checks: {successful_checks}/{len(urls)}")
    print(f"{SECTION_HEADER}")

    return results


# ============================================================================
# MAIN PROGRAM LOGIC
# ============================================================================
def main() -> None:
    """
    Main function to demonstrate website status checking functionality.

    Performs status check on a sample URL and displays comprehensive results.
    Can be easily modified to accept user input or process multiple URLs.
    """
    # SAMPLE URL FOR DEMONSTRATION
    # TradingView chart URL for cryptocurrency market analysis
    sample_url = "https://www.tradingview.com/chart/1jYHIDFA/?symbol=CRYPTOCAP%3ATOTAL2"

    try:
        # SINGLE URL STATUS CHECK
        print("Website Status Checker - Starting analysis...")
        results = check_status(sample_url)

        # RESULTS PROCESSING
        if results:
            print(f"\n{SUCCESS_INDICATOR} Analysis completed successfully")
            # Results dictionary can be used for further processing
            # Such as logging, alerting, or integration with monitoring systems
        else:
            print(f"\n{ERROR_INDICATOR} Analysis failed")

    # COMPREHENSIVE ERROR HANDLING
    except KeyboardInterrupt:
        print(f"\n\n{WARNING_INDICATOR} Status check interrupted by user")
    except Exception as e:
        print(f"\n{ERROR_INDICATOR} Unexpected error during status check: {e}")


# ============================================================================
# INTERACTIVE MODE FUNCTIONALITY
# ============================================================================
def interactive_mode() -> None:
    """
    Provides interactive mode for user-input URL checking.

    Allows users to input URLs manually for real-time status checking.
    """
    print(f"{SECTION_HEADER}")
    print("INTERACTIVE WEBSITE STATUS CHECKER")
    print(f"{SECTION_HEADER}")
    print("Enter URLs to check (type 'quit' to exit)")

    while True:
        # USER INPUT COLLECTION
        user_url = input(f"\nEnter URL to check: ").strip()

        # EXIT CONDITION
        if user_url.lower() in ['quit', 'exit', 'q']:
            print("Exiting interactive mode.")
            break

        # EMPTY INPUT HANDLING
        if not user_url:
            print("Please enter a valid URL.")
            continue

        # SINGLE URL CHECK
        check_status(user_url)


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    # EXECUTION MODE SELECTION
    # Default: Run with sample URL
    # Comment out main() and uncomment interactive_mode() for interactive mode

    #main()  # Single URL check with sample URL
    interactive_mode()  # Uncomment for interactive URL checking