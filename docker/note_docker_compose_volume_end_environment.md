Looking at the [Dockerfile](Dockerfile#L24)
 , at the moment the whole repository is copied on the container so that the code knows where to find thigs .. like data or static files. This means the docker container will require a rebuild every time the data needs an upate.

To avoid this,  it is possible to expose directories as volumes, which means they can be accessed directly from the host machine (this way you can update the data without the needs of rebuilding the container)

 In the docker-compose file add the following:

 ```yaml
     volumes:
      - source:destination
 ```

To let the container know about the destination folder, we ca use `ENVIRONMENT VARABLES`. This is done in the `environment` section of the `docker-compose` file:

```yaml
    environment:
      DATA_DIR: destination
```

At this point the code will be able to get the new `PATH` via:

```python
import os
data_dir = os.environ.get['DATA_DIR']
```

* This will require some changes in the code, so to be able to read the data from the new PATH e.g. in: [read_files_local](../read_files_local.py#L7)

```python
Opath='./data/SST/csv'
```

will look like:

```python
Opath=f'{data_dir}/SST/csv'
```
