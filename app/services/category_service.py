from app.extensions import db
from app.models.category import Category


def get_all_categories():
    """
    Return all categories ordered alphabetically.
    """
    return Category.query.order_by(Category.id.asc()).all()


def get_category_by_id(category_id):
    """
    Return a category by its ID.
    """
    return Category.query.get(category_id)


def create_category(name, description):
    """
    Create a new category.
    """

    existing = Category.query.filter_by(name=name).first()

    if existing:
        return False, "Category already exists."

    category = Category(
        name=name,
        description=description
    )

    db.session.add(category)
    db.session.commit()

    return True, "Category created successfully."


def update_category(category, name, description):
    """
    Update an existing category.
    """

    existing = Category.query.filter(
        Category.name == name,
        Category.id != category.id
    ).first()

    if existing:
        return False, "Category name already exists."

    category.name = name
    category.description = description

    db.session.commit()

    return True, "Category updated successfully."


def delete_category(category):
    """
    Delete a category.
    """

    db.session.delete(category)
    db.session.commit()

    return True, "Category deleted successfully."