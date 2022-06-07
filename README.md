# devon4py

## Roadmap

- [X] Swagger / OpenAPI integration
- [ ] Configuration file for each environment
- [ ] Enable/Disable Swagger
- [ ] API Port configuration
- [ ] Log Configuration
- [ ] Database Configuration
- [ ] Swagger Configuration
- [ ] JWT Configuration
- [ ] CORS Configuration
- [ ] Global Exception Management
- [ ] DB Entity Generation
- [ ] Code generation using Templates
- [ ] Log to files integration
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

### Environment Configuration

You can use Pydantic Settings to handle the settings or configurations for your application, with all the power of Pydantic models. The project uses Dependency Injection for managing dependencies across the application and easy mocking for testing.

**Create an **_.env_** file for each environment configuration**. The use of @lru_cache() lets you avoid reading the dotenv file again and again for each request, while allowing you to override it during testing.

Refer to [this link](https://fastapi.tiangolo.com/advanced/settings/) for more information on how to manage the configuration with FastAPI.