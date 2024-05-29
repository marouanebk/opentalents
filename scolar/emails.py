from django.core.mail import EmailMessage
from django.utils import timezone
from datetime import timedelta, datetime
from django.utils.timezone import activate
from django.conf import settings
from scolar.models import Formation, CP, Institution, Delegue
from views import trace_create  
import logging

def get_institution():
    institution_ = Institution.objects.all()
    if institution_.exists():
        return institution_[0]
    else:
        raise Exception

def signature_emails():
    institution = get_institution()
    return institution.signature_emails if institution.signature_emails else ''

def cp_remainder():
    # Set the time zone to Algeria
    activate("Africa/Algiers")
    
    # Configure logging
    logging.basicConfig(filename='cron/log/debug.log', level=logging.INFO)
    logging.info(f'Running cp_remainder function for the date: {timezone.now()}')
    
    # Get all formations with encours=True for the current year
    formations = Formation.objects.filter(annee_univ__encours=True)
    
    for formation in formations:
        # Get all CPs for this formation
        cps = CP.objects.filter(formation=formation)
        
        for cp in cps:
            # Check if CP's start date is within one week
            if cp.date_cp1:
                cp_date_debut_datetime = timezone.make_aware(datetime.combine(cp.date_cp1, datetime.min.time()))
                if cp_date_debut_datetime - timezone.now() == timedelta(days=7):
                    # Send email to enseignants and delegates of the formation
                    enseignants_emails = [enseignant.email for enseignant in cp.enseignants.all()]
                    delegues_emails = [delegue.email for delegue in Delegue.objects.filter(formation=formation).values_list('etudiants__email', flat=True)]
                    emails = enseignants_emails + delegues_emails
                    email = EmailMessage(
                        'Rappel: Date des Comités Pédagogiques Approchant',
                        f'Bonjour,\nLes dates des Comités Pédagogiques pour la formation {formation} approchent dans une semaine.\nDébut CP: {cp.date_cp1}\n{signature_emails()}',
                        to=emails
                    )
                    email.send(fail_silently=True)
                    logging.info(f'Emails sent for the CP: {cp.formation} on: {timezone.now()}')
                    for enseignant in cp.enseignants.all():
                        trace_create(None, enseignant, f"Rappel envoyé pour le CP de {formation} dans une semaine")
                    for delegue in Delegue.objects.filter(formation=formation):
                        trace_create(None, delegue.etudiants, f"Rappel envoyé pour le CP de {formation} dans une semaine")
                
                # Check if CP's start date is within 2 days
                if cp_date_debut_datetime - timezone.now() == timedelta(days=2):
                    emails = enseignants_emails + delegues_emails
                    email = EmailMessage(
                        'Rappel: Date des Comités Pédagogiques Approchant',
                        f'Bonjour,\nLes dates des Comités Pédagogiques pour la formation {formation} approchent dans 2 jours.\nDébut CP: {cp.date_cp1}\n{signature_emails()}',
                        to=emails
                    )
                    email.send(fail_silently=True)
                    logging.info(f'Emails sent for the CP: {cp.formation} on: {timezone.now()}')
                    for enseignant in cp.enseignants.all():
                        trace_create(None, enseignant, f"Rappel envoyé pour le CP de {formation} dans 2 jours")
                    for delegue in Delegue.objects.filter(formation=formation):
                        trace_create(None, delegue.etudiants, f"Rappel envoyé pour le CP de {formation} dans 2 jours")
            
            if cp.date_cp2:
                cp_date_fin_datetime = timezone.make_aware(datetime.combine(cp.date_cp2, datetime.min.time()))
                if cp_date_fin_datetime - timezone.now() == timedelta(days=7):
                    # Send email to enseignants and delegates of the formation
                    enseignants_emails = [enseignant.email for enseignant in cp.enseignants.all()]
                    delegues_emails = [delegue.email for delegue in Delegue.objects.filter(formation=formation).values_list('etudiants__email', flat=True)]
                    emails = enseignants_emails + delegues_emails
                    email = EmailMessage(
                        'Rappel: Date des Comités Pédagogiques Approchant',
                        f'Bonjour,\nLes dates des Comités Pédagogiques pour la formation {formation} approchent dans une semaine.\nFin CP: {cp.date_cp2}\n{signature_emails()}',
                        to=emails
                    )
                    email.send(fail_silently=True)
                    logging.info(f'Emails sent for the CP: {cp.formation} on: {timezone.now()}')
                    for enseignant in cp.enseignants.all():
                        trace_create(None, enseignant, f"Rappel envoyé pour le CP de {formation} dans une semaine")
                    for delegue in Delegue.objects.filter(formation=formation):
                        trace_create(None, delegue.etudiants, f"Rappel envoyé pour le CP de {formation} dans une semaine")
                
                # Check if CP's end date is within 2 days
                if cp_date_fin_datetime - timezone.now() == timedelta(days=2):
                    emails = enseignants_emails + delegues_emails
                    email = EmailMessage(
                        'Rappel: Date des Comités Pédagogiques Approchant',
                        f'Bonjour,\nLes dates des Comités Pédagogiques pour la formation {formation} approchent dans 2 jours.\nFin CP: {cp.date_cp2}\n{signature_emails()}',
                        to=emails
                    )
                    email.send(fail_silently=True)
                    logging.info(f'Emails sent for the CP: {cp.formation} on: {timezone.now()}')
                    for enseignant in cp.enseignants.all():
                        trace_create(None, enseignant, f"Rappel envoyé pour le CP de {formation} dans 2 jours")
                    for delegue in Delegue.objects.filter(formation=formation):
                        trace_create(None, delegue.etudiants, f"Rappel envoyé pour le CP de {formation} dans 2 jours")

# Run the function
cp_remainder()
