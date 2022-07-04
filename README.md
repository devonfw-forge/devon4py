# devon4py

## Roadmap

- [X] Swagger / OpenAPI integration
- [X] Configuration file for each environment
- [X] Enable/Disable Swagger
- [X] API Port configuration
- [X] Log Configuration
- [X] Database Configuration
- [ ] ASYNC Database Configuration
- [X] Swagger Configuration
- [X] JWT / Keycloak Integration
- [X] CORS Configuration
- [X] Global Exception Management
- [ ] DB Entity Generation
- [ ] Code generation using Templates
- [X] Log to files integration
- [ ] Log to Database integration
- [ ] Log to GrayLog integration
- [ ] Log to Splunk integration
- [ ] Kafka integration

## Based on FastAPI

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

The key features are:

- **Fast**: Very high performance, **on par with NodeJS and Go** (thanks to _Starlette_ and _Pydantic_). One of the fastest Python frameworks available.

- **Fast to code**: Increase the speed to develop features by about 200% to 300%.

- **Fewer bugs**: Reduce about 40% of human (developer) induced errors.

- **Intuitive**: Great editor support. Completion everywhere. Less time debugging.

- **Easy**: Designed to be easy to use and learn. Less time reading docs.

- **Short**: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.

- **Robust**: Get production-ready code. With automatic interactive documentation.

- **Standards-based**: Based on (and fully compatible with) the open standards for APIs: OpenAPI (previously known as Swagger) and JSON Schema.

FastAPI works on **_Uvicorn_**, an ASGI web server implementation for Python.

Unlike Flask, FastAPI is an ASGI (Asynchronous Server Gateway Interface) framework, brings together Starlette, Pydantic, OpenAPI, and JSON Schema.
Under the hood, FastAPI uses Pydantic for data validation and Starlette for tooling, making it blazing fast compared to Flask, giving comparable performance to high-speed web APIs in Node or Go.
Starlette + Uvicorn offers async request capability, something that Flask lacks.
With Pydantic along with type hints, you get a nice editor experience with autocompletion. You also get data validation, serialization and deserialization (for building an API), and automatic documentation (via JSON Schema and OpenAPI).


### Unlimited "plug-ins"
Or in other way, no need for them, import and use the code you need.

Any integration is designed to be so simple to use (with dependencies) that you can create a "plug-in" for your application in 2 lines of code using the same structure and syntax used for your path operations.

### Tested
- 100% test coverage.
- 100% type annotated code base.
- Used in production applications.

### Based on Starlette

FastAPI is fully compatible with (and based on) [Starlette](https://www.starlette.io/). So, any additional Starlette code you have, will also work.

FastAPI is actually a sub-class of Starlette. So, if you already know or use Starlette, most of the functionality will work the same way.

With FastAPI you get all of Starlette's features (as FastAPI is just Starlette on steroids):

- Seriously impressive performance. It is one of the fastest Python frameworks available, on par with NodeJS and Go.
- WebSocket support.
- In-process background tasks.
- Startup and shutdown events.
- Test client built on requests.
- CORS, GZip, Static Files, Streaming responses.
- Session and Cookie support.
- 100% test coverage.
- 100% type annotated codebase.

# Run the application
In this section you will find an overview on how to execute and configure the project.

## Dependencies
Dependencies are automatically managed by **Poetry**

To install dependencies run
```bash
poetry install
```
in same folder where your `.toml` file is located. 
Poetry will take care of:
- Installing the required Python interpreter 
- Installing all the libraries and modules 
- Creating the virtual environment for you

Refer to [this link](https://www.jetbrains.com/help/pycharm/poetry.html) to configure Poetry on PyCharm

## Running on local

Start the uvicorn live server with the command:

```
uvicorn main:app --reload
```

- **_main_**: the file main.py (the Python "module").
- **_app_**: the object created inside of main.py with the line app = FastAPI().
- _**--reload**_: make the server restart after code changes. Only use for development.

You can also launch the uvicorn server programmatically running directly the main.py file.

```
python main.py
```

## Environment Configuration

You can use Pydantic Settings to handle the settings or configurations for your application, with all the power of Pydantic models. The project uses Dependency Injection for managing dependencies across the application and easy mocking for testing.

**Create an **_.env_** file for each environment configuration**. The use of @lru_cache() lets you avoid reading the dotenv file again and again for each request, while allowing you to override it during testing.

Even when using a dotenv file, the application will still read environment variables as well as the dotenv file, **environment variables will always take priority over values loaded from a dotenv file**.

You can also specify the environment when launching the server. Corresponding **_.env_** file will be automatically loaded.

Settings and environment variables are managed by **Pydantic**, refer to [the documentation](https://pydantic-docs.helpmanual.io/usage/settings/) for more info.

```
ENV=PROD uvicorn main:app --reload
ENV=PROD python main.py
```

### Host & Port Configuration
The Port and Hosting configuration can be set directly on the **.env** file if launching the main.py file.

However, this configuration is related with the uvicorn server itself and can also be set with the _**--port [int]**_ flag. 

Refer to the [uvicorn documentation](https://www.uvicorn.org/settings/) for more info.

### Logging Configuration
The application uses the default **_logging_** module.

To use it inside an specific module init it first with the command:

```
logger = logging.getLogger(__name__)
```

You can use the __name__ variable to take the current file name as the default or specify a custom module name manually.

Configure the logging properties in the **_logging.yaml_** file. 
You can find more information in the [logging](https://docs.python.org/3/library/logging.html#module-logging) documentation.

## Database Management

