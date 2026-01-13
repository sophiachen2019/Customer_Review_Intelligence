import ocr_utils
from PIL import Image
import io

# Create a dummy image for testing if no real image is available
# In a real scenario, we'd load a file. Here we create a simple blank image 
# just to test the API connection, though Gemini might complain it's not a review.
# Ideally, the user should provide a path to a real image.

def create_dummy_image():
    img = Image.new('RGB', (100, 100), color = 'white')
    return img

def test_ocr():
    print("Testing OCR extraction...")
    try:
        # Try to load a real image if it exists, otherwise use dummy
        # For this automated test, we'll use a dummy but expect a specific response or error
        # that confirms the API was reached.
        img = create_dummy_image()
        
        print("Sending image to Gemini...")
        data = ocr_utils.extract_review_data(img)
        
        print("Response received:")
        print(data)
        
        if "error" in data:
            print("Test failed (API Error):", data['error'])
        else:
            print("Test passed (Data received)")
            
    except Exception as e:
        print(f"Test failed with exception: {e}")

if __name__ == "__main__":
    # This test requires the API key to be set in environment variables 
    # or secrets.toml for it to work fully.
    test_ocr()
