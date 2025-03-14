from django.test import TestCase
from django.utils.timezone import now

from dao.models import DAO, RapportDepouillement


class RapportDepouillementModelTest(TestCase):
    def setUp(self):
        self.dao = DAO.objects.create(
            dao_number="DAO-001",
            dao_title="Test DAO",
            date_publication=now(),
            date_soumission=now(),
        )

    def test_rapport_creation(self):
        """Teste la création d'un rapport de dépouillement."""
        rapport = RapportDepouillement.objects.create(
            dao=self.dao,
            taux_dollar_fcfa=630,
            taux_euro_fcfa=656,
        )
        self.assertEqual(rapport.dao, self.dao)
        self.assertEqual(rapport.taux_dollar_fcfa, 630)
        self.assertEqual(rapport.taux_euro_fcfa, 656)

    def test_convertir_en_fcfa(self):
        """Teste la méthode convertir_en_fcfa."""
        rapport = RapportDepouillement.objects.create(
            dao=self.dao,
            taux_dollar_fcfa=630,
            taux_euro_fcfa=656,
        )
        # Conversion USD
        self.assertEqual(rapport.convertir_en_fcfa(100, "USD"), 63000)
        # Conversion EUR
        self.assertEqual(rapport.convertir_en_fcfa(100, "EUR"), 65600)
        # Conversion FCFA
        self.assertEqual(rapport.convertir_en_fcfa(100, "FCFA"), 100)

    def test_str_method(self):
        """Teste la méthode __str__."""
        rapport = RapportDepouillement.objects.create(
            dao=self.dao,
            taux_dollar_fcfa=630,
            taux_euro_fcfa=656,
        )
        self.assertEqual(str(rapport), "Rapport de dépouillement pour DAO DAO-001")
