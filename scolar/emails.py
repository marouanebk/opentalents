from django.core.mail import EmailMessage
from django.utils import timezone
from datetime import timedelta,datetime
from django.utils.timezone import activate
from django.conf import settings
from scolar.models import Formation,CP,Institution
import logging

def get_institution():
    institution_ = Institution.objects.all()
    if institution_.exists():
        return institution_[0]
    else :
        raise Exception
    
def signature_emails(): 
    institution=get_institution()
    return institution.signature_emails if institution.signature_emails else ''

def cp_remainder():
    # Set the time zone to Algeria
    activate("Africa/Algiers")
  

# Configure logging
    logging.basicConfig(filename='cron/log/debug.log', level=logging.INFO)
    logging.info(f'Running cp_remainder function for the date : {timezone.now()}' )
    # Get all formations with encours=True for the current year
    formations = Formation.objects.filter(annee_univ__encours=True)
    
    for formation in formations:
        # Get all CPs for this formation
        cps = CP.objects.filter(formation=formation)
        
        for cp in cps:
            # Check if CP's start date is within one week
         if (cp.date_debut_semester):
            cp_date_debut_datetime = timezone.make_aware(datetime.combine(cp.date_debut_semester, datetime.min.time()))
            if cp_date_debut_datetime - timezone.now() == timedelta(days=7):
                # Send email to enseignants
                enseignants_emails = [enseignant.email for enseignant in cp.enseignants.all()]
                delegues_emails = [delegue.email for delegue in cp.delegues.all()]
                emails=enseignants_emails+delegues_emails
                email = EmailMessage('Reminder: CP Start Date Approaching',
                                 'Bonjour,\n'+ 
                                 "The start date of CP {cp} is approaching within one week."+
                                 signature_emails(), to=emails)
            
                email.send(fail_silently=True)
                logging.info(f'emails sent for the cp: {cp.formation} in : {timezone.now()}' )
            # Check if CP's end date is within 2 days
            if  cp_date_debut_datetime - timezone.now() == timedelta(days=2):
                enseignants_emails = [enseignant.email for enseignant in cp.enseignants.all()]
                delegues_emails = [delegue.email for delegue in cp.delegues.all()]
                emails=enseignants_emails+delegues_emails
                email = EmailMessage('Reminder: CP Start Date Approaching'
                                 'Bonjour,\n'+ 
                                 "The start date of CP {cp} is approaching within 2 days."+
                                 signature_emails(), to=emails
                                                    )
            
                email.send(fail_silently=True)
                logging.info(f'emails sent for the cp: {cp.formation} in : {timezone.now()}' )
         if (cp.date_fin_semester):
            cp_date_fin_datetime = timezone.make_aware(datetime.combine(cp.date_fin_semester, datetime.min.time()))
            if cp_date_fin_datetime - timezone.now() == timedelta(days=7):
                # Send email to enseignants
                enseignants_emails = [enseignant.email for enseignant in cp.enseignants.all()]
                delegues_emails = [delegue.email for delegue in cp.delegues.all()]
                emails=enseignants_emails+delegues_emails
                email = EmailMessage('Reminder: CP Start Date Approaching',
                                 'Bonjour,\n'+ 
                                 "The start date of CP {cp} is approaching within one week."+
                                 signature_emails(), to=emails)
            
                email.send(fail_silently=True)
                logging.info(f'emails sent for the cp: {cp.formation} in : {timezone.now()}' )
            # Check if CP's end date is within 2 days
            if  cp_date_fin_datetime - timezone.now() == timedelta(days=2):
                enseignants_emails = [enseignant.email for enseignant in cp.enseignants.all()]
                delegues_emails = [delegue.email for delegue in cp.delegues.all()]
                emails=enseignants_emails+delegues_emails
                email = EmailMessage('Reminder: CP Start Date Approaching'
                                 'Bonjour,\n'+ 
                                 "The start date of CP {cp} is approaching within 2 days."+
                                 signature_emails(), to=emails
                                                    )
            
                email.send(fail_silently=True)
                logging.info(f'emails sent for the cp: {cp.formation} in : {timezone.now()}' )

cp_remainder()