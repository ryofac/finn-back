from finn.core.schemas import OrmModel


class CategorySchema(OrmModel):
    id: int
    name: str


class CategoryCreateOrUpdateSchema(OrmModel):
    name: str
    description: str


class CategoryList(OrmModel):
    categories: list[CategorySchema]
