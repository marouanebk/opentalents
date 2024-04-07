from django.db import models
from django.db.models.deletion import CASCADE
from django.core.validators import RegexValidator, URLValidator
from django.db import transaction
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.fields import CharField
import decimal
from django.db.models import Q, F, Count, ExpressionWrapper, DecimalField, Avg, Max, Min, Sum, FloatField
import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group, Permission
from random import randint
from django.core.exceptions import ValidationError
import re
from django.utils.translation import ugettext as _
from django.apps import apps
from django.utils import timezone
from django.db.models import When, Value, Case, BooleanField
from django_cleanup import cleanup
import random
import string
from django.core.validators import FileExtensionValidator

class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

class User(AbstractUser):
    #REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()
    email = models.EmailField(
        verbose_name=("Email"), null=True, default=None, blank=True,
    )
   
@cleanup.ignore                
class Institution(models.Model):
    nom_plateforme = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nom de la plateforme")
    nom = models.CharField(max_length=100, verbose_name="Nom de l'établissement")
    nom_a = models.CharField(max_length=100, default='', verbose_name="Nom de l'établissement en arabe")
    sigle = models.CharField(max_length=10, verbose_name="Sigle de l'établissement")
    adresse = models.TextField()
    ville = models.CharField(max_length=50, default='')
    ville_a = models.CharField(max_length=50, default='', verbose_name="Ville en arabe")
    wilaya_institution = models.ForeignKey('Wilaya', on_delete=models.SET_NULL, null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True, validators=[RegexValidator('^[0-9\+]*$',
                               'Que des chiffres sans espaces et le + pour l\'international')])
    fax = models.CharField(max_length=20, null=True, blank=True, validators=[RegexValidator('^[0-9\+]*$',
                               'Que des chiffres sans espaces et le + pour l\'international')])
    web = models.URLField(null=True, blank=True, verbose_name="Site web")
    illustration_cursus = models.ImageField(upload_to='admin', null=True, blank=True )
    logo = models.ImageField(upload_to='admin', null=True, blank=True, verbose_name="Logo de l'établissement")
    logo_bis = models.ImageField(upload_to='admin', null=True, blank=True, verbose_name="Logo de la plateforme")
    banniere = models.ImageField(upload_to='admin', null=True, blank=True )
    header =  models.ImageField(upload_to='admin', null=True, blank=True, verbose_name="Entête des documents")
    footer =  models.ImageField(upload_to='admin', null=True, blank=True, verbose_name="Pied des documents")
    reference=models.CharField(max_length=50, null=True, blank=True, verbose_name="Référence des documents")
    identifiant_progres = models.CharField(max_length=50, null=True, blank=True)
    code_etablissement= models.CharField(max_length=50, null=True, blank=True,help_text="Veuillez insérer -code établissement- utilisé dans les fichiers de service national.")
    email_domain = models.CharField(max_length=100, null=True, blank=True, verbose_name="Domaine d'emails (exemple : institution.dz)")
    color = models.CharField(max_length=10, default="#343A40", verbose_name="Code couleur (HEX) de la plateforme (exemple : #343A40) ")
    users_direction=models.ManyToManyField('User', blank=True, verbose_name="Utilisateurs qui seront notifiés par e-mail en tant que direction", related_name='institution_direction')
    users_scolarite=models.ManyToManyField('User', blank=True, verbose_name="Utilisateurs qui seront notifiés par e-mail en tant que scolarité", related_name='institution_scolarite')
    users_stage=models.ManyToManyField('User', blank=True, verbose_name="Utilisateurs qui seront notifiés par le déroulement du processus de validation des stages de fin d'études", related_name='institution_stage')
    email_futurs_stagiaires = models.EmailField(null=True, blank=True, verbose_name="Adresse e-mail de diffusion des futurs stagiaires (qui sera notifiée par les nouveaux sujets de stage de fin d'études déposés)")
    users_theses=models.ManyToManyField('User', blank=True, verbose_name="Utilisateurs qui seront notifiés par le déroulement des processus de gestion des thèses de post-graduation", related_name='institution_theses')
    users_offres=models.ManyToManyField('User', blank=True, verbose_name="Utilisateurs qui seront notifiés par le déroulement des processus de gestion des offres (emplois, thèses, stages pratiques, etc.)", related_name='institution_offres')
    users_demandes_comptes=models.ManyToManyField('User', blank=True, verbose_name="Utilisateurs qui seront notifiés par les nouvelles demandes de compte (pour publier des offres, stages, etc.) (la fonctionnalité doit d'abord être activée)", related_name='institution_demandes_comptes')
    email_webmaster = models.EmailField(null=True, blank=True, verbose_name="Adresse e-mail du webmaster (pour notifications)")
    signature_emails=models.CharField(max_length=100, null=True, blank=True, help_text="La signature qui sera envoyée en bas de chaque mail de notification")
    activation_emails=models.BooleanField(default=True, verbose_name="Notifications par mail activées")
    activation_ddc=models.BooleanField(default=True, verbose_name="Domaines de connaissances activés")
    activation_competences=models.BooleanField(default=True, verbose_name="Ingénierie des compétences activée")
    activation_livret_competences=models.BooleanField(default=False, verbose_name="Livrets des compétences des étudiants activés (uniquement si l'ingénierie des compétences est activée)")
    activation_charges=models.BooleanField(default=True, verbose_name="Charges des enseignants activées")
    activation_google_agenda=models.BooleanField(default=True, verbose_name="Google Agenda activé")
    activation_authentification_google=models.BooleanField(default=True, verbose_name="Authentification Google (OAuth) activée")
    activation_feedback=models.BooleanField(default=True, verbose_name="Feedbacks des étudiants sur les enseignements activés")
    activation_theses=models.BooleanField(default=False, verbose_name="Thèses de post-graduation activées")
    activation_webhelp=models.BooleanField(default=False, verbose_name="Activation de la Web-Help (aide contextuelle en ligne)")
    activation_lettres_recommandation=models.BooleanField(default=True, verbose_name="Modèles de lettres de recommandation à générer par les enseignants au profit des étudiants activés")
    activation_enregistrement_etudiants=models.BooleanField(default=False, verbose_name="Demandes d'enregistrement des étudiants activées")
    activation_offres=models.BooleanField(default=False, verbose_name="Offres (emplois, thèses, stages pratiques, etc.) activées")
    activation_demandes_comptes=models.BooleanField(default=False, verbose_name="Demandes de création des comptes sur la plateforme activées (pour les personnes souhaitant déposer des offres d'emplois et/ou stages de fin d'études")
    activation_public_stages=models.BooleanField(default=False, verbose_name="Liste des stages visibles aux visiteurs")
    activation_public_projets=models.BooleanField(default=False, verbose_name="Projets de recherche visibles aux visiteurs")
    activation_public_equipesrecherche=models.BooleanField(default=False, verbose_name="Equipes de recherche visibles aux visiteurs")
    
   
class DomaineConnaissance(models.Model):
    '''
    Cette classe sert à catégoriser les matière en domaines de connaissance globaux
    '''
    intitule=models.CharField(max_length=80)
    description=models.TextField(null=True, blank=True)
    def __str__(self):
        return self.intitule


# Create your models here.

class Matiere(models.Model):
    '''
    La marière est l'élément de base de la formation.
    Une matière fait partie d'une Unité d'enseignement
    '''
    code=models.CharField(max_length=20)
    precision = models.CharField(max_length=10, null=True, blank=True)
    ddc=models.ForeignKey(DomaineConnaissance, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="DDC(Domaine de connaissances)")
    titre=models.CharField(max_length=80)
    titre_a=models.CharField(max_length=80, null=True, blank=True, verbose_name="Titre en arabe")
    titre_en=models.CharField(max_length=80, null=True, blank=True, verbose_name="Titre en anglais")
    coef=models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=1.0)
    credit=models.IntegerField(blank=True, default=0)
    edition=models.CharField(max_length=5, null=True, blank=True, help_text="Par exemple l'année de l'arrêté ministériel définissant la matière")
    vh_cours=models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Volume horaire cours")
    vh_td=models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Volume horaire TD")
    vh_tp=models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Volume horaire TP")
    pre_requis=models.TextField(null=True, blank=True)
    objectifs=models.TextField(null=True, blank=True)
    contenu=models.TextField(null=True, blank=True)
    travail_perso=models.TextField(null=True, blank=True)
    bibliographie=models.TextField(null=True, blank=True)
    mode_projet=models.BooleanField(default=False, verbose_name="Mode projet : Permet d'adapter les critères de Feedback")
    pfe=models.BooleanField(default=False, verbose_name="Projet/Matière de fin d'études avec soutenance finale")
    equipe=models.BooleanField(default=False, verbose_name="Matière en équipe, avec soutenance des groupes d'étudiants")
    seminaire=models.BooleanField(default=False, verbose_name="Séminaire")
    validable=models.BooleanField(default=False, verbose_name="Matière d'un stage sans note, avec deux états : Validé, Non validé, états qui apparaitront dans les relevés de notes.")
    
    def __str__(self):
        if self.precision:
            return f"{self.code} {self.precision}"
        else:
            return self.code
        
    
