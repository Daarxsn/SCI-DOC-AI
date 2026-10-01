from enum import Enum

from backend.schemas.udr import ElementType


class TranslationAction(str, Enum):
    TRANSLATE = "translate"
    PRESERVE = "preserve"
    SPECIALIZED = "specialized"
    REVIEW = "review"


class TranslationPolicy:
    SPECIALIZED_TYPES = {
        ElementType.EQUATION,
        ElementType.DIAGRAM,
        ElementType.GRAPH,
    }

    PRESERVE_TYPES = {
        ElementType.IMAGE,
        ElementType.PAGE_NUMBER,
    }

    def action_for(self, element_type: ElementType) -> TranslationAction:
        if element_type in self.PRESERVE_TYPES:
            return TranslationAction.PRESERVE

        if element_type in self.SPECIALIZED_TYPES:
            return TranslationAction.SPECIALIZED

        return TranslationAction.TRANSLATE
