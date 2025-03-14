from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from dao.models import DAO, ReponseDAO


class ReponseDAOModelTest(TestCase):
    def setUp(self):
        self.dao = DAO.objects.create(
            dao_number="DAO-001",
            dao_title="Test DAO",
            date_publication=now(),
            date_soumission=now(),
        )

    def test_reponse_creation_scan(self):
        """Teste la création d'une réponse de type SCAN."""
        reponse = ReponseDAO.objects.create(
            dao=self.dao,
            type_reponse="SCAN",
            fichier="reponses/test_scan.pdf",
        )
        self.assertEqual(reponse.type_reponse, "SCAN")
        self.assertEqual(reponse.fichier.name, "reponses/test_scan.pdf")

    def test_reponse_creation_url(self):
        """Teste la création d'une réponse de type URL."""
        reponse = ReponseDAO.objects.create(
            dao=self.dao,
            type_reponse="URL",
            url="https://example.com",
        )
        self.assertEqual(reponse.type_reponse, "URL")
        self.assertEqual(reponse.url, "https://example.com")

    def test_reponse_missing_file_for_scan(self):
        """Teste qu'une réponse SCAN sans fichier lève une exception."""
        with self.assertRaises(ValidationError):
            reponse = ReponseDAO(
                dao=self.dao,
                type_reponse="SCAN",
            )
            reponse.full_clean()

    def test_reponse_missing_url_for_url(self):
        """Teste qu'une réponse URL sans URL lève une exception."""
        with self.assertRaises(ValidationError):
            reponse = ReponseDAO(
                dao=self.dao,
                type_reponse="URL",
            )
            reponse.full_clean()

    def test_str_method(self):
        """Teste la méthode __str__."""
        reponse = ReponseDAO.objects.create(
            dao=self.dao,
            type_reponse="SCAN",
            fichier="reponses/test_scan.pdf",
        )
        self.assertEqual(str(reponse), "Réponse pour DAO DAO-001 (Type: SCAN)")