class Specialite(models.Model):
    code=models.CharField(max_length=5, primary_key=True)
    intitule=models.CharField(max_length=100)
    intitule_a=models.CharField(max_length=100, null=True, blank=True, verbose_name="Intitulé arabe")
    title=models.CharField(max_length=100, null=True, blank=True, verbose_name="Intitulé anglais")
    concernee_par_pfe=models.BooleanField(default=True, verbose_name="Spécialité concernée par les stages de fin d'études (afin de l'afficher dans la liste des spécialités lors du dépôt d'un stage)")
    def __str__(self):
        return f"{self.code}: {self.intitule}"

class AnneeUniv(models.Model):
    '''
    Année Universitaire qui comprend plusieurs formations
    '''
    annee_univ=models.CharField(max_length=9, unique=True, primary_key=True)
    debut=models.DateField()
    fin=models.DateField()
    encours=models.BooleanField(default=False,  blank=True)
    


    

class Periode(models.Model):
    '''
    Ca peut être un semestre ou trimestre ou autre. 
    '''
    code=models.CharField(max_length=2, null=True, choices=(('S1','Semestre 1'),('S2', 'Semestre 2'), ('T1', 'Trimestre 1'),('T2', 'Trimestre 2'),('T3', 'Trimestre 3'), ('AN', 'Annuel')))
    ordre=models.IntegerField()
    nb_semaines=models.IntegerField(null=True, blank=True, default=15)
    session=models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.code

SEXE=(
    ('', '---'),
    ('M','Masculin'),
    ('F','Féminin'),
)

class Personnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    nom=models.CharField(max_length=50)
    eps=models.CharField(max_length=50, null=True, blank=True)
    prenom=models.CharField(max_length=50)
    nom_a=models.CharField(max_length=50, null=True, blank=True, verbose_name="Nom en arabe")
    eps_a=models.CharField(max_length=50, null=True, blank=True, verbose_name="Eps en arabe")
    prenom_a=models.CharField(max_length=50, null=True, blank=True, verbose_name="Prénom en arabe")
    sexe=models.CharField(max_length=1, choices=SEXE, null=True, blank=True)
    tel=models.CharField(max_length=15, null=True, blank=True)
    bureau=models.CharField(max_length=10, null=True, blank=True)
    
    def get_email(self):
        return self.user.get_email() if self.user else ''
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"

STATUT=(
    ('', '---'),
    ('P','Permanent'),
    ('V','Vacataire'),
    ('A','Associé'),
    ('D','Doctorant'),
)

GRADE=(
    ('', '---'),
    ('MA','Maître Assistant'),
    ('MA.B','Maître Assistant B'),
    ('MA.A','Maître Assistant A'),
    ('MC','Maître de Conférences'),
    ('MC.B','Maître de Conférences B'),
    ('MC.A','Maître de Conférences A'),
    ('PR','Professeur'),
)

SITUATION=(
    ('', '---'),
    ('A','En activité'),
    ('D','Mise en disponibilité'),
    ('T','Détachement'),
    ('M','Congé de Maladie'),
    ('I','Invalidité'),
    ('R','Retraité'),
    ('X','Départ: Mutation, Démission, ...'),
)




class Enseignant(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    nom=models.CharField(max_length=50)
    eps=models.CharField(max_length=50, null=True, blank=True)
    prenom=models.CharField(max_length=50)
    nom_a=models.CharField(max_length=50, null=True, blank=True, verbose_name="Nom en arabe")
    eps_a=models.CharField(max_length=50, null=True, blank=True, verbose_name="Eps en arabe")
    prenom_a=models.CharField(max_length=50, null=True, blank=True, verbose_name="Prénom en arabe")
    sexe=models.CharField(max_length=1, choices=SEXE, null=True, blank=True)
    tel=models.CharField(max_length=15, null=True, blank=True)
    grade=models.CharField(max_length=4, choices=GRADE, null=True, blank=True)
    charge_statut=models.DecimalField(max_digits=5, decimal_places=2, default=288, blank=True)
    situation=models.CharField(max_length=1, null=True, blank=True, choices=SITUATION, default='A')
    statut=models.CharField(max_length=1, null=True, blank=True, choices = STATUT, default='P')
    bureau=models.CharField(max_length=10, null=True, blank=True)
    bal=models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Boîte aux lettres')
    edt=models.TextField(null=True,blank=True, verbose_name="Emploi du temps")
    webpage=models.URLField(null=True, blank=True)
    otp=models.CharField(max_length=6, null=True, blank=True, default='')
    photo=models.ImageField(upload_to='photos',null=True,blank=True, validators=[validate_image])
    public_profile=models.BooleanField(default=False, verbose_name='Profil public')
    bio=models.TextField(null=True,blank=True)
    publications=models.TextField(null=True,blank=True, validators=[validate_url_list], verbose_name="URLs des profils scientifiques (Google Scholar, ResearchGate, DBLP, ..), séparées par des sauts de ligne")
    date_naissance=models.DateField(null=True, blank=True,verbose_name='Date de naissance')
    date_embauche=models.DateField(null=True, blank=True,verbose_name="Date d'embauche")
    matricule=models.CharField(max_length=20, null=True, blank=True)
    organisme=models.ForeignKey('Organisme', on_delete=models.SET_NULL, null=True, blank=True, related_name='enseignants', verbose_name="Laboratoire/service/..")
   
class Autorite(models.Model):
    intitule=models.CharField(max_length=100, verbose_name="Intitulé")
    intitule_a=models.CharField(max_length=100, null=True, blank=True, verbose_name="Intitulé arabe")
    intitule_en=models.CharField(max_length=100, null=True, blank=True, verbose_name="Intitulé anglais")
    responsable=models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True, blank=True)
    titre_responsable=models.CharField(max_length=100, null=True, blank=True, verbose_name="Titre du responsable")
    titre_responsable_a=models.CharField(max_length=100, null=True, blank=True, verbose_name="Titre du responsable en arabe")
    titre_responsable_en=models.CharField(max_length=100, null=True, blank=True, verbose_name="Titre du responsable en anglais")
    signature=models.ImageField(upload_to='admin', null=True, blank=True)
    autorite=models.ForeignKey('Autorite', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Autorité mère", related_name="autorites_filles")
    
    def get_email_responsable(self):
        return self.responsable.get_email() if self.responsable else ''
    
    def __str__(self):
        if self.responsable:
            return f"{self.intitule} - Responsable : {self.responsable}"
        return self.intitule
    
        
class Cycle(models.Model):
    ordre=models.PositiveSmallIntegerField(null=True, blank=True)
    intitule=models.CharField(max_length=100)
    intitule_a=models.CharField(max_length=100, null=True, blank=True, verbose_name="Intitulé arabe")
    intitule_en=models.CharField(max_length=100, null=True, blank=True, verbose_name="Intitulé anglais")
    autorite=models.ForeignKey(Autorite, on_delete=models.SET_NULL, null=True, blank=True)
    reglement=models.FileField(upload_to='admin', null=True, blank=True)
    activation_rattrapage=models.BooleanField(default=False, verbose_name="Activation session rattrapages pour les programmes du cycle")
    activation_credits=models.BooleanField(default=False, verbose_name="Activation des crédits pour les programmes du cycle")
    activation_ues=models.BooleanField(default=False, verbose_name="Activation des unités d'enseignement (UE)s pour les programmes du cycle")
    activation_dettes=models.BooleanField(default=False, verbose_name="Activation des dettes pour les programmes du cycle")
    users_visualisation_notes=models.ManyToManyField('User', blank=True, verbose_name="Utilisateurs pouvant visualiser les notes du cycle", related_name='cycles_avec_acces_visualisation_notes')
    users_gestion_notes=models.ManyToManyField('User', blank=True, verbose_name="Utilisateurs pouvant gérer les notes du cycle", related_name='cycles_avec_acces_gestion_notes')
    users_gestion_etudiants=models.ManyToManyField('User', blank=True, verbose_name="Utilisateurs pouvant gérer les inscriptions du cycle : Modification groupes, décisions jury, observations, ..", related_name='cycles_avec_acces_gestion_etudiants')
    
    def get_email_responsable_autorite(self):
        return self.autorite.get_email_responsable() if self.autorite else ''
                
    def __str__(self):
        return self.intitule
    
class Diplome(models.Model):
    intitule=models.CharField(max_length=100)
    intitule_a=models.CharField(max_length=100, null=True, verbose_name="Intitulé en arabe")
    intitule_en=models.CharField(max_length=100, null=True, verbose_name="Intitulé en anglais", blank=True)
    domaine = models.CharField(max_length=100, null=True)
    domaine_a = models.CharField(max_length=100, null=True, blank=True, verbose_name="Domaine en arabe")
    domaine_en = models.CharField(max_length=100, null=True, blank=True, verbose_name="Domaine en anglais")
    filiere = models.CharField(max_length=100, null=True)
    filiere_a = models.CharField(max_length=100, null=True, blank=True, verbose_name="Filière en arabe")
    filiere_en = models.CharField(max_length=100, null=True, blank=True, verbose_name="Filière en anglais")
    code_filiere= models.CharField(max_length=100, null=True, blank=True,help_text="Veuillez insérer -Code de spécialité- utilisé dans les fichiers de service national.")
    code_diplome=models.CharField(max_length=100, null=True, blank=True,help_text="Veuillez insérez -Code de diplôme- utilisé dans les fichiers de service national.")
    code_cycle=models.CharField(max_length=100, null=True, blank=True,help_text="Veuillez insérez -Code de cycle- utilisé dans les fichiers de service national.")
    
    def __str__(self):
        return self.intitule
    
class Programme(models.Model):
    '''
    description statique des programmes
    '''
    code=models.CharField(max_length=18, unique=True)
    titre=models.CharField(max_length=100)
    titre_a=models.CharField(max_length=100, null=True, verbose_name="Titre en arabe")
    titre_en=models.CharField(max_length=100, null=True, verbose_name="Titre en anglais", blank=True)
    doctorat=models.BooleanField(default=False, verbose_name="Programme de post-graduation", blank=True)
    specialite=models.ForeignKey(Specialite, null=True, blank=True, on_delete=models.SET_NULL)
    description=models.TextField()
    diplome=models.ForeignKey(Diplome, on_delete=models.SET_NULL, null=True, blank=True)
    cycle=models.ForeignKey(Cycle, on_delete=models.SET_NULL, null=True, blank=False)
    #signature_par_autorite=models.BooleanField(default=False, verbose_name="Cochez si les documents liés au programme sont signés par l'autorité associée au programme, sinon ils seront signés par l'autorité associée au cycle")
    ordre=models.PositiveSmallIntegerField(null=True, blank=True)
    # si concours à la fin de ce programme car ça influt sur les décisions de jurys possibles.
    concours=models.BooleanField(default=False)
    assistant=models.ForeignKey(Personnel, on_delete=models.SET_NULL, null=True, blank=True)
    fictif=models.BooleanField(default=False, verbose_name="Programme fictif (Pour ne pas l'afficher dans les feedbacks, statistiques : Cas de Stages SPE / Programmes de doctorat)")
    matiere_equipe=models.ForeignKey(Matiere, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Matière en équipe concernée par le programme fictif")
    code_serv_national=models.CharField(max_length=18, null=True, blank=True,help_text="Insérer le code niveau utilisé dans les fichiers de service national")
    programme_complementaire_master=models.BooleanField(default=False, verbose_name="Programme complémentaire de Master (Le relevé provisoire des étudiants sera différent des autres programmes)")
   

class PeriodeProgramme(models.Model):
    periode=models.ForeignKey(Periode, on_delete=CASCADE)
    programme=models.ForeignKey(Programme, on_delete=CASCADE, related_name='periodes')
    # Ce code correspond à la codification du décrêt, par exemple en 2CS ce sera S3, S4, en 3CS, S5, S6
    # L'attribut code de la classe Periode correspond à la période chronologique dans l'année S1, S2, ou TR1, TR2, TR3, ...
    code = models.CharField(max_length = 10, null =True, blank=True, choices = PERIODES)
    
    def nb_matieres(self):
        somme=0
        for ue in self.ues.all():
            somme+=ue.nb_matieres()
        return somme

    def credit(self):
        somme=0
        ue_option_comptabilisee_list=[]
        for ue in self.ues.all():
            if ue.nature=='OBL':
                somme+=ue.credit()
            elif not ue.code in ue_option_comptabilisee_list:
                somme+=ue.credit()
                ue_option_comptabilisee_list.append(ue.code) 
        return somme
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['programme', 'periode'], name="periode-programme")
        ]

    def __str__(self):
        return f"{self.programme} {self.periode}"

