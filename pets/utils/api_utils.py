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
        logger.info(f"Fetching random number from {DOG_URL}")

        response = requests.get(DOG_URL + breed + END_URL, timeout=5)
        data = response.json()

        # Check if the request was successful
        response.raise_for_status()

        if data["status"] == "success":
            link = data["message"].strip()
        else:
            raise Exception(f"Dog API returned error: {data}")

        

        try:
            image = str(link)
        except ValueError:
            logger.error(f"Invalid response from dog api: {link}")
            raise ValueError(f"Invalid response from dog api: {link}")

        logger.debug(f"Received pet image: {image}")
        logger.info(f"Successfully fetched pet image")

        return image

    except requests.exceptions.Timeout:
        logger.error("Request to dog api timed out.")
        raise RuntimeError("Request to dog api timed out.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Request to dog api failed: {e}")
        raise RuntimeError(f"Request to dog api failed: {e}")
