## Running the fastapi instance

### Pre-requisites
* Docker
* Python 3.10.0
* (Optional) An xlsx file to transform into data for a plot, located in ``app/``
* A ``.env`` file located in ``app/`` with a single ``FILE_ID`` variable containing the id of the cloud file
* A json file with the credentials for a Service Account of GCP, located in ``app/Google`` (This account must have access to the desired file)

### Running locally
* Run ``pip install --no-cache-dir --upgrade -r requirements.txt``
* Run ``python app/api.py``

### Running with dockers
* Run ``docker build -t fastapi .``
* Run ``docker run -d -p 9000:9000 fastapi``

### Available routes
* ``plots`` to get the single plot from the xlsx file
* ``updatePlots`` to get a new version of the xlsx file (if the current version is older than 1 day) and get a single plot from it.



  