CAT_UE = (
    ('F','UE Fondamentale'),
    ('M','UE Méthodologique'),
    ('T','UE Transversale'),
    ('D','UE Découverte'),
)

class UE(models.Model):
    '''
    Un programme est composé de plusieurs UE
    '''
    '''
    Une UE obligatoire figure nécessairement dans tous les relevés de note
    Une UE optionnelle est composée de matières au choix dans la limite du nombre de crédits alloués à l'UE
    Donc plusieurs instances de l'UE sont créées en fonction des choix
    C'est dans Formation qui est l'instance temporelle de Programme qu'on fixe la liste des options retenues pour la promotion
    Puis dans le groupe on précise les UE spécifique à une option
    '''
    NATURES = (
        ('OBL','Obligatoire'),
        ('OPT','Optionnelle'),
    )
    code=models.CharField(max_length=8)
    code_a=models.CharField(max_length=20, null=True, blank=True, verbose_name="Code en arabe (uniquement pour le relevé de notes en arabe)")
    type=models.CharField(max_length=1, choices=CAT_UE)
    nature=models.CharField(max_length=3, choices=NATURES, null=True)
    matieres=models.ManyToManyField(Matiere, blank=True, related_name='matiere_ues')
    periode=models.ForeignKey(PeriodeProgramme, on_delete=CASCADE, null=True, blank=True, related_name='ues')
    coefold=models.IntegerField(null=True)
    

 
class Formation(models.Model):
    '''
    Formation correspond à un pallier ou spécialité
    '''
    programme=models.ForeignKey(Programme, on_delete=CASCADE)
    annee_univ=models.ForeignKey(AnneeUniv, on_delete=CASCADE)
    archive=models.BooleanField(default=False)
    moyenne_passage=models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=10.0)
    
    

class PeriodeFormation(models.Model):
    formation = models.ForeignKey(Formation, on_delete=CASCADE, null=True, blank=True, related_name='periodes')
    periode = models.ForeignKey(Periode, on_delete=CASCADE, null=True, blank=True)
    session = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return f"{self.formation} {self.periode.code} {self.session}"
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['formation', 'periode'], name="formation-periode")
        ]

class PV(models.Model):
    formation=models.ForeignKey(Formation, on_delete=models.SET_NULL, null=True, blank=True)
    content=models.TextField()
    annuel=models.BooleanField(default=False)
    periode=models.ForeignKey(Periode, on_delete=models.SET_NULL, null=True, blank=True)
    tri_rang=models.BooleanField(default=True)
    photo=models.BooleanField(default=True)
    anonyme=models.BooleanField(default=False)
    note_eliminatoire=models.BooleanField(default=True)
    moy_ue=models.BooleanField(default=False)
    rang=models.BooleanField(default=True)
    signature=models.BooleanField(default=True)
    reserve=models.BooleanField(default=False)
    post_rattrapage=models.BooleanField(default=False)
    date=models.DateField(null=True, blank=True)
    xlsx=models.FileField(upload_to='files/pvs', null=True, blank=True) 

    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['formation', 'annuel', 'periode', 'tri_rang', 'photo', 'anonyme', 'note_eliminatoire', 'rang','signature', 'post_rattrapage'], name="pv_config")
        ]
    def __str__(self):
        pv = f"PV {self.formation}"
        if not self.annuel:
            pv+=' '+str(self.periode)
        if self.tri_rang:
            pv+=' Rang'
        if self.note_eliminatoire:
            pv+=' NE'
        if self.photo:
            pv+=' Photos'
        if self.signature:
            pv+=' Sig'
        if self.post_rattrapage:
            pv+=' Post-Rattrapage'
        if self.anonyme:
            pv+=' Anonyme'
        return pv
    

class Module(models.Model):
    '''
    Il s'agit d'une instance d'une matière dans une formation
    '''
    matiere=models.ForeignKey(Matiere, on_delete=CASCADE)
    formation=models.ForeignKey(Formation, on_delete=CASCADE, related_name='modules')
    periode=models.ForeignKey(PeriodeProgramme, on_delete=models.SET_NULL, null=True, blank=True)
    # TODO on doit pas cascader delete de periode sinon on perd la base en un click
    coordinateur=models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True, blank=True)
    note_eliminatoire=models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=5.0)
    ponderation_moy=models.DecimalField(max_digits=3, decimal_places=2, default=0, blank=True, verbose_name="Pondération Moy Session Normale (de 0.00 à 1.00)")
    ponderation_moy_rattrapage=models.DecimalField(max_digits=3, decimal_places=2, default=0, blank=True, verbose_name="Pondération Moy Session Rattrapage (de 0.00 à 1.00)")
    activation_max_moy_normale_et_rattrapage=models.BooleanField(default=True, verbose_name="Comptabilisation du maximum entre la moyenne normale et la moyenne de rattrapage")
    seuil_rattrapage=models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=10.0)
    

    
