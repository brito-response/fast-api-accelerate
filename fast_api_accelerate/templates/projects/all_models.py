def all_models_template() -> str:
    return """from src.models.user import UserModel 

# alll model includes models many to many associations  examples: from src.models.post_category import post_category_association

"""