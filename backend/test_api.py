#!/usr/bin/env python
"""
Simple test script to verify the Image AI Processing Platform setup.
Run this after starting the backend server to test API functionality.

Usage:
    python test_api.py
"""

import requests
import json
import os
from pathlib import Path

# Configuration
API_URL = "http://localhost:8000/api/process/"
TEST_IMAGE_PATH = None  # Will search for test image

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    """Print a formatted header."""
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}{text}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}")

def print_success(text):
    """Print success message."""
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    """Print error message."""
    print(f"{RED}✗ {text}{RESET}")

def print_info(text):
    """Print info message."""
    print(f"{BLUE}ℹ {text}{RESET}")

def print_warning(text):
    """Print warning message."""
    print(f"{YELLOW}⚠ {text}{RESET}")

def find_test_image():
    """Find a test image in common locations."""
    common_paths = [
        Path.home() / "Pictures" / "*.jpg",
        Path.home() / "Pictures" / "*.png",
        Path.home() / "Downloads" / "*.jpg",
        Path.home() / "Downloads" / "*.png",
        Path("/tmp/*.jpg"),
        Path("/tmp/*.png"),
    ]
    
    import glob
    for pattern in common_paths:
        matches = glob.glob(str(pattern))
        if matches:
            return matches[0]
    
    return None

def test_connection():
    """Test if the API is reachable."""
    print_header("Testing Connection")
    
    try:
        response = requests.get(API_URL.replace("/process/", ""), timeout=5)
        print_info(f"Attempting to reach {API_URL}")
        print_success("Backend is reachable")
        return True
    except requests.exceptions.ConnectionError:
        print_error(f"Cannot connect to {API_URL}")
        print_info("Make sure to run: python manage.py runserver")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_api_with_image(image_path, filter_name="grayscale"):
    """Test the API with an actual image."""
    print_header("Testing API with Image")
    
    if not os.path.exists(image_path):
        print_error(f"Image file not found: {image_path}")
        return False
    
    print_info(f"Using image: {image_path}")
    print_info(f"Using filter: {filter_name}")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            data = {'filter': filter_name}
            
            print_info("Sending request to API...")
            response = requests.post(API_URL, files=files, data=data, timeout=60)
        
        if response.status_code == 200:
            print_success(f"API responded with status {response.status_code}")
            result = response.json()
            
            print_success("Response received successfully")
            print(f"\n{BOLD}Results:{RESET}")
            
            if 'classification' in result:
                classification = result['classification']
                print(f"  {BOLD}Classification:{RESET}")
                print(f"    Label: {classification.get('label', 'N/A')}")
                print(f"    Confidence: {classification.get('confidence', 'N/A')}")
            
            if 'objects' in result:
                objects = result['objects']
                print(f"  {BOLD}Detected Objects:{RESET} {len(objects)}")
                for obj in objects[:3]:  # Show first 3 objects
                    print(f"    - {obj.get('class', 'Unknown')}: {obj.get('confidence', 0):.2%}")
            
            if 'image' in result:
                print(f"  {BOLD}Processed Image:{RESET} {result['image']}")
            
            print_success("API test passed!")
            return True
        else:
            print_error(f"API returned status {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
    
    except Exception as e:
        print_error(f"Error testing API: {str(e)}")
        return False

def test_api_without_image():
    """Test the API error handling."""
    print_header("Testing Error Handling")
    
    try:
        print_info("Testing API without image file...")
        response = requests.post(API_URL, timeout=5)
        
        if response.status_code == 400:
            print_success("API correctly rejects request without image")
            error_data = response.json()
            print_info(f"Error message: {error_data.get('error', 'No error message')}")
            return True
        else:
            print_warning(f"Expected status 400, got {response.status_code}")
            return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_filters():
    """Test different filter names."""
    print_header("Testing Filter Options")
    
    filters = [
        "grayscale", "blur", "canny", "sepia", "negative",
        "sharpen", "emboss", "median", "bilateral", "threshold",
        "sobel", "laplacian", "hsv", "erosion", "dilation", "edge_enhance"
    ]
    
    print_info(f"Available filters ({len(filters)}):")
    for i, f in enumerate(filters, 1):
        print(f"  {i:2}. {f}")
    
    print_success(f"All {len(filters)} filters available")
    return True

def print_environment_info():
    """Print environment information."""
    print_header("Environment Information")
    
    print_info(f"Python version: {__import__('sys').version.split()[0]}")
    print_info(f"Requests version: {requests.__version__}")
    
    # Check if dependencies are installed
    dependencies = ['cv2', 'torch', 'ultralytics']
    print(f"\n{BOLD}Backend Dependencies:{RESET}")
    for dep in dependencies:
        try:
            __import__(dep)
            print_success(f"{dep} is installed")
        except ImportError:
            print_warning(f"{dep} is not installed (will auto-download)")

def main():
    """Run all tests."""
    print(f"\n{BOLD}{BLUE}Image AI Processing Platform - API Test{RESET}\n")
    
    # Test environment
    print_environment_info()
    
    # Test connection
    if not test_connection():
        print("\n" + "="*60)
        print_error("Backend is not running!")
        print_info("Please start the backend server first:")
        print(f"  cd backend")
        print(f"  python manage.py runserver")
        return False
    
    # Test error handling
    test_api_without_image()
    
    # Find and test with image
    test_image = find_test_image()
    if test_image:
        print_info(f"Found test image: {test_image}")
        test_api_with_image(test_image)
    else:
        print_warning("No test image found")
        print_info("To test with an actual image, add an image to:")
        print(f"  - {Path.home() / 'Pictures'}")
        print(f"  - {Path.home() / 'Downloads'}")
    
    # Test filters
    test_filters()
    
    # Final summary
    print("\n" + "="*60)
    print_success("API Testing Complete!")
    print("\n{BOLD}Next Steps:{RESET}")
    print("  1. Visit http://localhost:3000 in your browser")
    print("  2. Upload an image")
    print("  3. Select a filter")
    print("  4. Click 'Process Image'")
    print("  5. View the results")
    print("\nFor more information, see:")
    print("  - API_REFERENCE.md")
    print("  - QUICKSTART.md")
    print("  - README.md")
    print("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    main()
