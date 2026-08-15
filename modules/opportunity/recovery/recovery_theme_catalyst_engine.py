"""
EIOS
Everest Investment Operating System

Recovery Theme → Catalyst Intelligence Engine

Purpose
-------
Creates explicit relationships between a Recovery Theme and
known Catalyst Intelligence families/patterns.

Design Principles
-----------------
- Deterministic.
- No web access.
- No company selection.
- No valuation.
- No portfolio decision.
- No autonomous catalyst discovery.
- Does not mutate input.
- Catalyst families/patterns must be explicitly supplied.
- Transparent reasoning.
"""


from copy import deepcopy
from typing import Any, Dict, List, Optional

from modules.opportunity.recovery.recovery_theme_assessment import (
    RecoveryThemeAssessment,
)

from modules.opportunity.recovery.recovery_theme_catalyst_link import (
    RecoveryThemeCatalystLink,
    RecoveryCatalystRelevance,
    RecoveryCatalystRelationship,
    RecoveryCatalystTransmission,
)


class RecoveryThemeCatalystEngine:
    """
    Deterministic bridge between Recovery Theme Intelligence
    and Catalyst Intelligence.
    """

    # ======================================================
    # PUBLIC API
    # ======================================================

    @staticmethod
    def assess(
        theme: RecoveryThemeAssessment,
        catalysts: Optional[List[Dict[str, Any]]] = None,
    ) -> List[RecoveryThemeCatalystLink]:
        """
        Create catalyst links for a recovery theme.

        `catalysts` must be explicitly supplied.

        Each catalyst dictionary may contain:

            catalyst_id
            catalyst_family
            catalyst_pattern
            transmission
            relevance
            relationship
            catalyst_strength
            catalyst_confidence
            rationale
            expected_effect
            timing
            persistence
            dependencies
            supporting_evidence
            contradictory_evidence
            beneficiaries
            adversely_affected
            risks
            invalidation_conditions

        Unknown fields are ignored.

        Inputs are not mutated.
        """

        if theme is None:
            return []

        if not catalysts:
            return []

        results: List[
            RecoveryThemeCatalystLink
        ] = []

        for catalyst in catalysts:

            if not isinstance(
                catalyst,
                dict,
            ):
                continue

            link = (
                RecoveryThemeCatalystEngine._build_link(
                    theme,
                    catalyst,
                )
            )

            results.append(link)

        return results

    # ======================================================
    # BUILD LINK
    # ======================================================

    @staticmethod
    def _build_link(
        theme: RecoveryThemeAssessment,
        catalyst: Dict[str, Any],
    ) -> RecoveryThemeCatalystLink:

        link = RecoveryThemeCatalystLink()

        # --------------------------------------------------
        # Identity
        # --------------------------------------------------

        link.link_id = (
            str(
                catalyst.get(
                    "link_id",
                    "",
                )
            )
        )

        if not link.link_id:

            catalyst_id = str(
                catalyst.get(
                    "catalyst_id",
                    "",
                )
            )

            link.link_id = (
                f"{theme.theme_id}"
                f"::{catalyst_id}"
            )

        link.theme_id = (
            theme.theme_id
        )

        link.theme_name = (
            theme.theme_name
        )

        # --------------------------------------------------
        # Catalyst identity
        # --------------------------------------------------

        link.catalyst_id = str(
            catalyst.get(
                "catalyst_id",
                "",
            )
        )

        link.catalyst_family = str(
            catalyst.get(
                "catalyst_family",
                "",
            )
        )

        link.catalyst_pattern = str(
            catalyst.get(
                "catalyst_pattern",
                "",
            )
        )

        # --------------------------------------------------
        # Classification
        # --------------------------------------------------

        link.relevance = (
            RecoveryThemeCatalystEngine
            ._enum_value(
                RecoveryCatalystRelevance,
                catalyst.get(
                    "relevance"
                ),
            )
        )

        link.relationship = (
            RecoveryThemeCatalystEngine
            ._enum_value(
                RecoveryCatalystRelationship,
                catalyst.get(
                    "relationship"
                ),
            )
        )

        link.transmission = (
            RecoveryThemeCatalystEngine
            ._enum_value(
                RecoveryCatalystTransmission,
                catalyst.get(
                    "transmission"
                ),
            )
        )

        # --------------------------------------------------
        # Economic mechanism
        # --------------------------------------------------

        link.economic_mechanism = (
            str(
                catalyst.get(
                    "economic_mechanism",
                    theme.economic_mechanism,
                )
            )
        )

        link.transmission_description = str(
            catalyst.get(
                "transmission_description",
                "",
            )
        )

        link.catalyst_rationale = str(
            catalyst.get(
                "rationale",
                catalyst.get(
                    "catalyst_rationale",
                    "",
                ),
            )
        )

        link.expected_effect = str(
            catalyst.get(
                "expected_effect",
                "",
            )
        )

        # --------------------------------------------------
        # Recovery context
        # --------------------------------------------------

        link.recovery_stage = (
            theme.stage.value
        )

        link.recovery_direction = (
            theme.direction.value
        )

        link.recovery_breadth = (
            theme.recovery_breadth
        )

        link.confirmed_recovery_breadth = (
            theme.confirmed_recovery_breadth
        )

        link.recovery_confidence = (
            theme.confidence
        )

        # --------------------------------------------------
        # Catalyst context
        # --------------------------------------------------

        link.catalyst_strength = (
            RecoveryThemeCatalystEngine
            ._bounded_float(
                catalyst.get(
                    "catalyst_strength",
                    0.0,
                )
            )
        )

        link.catalyst_confidence = (
            RecoveryThemeCatalystEngine
            ._bounded_float(
                catalyst.get(
                    "catalyst_confidence",
                    0.0,
                )
            )
        )

        link.catalyst_timing = str(
            catalyst.get(
                "timing",
                catalyst.get(
                    "catalyst_timing",
                    "",
                ),
            )
        )

        link.catalyst_persistence = str(
            catalyst.get(
                "persistence",
                catalyst.get(
                    "catalyst_persistence",
                    "",
                ),
            )
        )

        link.catalyst_dependencies = (
            RecoveryThemeCatalystEngine
            ._string_list(
                catalyst.get(
                    "dependencies",
                    catalyst.get(
                        "catalyst_dependencies",
                        [],
                    ),
                )
            )
        )

        # --------------------------------------------------
        # Evidence
        # --------------------------------------------------

        link.supporting_evidence = (
            RecoveryThemeCatalystEngine
            ._string_list(
                catalyst.get(
                    "supporting_evidence",
                    [],
                )
            )
        )

        link.contradictory_evidence = (
            RecoveryThemeCatalystEngine
            ._string_list(
                catalyst.get(
                    "contradictory_evidence",
                    [],
                )
            )
        )

        link.evidence_sources = (
            RecoveryThemeCatalystEngine
            ._string_list(
                catalyst.get(
                    "evidence_sources",
                    [],
                )
            )
        )

        # --------------------------------------------------
        # Impact mapping
        # --------------------------------------------------

        link.potential_beneficiaries = (
            RecoveryThemeCatalystEngine
            ._string_list(
                catalyst.get(
                    "beneficiaries",
                    catalyst.get(
                        "potential_beneficiaries",
                        [],
                    ),
                )
            )
        )

        link.potential_adversely_affected = (
            RecoveryThemeCatalystEngine
            ._string_list(
                catalyst.get(
                    "adversely_affected",
                    catalyst.get(
                        "potential_adversely_affected",
                        [],
                    ),
                )
            )
        )

        link.second_order_effects = (
            RecoveryThemeCatalystEngine
            ._string_list(
                catalyst.get(
                    "second_order_effects",
                    [],
                )
            )
        )

        link.transmission_channels = (
            RecoveryThemeCatalystEngine
            ._string_list(
                catalyst.get(
                    "transmission_channels",
                    [],
                )
            )
        )

        # --------------------------------------------------
        # Risk
        # --------------------------------------------------

        link.key_risks = (
            RecoveryThemeCatalystEngine
            ._string_list(
                catalyst.get(
                    "risks",
                    catalyst.get(
                        "key_risks",
                        [],
                    ),
                )
            )
        )

        link.invalidation_conditions = (
            RecoveryThemeCatalystEngine
            ._string_list(
                catalyst.get(
                    "invalidation_conditions",
                    [],
                )
            )
        )

        link.contradiction_score = (
            RecoveryThemeCatalystEngine
            ._bounded_float(
                catalyst.get(
                    "contradiction_score",
                    0.0,
                )
            )
        )

        # --------------------------------------------------
        # Reasoning
        # --------------------------------------------------

        link.reasons = (
            RecoveryThemeCatalystEngine
            ._build_reasons(
                theme,
                catalyst,
                link,
            )
        )

        if (
            link.contradiction_score
            >= 30.0
        ):

            link.warnings.append(
                "Catalyst evidence contains "
                "material contradiction."
            )

        if not link.catalyst_family:

            link.warnings.append(
                "Catalyst family is not specified."
            )

        if not link.catalyst_pattern:

            link.warnings.append(
                "Catalyst pattern is not specified."
            )

        return link

    # ======================================================
    # ENUM CONVERSION
    # ======================================================

    @staticmethod
    def _enum_value(
        enum_class,
        value,
    ):

        if value is None:
            return list(enum_class)[0]

        if isinstance(
            value,
            enum_class,
        ):
            return value

        text = str(value)

        for member in enum_class:

            if (
                text
                == member.value
            ):
                return member

            if (
                text
                == member.name
            ):
                return member

        return list(enum_class)[0]

    # ======================================================
    # BOUNDED FLOAT
    # ======================================================

    @staticmethod
    def _bounded_float(
        value,
    ) -> float:

        try:

            number = float(
                value
            )

        except (
            TypeError,
            ValueError,
        ):

            return 0.0

        return max(
            0.0,
            min(
                100.0,
                number,
            ),
        )

    # ======================================================
    # STRING LIST
    # ======================================================

    @staticmethod
    def _string_list(
        value,
    ) -> List[str]:

        if value is None:
            return []

        if isinstance(
            value,
            str,
        ):

            return [
                value
            ]

        if not isinstance(
            value,
            (list, tuple, set),
        ):

            return []

        return [
            str(item)
            for item in value
            if item is not None
        ]

    # ======================================================
    # REASONING
    # ======================================================

    @staticmethod
    def _build_reasons(
        theme: RecoveryThemeAssessment,
        catalyst: Dict[str, Any],
        link: RecoveryThemeCatalystLink,
    ) -> List[str]:

        reasons: List[str] = []

        if theme.theme_name:

            reasons.append(
                f"Recovery theme '{theme.theme_name}' "
                "is linked to the supplied catalyst."
            )

        if link.catalyst_family:

            reasons.append(
                f"Catalyst family: "
                f"{link.catalyst_family}."
            )

        if link.catalyst_pattern:

            reasons.append(
                f"Catalyst pattern: "
                f"{link.catalyst_pattern}."
            )

        if (
            link.recovery_breadth
            >= 60.0
        ):

            reasons.append(
                "Recovery breadth provides broad "
                "theme-level support."
            )

        if (
            link.confirmed_recovery_breadth
            >= 40.0
        ):

            reasons.append(
                "Confirmed recovery breadth provides "
                "additional support."
            )

        if (
            link.recovery_confidence
            >= 70.0
        ):

            reasons.append(
                "Recovery theme confidence is high."
            )

        if (
            link.relevance
            != RecoveryCatalystRelevance.UNKNOWN
        ):

            reasons.append(
                f"Catalyst relevance is "
                f"{link.relevance.value}."
            )

        if (
            link.relationship
            != RecoveryCatalystRelationship.UNKNOWN
        ):

            reasons.append(
                f"Catalyst relationship is "
                f"{link.relationship.value}."
            )

        return reasons


__all__ = [
    "RecoveryThemeCatalystEngine",
]