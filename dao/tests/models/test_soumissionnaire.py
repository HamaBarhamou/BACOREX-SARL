from django.test import TestCase

from dao.models import Soumissionnaire


class SoumissionnaireModelTest(TestCase):
    def test_soumissionnaire_creation(self):
        """Teste la création d'un soumissionnaire."""
        soumissionnaire = Soumissionnaire.objects.create(
            nom="Soumissionnaire Test",
            adresse="123 Rue Test",
            telephone="+123456789",
            email="test@example.com",
        )
        self.assertEqual(soumissionnaire.nom, "Soumissionnaire Test")
        self.assertEqual(soumissionnaire.adresse, "123 Rue Test")
        self.assertEqual(soumissionnaire.telephone, "+123456789")
        self.assertEqual(soumissionnaire.email, "test@example.com")

    def test_soumissionnaire_str_method(self):
        """Teste la méthode __str__."""
        soumissionnaire = Soumissionnaire.objects.create(nom="Soumissionnaire Test")
        self.assertEqual(str(soumissionnaire), "Soumissionnaire Test")
