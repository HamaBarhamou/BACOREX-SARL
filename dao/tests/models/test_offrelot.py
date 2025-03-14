from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from decimal import Decimal
from dao.models import (
    DAO,
    Lot,
    RapportDepouillement,
    Soumissionnaire,
    LigneRapport,
    OffreLot,
    Configuration,
)


class OffreLotModelTest(TestCase):
    def setUp(self):
        self.dao = DAO.objects.create(
            dao_number="DAO-001",
            dao_title="Test DAO",
            date_publication=now(),
            date_soumission=now(),
        )
        self.lot = Lot.objects.create(dao=self.dao, nom_lot="Lot 1")
        self.rapport = RapportDepouillement.objects.create(dao=self.dao)
        self.soumissionnaire = Soumissionnaire.objects.create(
            nom="Soumissionnaire Test"
        )
        self.ligne_rapport = LigneRapport.objects.create(
            rapport=self.rapport,
            soumissionnaire=self.soumissionnaire,
        )
        Configuration.objects.create(tva_pourcentage=Decimal("19.00"))

    def test_offre_lot_creation(self):
        """Teste la création d'une offre de lot."""
        offre = OffreLot.objects.create(
            ligne_rapport=self.ligne_rapport,
            lot=self.lot,
            offre_financiere=Decimal("1000.00"),
            devise="FCFA",
        )
        self.assertEqual(offre.offre_financiere, Decimal("1000.00"))
        self.assertEqual(offre.devise, "FCFA")

    def test_offre_lot_conversion_fcfa(self):
        """Teste la conversion en FCFA."""
        offre = OffreLot.objects.create(
            ligne_rapport=self.ligne_rapport,
            lot=self.lot,
            offre_financiere=Decimal("1000.00"),
            devise="USD",
        )
        # 1000 USD * 630 (taux USD) = 630000 FCFA HT
        # 630000 FCFA HT + 19% TVA = 749700 FCFA TTC
        self.assertEqual(offre.get_offre_fcfa(), Decimal("749700.00"))

    def test_offre_lot_str_method(self):
        """Teste la méthode __str__."""
        offre = OffreLot.objects.create(
            ligne_rapport=self.ligne_rapport,
            lot=self.lot,
            offre_financiere=Decimal("1000.00"),
            devise="FCFA",
        )
        self.assertEqual(str(offre), "Offre pour Lot 1 par Soumissionnaire Test")