class Evaluation(models.Model):
    '''
    On définit ici les évlautaions prévues dans un module
    '''
    type=models.CharField(max_length=20,choices=TYPES_EVAL)
    ponderation=models.DecimalField(max_digits=6, decimal_places=5, default=0, verbose_name="Pondération")
    ponderation_rattrapage=models.DecimalField(max_digits=6, decimal_places=5, default=0, blank=True)
    module=models.ForeignKey(Module,on_delete=CASCADE, related_name='evaluations')
    
    def __str__(self):
        return f"{self.type} {self.module}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['type', 'module'], name="eval-module")
    ]

    
class Section(models.Model):
    '''
    Section de cours. Une formation est organisée en sections
    '''

    code=models.CharField(max_length=1,null=True,choices=CODES_SEC)
    formation=models.ForeignKey(Formation, on_delete=CASCADE, null=True, related_name='sections')




    

class Groupe(models.Model):
    '''
    Groupe de TD ou TP
    UN groupe appartient à une section
    Un groupe particulier est créé automatiquement pour représenter une section et qui porte un code null
    '''
    code=models.CharField(max_length=10,null=True)
    section=models.ForeignKey(Section, on_delete=CASCADE, null=True, related_name='groupes')
    option=models.ManyToManyField(UE, blank=True)
    edt=models.TextField(null=True,blank=True, default='Agenda Empty')





class ModulesSuivis(models.Model):
    SAISIE_ETAT=(
        ('N','Pas encore'),
        ('C','En cours'),
        ('T','Terminé'),
    )

    module=models.ForeignKey(Module, on_delete=CASCADE, related_name='groupes_suivis')
    groupe=models.ForeignKey(Groupe, on_delete=CASCADE, related_name='modules_suivis')
    saisie_notes=models.CharField(max_length=1, choices= SAISIE_ETAT, default='N')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['module', 'groupe'], name="module-groupe")
        ]
        indexes = [
            models.Index(fields = ['module', 'groupe'])
        ]
        

class Activite(models.Model):
    '''
    Il y a plusieurs activités dans un module comme un cours + TD + TP ...
    '''
    type=models.CharField(max_length=10,choices=TYPES_ACT)
    module=models.ForeignKey(Module, on_delete=CASCADE)
    cible=models.ManyToManyField(Groupe, blank=True, related_name='activites')
    assuree_par=models.ManyToManyField(Enseignant, related_name='enseignants')
    vh=models.DecimalField(max_digits=4, decimal_places=2, null=True, verbose_name="Volume horaire")
    repeter_chaque_semaine=models.BooleanField(default=True)
    repartir_entre_intervenants=models.BooleanField(default=False)
    
  
        
    class Meta:
        indexes = [
            models.Index(fields=['module'])
        ]
    
    def __str__(self):
        cible_str = " + ".join(str(groupe) for groupe in self.cible.all())
        return f"{dict(TYPES_ACT)[self.type]}: {self.module.matiere.code} + {cible_str}"



class ActiviteChargeConfig(models.Model):
    categorie=models.CharField(max_length=5, choices=TYPE_CHARGE, null=True )
    type=models.CharField(max_length=10)
    titre=models.CharField(max_length=50, null=True)
    vh=models.DecimalField(max_digits=5, decimal_places=2, default=0)
    vh_eq_td=models.DecimalField(max_digits=5, decimal_places=2, default=0)
    repeter_chaque_semaine=models.BooleanField(default=True)
    repartir_entre_intervenants=models.BooleanField(default=False)
    def __str__(self):
        return f"{dict(TYPE_CHARGE)[self.categorie]} {self.titre}"
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['type'], name="activite-charge_config")
        ]
    
class Charge(models.Model):
    '''
        Charge d'un enseignant issue de ses activités d'enseignement, encadrement, administration, surveillance, missions, etc.
    '''
    type=models.CharField(max_length=1, choices=TYPE_CHARGE)
    activite=models.ForeignKey(Activite, on_delete=CASCADE, null=True, blank=True)
    obs=models.CharField(max_length=50, null=True, blank=True)
    vh=models.DecimalField(max_digits=5, decimal_places=2, default=0)
    vh_eq_td=models.DecimalField(max_digits=5, decimal_places=2, default=0)
    annee_univ=models.ForeignKey(AnneeUniv, on_delete=models.SET_NULL, null=True)
    periode = models.ForeignKey(Periode, on_delete=models.SET_NULL, null=True)
    realisee_par=models.ForeignKey(Enseignant, on_delete=CASCADE, related_name='charges')
    cree_par=models.ForeignKey(Enseignant, on_delete=CASCADE, null=True, blank=True)
    repeter_chaque_semaine=models.BooleanField(default=False, null=True, blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['activite', 'realisee_par'], name="activite-enseignant")
        ]
        indexes = [
            models.Index(fields=['realisee_par'])
        ]


class Pays(models.Model):
    code=models.CharField(max_length=2, primary_key=True)
    nom=models.CharField(max_length=50)
    def __str__(self):
        return self.nom

class Wilaya(models.Model):
    code=models.CharField(max_length=2, primary_key=True)
    nom=models.CharField(max_length=50)
    def __str__(self):
        return f"{self.code} {self.nom}"

class Commune(models.Model):
    code_postal=models.CharField(max_length=5, primary_key=True)
    nom=models.CharField(max_length=50)
    wilaya=models.ForeignKey(Wilaya, on_delete=models.SET_NULL, null=True, related_name='communes')
    def __str__(self):
        return f"{self.code_postal} {self.nom}"
   


#Remarque : A chaque fois qu'un nouveau modèle est créé et pointant vers le modèle Etudiant, il faut que la méthode matricule_update du modèle Etudiant puisse mettre à jour le nouveau modèle ajouté vers le nouvel objet étudiant créé
#C'est car le matricule d'un étudiant est une clé primaire il n'est pas possible de la modifier
#Donc on passe par une duplication de l'objet Etudiant et le changement des liens des objets pointant vers l'étudiant via la méthode matricule_update
#Le cleanup ignore est car si on change de matricule à l'étudiant, il est supprimé puis recréé ce qui supprime tous ses fichiers; On ignore donc le cleanup pour le modèle étudiant
@cleanup.ignore
class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, error_messages={
            'unique': (
                "Un étudiant associé à cet utilisateur existe déjà."),
        },)
    matricule=models.CharField(max_length=20,primary_key=True, error_messages={
            'unique': (
                "Un étudiant avec ce matricule existe déjà."),
        },)
    nom=models.CharField(max_length=50)
    prenom=models.CharField(max_length=50)
    sexe=models.CharField(max_length=1, choices=SEXE, null=True, blank=True)
    date_naissance=models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    lieu_naissance=models.CharField(max_length=100, null=True, blank=True)
    wilaya_naissance=models.ForeignKey(Wilaya, on_delete=models.SET_NULL, null=True, blank=True)
    wilaya_residence=models.ForeignKey(Wilaya, on_delete=models.SET_NULL, null=True, blank=True, related_name='origines')
    commune_residence=models.ForeignKey(Commune, on_delete=models.SET_NULL, null=True, blank=True)
    interne=models.BooleanField(default=False, null=True, blank=True)
    residence_univ=models.TextField(null=True, blank=True)
    addresse_principale=models.TextField(null=True, blank=True)
    nom_a=models.CharField(max_length=50, null=True, blank=True, verbose_name="Nom en arabe")
    prenom_a=models.CharField(max_length=50, null=True, blank=True, verbose_name="Prénom en arabe")
    lieu_naissance_a=models.CharField(max_length=100, null=True, blank=True, verbose_name="Lieu de naissance en arabe")
    photo=models.ImageField(upload_to='photos',null=True,blank=True)
    activite_extra=models.TextField(null=True, blank=True)
    tuteur=models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True, blank=True)    
    github=models.URLField(null=True, blank=True)
    linkdin=models.URLField(null=True, blank=True)
    public_profile=models.BooleanField(default=False)   
    tel=models.CharField(max_length=15, null=True, blank=True)
    numero_securite_sociale=models.CharField(max_length=15, validators=[RegexValidator('^[0-9\+]*$',
                               'Que des chiffres sans espaces')], null=True, blank=True)
    nom_mere=models.CharField(max_length=50, null=True, blank=True, verbose_name="Nom de la mère")       
    nom_mere_a=models.CharField(max_length=50, null=True, blank=True, verbose_name="Nom de la mère en arabe")
    prenom_mere=models.CharField(max_length=50, null=True, blank=True, verbose_name="Prénom de la mère")
    prenom_mere_a=models.CharField(max_length=50, null=True, blank=True, verbose_name="Prénom de la mère en arabe")
    fonction_mere=models.CharField(max_length=50, null=True, blank=True, verbose_name="Fonction de la mère")
    prenom_pere=models.CharField(max_length=50, null=True, blank=True, verbose_name="Prénom du père")
    prenom_pere_a=models.CharField(max_length=50, null=True, blank=True, verbose_name="Prénom du père en arabe")
    fonction_pere=models.CharField(max_length=50, null=True, blank=True, verbose_name="Fonction du père")
    tel_parents=models.CharField(max_length=15, null=True, blank=True)
    annee_bac=models.CharField(max_length=10, null=True, blank=True)
    n_inscription_bac=models.CharField(max_length=20,null=True, blank=True, verbose_name="Numéro d'inscription au bac")    
    moyenne_bac=models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0)
    serie_bac=models.CharField(max_length=50, choices=Serie_bac, null=True, blank=True)    
    lycee_bac=models.CharField(max_length=100, null=True, blank=True)
    matricule_progres=models.CharField(max_length=50,null=True,blank=True)
    livret_competences=models.FileField(upload_to='files/livrets', null=True, blank=True) 
    livret_last_upload=models.DateTimeField(null=True, blank=True)
   

