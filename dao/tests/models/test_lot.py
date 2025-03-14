from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from dao.models import DAO, Lot


class LotModelTest(TestCase):
    def setUp(self):
        self.dao = DAO.objects.create(
            dao_number="DAO-001",
            dao_title="Test DAO",
            date_publication=now(),
            date_soumission=now(),
        )

    def test_lot_creation(self):
        """Teste la création d'un lot avec tous les champs."""
        lot = Lot.objects.create(
            dao=self.dao,
            nom_lot="Lot 1",
            description="Description du lot 1",
        )
        self.assertEqual(lot.nom_lot, "Lot 1")
        self.assertEqual(lot.description, "Description du lot 1")
        self.assertEqual(lot.dao, self.dao)

    def test_lot_missing_required_fields(self):
        """Teste qu'un lot sans champs obligatoires lève une exception."""
        with self.assertRaises(ValidationError):
            lot = Lot()
            lot.full_clean()  # Appelle la validation

    def test_lot_str_method(self):
        """Teste la méthode __str__."""
        lot = Lot.objects.create(
            dao=self.dao,
            nom_lot="Lot 1",
            description="Description du lot 1",
        )
        self.assertEqual(str(lot), "DAO-001 - Lot 1")

    def test_lot_without_description(self):
        """Teste la création d'un lot sans description."""
        lot = Lot.objects.create(
            dao=self.dao,
            nom_lot="Lot 1",
        )
        self.assertIsNone(lot.description)
