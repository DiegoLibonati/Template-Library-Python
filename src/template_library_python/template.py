from template_library_python.configs.logger_config import setup_logger
from template_library_python.constants.codes import CODE_NOT_FOUND_TEMPLATE, CODE_NOT_VALID_INTEGER
from template_library_python.constants.messages import MESSAGE_NOT_FOUND_TEMPLATE, MESSAGE_NOT_VALID_INTEGER
from template_library_python.models.template_model import TemplateModel
from template_library_python.utils.exceptions import NotFoundError, ValidationError

logger = setup_logger("Template Library - template.py")


class Template:
    def __init__(self, name: str) -> None:
        self.name = name

    @property
    def pydantic_model(self) -> TemplateModel:
        return TemplateModel(name=self.name)

    def say_hello(self) -> None:
        logger.info(f"Hello: {self.name}")

    def throw_not_found(self) -> None:
        raise NotFoundError(code=CODE_NOT_FOUND_TEMPLATE, message=MESSAGE_NOT_FOUND_TEMPLATE)

    def sum(self, num1: int, num2: int) -> int:
        if not isinstance(num1, int) or not isinstance(num2, int):
            raise ValidationError(code=CODE_NOT_VALID_INTEGER, message=MESSAGE_NOT_VALID_INTEGER)
        return num1 + num2


def main() -> None:
    name: str = "Die"

    num1: int = 1
    num2: int = 2

    library = Template(name=name)

    library.say_hello()

    sum = library.sum(num1=num1, num2=num2)

    logger.info(f"Sum: {sum}")

    logger.info(f"Model: {type(library.pydantic_model)}")

    # library.throw_not_found()


if __name__ == "__main__":
    main()