class Salle(models.Model):
    code= models.CharField(max_length=50)
    version = models.CharField(max_length=50, default='v0')
    calendarId= models.CharField(max_length=100, null=True, blank=True)
    nb_lignes= models.PositiveSmallIntegerField(default=0)
    nb_colonnes= models.PositiveSmallIntegerField(default=0)
    
    def capacite(self):
        return self.places.filter(disponible=True).count()
    
    def capacite_max(self):
        return self.nb_lignes * self.nb_colonnes

    def place_disponible_list(self):
        
        return self.places.filter(disponible=True).order_by('code')
    
    def ligne_list(self):
        return range(1, self.nb_lignes+1)
    
    def colonne_list(self):
        return char_range(self.nb_colonnes)
    
    def __str__(self):
        return f"{self.code}{self.version}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code', 'version'], name="salle-code-version")
        ]
    
class Place(models.Model):
    code = models.CharField(max_length=3, null=False, blank=False)
    disponible = models.BooleanField(default=True)
    salle = models.ForeignKey(Salle, on_delete=CASCADE, related_name='places')
    num_ligne = models.PositiveSmallIntegerField(default=0)
    num_colonne = models.CharField(max_length=1, null=True, blank=True)
    
    def __str__(self):
        return f"{self.salle}({self.code})"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['salle','code'], name="salle-place")
        ]
        constraints = [
            models.UniqueConstraint(fields=['salle','num_ligne','num_colonne'], name="salle-num_ligne-num_colonne")
        ]
        indexes = [models.Index(fields=['salle','code'])]
     
class Seance(models.Model):
    '''
    Instance d'une activité durant le semestre
    '''
    date=models.DateField()
    heure_debut=models.TimeField(null=True, blank=True)
    heure_fin=models.TimeField(null=True, blank=True)
    salles=models.ManyToManyField(Salle, blank=True)
    activite=models.ForeignKey(Activite, on_delete=CASCADE)
    rattrapage=models.BooleanField(default=False)
    

class AbsenceEtudiant(models.Model):
    '''
    Permet de stocker les absences et leurs justifications
    '''
    etudiant=models.ForeignKey(Etudiant, on_delete=CASCADE, null=True, blank=True)
    seance=models.ForeignKey(Seance, on_delete=CASCADE, null=True, blank=True)
    justif=models.BooleanField(default=False)
    motif=models.TextField(max_length=50, null=True, blank=True)
    date_justif=models.DateField(null=True, blank=True)  
    
    def nb_absences(self):
        aggregate = AbsenceEtudiant.objects.filter(etudiant=self.etudiant, seance__activite__module=self.seance.activite.module).aggregate(nb_absences=Count('etudiant'))
        return aggregate['nb_absences']
    

    def __str__(self):
        return f"{self.etudiant} {self.seance}"
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['etudiant', 'seance'], name="etudiant-seance")
        ]

class AbsenceEnseignant(models.Model):
    '''
    Permet de stocker les absences et leurs justifications
    '''
    enseignant=models.ForeignKey(Enseignant, on_delete=models.CASCADE, null=True, blank=True)
    seance=models.ForeignKey(Seance, on_delete=CASCADE, null=True, blank=True)
    justif=models.BooleanField(default=False)
    date_justif=models.DateField(null=True, blank=True)
    motif=models.TextField(max_length=50, null=True, blank=True)
    seance_remplacement=models.ForeignKey(Seance, on_delete=CASCADE, null=True, blank=True, related_name='remplacement')


    
class Soutenance(models.Model):
    groupe = models.OneToOneField(Groupe, on_delete=CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    depot_biblio = models.SmallIntegerField(default=3, choices=OPTIONS_DEPOT)
    president = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True, blank=True, related_name='president')
    rapporteur = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True, blank=True, related_name='rapporteur')
    examinateur = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True, blank=True, related_name='examinateur')
    coencadrant = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True, blank=True, related_name='coencadrant')
    assesseur1 = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True, blank=True, related_name='assesseur1')
    assesseur2 = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True, blank=True, related_name='assesseur2')
    invite1 = models.CharField(max_length=100, null=True, blank=True)
    invite2 = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['groupe'], name="groupe-soutenance")
        ]
    
    def __str__(self):
        return f"{self.groupe} : {self.date}"
    
class Inscription(models.Model):
    etudiant=models.ForeignKey(Etudiant, on_delete=CASCADE, related_name='inscriptions')
    formation=models.ForeignKey(Formation,on_delete=CASCADE)
    groupe=models.ForeignKey(Groupe, null=True, blank=True, on_delete=models.SET_NULL, related_name='inscrits')
    moy=models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0)
    moy_ra=models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0)
    #moy_post_delib=models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0)
    rang=models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    decision_jury=models.CharField(max_length=2,choices=DECISIONS_JURY, null=True, blank=True, default='X')
    # proposition decision_jury qui ne soit pas vue par les étudiants, avant confirmation déliberations
    proposition_decision_jury=models.CharField(max_length=2,choices=DECISIONS_JURY, null=True, blank=True, default='X')
    observation=models.CharField(max_length=100,null=True, blank=True) 
    mention = models.CharField(max_length=2, choices=MENTION, null=True, blank=True, default='X')
    quittance = models.ImageField(upload_to='quittances', null=True, blank=True )

class ResidenceUniv(models.Model):
    nom = models.CharField(max_length=50)
    adresse = models.TextField()
    tel = models.CharField(max_length=15, validators=[RegexValidator('^[0-9\+]*$',
                               'Que des chiffres sans espaces et le + pour l\'international')])
    wilaya = models.ForeignKey(Wilaya, on_delete=CASCADE)
    commune = models.ForeignKey(Commune, on_delete=CASCADE)

    def __str__(self):
        return self.nom

# pour ne pas supprimer une quittance du dossier une fois sa préinscription supprimée
@cleanup.ignore
class Preinscription(models.Model):
    
    inscription = models.OneToOneField(Inscription, on_delete=models.CASCADE)
    wilaya_residence=models.ForeignKey(Wilaya, on_delete=models.CASCADE, null=True, blank=True)
    commune_residence=models.ForeignKey(Commune, on_delete=models.CASCADE, null=True, blank=True)
    interne=models.BooleanField(default=False, null=True, blank=True)
    residence_univ=models.ForeignKey(ResidenceUniv, on_delete=models.SET_NULL, null=True, blank=True)
    adresse_principale=models.TextField(null=True, blank=True)
    photo=models.ImageField(upload_to='tmp',null=True,blank=True, validators=[validate_image])
    quittance=models.ImageField(upload_to='tmp',null=True,blank=True, validators=[validate_image])
    tel=models.CharField(max_length=15, validators=[RegexValidator('^[0-9\+]*$',
                               'Que des chiffres sans espaces et le + pour l\'international')], null=True, blank=True)
    numero_securite_sociale=models.CharField(max_length=15, validators=[RegexValidator('^[0-9\+]*$',
                               'Que des chiffres sans espaces')], null=True, blank=True)
    fonction_pere=models.CharField(max_length=50, null=True, blank=True, verbose_name="Fonction du père")
    fonction_mere=models.CharField(max_length=50, null=True, blank=True, verbose_name="Fonction de la mère")
    tel_parents=models.CharField(max_length=15, null=True, blank=True)
    lycee_bac=models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return str(self.inscription)

   
class ReservationPlaceEtudiant(models.Model):
    inscription = models.ForeignKey(Inscription, on_delete=CASCADE)
    seance = models.ForeignKey(Seance, on_delete=CASCADE)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['inscription', 'seance'], name="reservation_place_etudiant"),
            models.UniqueConstraint(fields=['seance', 'place'], name="seance_place")
        ]
    
    def __str__(self):
        return f"{self.inscription} : {self.seance.activite.module.matiere.code} --> {self.place.salle.code} ({self.place})"

class SurveillanceEnseignant(models.Model):
    enseignant = models.ForeignKey(Enseignant, on_delete=CASCADE)
    seance = models.ForeignKey(Seance, on_delete=CASCADE)
    salle = models.ForeignKey(Salle, on_delete=CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['enseignant', 'seance'], name="surveillance_enseignant")
        ]

