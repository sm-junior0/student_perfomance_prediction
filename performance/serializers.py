from rest_framework import serializers


class PredictionSerializer(serializers.Serializer):
    """
    Validates student input data before ML prediction.
    
    Provides:
    - Field-level type coercion and range checks
    - Cross-field logical validation (e.g., hours in a day)
    - Consistency checks for realistic data patterns
    """

    # ── Field definitions with range validation ──────────────────────────
    hours_studied = serializers.FloatField(
        min_value=0, max_value=12,
        help_text="Daily study hours (0-12)",
        error_messages={
            'min_value': 'Study hours cannot be negative.',
            'max_value': 'Study hours cannot exceed 12 (realistic daily limit).',
            'invalid': 'Study hours must be a valid number.',
            'required': 'Study hours is required.',
        }
    )

    previous_scores = serializers.IntegerField(
        min_value=0, max_value=100,
        help_text="Previous exam score as percentage (0-100)",
        error_messages={
            'min_value': 'Previous scores cannot be negative.',
            'max_value': 'Previous scores cannot exceed 100%.',
            'invalid': 'Previous scores must be a whole number.',
            'required': 'Previous scores is required.',
        }
    )

    extracurricular = serializers.BooleanField(
        help_text="Whether the student participates in extracurricular activities",
        error_messages={
            'invalid': 'Extracurricular must be true/false (Yes/No).',
            'required': 'Extracurricular activities field is required.',
        }
    )

    sleep_hours = serializers.FloatField(
        min_value=4, max_value=12,
        help_text="Daily sleep hours (4-12)",
        error_messages={
            'min_value': 'Sleep hours must be at least 4 (health minimum).',
            'max_value': 'Sleep hours cannot exceed 12.',
            'invalid': 'Sleep hours must be a valid number.',
            'required': 'Sleep hours is required.',
        }
    )

    sample_papers = serializers.IntegerField(
        min_value=0, max_value=20,
        help_text="Number of sample question papers practiced (0-20)",
        error_messages={
            'min_value': 'Sample papers cannot be negative.',
            'max_value': 'Sample papers cannot exceed 20.',
            'invalid': 'Sample papers must be a whole number.',
            'required': 'Sample papers practiced is required.',
        }
    )

    # ── Field-level validation ───────────────────────────────────────────

    def validate_hours_studied(self, value):
        """Ensure study hours are in realistic 0.5-hour increments."""
        if value % 0.5 != 0:
            raise serializers.ValidationError(
                "Study hours should be in 0.5-hour increments (e.g., 1, 1.5, 2)."
            )
        return value

    def validate_sleep_hours(self, value):
        """Ensure sleep hours are in realistic 0.5-hour increments."""
        if value % 0.5 != 0:
            raise serializers.ValidationError(
                "Sleep hours should be in 0.5-hour increments (e.g., 6, 6.5, 7)."
            )
        return value

    # ── Cross-field (object-level) validation ────────────────────────────

    def validate(self, data):
        """
        Validate logical consistency across all fields together.
        """
        errors = {}

        hours = data.get('hours_studied', 0)
        sleep = data.get('sleep_hours', 0)
        scores = data.get('previous_scores', 0)
        papers = data.get('sample_papers', 0)
        extra = data.get('extracurricular', False)

        # 1. Total hours in a day cannot exceed 24
        if hours + sleep > 24:
            errors['non_field_errors'] = [
                f"Study ({hours}h) + Sleep ({sleep}h) = {hours + sleep}h "
                f"exceeds 24 hours in a day."
            ]

        # 2. Must leave at least 4 hours for eating, hygiene, commuting, etc.
        if hours + sleep > 20:
            errors.setdefault('non_field_errors', []).append(
                "Study + Sleep hours exceed 20. "
                "You must leave at least 4 hours for meals, hygiene, and other activities."
            )

        # 3. Sustainability check — extreme study with very low sleep
        if hours > 10 and sleep < 5:
            errors.setdefault('non_field_errors', []).append(
                "Unsustainable: 10+ study hours with less than 5 hours of sleep "
                "is not realistic long-term."
            )

        # 4. Zero-effort pattern
        if hours == 0 and papers == 0 and not extra:
            errors.setdefault('non_field_errors', []).append(
                "Zero study hours, no practice papers, and no extracurricular "
                "activities indicates no academic effort."
            )

        # 5. Bias prevention — perfect past scores with minimal current effort
        if scores == 100 and hours < 3:
            errors.setdefault('non_field_errors', []).append(
                "A perfect previous score (100) with less than 3 study hours "
                "is suspicious and may produce biased predictions."
            )

        # 6. Inconsistency — high past scores but zero current effort
        if scores >= 90 and hours == 0 and papers == 0:
            errors.setdefault('non_field_errors', []).append(
                "High previous scores (90+) are inconsistent with zero current "
                "study hours and zero practice papers."
            )

        if errors:
            raise serializers.ValidationError(errors)

        return data
