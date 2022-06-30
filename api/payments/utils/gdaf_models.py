from django.db.models import Sum

from gdaf.models import Contribuable, NoteImpositionPaiement


def get_montant_excedant(contribuable, get_objects=False):
    if not isinstance(contribuable, Contribuable):
        contribuable = Contribuable.objects.filter(reference=contribuable)

    return_data = 0
    if get_objects:
        return_data = 0, NoteImpositionPaiement.objects.none()

    if not contribuable:
        return return_data

    payments = NoteImpositionPaiement.objects.filter(
        note_imposition__contribuable=contribuable, montant_excedant__gt=0
    )
    excedant_sum = payments.aggregate(sumall=Sum("montant_excedant"))["sumall"] or 0

    return_data = excedant_sum
    if get_objects:
        return_data = excedant_sum, payments

    return return_data
