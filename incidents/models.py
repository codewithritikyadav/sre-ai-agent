from django.db import models
from .ai_analyzer import analyze_logs


class Incident(models.Model):

    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    title = models.CharField(max_length=255)

    logs = models.TextField()

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='Low'
    )

    root_cause = models.TextField(blank=True, null=True)

    suggestion = models.TextField(blank=True, null=True)

    anomaly_score = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        analysis = analyze_logs(self.logs)

        # Remove markdown symbols if Gemini returns them
        analysis = analysis.replace("*", "")

        try:
            lines = analysis.split("\n")

            severity = ""
            root_cause = ""
            suggestion = ""

            for line in lines:

                if "Severity:" in line:
                    severity = line.replace("Severity:", "").strip()

                elif "Root Cause:" in line:
                    root_cause = line.replace("Root Cause:", "").strip()

                elif "Suggested Fix:" in line:
                    suggestion = line.replace("Suggested Fix:", "").strip()

            if severity:
                self.severity = severity

            self.root_cause = root_cause
            self.suggestion = suggestion

        except Exception as e:
            print("AI Parsing Error:", e)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title