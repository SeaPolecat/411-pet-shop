import logging
import os
import requests

from pets.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)

DOG_URL = os.getenv("DOG_URGL", "https://dog.ceo/api/breed/")
END_URL = "/images/random"

def get_image(breed) -> str:
    try:
        # Log the API request being initiated
        logger.info(f"Fetching random number from {DOG_URL}")

        # Make the GET request to the Dog CEO API with a timeout of 5 seconds
        response = requests.get(DOG_URL + breed + END_URL, timeout=5)
        
        # Parse the JSON response from the API
        data = response.json()

        # Raise an HTTPError if the status code indicates a failure (e.g., 4xx or 5xx)
        response.raise_for_status()

        # Check if the API returned a success status in the JSON payload
        if data.get("status") == "success":
            link = data.get("message", "").strip()  # Extract and clean the image URL
        else:
            # Log and raise an exception if the API reported an error status
            logger.error(f"Dog API returned error: {data}")
            raise Exception(f"Dog API returned error: {data}")

        # Validate that the link is a proper string (basic sanity check)
        try:
            image = str(link)
        except ValueError:
            # Log and raise an exception if the link is somehow invalid
            logger.error(f"Invalid response from dog api: {link}")
            raise ValueError(f"Invalid response from dog api: {link}")

        # Log the received image URL for debugging purposes
        logger.debug(f"Received pet image: {image}")
        logger.info(f"Successfully fetched pet image")

        return image  # Return the validated image URL

    # Handle timeout errors separately with a specific log and exception
    except requests.exceptions.Timeout:
        logger.error("Request to dog api timed out.")
        raise RuntimeError("Request to dog api timed out.")

    # Catch any other request-related exceptions and log them
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to dog api failed: {e}")
        raise RuntimeError(f"Request to dog api failed: {e}")
