from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from dao.models import Configuration


class ConfigurationModelTest(TestCase):
    def test_default_tva(self):
        """Teste que la TVA par défaut est correcte."""
        config = Configuration.objects.create()
        self.assertEqual(config.tva_pourcentage, Decimal("19.00"))

    def test_get_tva(self):
        """Teste la méthode get_tva."""
        Configuration.objects.create(tva_pourcentage=Decimal("20.00"))
        self.assertEqual(Configuration.get_tva(), Decimal("20.00"))

    def test_str_method(self):
        """Teste la méthode __str__."""
        config = Configuration.objects.create(tva_pourcentage=Decimal("19.00"))
        self.assertEqual(str(config), "Configuration (TVA: 19.00%)")

    def test_tva_negative(self):
        """Teste qu'une TVA négative lève une exception."""
        with self.assertRaises(ValidationError):
            config = Configuration(tva_pourcentage=Decimal("-10.00"))
            config.full_clean()  # Appelle la validation

    def test_tva_too_high(self):
        """Teste qu'une TVA trop élevée lève une exception."""
        with self.assertRaises(ValidationError):
            config = Configuration(tva_pourcentage=Decimal("1000.00"))
            config.full_clean()  # Appelle la validation