class InscriptionPeriode(models.Model):
    inscription=models.ForeignKey(Inscription, on_delete=CASCADE, related_name='inscription_periodes')
    # TODO supprimer cet attribut et le remplacer par periodepgm qui suit
    periode=models.ForeignKey(Periode, on_delete=models.SET_NULL, null=True, blank=True)
    periodepgm=models.ForeignKey(PeriodeProgramme, on_delete=CASCADE, null=True, blank=True)
    groupe=models.ForeignKey(Groupe, on_delete=models.SET_NULL, null=True, blank=True, related_name='inscrits_periode')
    moy=models.DecimalField(max_digits=4, decimal_places=2, default=0)
    moy_importee=models.DecimalField(max_digits=4, decimal_places=2, default=0)
    moy_post_delib_importee=models.DecimalField(max_digits=4, decimal_places=2, default=0)
    is_moy_importee=models.BooleanField(default=False)
    ne=models.PositiveSmallIntegerField(default=0)
    rang=models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    acquis=models.BooleanField(default=False)


class ResultatUE(models.Model):
    ue=models.ForeignKey(UE, on_delete=models.SET_NULL, null=True, blank=True)
    inscription_periode=models.ForeignKey(InscriptionPeriode, on_delete=CASCADE, related_name='resultat_ues')
    #TODO à supprimer c'est un champ qu'on recalcule au besoin
    moy=models.DecimalField(max_digits=4, decimal_places=2, default=0)
    #moy_post_delib=models.DecimalField(max_digits=4, decimal_places=2, default=0)
    
   
class Resultat(models.Model):
    '''
    Résultats d'un module pour un étudiant
    '''
    ECTS=(
        ('A','Excellent: 10%'),
        ('B','Très bien: 25%'),
        ('C','Bien: 30%'),
        ('D','Satisfaisant; 25%'),
        ('E','Passable: 10%'),
        ('Fx','Insuffisant'),
        ('F','Insuffisant'),
    )

    module=models.ForeignKey(Module, on_delete=CASCADE, null=True, blank=True)
    inscription=models.ForeignKey(Inscription, on_delete=CASCADE, null=True, blank=True, related_name='resultats')
    
    moy=models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0)
    moy_rattrapage=models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0)
    # cet attribut devrait disparaître vu que calcul_ects se base sur moy_post_delib
    moy_post_delib=models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0)
    ects=models.CharField(max_length=2, choices = ECTS, default='F', null=True, blank=True)
    # TODO à supprimer on garde uniquement esct_post_delib
    #ects_post_delib=models.CharField(max_length=2, choices = ECTS, default = 'F', null=True, blank=True)
    # pour gérer les redoublants avec des modules acquis, pour éviter de les faire apparaître sur les listes de présence
    acquis=models.BooleanField(default=False)
    entree_rattrapage=models.BooleanField(default=False)
    resultat_ue=models.ForeignKey(ResultatUE, on_delete=CASCADE, null=True, blank=True, related_name='resultat_matieres')
    dette=models.BooleanField(default=False)
    etat_dette=models.CharField(max_length=2, choices = STATUT_DETTE, default='X', null=True, blank=True)
    ancien_resultat=models.ForeignKey('Resultat', on_delete=models.SET_NULL, null=True, blank=True, related_name='nouveaux_resultats')
    resultat_en_cours=models.ForeignKey('Resultat', on_delete=models.SET_NULL, null=True, blank=True, related_name='ancien_resultat_du_resultat_en_cours')

   
    
class Note(models.Model):
    '''
    Une note correspondant à une évaluation prévue dans un module
    '''
    note=models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0)
    note_post_delib=models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0)
    evaluation=models.ForeignKey(Evaluation, on_delete=CASCADE, null=True, blank=True)
    resultat=models.ForeignKey(Resultat, on_delete=CASCADE, null=True, blank=True, related_name='notes')
    def __str__(self):
        return f"{self.resultat} {self.evaluation} {self.note}"
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['evaluation', 'resultat'], name="evaluation-resultat")
        ]

class GoogleCalendar(models.Model):
    code = models.CharField(max_length=20)
    calendarId = models.CharField(max_length=100)

    def __str__(self):
        return self.code
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code'], name="gcal-code")
        ]
    
class Organisme(models.Model):
    sigle = models.CharField(max_length=50, primary_key=True, validators=[RegexValidator('^[A-Z_\-\&\@\ 0-9]+$',
                               'Saisir en majuscule')])
    nom = models.CharField(max_length=200)
    adresse = models.TextField(null=True, blank=True)
    pays=models.ForeignKey(Pays, on_delete=CASCADE, default='DZ')
    type=models.CharField(max_length=2, choices=TYPE_ORGANISME)
    nature=models.CharField(max_length=2, choices=NATURE_ORGANISME, null=True, blank=True)
    statut=models.CharField(max_length=5, choices=STATUT_ORGANISME, null=True, blank=True)
    taille=models.CharField(max_length=5, choices=TAILLE_ORGANISME, null=True, blank=True) 
    secteur=models.CharField(max_length=2, choices=SECTEUR_ORGANISME, null=True, blank=True)
    interne=models.BooleanField(default=False, verbose_name="Organisme interne au sein de l'établissement (laboratoire, service, ..)")
   
class PFE(models.Model):
    type = models.CharField(max_length=2, choices=TYPE_STAGE, default='P')
    specialites = models.ManyToManyField(Specialite)
    organisme = models.ForeignKey(Organisme, on_delete=models.SET_NULL, null=True)
    groupe = models.OneToOneField(Groupe, on_delete=models.SET_NULL, null=True, blank=True)
    coencadrants = models.ManyToManyField(Enseignant, blank=True, related_name='pfes')
    promoteur = models.TextField(max_length=100, null=True)
    email_promoteur = models.EmailField(null=True)
    tel_promoteur = models.CharField(max_length=20, null=True, blank=True, validators=[RegexValidator('^[0-9\+]*$',
                               'Que des chiffres sans espaces et le + pour l\'international')])
    intitule = models.TextField(null=True)
    resume = models.TextField(null=True)
    keywords = models.TextField(null=True)
    objectifs = models.TextField(null=True)
    resultats_attendus = models.TextField(null=True)
    antecedents = models.TextField(null=True, blank=True)
    moyens_informatiques = models.CharField(max_length=3, choices=OPTION_MOYENS, null=True, blank=True)
    echeancier = models.TextField(null=True)
    bibliographie = models.TextField(null=True, blank=True)
    statut_validation = models.CharField(max_length=2, choices=STATUT_VALIDATION, default='C')
    reponse_aux_experts = models.TextField(null=True, blank=True)
    reserve_pour = models.ManyToManyField(Inscription, related_name='reservations_pfe')
    projet_recherche = models.CharField(max_length=200, null=True, blank=True)
    # cet attribut sert à bloquer les notifications après la validation du sujet suite à de nouvelles modifications
    notification = models.BooleanField(default=True)
   
class Validation(models.Model):
    pfe = models.ForeignKey(PFE, on_delete=CASCADE, related_name='validations')
    expert = models.ForeignKey(Enseignant, on_delete=CASCADE)
    avis = models.CharField(max_length=2, choices=OPTIONS_VALIDATION, default='X')
    commentaire=models.TextField(null=True, blank=True)
    debut=models.DateField(null=True, blank=True)
    fin=models.DateField(null=True)
    
    def __str__(self):
        return f"{self.pfe} - {self.expert} - {dict(OPTIONS_VALIDATION).get(self.avis)}"
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['pfe','expert', 'avis'], name="pfe-expert-avis")
#         ]
 
class Equipe(models.Model):

    pfe=models.OneToOneField(PFE, on_delete=CASCADE, related_name='equipe', null=True)
    inscriptions=models.ManyToManyField(Inscription, related_name='equipes')
        
    def __str__(self):
        return " - ".join(str(i) for i in [self.pfe.intitule, *self.inscriptions.all()])

class Question(models.Model):
    code=models.CharField(max_length=3, primary_key=True)
    intitule=models.CharField(max_length=80)   
    projet_na=models.BooleanField(default=False)
    cours_na=models.BooleanField(default=False)         
    def __str__(self):
        return f"{self.code} : {self.intitule}"

class Feedback(models.Model):
    
    module=models.ForeignKey(Module, on_delete=CASCADE, related_name='feedbacks')
    inscription=models.ForeignKey(Inscription, on_delete=CASCADE, null=True, blank=True)
    comment=models.TextField(null=True, blank=True)
    show=models.BooleanField(default=True)
    def __str__(self):
#         if self.resultat:
#             return str(self.module.matiere.code) +' by '+str(self.resultat.etudiant)
#         else : 
        return f"{self.module.matiere.code} by anonymous"

