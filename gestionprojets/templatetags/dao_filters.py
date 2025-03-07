from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()


@register.filter
def get(dictionary, key):
    """Récupère une valeur d'un dictionnaire par sa clé"""
    if dictionary and key in dictionary:
        return dictionary[key]
    return None


@register.filter
def get_offres_for_lot(ligne_offres_values, lot_id):
    # Récupère toutes les offres pour un lot spécifique
    offres = []
    for ligne_dict in ligne_offres_values:
        if lot_id in ligne_dict and lot_id != "ligne_id":
            offre = ligne_dict[lot_id]
            if offre:  # Vérifier que la valeur n'est pas None ou vide
                offres.append({"ligne_id": ligne_dict["ligne_id"], "value": offre})
    return offres


@register.filter
def min_offre(offres):
    """Trouve l'offre minimale parmi une liste d'offres"""
    if not offres:
        return None
    return min(offres, key=lambda x: x["value"])


@register.filter
def max_offre(offres):
    """Trouve l'offre maximale parmi une liste d'offres"""
    if not offres:
        return None
    return max(offres, key=lambda x: x["value"])


@register.filter
def min_offre_value(offres):
    """Renvoie juste la valeur minimale parmi les offres"""
    min_obj = min_offre(offres)
    return min_obj["value"] if min_obj else Decimal("0")


@register.filter
def max_offre_value(offres):
    """Renvoie juste la valeur maximale parmi les offres"""
    max_obj = max_offre(offres)
    return max_obj["value"] if max_obj else Decimal("0")


@register.filter
def subtract(value, arg):
    """Soustrait arg de value"""
    return Decimal(str(value)) - Decimal(str(arg))


@register.filter
def divide(value, arg):
    """Divise value par arg, évite la division par zéro"""
    try:
        return Decimal(str(value)) / Decimal(str(arg))
    except (ZeroDivisionError, InvalidOperation):
        return Decimal("0")


@register.filter
def multiply(value, arg):
    """Multiplie value par arg"""
    return Decimal(str(value)) * Decimal(str(arg))


# Transformé en simple_tag pour accepter plusieurs arguments
@register.simple_tag
def sort_by_offre_for_lot(lignes, ligne_offres, lot_id):
    """Trie les soumissionnaires par offre croissante pour un lot donné"""
    result = []
    for ligne in lignes:
        offres_for_ligne = ligne_offres.get(ligne.id, {})
        offre_value = offres_for_ligne.get(lot_id)
        if (
            offre_value is not None
        ):  # Inclure seulement les soumissionnaires qui ont fait une offre
            # Récupérer l'offre d'origine et sa devise
            original_offre = None
            original_devise = None
            for offre in ligne.offres_lots.all():
                if offre.lot.id == lot_id:
                    original_offre = offre.offre_financiere
                    original_devise = offre.devise
                    break

            result.append(
                {
                    "soumissionnaire": ligne.soumissionnaire,
                    "offre_value": offre_value,
                    "original_offre": original_offre,
                    "original_devise": original_devise,
                    "observations": ligne.observations,
                }
            )
    # Trier par montant de l'offre (croissant)
    return sorted(result, key=lambda x: x["offre_value"])


# Transformé en simple_tag pour accepter plusieurs arguments
@register.simple_tag
def get_rang_for_lot(ligne, lignes, ligne_offres, lot_id):
    """Détermine le rang d'un soumissionnaire pour un lot spécifique"""
    sorted_lignes = sort_by_offre_for_lot(lignes, ligne_offres, lot_id)
    for i, item in enumerate(sorted_lignes):
        if item["soumissionnaire"].id == ligne.soumissionnaire.id:
            return i + 1
    return None


@register.filter
def avg_offre_value(offres_pour_lot):
    """Calcule la moyenne des offres pour un lot"""
    if not offres_pour_lot:
        return 0
    total = sum(offre["value"] for offre in offres_pour_lot)
    return total / len(offres_pour_lot)


@register.filter
def get_devise(ligne_id, lot_id, offres_lots):
    """Récupère la devise d'une offre"""
    for offre in offres_lots:
        if offre.ligne_rapport.id == ligne_id and offre.lot.id == lot_id:
            return offre.devise
    return "FCFA"  # Par défaut
