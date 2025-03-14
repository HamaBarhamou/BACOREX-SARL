from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import now

from dao.models import DAO


class DAOModelTest(TestCase):
    def test_dao_creation(self):
        """Teste la création d'un DAO avec tous les champs."""
        dao = DAO.objects.create(
            dao_number="DAO-001",
            dao_title="Test DAO",
            date_publication=now(),
            date_soumission=now(),
        )
        self.assertEqual(dao.dao_number, "DAO-001")
        self.assertEqual(dao.dao_title, "Test DAO")
        self.assertFalse(dao.is_closed)

    def test_dao_missing_required_fields(self):
        """Teste qu'un DAO sans champs obligatoires lève une exception."""
        with self.assertRaises(ValidationError):
            dao = DAO()
            dao.full_clean()  # Appelle la validation

    def test_dao_str_method(self):
        """Teste la méthode __str__."""
        dao = DAO.objects.create(
            dao_number="DAO-001",
            dao_title="Test DAO",
            date_publication=now(),
            date_soumission=now(),
        )
        self.assertEqual(str(dao), "DAO-001 Test DAO")

    def test_dao_unique_number(self):
        """Teste que le numéro de DAO est unique."""
        DAO.objects.create(
            dao_number="DAO-001",
            dao_title="Test DAO",
            date_publication=now(),
            date_soumission=now(),
        )
        with self.assertRaises(Exception):  # IntegrityError ou ValidationError
            DAO.objects.create(
                dao_number="DAO-001",
                dao_title="Test DAO 2",
                date_publication=now(),
                date_soumission=now(),
            )