class Reponse(models.Model):
    REPONSE=(
        ('++','Tout à fait d\'accord'),
        ('+','D\'accord'),
        ('-','Pas d\'accord'),
        ('--','En total désaccord'),
    )
    feedback=models.ForeignKey(Feedback, on_delete=CASCADE, related_name='reponses')
    question=models.ForeignKey(Question, on_delete=CASCADE)
    reponse=models.CharField(max_length=2, choices=REPONSE)
    def __str__(self):
        return f"{self.question} {self.feedback}"

class CompetenceFamily(models.Model):
    code=models.CharField(max_length=5, primary_key = True)
    intitule = models.CharField(max_length = 120)
    def __str__(self):
        return f"{self.code} : {self.intitule}"

class Competence(models.Model):
    code = models.CharField(max_length = 10)
    competence_family = models.ForeignKey(CompetenceFamily, on_delete = CASCADE, null = True, related_name='competences')
    intitule = models.CharField(max_length = 160)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code', 'competence_family'], name="competence-competence-family")
        ]
    def __str__(self):
        return f"{self.code} : {self.intitule}"

class CompetenceElement(models.Model):

    TYPE=(
        ('MOD','Modélisation'),
        ('MET','Méthodologie'),
        ('TEC','Technique'),
        ('OPE','Opérationnel'),        
    )

    code = models.CharField(max_length = 10)
    competence = models.ForeignKey(Competence, on_delete=CASCADE, null=True, related_name='competence_elements')
    intitule = models.CharField(max_length = 160)
    type = models.CharField(max_length = 5, choices = TYPE)
    objectif = models.TextField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code', 'competence'], name="competence-element-competence")
        ]
    def __str__(self):
        return f"{self.code} : {self.intitule}"
    
class MatiereCompetenceElement(models.Model):
    matiere = models.ForeignKey(Matiere, on_delete=CASCADE, null=True)
    competence_element = models.ForeignKey(CompetenceElement, on_delete=CASCADE, null=True, related_name='competence_elements')
    niveau = models.CharField(max_length = 1, choices = NIVEAU)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['matiere', 'competence_element'], name="matiere-competence-element")
        ]
        
        indexes = [models.Index(fields=['matiere','competence_element'])]
        
    def __str__(self):
        return f"{self.matiere} : {self.competence_element}"
    
class Semainier(models.Model):
  
    module=models.ForeignKey(Module, on_delete=CASCADE)
    semaine=models.PositiveSmallIntegerField(choices=SEMAINE)
    activite_cours=models.CharField(max_length=255, null=True, blank=True)
    activite_dirigee=models.TextField(null=True, blank=True)
    observation=models.CharField(max_length=255, null=True, blank=True)
    objectifs=models.CharField(max_length=255, null=True, blank=True)
    matiere_competence_element=models.ForeignKey(MatiereCompetenceElement, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['module', 'semaine'], name="module-semaine")
        ]
    def __str__(self):
        return f"{self.module.matiere.code} : {self.semaine}"
    
class EvaluationCompetenceElement(models.Model):
    evaluation=models.ForeignKey(Evaluation, on_delete=CASCADE, related_name='competence_elements')
    competence_element=models.ForeignKey(CompetenceElement, on_delete=CASCADE)
    commune_au_groupe=models.BooleanField(default=False)
    ponderation=models.DecimalField(max_digits=4, decimal_places=2, default=0)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['evaluation', 'competence_element'], name="evaluation_competence_element")
        ]
    def __str__(self):
        return f"{self.evaluation.type} : {self.competence_element.intitule}"

class NoteCompetenceElement(models.Model):
    evaluation_competence_element=models.ForeignKey(EvaluationCompetenceElement, on_delete=CASCADE, null=True, blank=True)
    note_globale=models.ForeignKey(Note, on_delete=CASCADE, null=True, blank=True) #Note globale à laquelle contribue cette note d'un élément de compétence
    valeur=models.DecimalField(max_digits=6, decimal_places=4, default=0) # pour obtenir les points attribués: valeur * eval_competence_element.ponderation * 20
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['evaluation_competence_element','note_globale'], name="evaluation_competence_element_note_globale")
        ]


class CompetenceEvalConfig(models.Model):  
    evaluation=models.OneToOneField(Evaluation, on_delete=CASCADE, null=True, related_name='competence_eval_config')
    A=models.DecimalField(max_digits=4, decimal_places=2, default=dict(NOTES_PAR_DEFAUT).get('A'))
    B=models.DecimalField(max_digits=4, decimal_places=2, default=dict(NOTES_PAR_DEFAUT).get('B'))
    C=models.DecimalField(max_digits=4, decimal_places=2, default=dict(NOTES_PAR_DEFAUT).get('C'))
    D=models.DecimalField(max_digits=4, decimal_places=2, default=dict(NOTES_PAR_DEFAUT).get('D'))
    E=models.DecimalField(max_digits=4, decimal_places=2, default=dict(NOTES_PAR_DEFAUT).get('E'))
    F=models.DecimalField(max_digits=4, decimal_places=2, default=dict(NOTES_PAR_DEFAUT).get('F'))
    def __str__(self):
        return str(self.evaluation)
    
class Trace(models.Model):
    source=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='actions_faites')
    source_text=models.CharField(max_length=255, null=True, blank=True)
    cible=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='actions_recues')
    cible_text=models.CharField(max_length=255, null=True, blank=True)
    action=models.TextField()
    date_time= models.DateTimeField(default=timezone.now)
    seen=models.BooleanField(default=False, verbose_name="Vu par la cible")

