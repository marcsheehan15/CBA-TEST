import os

import pytest
import logging

import requests

from petstore_tests.api_client import APIClient
from petstore_tests.models import Pet

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

client = APIClient()

# URL to the image stored on the internet
IMAGE_URL = "https://media.istockphoto.com/id/874937848/photo/many-different-breeds-of-dogs-on-the-grass.jpg?s=1024x1024&w=is&k=20&c=13twYZwN8UcmJK5dqDPTnjxfWPQ2ed5854OZVceVpBk="
@pytest.fixture
def sample_pet():
    return Pet(
        name="Buddy",
        photoUrls=["https://example.com/photo.jpg"],
        status="sold"
    )


def test_upload_pet_image(sample_pet):
    logger.info("Starting test_upload_pet_image")

    # Download the image from the internet
    response = requests.get(IMAGE_URL)
    if response.status_code == 200:
        with open("sample_image.jpg", 'wb') as file:
            file.write(response.content)
    else:
        logger.error(f"Failed to download image. Status code: {response.status_code}")
        pytest.fail("Failed to download image from the internet.")

    pet_id = 123  # This would be the ID of the pet you want to upload the image for

    with open("sample_image.jpg", 'rb') as image_file:
        upload_response = client.post(f"/pet/{pet_id}/uploadImage", files={'file': image_file})

    logger.info(f"Received response: {upload_response}")

    # Validate the response
    assert upload_response.get('code') == 200
    assert 'message' in upload_response

    # Clean up
    os.remove("sample_image.jpg")

    logger.info("test_upload_pet_image passed")

def test_get_pet_by_id(sample_pet):
    logger.info("Starting test_get_pet_by_id")
    created_pet = client.post("/pet", json=sample_pet.dict())
    pet_id = created_pet['id']
    logger.info(f"Created pet with ID: {pet_id}")

    response = client.get(f"/pet/{pet_id}")
    pet = Pet(**response)

    assert pet.name == sample_pet.name
    assert pet.photoUrls == sample_pet.photoUrls
    assert pet.status == sample_pet.status
    logger.info("test_get_pet_by_id passed")


def test_add_new_pet(sample_pet):
    logger.info("Starting test_add_new_pet")
    response = client.post("/pet", json=sample_pet.dict())

    logger.info(f"Received response: {response}")
    assert response['name'] == sample_pet.name
    assert response['status'] == sample_pet.status
    assert response['photoUrls'] == sample_pet.photoUrls
    logger.info("test_add_new_pet passed")


def test_find_pets_by_status():
    logger.info("Starting test_find_pets_by_status")
    status = "available"
    response = client.get(f"/pet/findByStatus", params={"status": status})

    logger.info(f"Received response: {response}")
    assert isinstance(response, list)
    assert all(pet['status'] == status for pet in response)
    logger.info("test_find_pets_by_status passed")


def test_update_pet_with_form_data(sample_pet):
    logger.info("Starting test_update_pet_with_form_data")

    # Add the pet
    created_pet = client.post("/pet", json=sample_pet.dict())
    pet_id = created_pet.get('id')

    if not pet_id:
        logger.error("Failed to create pet. Response: %s", created_pet)
        pytest.fail("Failed to create pet. No pet ID returned.")

    # Update the pet with form data
    updated_status = "sold"
    response = client.post(f"/pet/{pet_id}", data={"status": updated_status})

    logger.info(f"Received response: {response}")

    # Validate the "code", "type", and "message" fields in the response
    assert 'code' in response, "Response does not contain 'code' key"
    assert 'type' in response, "Response does not contain 'type' key"
    assert 'message' in response, "Response does not contain 'message' key"

    # Assuming you have expected values for code, type, and message, otherwise, you can assert based on your requirements
    assert response['code'] == 200, f"Expected code 200, but got {response.get('code')}"
    assert response['type'] == "unknown", f"Expected type 'success', but got {response.get('type')}"

    logger.info("test_update_pet_with_form_data passed")


def test_update_pet(sample_pet):
    logger.info("Starting test_update_pet")
    created_pet = client.post("/pet", json=sample_pet.dict())
    pet_id = created_pet['id']
    logger.info(f"Created pet with ID: {pet_id}")

    updated_pet_data = sample_pet.copy(update={"status": "sold"})
    client.put(f"/pet", json=updated_pet_data.dict())

    response = client.get(f"/pet/{pet_id}")
    updated_pet = Pet(**response)

    assert updated_pet.status == "sold"
    logger.info("test_update_pet passed")


def test_delete_pet(sample_pet):
    logger.info("Starting test_delete_pet")
    created_pet = client.post("/pet", json=sample_pet.dict())
    pet_id = created_pet['id']
    logger.info(f"Created pet with ID: {pet_id}")

    status_code = client.delete(f"/pet/{pet_id}")
    assert status_code == 200

    try:
        client.get(f"/pet/{pet_id}")
        assert False, "Expected an error but got a successful response"
    except requests.exceptions.HTTPError as e:
        assert e.response.status_code == 404
    logger.info("test_delete_pet passed")
