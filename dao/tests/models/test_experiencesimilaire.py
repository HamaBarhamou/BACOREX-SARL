from django.utils.timezone import now
from django.test import TestCase
from decimal import Decimal
from dao.models import ExperienceSimilaire


class ExperienceSimilaireModelTest(TestCase):
    def test_experience_similaire_creation(self):
        """Teste la création d'une expérience similaire."""
        experience = ExperienceSimilaire.objects.create(
            reference_marche="REF-001",
            objet="Objet de test",
            description_travaux="Description de test",
            delai_execution_jours=30,  # Champ obligatoire
            nom_client="Client Test",
            financement="Financement Test",
            maitre_ouvrage="Maître d'ouvrage Test",
            montant_contrat=Decimal("1000000.00"),
            date_demarrage_travaux=now(),
            date_fin_travaux=now(),
            document="documents/test.pdf",
        )
        self.assertEqual(experience.reference_marche, "REF-001")
        self.assertEqual(experience.objet, "Objet de test")

    def test_experience_similaire_str_method(self):
        """Teste la méthode __str__."""
        experience = ExperienceSimilaire.objects.create(
            reference_marche="REF-001",
            objet="Objet de test",
            description_travaux="Description de test",
            delai_execution_jours=30,  # Champ obligatoire
            nom_client="Client Test",
            financement="Financement Test",
            maitre_ouvrage="Maître d'ouvrage Test",
            montant_contrat=Decimal("1000000.00"),
            date_demarrage_travaux=now(),
            date_fin_travaux=now(),
            document="documents/test.pdf",
        )
        self.assertEqual(str(experience), "REF-001")
