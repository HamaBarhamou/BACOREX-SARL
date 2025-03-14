from django.test import TestCase
from django.utils.timezone import now
from dao.models import DAO, RapportDepouillement, Soumissionnaire, LigneRapport


class LigneRapportModelTest(TestCase):
    def setUp(self):
        self.dao = DAO.objects.create(
            dao_number="DAO-001",
            dao_title="Test DAO",
            date_publication=now(),
            date_soumission=now(),
        )
        self.rapport = RapportDepouillement.objects.create(dao=self.dao)
        self.soumissionnaire = Soumissionnaire.objects.create(
            nom="Soumissionnaire Test"
        )

    def test_ligne_rapport_creation(self):
        """Teste la création d'une ligne de rapport."""
        ligne = LigneRapport.objects.create(
            rapport=self.rapport,
            soumissionnaire=self.soumissionnaire,
            observations="Observations de test",
        )
        self.assertEqual(ligne.rapport, self.rapport)
        self.assertEqual(ligne.soumissionnaire, self.soumissionnaire)
        self.assertEqual(ligne.observations, "Observations de test")

    def test_ligne_rapport_str_method(self):
        """Teste la méthode __str__."""
        ligne = LigneRapport.objects.create(
            rapport=self.rapport,
            soumissionnaire=self.soumissionnaire,
        )
        self.assertEqual(str(ligne), "Ligne pour Soumissionnaire Test")
