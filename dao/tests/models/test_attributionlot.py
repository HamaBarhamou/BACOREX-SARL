from decimal import Decimal

from django.test import TestCase
from django.utils.timezone import now

from dao.models import (
    DAO,
    AttributionLot,
    LigneRapport,
    Lot,
    OffreLot,
    RapportDepouillement,
    Soumissionnaire,
)


class AttributionLotModelTest(TestCase):
    def setUp(self):
        self.dao = DAO.objects.create(
            dao_number="DAO-001",
            dao_title="Test DAO",
            date_publication=now(),
            date_soumission=now(),
        )
        self.lot = Lot.objects.create(dao=self.dao, nom_lot="Lot 1")
        self.soumissionnaire = Soumissionnaire.objects.create(
            nom="Soumissionnaire Test"
        )
        self.rapport = RapportDepouillement.objects.create(dao=self.dao)
        self.ligne_rapport = LigneRapport.objects.create(
            rapport=self.rapport,
            soumissionnaire=self.soumissionnaire,
        )
        self.offre = OffreLot.objects.create(
            ligne_rapport=self.ligne_rapport,
            lot=self.lot,
            offre_financiere=Decimal("1000.00"),
            devise="FCFA",
        )

    def test_attribution_lot_creation(self):
        """Teste la création d'une attribution de lot."""
        attribution = AttributionLot.objects.create(
            lot=self.lot,
            soumissionnaire=self.soumissionnaire,
            statut="ATTRIBUE",
        )
        self.assertEqual(attribution.statut, "ATTRIBUE")

    def test_attribution_lot_str_method(self):
        """Teste la méthode __str__."""
        attribution = AttributionLot.objects.create(
            lot=self.lot,
            soumissionnaire=self.soumissionnaire,
            statut="ATTRIBUE",
        )
        self.assertEqual(
            str(attribution),
            "Attribution DAO-001 - Lot 1 - Soumissionnaire Test (Attribué)",
        )