class Doctorant(models.Model):
    etudiant = models.OneToOneField(Etudiant, on_delete=models.SET_NULL, null=True, blank=True)
    enseignant = models.OneToOneField(Enseignant, on_delete=models.SET_NULL, null=True, blank=True)
    organisme=models.ForeignKey(Organisme, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctorants')

  
          
class Projet(models.Model):
    code = models.CharField(null=True, blank=True, max_length=50)
    type=models.CharField(max_length=20,choices=TYPE_PROJET, blank=True)
    titre = models.CharField(null=True, max_length=300)
    chef = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True, blank=True, related_name='projets_en_chef')
    chef_externe=models.CharField(max_length=200, null=True, blank=True, verbose_name="Chef externe (s'il y a lieu)")
    membres =models.ManyToManyField(Enseignant, blank=True, related_name='projets_en_membre', verbose_name="Membres enseignants")
    membres_doctorants=models.ManyToManyField(Doctorant, blank=True, related_name='projets_en_membre', verbose_name="Membres doctorants")
    membres_externes=models.TextField(null=True,blank=True, verbose_name="Membres externes")
    organisme=models.ForeignKey('Organisme', on_delete=models.SET_NULL, null=True, blank=True, related_name='projets')
    annee_debut=models.ForeignKey(AnneeUniv ,related_name='projets_commences' , null= True, blank=True, on_delete=models.SET_NULL)
    annee_fin=models.ForeignKey(AnneeUniv ,related_name='projets_termines' , null= True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return str(self.titre)

class These(models.Model):
    sujet = models.OneToOneField(PFE,null= True, blank=True, on_delete= models.SET_NULL)
    directeur = models.ForeignKey(Enseignant, related_name='directions',on_delete= models.SET_NULL, null = True, blank = True)
    directeur_externe=models.CharField(max_length=300, null=True, blank=True)
    codirecteur = models.ForeignKey(Enseignant,related_name='codirections' , null= True, blank=True, on_delete=models.SET_NULL)
    codirecteur_externe=models.CharField(max_length=300, null=True, blank=True)
    doctorant = models.OneToOneField(Doctorant, related_name='these' , null= True, blank=True, on_delete=models.SET_NULL)
    annee_univ=models.ForeignKey(AnneeUniv ,related_name='theses' , null= True, blank=True, on_delete=models.SET_NULL)
    projet=models.ForeignKey(Projet, related_name='theses',on_delete= models.SET_NULL, null = True, blank = True)

       
class OptionCritere(models.Model):
    ordre=models.IntegerField(null=True)
    option=models.CharField(max_length=100, null=True, blank=False)
    
    def __str__(self):
        return str(self.option)

class Critere(models.Model):
    ordre=models.IntegerField(null=True)
    critere=models.CharField(max_length=500, null=True, blank=False, verbose_name="Enoncé du critère")
    options= models.ManyToManyField(OptionCritere, blank=True)
    programmes= models.ManyToManyField(Programme, blank=True)
    commentaire=models.BooleanField(default=True, verbose_name="Possibilité d'introduire un commentaire au critère")

    

class EtatAvancement(models.Model):
    inscription = models.ForeignKey(Inscription, null=True, on_delete=CASCADE, related_name="etat_avancement")
    jury = models.ManyToManyField(Enseignant, blank=True, related_name='etats_avancements_en_jury')
    avis_directeur=models.TextField(null=True, verbose_name="Avis du directeur de thèse")
    final=models.BooleanField(default=False)
    decision_1=models.CharField(max_length=20,choices=DECISIONS_1, null=True)
    decision_finale=models.CharField(max_length=20,choices=DECISIONS_FINALES, null=True)


class EvaluationCritere(models.Model):
    etat_avancement=models.ForeignKey(EtatAvancement, on_delete=CASCADE)
    critere=models.ForeignKey(Critere, on_delete=CASCADE)
    options=models.ManyToManyField(OptionCritere, blank=True, related_name='evaluations_criteres')
    commentaire=models.TextField()
    

class SeminaireSuivi(models.Model):
    inscriptions = models.ManyToManyField(Inscription, blank=True, related_name="seminaires_suivis")
    matiere = models.ForeignKey(Matiere, null=True, on_delete=models.SET_NULL, related_name="matiere")  
    animateur_interne =models.ForeignKey(Enseignant, null=True, blank=True, on_delete= models.SET_NULL, related_name="seminaire_animateur")
    animateur_externe=models.CharField(max_length=30,null=True,blank=True)
    date=models.DateField(null=True,blank=True,)
    annee_univ=models.ForeignKey(AnneeUniv, null= True, blank=True, on_delete=models.SET_NULL)



class DocumentConfig(models.Model):
    code=CharField(max_length=100)
    actif=models.BooleanField(default=False)
    programme=models.ForeignKey(Programme, on_delete=CASCADE, null=True, blank=True)
    diplome=models.ForeignKey(Diplome, on_delete=CASCADE, null=True, blank=True)
    autorite=models.ForeignKey(Autorite, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Autorité", related_name="documents_signes")
    autorite_entete=models.ForeignKey(Autorite, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Autorité affichée dans l'entête du document", related_name="documents_en_entete")
    
    def type(self):
        return dict(DOCUMENTS)[self.code][1]
        
    def __str__(self):
        doc = dict(DOCUMENTS)[self.code][0]
        if self.programme :
            return f"{doc} {self.programme}"
        if self.diplome :
            return f"{doc} {self.diplome}"
        return doc
        
class Poste(models.Model):
    inscription = models.OneToOneField(Inscription, on_delete=CASCADE, unique=True, error_messages={
            'unique': (
                "Un poste est déjà associé à cette inscription"),
        },)
    specialite=models.ForeignKey(Specialite, null=True, blank=True, on_delete=models.SET_NULL)   
    organisme = models.ForeignKey(Organisme, on_delete=models.SET_NULL, null=True)
    responsable = models.ForeignKey(Enseignant, related_name='postes_en_responsable',on_delete= models.SET_NULL, null = True, blank = True)
    responsable_ext=models.CharField(max_length=300, null=True, blank=True, verbose_name="Responsable ext")



@cleanup.ignore
class EnregistrementEtudiant(models.Model):
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date et heure")
    statut = models.CharField(max_length=1, choices=STATUT_ENREGISTREMENT, null=True, blank=True, default='W')
    message = models.TextField(default='', blank=True, verbose_name="Message à transmettre à l'utilisateur")
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(null=True, verbose_name="Adresse e-mail")
    nom=models.CharField(max_length=50)
    prenom=models.CharField(max_length=50)
    sexe=models.CharField(max_length=1, choices=SEXE, null=True, blank=True)
    date_naissance=models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    lieu_naissance=models.CharField(max_length=100, null=True, blank=True, verbose_name="Lieu de naissance")
    wilaya_naissance=models.ForeignKey(Wilaya, on_delete=models.SET_NULL, null=True, blank=True, related_name="wilaya_naissance_enregistrements")
    wilaya_residence=models.ForeignKey(Wilaya, on_delete=models.SET_NULL, null=True, blank=True, related_name='origines_enregistrements')
    commune_residence=models.ForeignKey(Commune, on_delete=models.SET_NULL, null=True, blank=True)
    interne=models.BooleanField(default=False, null=True, blank=True, verbose_name="Interne dans une cité universitaire")
    residence_univ=models.TextField(null=True, blank=True, verbose_name="Nom de la cité universitaire si vous êtes interne")
    addresse_principale=models.TextField(null=True, blank=True, verbose_name="Adresse principale")
    programme=models.ForeignKey(Programme, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Actuellement scolarisé en")
    nom_a=models.CharField(max_length=50, null=True, blank=True, verbose_name="Nom en arabe")
    prenom_a=models.CharField(max_length=50, null=True, blank=True, verbose_name="Prénom en arabe")
    lieu_naissance_a=models.CharField(max_length=100, null=True, blank=True, verbose_name="Lieu de naissance en arabe")
    photo=models.ImageField(upload_to='photos',null=True,blank=True, verbose_name="Photo d'identité scannée (taille maximale 1 MO)") 
    tel=models.CharField(max_length=15, null=True, blank=True, verbose_name="Numéro de téléphone", validators=[RegexValidator('^[0-9\+]*$',
                               'Que des chiffres sans espaces et le + pour l\'international')])
    numero_securite_sociale=models.CharField(max_length=15, validators=[RegexValidator('^[0-9\+]*$',
                               'Que des chiffres sans espaces')], null=True, blank=True)

    def __str__(self):
        return f"{self.email} {self.nom} {self.prenom}"


class EquipeRecherche(models.Model):
    code = models.CharField(null=True, blank=True, max_length=50, verbose_name="Code/Sigle")
    nom = models.CharField(null=True, max_length=300)
    responsable = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True, blank=True, related_name='equipes_en_responsable')
    responsable_externe=models.CharField(max_length=200, null=True, blank=True, verbose_name="Responsable externe (s'il y a lieu)")
    membres =models.ManyToManyField(Enseignant, blank=True, related_name='equipes_en_membre')
    membres_doctorants=models.ManyToManyField(Doctorant, blank=True, related_name='equipes_en_membre', verbose_name="Membres doctorants")
    membres_externes=models.TextField(null=True,blank=True, verbose_name="Membres externes")
    organisme=models.ForeignKey('Organisme', on_delete=models.SET_NULL, null=True, blank=True, related_name='equipes')
    description = models.TextField(null=True, blank=True)
   
    
class Offre(models.Model):
    user=models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='offres', verbose_name="Offre déposée par")
    emetteur = models.TextField(max_length=200, null=True, verbose_name="Émetteur réel de l'offre")
    type = models.CharField(max_length=20, choices=TYPE_OFFRE, default='EMPLOI', null=True, blank=True)
    intitule = models.TextField(null=True, verbose_name="Intitulé de l'offre")
    specialites = models.ManyToManyField(Specialite, verbose_name="Spécialités ciblées")
    organisme = models.ForeignKey(Organisme, on_delete=models.SET_NULL, null=True, blank=True)
    date=models.DateField(null=True, blank=True,verbose_name='Date de dépôt')
    description = models.TextField(null=True, verbose_name="Description détaillée de l'offre")
    fichier1 = models.FileField(upload_to='files/offres', null=True, blank=True, verbose_name="Pièce jointe 1 (facultatif)", validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']), file_size])
    fichier2 = models.FileField(upload_to='files/offres', null=True, blank=True, verbose_name="Pièce jointe 2 (facultatif)", validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']), file_size])
    fichier3 = models.FileField(upload_to='files/offres', null=True, blank=True, verbose_name="Pièce jointe 3 (facultatif)", validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']), file_size])
    statut = models.CharField(max_length=2, choices=STATUT_OFFRE, default='C')
    notification = models.BooleanField(default=True, verbose_name="Notifier le déposant par e-mail de la validation de l'offre ainsi que pour chaque nouvelle candidature")
    activation_candidatures = models.BooleanField(default=True, verbose_name="Activation de l'espace de candidature pour cette offre (les utilisateurs pourront candidater directement sur la plateforme)")

   
class Candidature(models.Model):
    user=models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='candidatures', verbose_name="Candidat")
    nom=models.CharField(max_length=50, null=True)
    prenom=models.CharField(max_length=50, null=True, verbose_name="Prénom(s)")
    offre = models.ForeignKey(Offre, on_delete=CASCADE, null=True)
    reponse=models.TextField(null=True, verbose_name="Pourquoi moi ?")
    competences=models.TextField(null=True, verbose_name="Mes compétences que j'estime adéquates à l'offre")
    motivations=models.TextField(null=True, verbose_name="Mes motivations")
    cv = models.FileField(upload_to=candidature_file_name, null=True, blank=True, verbose_name="CV (facultatif)", validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']), file_size])
    fichier1 = models.FileField(upload_to=candidature_file_name, null=True, blank=True, verbose_name="Autre pièce jointe (facultatif)", validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']), file_size])
    date_time= models.DateTimeField(default=timezone.now, verbose_name="Date et heure")
    last_edit= models.DateTimeField(null=True, blank=True, verbose_name="Dernière modification")
    acces_profil=models.BooleanField(default=False, verbose_name="Accorder l'accès à mon profil à l'utilisateur ayant déposé l'offre (parcours, activités et photo uniquement)")
    
    def __str__(self):
        return f"{self.user} : {self.offre}"
