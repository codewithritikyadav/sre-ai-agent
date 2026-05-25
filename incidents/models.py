from django.db import models

from django.contrib.auth.models import User

from .ai_analyzer import analyze_logs

from ml_engine.anomaly_detector import calculate_anomaly


class Incident(models.Model):

    SEVERITY_CHOICES = [

        ('Low', 'Low'),

        ('Medium', 'Medium'),

        ('High', 'High'),

        ('Critical', 'Critical'),

    ]

    # User
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # Title
    title = models.CharField(
        max_length=255
    )

    # Logs
    logs = models.TextField()

    # Severity
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='Medium'
    )

    # AI Output
    root_cause = models.TextField(
        blank=True,
        null=True
    )

    suggestion = models.TextField(
        blank=True,
        null=True
    )

    # ML Score
    anomaly_score = models.FloatField(
        default=0
    )

    # Time
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        # AI Analysis
        if not self.root_cause:

            analysis = analyze_logs(self.logs)

            # SAFE FALLBACK
            if not analysis:

                analysis = """
Severity: Medium

Root Cause: AI analysis unavailable.

Suggested Fix: Check Gemini API configuration.
"""

            analysis = str(analysis).replace("*", "")

            lines = analysis.split("\n")

            severity = "Medium"

            root_cause = "Unknown issue."

            suggestion = "Investigate system logs."

            for line in lines:

                line = line.strip()

                if "Severity:" in line:

                    severity = line.replace(
                        "Severity:",
                        ""
                    ).strip()

                elif "Root Cause:" in line:

                    root_cause = line.replace(
                        "Root Cause:",
                        ""
                    ).strip()

                elif "Suggested Fix:" in line:

                    suggestion = line.replace(
                        "Suggested Fix:",
                        ""
                    ).strip()

            self.severity = severity

            self.root_cause = root_cause

            self.suggestion = suggestion

        # ML Score
        self.anomaly_score = calculate_anomaly(
            self.logs
        )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.title