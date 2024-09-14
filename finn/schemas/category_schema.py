from finn.schemas.base_schema import OrmModel


class CategorySchema(OrmModel):
    id: int
    name: str


class CategoryList(OrmModel):
    categories: list[CategorySchema]
