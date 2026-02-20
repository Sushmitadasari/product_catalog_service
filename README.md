# Product Catalog Service

A robust backend microservice for an e-commerce platform that manages a product catalog. Built using Python, FastAPI, SQLAlchemy, and PostgreSQL. It implements the Repository Pattern, Unit of Work, and advanced search features.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sushmitadasari/product_catalog_service
   cd product_catalog_service
   ```

2. **Run with Docker Compose:**
   ```bash
   docker-compose up --build -d
   ```
   *The database will automatically be seeded on startup with initial products and categories.*

## API Endpoints

Once running, access the auto-generated Swagger UI documentation at:
**[http://localhost:8000/docs](http://localhost:8000/docs)**

### Key Endpoints:
- `POST /products` - Create a product
- `GET /products/search` - Advanced search by keyword `q`, `category_id`, `min_price`, `max_price`.
- `GET /products` - Get all products (paginated)
- `GET /products/{id}` - Get a product by ID
- `PUT /products/{id}` - Update a product
- `DELETE /products/{id}` - Delete a product
- `GET /categories` - Get all categories
- *(And mapping CRUD endpoints for categories)*

### Example Request
```bash
curl -X GET "http://localhost:8000/products/search?q=phone&max_price=1000"
```

## Architectural Decisions

- **Repository Pattern:** Implemented generic CRUD repositories `IRepository` and concrete `ProductRepository` / `CategoryRepository` using SQLAlchemy. This abstracts the data access layer completely from the business logic.
- **Unit of Work (UoW):** The `SQLUnitOfWork` orchestrates transactions across multiple repositories. Services act upon `IUnitOfWork` allowing atomic transactions such as product creation mixed with complex category associations.
- **Search Strategy:** Implemented a robust filtering query leveraging SQLAlchemy ORM and underlying database indexes. Search leverages `ilike` operations against indexed column parameters in `Search`.

## Testing

Run unit and integration tests locally using `pytest`:

1. Install dependencies: `pip install -r requirements.txt`
2. Run tests: `pytest tests/`
   
*(Integration tests use an in-memory SQLite database mapped to SQLAlchemy for speed and isolation).*
