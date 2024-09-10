**Files and Directories**
- **api_client.py:** Contains the APIClient class used to interact with the Petstore API.
- **models.py:** Defines Pydantic models for API requests and responses.
-**test_pet_endpoint.py:** Contains the pytest test cases for various Petstore API endpoints.
- **images/sample_image.jpg:** A sample image file used for testing. (Note: Currently repo downloads web based file so image folders a redundency.)
- **requirements.txt:** Lists Python package dependencies.
- **Dockerfile:** Docker configuration to build a container for the project.
- **.github/workflows/ci.yml:** GitHub Actions configuration for CI.

**Setup and Installation**
**Prerequisites**
**Ensure you have the following installed:**

- Python 3.9+
- Docker (optional, for Docker setup)
- Git
- pytest

**Running Tests Locally**
1. To run tests use the following command: 
_pytest --maxfail=1 --disable-warnings -q_

--maxfail=1: Stop after the first failure.
--disable-warnings: Suppress warnings.
-q: Run in quiet mode.

At a later date you could also add pytest.mark commands to run individual test cases. 

**Docker Setup**
1. **Build Docker Image**
   _docker build -t petstore-tests_

2. **Run the Docker Container**
_docker run --rm petstore-tests_

**CI Workflow**
You can also run the test cases using a Github CI pipeline currently It is configured similar to the command above to exit on first failure but this can be modified. 

**Pipeline actions**
- Checks out the code
- Sets up Python
- Installs dependencies
- Runs Pytest

Again this is very roughly put together process improvements can always be made in further iterations. Thanks for your consideration and I look forward to hearing from you. 
