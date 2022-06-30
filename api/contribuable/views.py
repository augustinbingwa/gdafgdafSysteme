from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework import status
from api.serializers import NoteImpositionSerializer
import json
import collections

from mod_finance.models import NoteImposition
from mod_crm.models import Contribuable,PersonnePhysique

class amountToPaybyNic(APIView):
    def post(selfs,request):
        nic = request.data['nic']
        entity = request.data['entity']
        try:
            contribuable = Contribuable.objects.get(matricule=nic)
            try:
                note = NoteImposition.objects.filter(entity=entity,contribuable_id=contribuable.id)
            except:
                return JsonResponse({'message': 'The note does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except :
            return JsonResponse({'message': 'The matricule does not exist'}, status=status.HTTP_404_NOT_FOUND)

        list = ''
        for nt in note:
            if nt.taxe_montant_paye < nt.taxe_montant:
                list += "{'reference':"+nt.reference+"},"
        # print(json.dumps(list))
        data = {
            'contribuable': [
                {
                    'matricule': contribuable.matricule,
                    'nom': contribuable.nom,
                }
            ],

        }

        return JsonResponse(data)

class allAmountToPaybyNic(APIView):
    def post(selfs,request):
        nic = request.data['nic']
        try:
            contribuable = Contribuable.objects.get(matricule=nic)
            note = NoteImposition.objects.filter(contribuable_id=contribuable.id)
        except :
            return JsonResponse({'message': 'The matricule does not exist'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'contribuable': [
                {
                    'matricule': contribuable.matricule,
                    'nom': contribuable.nom,
                }
            ],
        }
        return JsonResponse(data)

class amountToPaybyIdCard(APIView):
    def post(selfs,request):
        cni = request.data['cni']
        entity = request.data['entity']
        try:
            contribuable = PersonnePhysique.objects.get(identite_numero=cni)
            note = NoteImposition.objects.filter(entity=entity, contribuable_id=contribuable.id)
        except :
            return JsonResponse({'message': cni +' does not exist'}, status=status.HTTP_404_NOT_FOUND)

        for ni in note:
            if ni.taxe_montant_paye < ni.taxe_montant:
                print(ni)

        data = {
            'contribuable': [
                {
                    'matricule': contribuable.matricule,
                    'nom': contribuable.nom,
                    'cni': contribuable.identite_numero,
                }
            ],
        }

        return JsonResponse(data)

class allAmountToPaybyIdCard(APIView):
    def post(selfs,request):
        cni = request.data['cni']
        try:
            contribuable = PersonnePhysique.objects.get(identite_numero=cni)
            note = NoteImposition.objects.filter(contribuable_id=contribuable.id)
        except :
            return JsonResponse({'message': cni +' does not exist'}, status=status.HTTP_404_NOT_FOUND)

        for ni in note:
            if ni.taxe_montant_paye < ni.taxe_montant:
                print(ni)

        data = {
            'contribuable': [
                {
                    'matricule': contribuable.matricule,
                    'nom': contribuable.nom,
                    'cni': contribuable.identite_numero,
                }
            ],
        }

        return JsonResponse(data)