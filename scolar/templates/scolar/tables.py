import django_tables2 as tables

import django_filters
from django_filters.widgets import BooleanWidget
# from scolar.models import User, DomaineConnaissance, Matiere, MatiereCompetenceElement, Specialite, AnneeUniv, Periode, Enseignant, Departement, Diplome, Programme, PeriodeProgramme, UE, Formation, Module, Evaluation, \
#     Section, Groupe, PFE, ModulesSuivis, Activite, Charge, Etudiant, Seance, AbsenceEtudiant, Soutenance, Inscription, InscriptionPeriode, ResultatUE, Resultat, Note, Question, Feedback, Reponse, Competence, CompetenceElement, \
#     CompetenceFamily, Semainier, EvaluationCompetenceElement, AbsenceEnseignant
from scolar.models import *
from crispy_forms.layout import Layout, Submit, Div, Field
from crispy_forms.helper import FormHelper
from django.utils.html import format_html
from django import forms
import datetime
from bootstrap_datepicker_plus import DatePickerInput
from django.shortcuts import get_object_or_404

from django_tables2 import A

class MatiereTable(tables.Table):
    code = tables.LinkColumn('matiere_detail', args=[tables.A('pk')])
    action = '{% load icons %}\
            {% if perms.scolar.change_matiere %}\
                <a href="{% url "matiere_update" pk=record.id %}" > {% icon "pencil-alt" %} </a>\
            {% endif %}'
    edit= tables.TemplateColumn(action, orderable=False)
    class Meta:
        model = Matiere
        fields=('code','precision', 'titre', 'ddc','credit','coef','edition', 'vh_cours', 'vh_td')        
        template_name = "django_tables2/bootstrap4.html"

class MatiereFilter(django_filters.FilterSet):
    ddc = django_filters.ModelChoiceFilter(field_name='ddc', queryset = DomaineConnaissance.objects.all().order_by('intitule'), empty_label ='Domaine', label ='Domaine')
    titre = django_filters.CharFilter(field_name='titre', lookup_expr='icontains', label = 'Mot clé dans Titre')
    contenu = django_filters.CharFilter(field_name='contenu', lookup_expr='icontains', label = 'Mot clé dans Description')
    programme = django_filters.ModelChoiceFilter(distinct=True, field_name='matiere_ues__periode__programme', queryset = Programme.objects.all().order_by('ordre'), empty_label ='Programme')    
   
    class Meta:
        model = Matiere
        fields = ('ddc','titre', 'contenu', 'programme',)


class ActiviteFilter(django_filters.FilterSet):
    type=django_filters.ChoiceFilter(field_name='type', choices=TYPES_ACT, label="Type d'activité", empty_label="Type d'activité")
    semestre = django_filters.ModelChoiceFilter(field_name='module__periode__periode', queryset = Periode.objects.all().order_by('code'), label ='Semestre', empty_label='Semestre')
    class Meta:
        model = Activite
        fields = ('type','semestre')
        
        
class ActiviteTable(tables.Table):
    cible=tables.Column()
    def render_cible(self,value,record):
        cible_=''
        for groupe in value.all():
            cible_=cible_+' '+str(groupe)
        return format_html("<b>{}</b>",cible_)
    action= '{% if not record.module.matiere.pfe %}\
                {% for groupe in record.cible.all %}\
                    {% if groupe.code %}\
                        <a href="{% url "absencesform" activite_pk=record.id groupe_pk=groupe.id %}" class="btn btn-danger">{{ groupe.code }} </a>\
                    {% else %}\
                        {% for groupe_section in groupe.section.groupes.all %}\
                            {% if groupe_section.code %}\
                                <a href="{% url "absencesform" activite_pk=record.id groupe_pk=groupe_section.id  %}" class="btn btn-danger">{{ groupe_section.code }}</a>\
                            {% endif %}\
                        {% endfor %}\
                    {% endif %}\
                {% endfor %}\
            {% endif %}'
                
    absences   = tables.TemplateColumn(action, orderable=False)

    action= '{% if not record.module.matiere.pfe %}\
                <a href="{% url "assiduite" activite_pk=record.id %}" class="btn btn-danger"> Assiduite</a>\
            {% endif %}'
    gestion_assiduite   = tables.TemplateColumn(action, orderable=False)
    action= '{% for groupe in record.cible.all %}\
                {% if groupe.code %}\
                    <a href="{% url "note_list" matiere_pk=record.module.matiere.id groupe_pk=groupe.id %}" class="btn btn-info">{{ groupe.code }} </a>\
                {% else %}\
                    {% for groupe_section in groupe.section.groupes.all %}\
                        {% if groupe_section.code %}\
                            <a href="{% url "note_list" matiere_pk=record.module.matiere.id groupe_pk=groupe_section.id %}" class="btn btn-info">{{ groupe_section.code }}</a>\
                        {% endif %}\
                    {% endfor %}\
                {% endif %}\
            {% endfor %}'
                
    notes   = tables.TemplateColumn(action, orderable=False)
    action= '{% load icons %}\
            <a href="{% url "feedback_module_detail" module_pk=record.module.id %}">{% icon "chart-bar" %}</a>'
    feedback   = tables.TemplateColumn(action, orderable=False)
    class Meta:
        model= Activite
        fields = ['type', 'module__matiere__code', 'vh', 'cible']
        template_name= "django_tables2/bootstrap4.html"
        
           
class InscriptionTable(tables.Table):
    action='{% for periode_ in record.inscription_periodes.all %}\
                <strong>{{ periode_.periodepgm.periode.code }} : </strong> {{ periode_.groupe.code }}<br>\
            {% endfor %}'

    groupe   = tables.TemplateColumn(action, orderable=False)
    
    action='<a href="{% url "etudiant_inscription_list" etudiant_pk=record.etudiant.matricule %}" class="btn btn-info"> Inscriptions </a>'

    detail   = tables.TemplateColumn(action, orderable=False)
    
    class Meta:
        model= Inscription
        fields = ('etudiant__matricule', 'etudiant__nom', 'etudiant__nom_a','etudiant__prenom', 'etudiant__prenom_a', 'formation__programme')
        template_name= "django_tables2/bootstrap4.html"
        

class InscriptionFilter(django_filters.FilterSet):
    etudiant = django_filters.CharFilter(field_name='etudiant__nom', lookup_expr='icontains', label='Nom de l\'étudiant')
    programme = django_filters.ModelChoiceFilter(field_name='formation__programme', queryset=Programme.objects.all().order_by('ordre'), label='Année d\'étude', empty_label='Année d\'étude')
    groupe = django_filters.ModelChoiceFilter(field_name='groupe', queryset=Groupe.objects.filter(section__formation__annee_univ__encours=True).exclude(code__isnull=True).order_by('section__formation__programme__ordre', 'code'), label='Groupe', empty_label='Groupe')
    class Meta:
        model = Inscription
        fields = ('etudiant', 'programme', 'groupe')
        

class ValidationTable(tables.Table):
    link='{% load icons %}\
            {% if user.is_enseignant %}\
                {% if user.enseignant == record.expert %}\
                    {% if record.pfe.statut_validation != "V" and record.pfe.statut_validation != "N" %}\
                        {% if record.avis == "X" %}\
                            <a href="{% url "validation_update" pk=record.id pfe_pk=record.pfe.id %}" > {% icon "pencil-alt" %} </a>\
                        {% endif %}\
                    {% endif %}\
                {% endif %}\
            {% endif %}'
                    
    action = tables.TemplateColumn(link, orderable=False)
    link='{% load icons %}\
            <a href="{% url "validation_delete" pk=record.id pfe_pk=record.pfe.id %}" > {% icon "trash" %} </a>'
    edit = tables.TemplateColumn(link, orderable=False)
    
    class Meta:
        model= Validation
        fields = ('pfe__intitule', 'pfe__organisme', 'expert', 'debut', 'fin', 'avis', 'commentaire')
        template_name= "django_tables2/bootstrap4.html"
        row_attrs = { "style": lambda record: "background-color: #37D263;" if record.avis == 'V' 
                                        else "background-color: #DB7E7A;" if record.avis == 'N'
                                        else "background-color: #ACD992;" if record.avis == 'SR'
                                        else "background-color: #DECD23;" if record.avis == 'MR'
                                        else "background-color: ##FFFFFF;"}

class PFETable(tables.Table):
    action='{% load icons usergroup %}\
            <a href="{% url "pfe_detail" pk=record.id %}" > {% icon "eye" %} </a>\
            {% if user.is_authenticated %}\
                {% if record.statut_validation == "RR" or  record.statut_validation == "S" or  record.statut_validation == "N" %}\
                    {% if user.is_enseignant %}\
                        {% if request.user.enseignant in record.coencadrants.all %}\
                            <a href="{% url "pfe_update" pk=record.id %}" class="btn btn-warning"  > Réviser </a>\
                        {% endif %}\
                    {% endif %}\
                    {% if user.is_etudiant %}\
                        {% for inscription in user.etudiant.inscriptions_encours %}\
                            {% if inscription in record.reserve_pour.all %}\
                                <a href="{% url "pfe_update" pk=record.id %}" class="btn btn-warning"  > Réviser </a>\
                            {% endif %}\
                        {% endfor %}\
                    {% endif %}\
                {% elif record.statut_validation == "V"%}\
                    <a href="{% url "pfe_fiche_pdf" pfe_pk=record.id %}" > {% icon "file-pdf" %} </a>\
                    {% if user.is_enseignant or user.is_stage %}\
                        <a href="{% url "pfe_update" pk=record.id %}" class="btn btn-warning"  > Affectation </a>\
                    {% endif %}\
                {% endif %}\
            {% endif %}'
                
            
    detail   = tables.TemplateColumn(action, orderable=False)
    action='{% load icons %}\
            <a href="{% url "pfe_update" pk=record.id %}" > {% icon "pencil-alt" %}</a>\
            <a href="{% url "pfe_delete" pk=record.id %}" > {% icon "trash" %}</a>'
            
    edit   = tables.TemplateColumn(action, orderable=False)
    
    class Meta:
        model= PFE
        fields = ('id', 'type', 'specialites', 'intitule', 'organisme__sigle', 'coencadrants', 'email_promoteur', 'nb_avis', 'statut_validation')
        template_name= "django_tables2/bootstrap4.html"
        

class PFEFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(field_name='resume', lookup_expr='icontains', label='Mot Clé dans la description')
    pays = django_filters.ModelChoiceFilter(field_name='organisme__pays', queryset=Pays.objects.all().order_by('nom'), label='Pays', empty_label='Pays')
    type = django_filters.ChoiceFilter(field_name='type', choices=TYPE_STAGE, label='Type', empty_label='Type')
    statut_validation = django_filters.ChoiceFilter(field_name='statut_validation', choices=STATUT_VALIDATION, label='Etat Validation', empty_label='Etat Validation')

    class Meta:
        model = PFE
        fields = ('id', 'type', 'keyword', 'pays', 'statut_validation',)
        
class OrganismeTable(tables.Table):
    action='{% load icons %}\
            <a href="{% url "organisme_update" pk=record.sigle %}" > {% icon "pencil-alt" %}</a>\
            <a href="{% url "organisme_delete" pk=record.sigle %}" > {% icon "trash" %}</a>'
            
    edit   = tables.TemplateColumn(action, orderable=False)
    
    class Meta:
        model= Organisme
        fields = ['sigle', 'nom', 'adresse', 'pays', 'type', 'secteur', 'taille']
        template_name= "django_tables2/bootstrap4.html"
        

class OrganismeFilter(django_filters.FilterSet):
    sigle = django_filters.CharFilter(field_name='sigle', lookup_expr='icontains', label='Sigle')
    nom = django_filters.CharFilter(field_name='nom', lookup_expr='icontains', label='Nom')
    pays = django_filters.ModelChoiceFilter(field_name='pays', queryset=Pays.objects.all().order_by('nom'), label='Pays', empty_label='Pays')
    type = django_filters.ChoiceFilter(field_name='type', choices=TYPE_ORGANISME, label='Type', empty_label='Type')
    secteur = django_filters.ChoiceFilter(field_name='secteur', choices=SECTEUR_ORGANISME, label='Secteur', empty_label='Secteur d\'activité')

    class Meta:
        model = Organisme
        fields = ['sigle', 'nom', 'pays', 'type', 'secteur']
        

class InscriptionGroupeTable(tables.Table):
    etudiant__photo=tables.Column()
    def render_etudiant__photo(self,value,record):
        return format_html("<img src='{}' width='80'>",value.url)
    
    action= '{% load icons %}\
            <a href="{% url "etudiant_detail" pk=record.etudiant.matricule %}" > {% icon "eye" %}</a> '
    detail   = tables.TemplateColumn(action, orderable=False)

    action= '{% load icons %}\
            {% if perms.scolar.change_inscription %}\
                <a href="{% url "inscription_update" pk=record.id %}" > {% icon "pencil-alt" %}</a>\
            {% endif %}'
    edit   = tables.TemplateColumn(action, orderable=False)
    class Meta:
        model= Inscription
        fields = ('etudiant__matricule', 'etudiant__nom', 'etudiant__nom_a','etudiant__prenom', 'etudiant__prenom_a',)
        template_name= "django_tables2/bootstrap4.html"

class EvaluationCompetenceElementTable(tables.Table):
    action= '{% load icons %}\
            <a href="{% url "evaluation_competence_element_update" pk=record.id evaluation_pk=record.evaluation.id %}">{% icon "pencil-alt" %}</a>\
            <a href="{% url "evaluation_competence_element_delete" pk=record.id evaluation_pk=record.evaluation.id %}">{% icon "trash" %}</a>'
    actions   = tables.TemplateColumn(action, orderable=False)
    class Meta:
        model= EvaluationCompetenceElement
        fields = ['competence_element', 'ponderation', 'commune_au_groupe']
        template_name= "django_tables2/bootstrap4.html"
        


class AbsenceEtudiantFilter(django_filters.FilterSet):
    etudiant = django_filters.CharFilter(field_name='etudiant__nom', lookup_expr='icontains', label ='Nom étudiant')
    module = django_filters.ModelChoiceFilter(field_name='seance__activite__module', queryset = Module.objects.filter(formation__annee_univ__encours=True).order_by('formation__programme__ordre', 'formation__programme__code', 'periode__periode__code', 'matiere__code'), label = 'Module', empty_label='Module')
    groupe = django_filters.ModelChoiceFilter(field_name='seance__activite__cible', queryset = Groupe.objects.filter(section__formation__annee_univ__encours=True).order_by('section__formation__programme__ordre'), label = 'Groupe', empty_label='Groupe')
    enseignant = django_filters.ModelChoiceFilter(field_name='seance__activite__assuree_par', queryset = Enseignant.objects.all().order_by('nom'), label = 'Enseignant', empty_label='Enseignant')
    date_absence = django_filters.DateFilter(field_name='seance__date', label ='Date de l\'absence', widget=DatePickerInput(format='%m/%d/%Y'), initial=datetime.date.today())
    justif = django_filters.BooleanFilter(field_name='justif',label ='Justifiée' )
    class Meta:
        model = AbsenceEtudiant
        fields = ('etudiant', 'module', 'groupe', 'enseignant', 'date_absence', 'justif')
        
        
class AbsenceEtudiantTable(tables.Table):
    seance__activite__cible=tables.Column()
    def render_seance__activite__cible(self,value,record):
        cible_=''
        for groupe in value.all():
            cible_=cible_+' '+str(groupe)
        return format_html("<b>{}</b>",cible_)
    action= '{% load icons %}\
            {% if perms.scolar.change_absenceetudiant %}\
                <a href="{% url "absence_update" pk=record.id %}"> {% icon "pencil-alt" %} </a>\
            {% endif %}\
            {% if perms.scolar.delete_absenceetudiant %}\
                <a href="{% url "absence_etudiant_delete" pk=record.id activite_pk=record.seance.activite.id seance_pk=record.seance.id %}"> {% icon "trash" %} </a>\
            {% endif %}'
    actions   = tables.TemplateColumn(action, orderable=False)
    class Meta:
        model= AbsenceEtudiant
        fields = ('etudiant', 'seance', 'seance__activite__cible', 'justif', 'motif')
        template_name= "django_tables2/bootstrap4.html"
        

class AbsenceEnseignantFilter(django_filters.FilterSet):
    enseignant = django_filters.CharFilter(field_name='enseignant__nom', lookup_expr='icontains', label ='Nom enseignant')
    formation = django_filters.ModelChoiceFilter(field_name='seance__activite__module__formation', queryset = Formation.objects.filter(annee_univ__encours=True).order_by('programme__ordre'), label = 'Formation', empty_label='Formation')
    justif = django_filters.BooleanFilter(field_name='justif',label ='Justifiée' )
    class Meta:
        model = AbsenceEnseignant
        fields = ['enseignant', 'formation', 'justif']
        
        
class AbsenceEnseignantTable(tables.Table):
    seance__activite__cible=tables.Column()
    def render_seance__activite__cible(self,value,record):
        cible_=''
        for groupe in value.all():
            cible_=cible_+' '+str(groupe)
        return format_html("<b>{}</b>",cible_)
    action= '{% load icons%}\
            {% if perms.scolar.add_seance %}\
                <a href="{% url "seance_rattrapage_create" activite_pk=record.seance.activite.id %}" class="btn btn-primary"> Rattrapage </a>\
            {% endif %}\
            {% if perms.scolar.change_absenceenseignant %}\
                <a href="{% url "absence_enseignant_update" pk=record.id %}" class="btn btn-warning"> Modifier </a>\
            {% endif %}'
    edit   = tables.TemplateColumn(action, orderable=False)
    class Meta:
        model= AbsenceEnseignant
        fields = ('enseignant', 'seance', 'seance__activite__cible', 'justif', 'motif')
        template_name= "django_tables2/bootstrap4.html"
        

        
        
        
class InscriptionEtudiantTable(tables.Table):
    rang=tables.Column()
    def render_rang(self,value,record):
        return format_html("{} / <b>{}</b>",str(value), str(record.nb_inscrits()))
    
    action= '{% load icons %}\
                <a href="{% url "fiche_inscription_pdf" inscription_pk=record.id %}">Fiche d\'Inscription {% icon "file-pdf" %}</a>\
                <a href="{% url "releve_notes" inscription_pk=record.id %}">Notes</a>\
                <a href="{% url "releve_ects" inscription_pk=record.id %}">ECTS</a>'
    detail   = tables.TemplateColumn(action, orderable=False)
    action= '{% load icons %}\
            {% if perms.scolar.change_inscription %}\
                <a href="{% url "inscription_update" pk=record.id %}">{% icon "pencil-alt" %}</a>\
            {% endif %}\
            {% if perms.scolar.delete_inscription %}\
                <a href="{% url "inscription_delete" pk=record.id etudiant_pk=record.etudiant.matricule %}">{% icon "trash" %}</a>\
            {% endif %}'
    edit   = tables.TemplateColumn(action, orderable=False)
    
    class Meta:
        model= Inscription
        fields = ('formation', 'moy', 'rang',  'decision_jury', )
        template_name= "django_tables2/bootstrap4.html"

class InscriptionEtudiantDocumentsTable(tables.Table):
    action= '{% load usergroup dictionary %}\
            {% if record.decision_jury != "X" %}\
                {% if record.formation.programme.ordre >= 5 and record.decision_jury == "A" %}\
                    <a href="{% url "releve_notes_pdf" inscription_pk=record.id %}" class="btn btn-info">Relevé</a> \
                {% elif record.formation.archive %}\
                    <a href="{% url "releve_notes_pdf" inscription_pk=record.id signature=1 %}" class="btn btn-info">Relevé</a> \
                    <a href="{% url "releve_ects_pdf" inscription_pk=record.id signature=1 %}" class="btn btn-info">ECTS</a>\
                    {% if user.is_scolarite or user.is_direction %}\
                        <a href="{% url "releve_notes_pdf" inscription_pk=record.id signature=0 %}" class="btn btn-info">Relevé-S</a>\
                        <a href="{% url "releve_ects_pdf" inscription_pk=record.id signature=0 %}" class="btn btn-info">ECTS-S </a>\
                    {% endif %}\
                {% else %}\
                    {% for periode in record.inscription_periodes.all %}\
                        <a href="{% url "releve_notes_provisoire_pdf" inscription_pk=record.id periode_pk=periode.periodepgm.id signature=1 %}" class="btn btn-info">RP. {{periode.periodepgm.code}}</a>\
                        {% if user.is_scolarite or user.is_direction %}\
                            <a href="{% url "releve_notes_provisoire_pdf" inscription_pk=record.id periode_pk=periode.periodepgm.id signature=0 %}" class="btn btn-info">RP. {{periode.periodepgm.code}}-S </a>\
                        {% endif %}\
                    {% endfor %}\
                {% endif %}\
                {% if record.decision_jury != "F" and not record.decision_jury|startswith:"M" and record.decision_jury != "X" %}\
                    <a href="{% url "certificat_pdf" inscription_pk=record.id signature=1 %}" class="btn btn-success">Cert3Lx4</a>\
                    {% if user.is_scolarite or user.is_direction %}\
                         <a href="{% url "certificat_pdf" inscription_pk=record.id signature=0 %}" class="btn btn-success">Cert3Lx4-S</a>\
                    {% endif %}\
                {% endif %}\
                {% if record.decision_jury|startswith:"M" %}\
                    <a href="{% url "certificat_conges_pdf" inscription_pk=record.id signature=1 %}" class="btn btn-success">CertAcad</a>\
                {% endif %}\
                <a href="{% url "matiere_detail_list_pdf" programme_pk=record.formation.programme.id %}" class="btn btn-info">Syllabus</a>\
            {% elif user.is_direction or user.is_scolarite %}\
                <a href="{% url "certificat_pdf" inscription_pk=record.id signature=1 %}" class="btn btn-success">Cert3Lx4</a>\
                <a href="{% url "certificat_pdf" inscription_pk=record.id signature=0 %}" class="btn btn-success">Cert3Lx4-S</a>\
            {% endif %}'
                    #<a href="{% url "certificat_old_pdf" inscription_pk=record.id %}" class="btn btn-success">Cert. 2L</a>\
    detail   = tables.TemplateColumn(action, orderable=False)
    class Meta:
        model= Inscription
        fields = ('formation', 'moy', 'rang', 'decision_jury', 'obs_jury', )
        template_name= "django_tables2/bootstrap4.html"
      

class ActiviteChargeConfigTable(tables.Table):
    
    action= '{% load icons %}\
            {% if perms.scolar.change_activitechargeconfig %}\
                <a href="{% url "activite_charge_config_update" record.id %}">{% icon "pencil-alt" %}</a>\
            {% endif %}\
            {% if perms.scolar.delete_activitechargeconfig %}\
                <a href="{% url "activite_charge_config_delete" record.id %}">{% icon "trash" %}</a>\
            {% endif %}'

    edit   = tables.TemplateColumn(action, orderable=False)
    class Meta:
        model= ActiviteChargeConfig
        fields = ('categorie', 'type', 'titre', 'vh', 'vh_eq_td',  'repeter_chaque_semaine', 'repartir_entre_intervenants')
        template_name= "django_tables2/bootstrap4.html"
        
class ActiviteEtudiantTable(tables.Table):
    module=tables.Column()
    def render_module(self, value, record):
        link='<a href="/scolar/module_detail/'+str(value.id)+'">'+str(value.matiere.code)+'</a>'
        return format_html(link)
    assuree_par=tables.Column()
    def render_assuree_par(self,value,record):
        enseignant_list=''
        for enseignant in value.all():
            enseignant_list+=' '+str(enseignant)
        return format_html("<b>{}</b>",enseignant_list)
    
    action= '<a href="{% url "etudiant_module_absences" etudiant_pk=request.user.etudiant.matricule  module_pk=record.module.id %}" class="btn btn-danger" role="button"> Absences</a>\
             <a href="{% url "etudiant_module_notes" etudiant_pk=request.user.etudiant.matricule matiere_pk=record.module.matiere.id %}" class="btn btn-primary" role="button">Notes</a>'
    detail   = tables.TemplateColumn(action, orderable=False)
    
    class Meta:
        model= Activite
        fields=('type','module','vh','assuree_par')
        template_name= "django_tables2/bootstrap4.html"


def matieres(request):
    if request is None:
        return Matiere.objects.all().order_by('code')
    inscriptions_encours=request.user.etudiant.inscriptions_encours()
    resultats= Resultat.objects.filter(inscription__in=inscriptions_encours).values('module__matiere__id').order_by('module__periode__periode', 'module__matiere__code')
    return Matiere.objects.filter(id__in=resultats)
     
class ActiviteEtudiantFilter(django_filters.FilterSet):
    periode = django_filters.ModelChoiceFilter(field_name='module__periode__periode', queryset=Periode.objects.all().order_by('ordre'), label='Semestre', empty_label='Semestre')
    type=django_filters.ChoiceFilter(field_name='type', choices=TYPES_ACT, label="Type d'activité", empty_label="Type d'activité")
    matiere = django_filters.ModelChoiceFilter(field_name='module__matiere', queryset=matieres, label='Matière', empty_label='Matière')

    class Meta:
        model = Activite
        fields = ('periode', 'type','matiere')
           
class MatiereCompetenceElementTable(tables.Table):
    action = '{% load icons %}\
        {% if perms.scolar.change_matierecompetenceelement %}\
            <a href="{% url "matiere_competence_element_update" pk=record.id matiere_pk=record.matiere.id %}"> {% icon "pencil-alt" %} </a>\
        {% endif %}\
        {% if perms.scolar.delete_matierecompetenceelement %}\
            <a href="{% url "matiere_competence_element_delete" pk=record.id matiere_pk=record.matiere.id %}"> {% icon "trash" %} </a>\
        {% endif %}'

    edit= tables.TemplateColumn(action, orderable=False)

    class Meta:
        model= MatiereCompetenceElement
        fields = ('matiere__code', 'matiere__titre', 'competence_element__code', 'competence_element__intitule', 'competence_element__objectif', 'niveau')
        template_name= "django_tables2/bootstrap4.html"


class CompetenceFamilyTable(tables.Table):
    action = '{% load icons %}\
        <a href="{% url "competence_list" competence_family_pk=record.code %}"> {% icon "eye" %} </a>'

    detail= tables.TemplateColumn(action, orderable=False)

    action = '{% load icons %}\
        {% if perms.scolar.change_competencefamily %}\
            <a href="{% url "competence_family_update" pk=record.code %}"> {% icon "pencil-alt" %} </a>\
        {% endif %}\
        {% if perms.scolar.delete_competencefamily %}\
            <a href="{% url "competence_family_delete" pk=record.code %}"> {% icon "trash" %} </a>\
        {% endif %}'

    edit= tables.TemplateColumn(action, orderable=False)
    class Meta:
        model = CompetenceFamily
        template_name= "django_tables2/bootstrap4.html"

class CompetenceTable(tables.Table):
    action = '{% load icons %}\
        <a href="{% url "competence_element_list" competence_pk=record.id %}"> {% icon "eye" %} </a>'

    detail = tables.TemplateColumn(action, orderable=False)

    action = '{% load icons %}\
        {% if perms.scolar.change_competence %}\
            <a href="{% url "competence_update" pk=record.id competence_family_pk=record.competence_family.code %}"> {% icon "pencil-alt" %} </a>\
        {% endif %}\
        {% if perms.scolar.delete_competence %}\
            <a href="{% url "competence_delete" pk=record.id competence_family_pk=record.competence_family.code %}"> {% icon "trash" %} </a>\
        {% endif %}'

    edit= tables.TemplateColumn(action, orderable=False)
    class Meta:
        model = Competence
        fields = ['code', 'intitule']
        template_name= "django_tables2/bootstrap4.html"

class CompetenceElementTable(tables.Table):
    action = '{% load icons %}\
        {% if perms.scolar.change_competenceelement %}\
            <a href="{% url "competence_element_update" pk=record.id competence_pk=record.competence.id %}"> {% icon "pencil-alt" %} </a>\
        {% endif %}\
        {% if perms.scolar.delete_competenceelement %}\
            <a href="{% url "competence_element_delete" pk=record.id competence_pk=record.competence.id %}"> {% icon "trash" %} </a>\
        {% endif %}'

    edit= tables.TemplateColumn(action, orderable=False)
    class Meta:
        model = CompetenceElement
        fields = ['code', 'intitule', 'type', 'objectif']
        template_name= "django_tables2/bootstrap4.html"

class PVTable(tables.Table):
    action = '{% load icons %}\
        <a href="{% url "pv_detail" pk=record.id %}" target="_blank"> {% icon "eye" %} </a>'

    detail= tables.TemplateColumn(action, orderable=False)
    action = '{% load icons %}\
        <a href="{% url "pv_delete" pk=record.id %}"> {% icon "trash" %} </a>'
    edit= tables.TemplateColumn(action, orderable=False)
    class Meta:
        model = PV
        fields = ['annuel', 'periode', 'note_eliminatoire', 'moy_ue', 'rang', 'tri_rang', 'photo', 'signature', 'anonyme', 'reserve']
        template_name= "django_tables2/bootstrap4.html"

class DiplomeTable(tables.Table):
    action = '{% load icons %}\
            {% if perms.scolar.change_diplome %}\
                <a href="{% url "diplome_update" pk=record.id %}" > {% icon "pencil-alt" %} </a>\
            {% endif %}\
            {% if perms.scolar.delete_diplome %}\
                <a href="{% url "diplome_delete" pk=record.id %}" > {% icon "trash" %} </a>\
            {% endif %}'
                  
    edit= tables.TemplateColumn(action, orderable=False)
    class Meta:
        model = Diplome
        fields = ['intitule',]
        template_name= "django_tables2/bootstrap4.html"

class DepartementTable(tables.Table):
    action = '{% load icons %}\
            {% if perms.scolar.change_departement %}\
                <a href="{% url "departement_update" pk=record.id %}" > {% icon "pencil-alt" %} </a>\
            {% endif %}\
            {% if perms.scolar.delete_departement %}\
                <a href="{% url "departement_delete" pk=record.id %}" > {% icon "trash" %} </a>\
            {% endif %}'
                  
    edit= tables.TemplateColumn(action, orderable=False)
    class Meta:
        model = Departement
        fields = ['intitule', 'intitule_a', 'responsable']
        template_name= "django_tables2/bootstrap4.html"

class SpecialiteTable(tables.Table):
    action = '{% load icons %}\
        {% if perms.scolar.change_specialite %}\
            <a href="{% url "specialite_update" pk=record.code %}"> {% icon "pencil-alt" %} </a>\
        {% endif %}'
    edit= tables.TemplateColumn(action, orderable=False)
    class Meta:
        model = Specialite
        template_name= "django_tables2/bootstrap4.html"

class PeriodeTable(tables.Table):
    action = '{% load icons %}\
        {% if perms.scolar.change_periode %}\
            <a href="{% url "periode_update" pk=record.id %}"> {% icon "pencil-alt" %} </a>\
        {% endif %}'
    edit= tables.TemplateColumn(action, orderable=False)
    class Meta:
        model = Periode
        fields=('code', 'session', 'ordre', 'nb_semaines')
        template_name= "django_tables2/bootstrap4.html"

class ProgrammeTable(tables.Table):
    action = '{% load icons %}\
            <a href="{% url "programme_detail" pk=record.id %}" > {% icon "eye" %} </a>'
    detail= tables.TemplateColumn(action, orderable=False)
    action = '{% load icons %}\
            {% if perms.scolar.change_programme %}\
                <a href="{% url "programme_update" pk=record.id %}" > {% icon "pencil-alt" %} </a>\
            {% endif %}'
    edit= tables.TemplateColumn(action, orderable=False)

    class Meta:
        model = Programme
        fields = ('code', 'titre', 'specialite', 'diplome', 'email_assistant')
        template_name= "django_tables2/bootstrap4.html"


class FormationTable(tables.Table):
    action='{% load icons %}\
            <a href="{% url "section_list" formation_pk=record.id %}" class="btn btn-link"> Sections </a> '
    detail=tables.TemplateColumn(action, orderable=False)
    action='{% load icons %}\
            <a href="{% url "export_inscriptions" formation_pk=record.id %}" > Liste Inscrits {% icon "file-excel" %} </a> '
    Inscrits=tables.TemplateColumn(action, orderable=False)    
    action='{% load icons %}\
            {% if perms.scolar.delete_formation %}\
                <a href="{% url "formation_delete" pk=record.id annee_univ_pk=record.annee_univ %}"> {% icon "trash" %} </a>\
            {% endif %}\
            {% if perms.scolar.change_formation %}\
                <a href="{% url "formation_archive_toggle" formation_pk=record.id %}"> {% icon "database" %} </a>\
            {% endif %}'
    edit=tables.TemplateColumn(action, orderable=False)
    
    class Meta:
        model = Formation
        fields=('programme','annee_univ', 'archive')
        template_name= "django_tables2/bootstrap4.html"

class PreinscriptionTable(tables.Table):
#     quittance=tables.Column()
#     def render_quittance(self,value,record):
#         return format_html("<img src='{}' width='300'>",value.url)

    action='{% load icons %}\
            <a href="{% url "validation_preinscription" inscription_pk=record.inscription.id %}" class="btn btn-warning"> Vérifier </a> '
    edit=tables.TemplateColumn(action, orderable=False)
    
    class Meta:
        model = Preinscription
        fields=('inscription__formation','inscription__etudiant')
        template_name= "django_tables2/bootstrap4.html"

class PreinscriptionFilter(django_filters.FilterSet):
    departement = django_filters.ModelChoiceFilter(field_name='inscription__formation__programme__departement', queryset=Departement.objects.all().order_by('cycle_ordre'), label='Département', empty_label='Département')
    
    class Meta:
        model = Preinscription
        fields = ('departement',)

class ResidenceUnivTable(tables.Table):
    
    class Meta:
        model = ResidenceUniv
        fields=('nom','adresse', 'wilaya', 'commune', 'tel')
        template_name= "django_tables2/bootstrap4.html"

class DeliberationFormationTable(tables.Table):
    action='{% load icons usergroup %}\
            <a href="{% url "deliberation_detail" formation_pk=record.id %}"> Délibérer </a>'
    detail=tables.TemplateColumn(action, orderable=False)
    class Meta:
        model = Formation
        fields=('annee_univ','programme',)
        template_name= "django_tables2/bootstrap4.html"

class PlanificationTable(tables.Table):
    action='{% for periode in record.programme.periodes.all %}\
                <a href="{% url "planification_update" formation_pk=record.id periode_pk=periode.id %}" class="btn btn-primary"> {{ periode.periode.code }} </a>\
            {% endfor %}'
    detail=tables.TemplateColumn(action, orderable=False)

    class Meta:
        model = Formation
        fields = ('programme','annee_univ')
        template_name= "django_tables2/bootstrap4.html"

class FormationFilter(django_filters.FilterSet):
    annee_univ = django_filters.ModelChoiceFilter(field_name='annee_univ', queryset=AnneeUniv.objects.all().order_by('-annee_univ'), label='Année Universitaire', empty_label='Année Universitaire')
    programme = django_filters.ModelChoiceFilter(field_name='programme', queryset=Programme.objects.all().order_by('ordre'), label='Programme', empty_label='Programme')
    class Meta:
        model = Formation
        fields = ('annee_univ', 'programme')

        

class EtudiantTable(tables.Table):
    photo=tables.Column()
    def render_photo(self,value,record):
        return format_html("<img src='{}' width='80'>",value.url)

    action= '<a href="{% url "etudiant_detail" pk=record.matricule %}" class="btn btn-info" role="button"> Détail</a>'
    detail=tables.TemplateColumn(action, orderable=False)


    class Meta:
        model = Etudiant
        fields = ('nom', 'nom_a', 'prenom', 'prenom_a', 'date_naissance', 'user__email', 'tel')
        template_name= "django_tables2/bootstrap4.html"

class EtudiantFilter(django_filters.FilterSet):
    matricule = django_filters.CharFilter(field_name='matricule', lookup_expr='iexact', label ='Matricule')
    nom = django_filters.CharFilter(field_name='nom', lookup_expr='icontains', label ='Nom de l\'étudiant(e)')
    rang_min = django_filters.NumberFilter(field_name='rang_min', lookup_expr='lte', label='Rang <')
    programme = django_filters.ModelChoiceFilter(field_name='inscriptions__formation', queryset=Formation.objects.filter(annee_univ__encours=True).order_by('programme__ordre'), label='Formation', empty_label='Formation')
    class Meta:
        model = Etudiant
        fields = ('matricule', 'nom','rang_min', 'programme')

        

class PVEnseignantTable(tables.Table):
    action = '{% load icons %}\
        <a href="{% url "pv_detail" pk=record.id %}" target="_blank"> {% icon "eye" %} </a>'

    detail= tables.TemplateColumn(action, orderable=False)
    class Meta:
        model = PV
        fields = ['formation', 'annuel', 'periode', 'photo']
        template_name= "django_tables2/bootstrap4.html"

class PVFilter(django_filters.FilterSet):
    annee_univ = django_filters.ModelChoiceFilter(field_name='formation__annee_univ', queryset=AnneeUniv.objects.all().order_by('-annee_univ'), label='Année Universitaire', empty_label='Année Universitaire')
    programme = django_filters.ModelChoiceFilter(field_name='formation__programme', queryset=Programme.objects.all().order_by('ordre'), label='Programme', empty_label='Programme')
    periode = django_filters.ModelChoiceFilter(field_name='periode', queryset=Periode.objects.all().order_by('ordre'), label='Semestre', empty_label='Semestre')
    
    class Meta:
        model = PV
        fields = ('annee_univ', 'programme', 'periode',)

        


class EnseignantTable(tables.Table):
    action='{% load icons %}\
            <a href="{% url "enseignant_edt" enseignant_pk=record.id %}" > {% icon "calendar-check" %} </a>'
    edt=tables.TemplateColumn(action, orderable=False)
    action='{% load icons %}\
            {% if perms.scolar.change_enseignant %}\
                <a href="{% url "enseignant_update" pk=record.id %}"> {% icon "pencil-alt" %} </a>\
            {% endif %}'
    edit=tables.TemplateColumn(action, orderable=False)

    class Meta:
        model = Enseignant
        fields = ('nom', 'eps', 'prenom', 'grade', 'tel', 'user__email', 'bureau', 'bal')
        template_name= "django_tables2/bootstrap4.html"

class EnseignantFilter(django_filters.FilterSet):
    nom = django_filters.CharFilter(field_name='nom', lookup_expr='icontains', label ='Nom de l\'enseignant(e)')
    grade = django_filters.ChoiceFilter(field_name='grade', choices=GRADE, label="Grade", empty_label="Grade")
    statut = django_filters.ChoiceFilter(field_name='statut', choices=STATUT, label="Statut", empty_label="Statut")
    situation = django_filters.ChoiceFilter(field_name='situation', choices=SITUATION, label="Situation", empty_label="Situation")
    class Meta:
        model = Enseignant
        fields = ('nom', 'grade', 'situation', 'statut')


class ChargeEnseignantTable(tables.Table):
    action= '{% load icons %}\
            {% if perms.scolar.change_charge %}\
                <a href="{% url "charge_enseignant_update" pk=record.id %}" > {% icon "pencil-alt" %}</a>\
            {% endif %}\
            {% if perms.scolar.delete_charge %}\
                <a href="{% url "charge_enseignant_delete" enseignant_pk=record.realisee_par.id pk=record.id %}" > {% icon "trash" %}</a>\
            {% endif %}'
            
    edit=tables.TemplateColumn(action, orderable=False)

    class Meta:
        model = Charge
        fields = ('periode', 'type', 'activite', 'obs', 'vh', 'vh_eq_td', 'cree_par', 'repeter_chaque_semaine')
        template_name= "django_tables2/bootstrap4.html"

class SectionTable(tables.Table):
    action='{% load icons %}\
            <a href="{% url "groupe_list" section_pk=record.id %}" class="btn btn-link"> Groupes </a> '
    detail=tables.TemplateColumn(action, orderable=False)
    action='{% load icons %}\
            {% if perms.scolar.delete_section %}\
                <a href="{% url "section_delete" pk=record.id formation_pk=record.formation.id %}"> {%  icon "trash" %} </a>\
            {% endif %}'
    edit=tables.TemplateColumn(action, orderable=False)

    class Meta:
        model = Section
        fields=('code', 'formation', 'taille')
        template_name= "django_tables2/bootstrap4.html"

class GroupeTable(tables.Table):
    action='{% load icons %}\
            {% for periode_ in record.section.formation.programme.periodes.all %}\
                {% if record.code %}\
                    <a href="{% url "etudiant_groupe_list" groupe_pk=record.id periode_pk=periode_.id %}"> {{ periode_.periode.code }} {% icon "user-friends" %} </a>\
                {% endif %}\
            {% endfor %}'
    detail=tables.TemplateColumn(action, orderable=False)
    action='{% load icons %}\
            {% if record.code %}\
                {% if perms.scolar.change_groupe %}\
                    <a href="{% url "groupe_update" pk=record.id section_pk=record.section.id %}"> {% icon "pencil-alt" %} </a> \
                {% endif %}\
                {% if perms.scolar.delete_groupe %}\
                    <a href="{% url "groupe_delete" pk=record.id section_pk=record.section.id %}"> {% icon "trash" %} </a>\
                {% endif %}\
            {% endif %}'
    edit=tables.TemplateColumn(action, orderable=False)

    taille=tables.Column(orderable=False)
    def render_taille(self,value,record):
        taille_periode_list=''
        for item in value:
            taille_periode_list+=item['periodepgm__periode__code']+' : '+str(item['taille'])+" "
        return format_html("{}", taille_periode_list)

    option=tables.Column()
    def render_option(self,value,record):
        ue_list=''
        for ue in value.all():
            ue_list+=str(ue)+'   '
        return format_html("{}",ue_list)

    class Meta:
        model = Groupe
        fields=('code', 'section','option', 'taille')
        template_name= "django_tables2/bootstrap4.html"

class GroupeAllTable(tables.Table):
    action='{% load icons %}\
            {% for periode_ in record.section.formation.programme.periodes.all %}\
                {% if record.code %}\
                    <a href="{% url "etudiant_groupe_list" groupe_pk=record.id periode_pk=periode_.id %}"> {{ periode_.periode.code }} {% icon "user-friends" %} </a>\
                {% endif %}\
            {% endfor %}'
    detail=tables.TemplateColumn(action, orderable=False)
    action='{% load icons %}\
            {% for periode_ in record.section.formation.programme.periodes.all %}\
                {% if record.code %}\
                    <a href="{% url "groupe_list_export" groupe_pk=record.id periode_pk=periode_.id %}" class="btn btn-success"> {{ periode_.periode.code }} {% icon "file-export" %} </a>\
                {% endif %}\
            {% endfor %}'
    admin=tables.TemplateColumn(action, orderable=False)
    
    option=tables.Column()
    def render_option(self,value,record):
        ue_list=''
        for ue in value.all():
            ue_list+=str(ue)+'   '
        return format_html("{}",ue_list)
    
    taille=tables.Column(orderable=False)
    def render_taille(self,value,record):
        taille_periode_list=''
        for item in value:
            taille_periode_list+=item['periodepgm__periode__code']+' : '+str(item['taille'])+" "
        return format_html("{}", taille_periode_list)
    
    class Meta:
        model = Groupe
        fields=('section__formation__programme','section','code', 'option','taille')
        template_name= "django_tables2/bootstrap4.html"

class GroupeAllFilter(django_filters.FilterSet):
    programme = django_filters.ModelChoiceFilter(field_name='section__formation__programme', queryset=Programme.objects.all().order_by('ordre'), label ='Formation', empty_label='Formation')

    class Meta:
        model = Groupe
        fields = ('programme',)
        

class NotesFormationTable(tables.Table):
    action='{% for periode in record.programme.periodes.all %}\
                    <a href="{% url "notes_formation_detail" formation_pk=record.id periode_pk=periode.id %}" class="btn btn-primary"> Notes {{periode.periode.code}} </a>\
            {% endfor %}'
                    
    detail=tables.TemplateColumn(action, orderable=False)
    class Meta:
        model = Formation
        exclude = ['id']
        template_name= "django_tables2/bootstrap4.html"




class TutoratTable(tables.Table):
    action='{% load icons %}\
            <a href="{% url "etudiant_detail" pk=record.etudiant.matricule %}"> {% icon "eye" %} </a>'
    detail=tables.TemplateColumn(action, orderable=False)
    class Meta:
        model = Inscription
        fields = ('etudiant', 'formation__programme')
        template_name= "django_tables2/bootstrap4.html"

class ModuleTable(tables.Table):
    action='<a href="{% url "module_detail" pk=record.id %}" class="btn btn-primary"> Coordination </a>'
    coordonner=tables.TemplateColumn(action, orderable=False)
    action='<a href="{% url "notes_formation_coordinateur_detail" formation_pk=record.formation.id periode_pk=record.periode.id module_pk=record.id %}" class="btn btn-success"> Notes </a>'
    notes=tables.TemplateColumn(action, orderable=False)
    
    formule_='Moy = \
                {% for eval_ in record.evaluations.all %}\
                    {% if forloop.first %}\
                        {{ eval_.ponderation}} x {{eval_.type}}\
                    {% else %}\
                        + {{ eval_.ponderation}} x {{eval_.type}}\
                    {% endif %}\
                {% endfor %}'
    formule=tables.TemplateColumn(formule_, orderable=False)

    class Meta:
        model = Module
        fields = ('matiere', 'periode')
        template_name= "django_tables2/bootstrap4.html"

class ModuleFeedbackTable(tables.Table):
    action='{% load icons %}\
            <a href="{% url "feedback_module_detail" module_pk=record.id %}" > {% icon "chart-bar" %} </a> '
    detail=tables.TemplateColumn(action, orderable=False)
    action='{% load icons %}\
            {% if perms.scolar.change_feedback %}\
                <a href="{% url "feedback_list" module_pk=record.id %}" > {% icon "pencil-alt" %} </a> \
            {% endif %}\
            {% if perms.scolar.add_feedback %}\
                <a href="{% url "import_feedback_module" module_pk=record.id %}" > {% icon "upload" %} </a>\
            {% endif %}'
    edit=tables.TemplateColumn(action, orderable=False)
    
    class Meta:
        model = Module
        fields = ['formation', 'periode', 'matiere']
        template_name= "django_tables2/bootstrap4.html"

class ModuleFilter(django_filters.FilterSet):
    matiere = django_filters.CharFilter(distinct=True, field_name='matiere__code', lookup_expr='icontains', label='Matière')
    formation = django_filters.ModelChoiceFilter(field_name='formation__programme', queryset=Programme.objects.all().order_by('ordre'), label='Formation', empty_label='Formation')
    annee_univ = django_filters.ModelChoiceFilter(field_name='formation__annee_univ', queryset=AnneeUniv.objects.all().order_by('annee_univ'), label='Année Universitaire', empty_label='Année Universitaire')
    periode = django_filters.ModelChoiceFilter(field_name='periode__periode', queryset=Periode.objects.all().order_by('ordre'), label='Semestre', empty_label='Semestre')
    class Meta:
        model = Module
        fields = ('matiere', 'formation', 'annee_univ', 'periode')


class CoordinationModuleFilter(django_filters.FilterSet):
    matiere = django_filters.CharFilter(distinct=True, field_name='matiere__code', lookup_expr='icontains', label='Matière')
    formation = django_filters.ModelChoiceFilter(field_name='formation__programme', queryset=Programme.objects.all().order_by('ordre'), label='Formation', empty_label='Formation')
    periode = django_filters.ModelChoiceFilter(field_name='periode__periode', queryset=Periode.objects.all().order_by('ordre'), label='Semestre', empty_label='Semestre')
    class Meta:
        model = Module
        fields = ('matiere', 'formation', 'periode')



class SemainierTable(tables.Table):
    action='{% load icons %}\
            <a href="{% url "semainier_update" pk=record.id module_pk=record.module.id %}"> {% icon "pencil-alt" %} </a>\
            <a href="{% url "semainier_delete" pk=record.id module_pk=record.module.id %}"> {% icon "trash" %} </a>'
    actions=tables.TemplateColumn(action, orderable=False)
    class Meta:
        model = Semainier
        fields = ('semaine', 'activite_cours', 'activite_dirigee', 'observation', 'objectifs', 'matiere_competence_element__competence_element__intitule')
        template_name= "django_tables2/bootstrap4.html"

class FeedbackTable(tables.Table):
    action='{% load icons %}\
            {% if perms.scolar.change_feedback %}\
                <a href="{% url "feedback_update" pk=record.id module_pk=record.module.id %}" > {% icon "pencil-alt" %} </a>\
            {% endif %}'
            
    edit=tables.TemplateColumn(action, orderable=False)
    class Meta:
        model = Feedback
        fields=('comment','show')
        template_name= "django_tables2/bootstrap4.html"

class EvaluationTable(tables.Table):
    action='{% if perms.scolar.delete_evaluation %}\
                <a href="{% url "evaluation_delete" pk=record.id module_pk=record.module.id %}" class="btn btn-danger"> Supprimer </a>  \
            {% endif %}\
            {% if perms.scolar.change_evaluation %}\
                <a href="{% url "evaluation_update" pk=record.id module_pk=record.module.id %}" class="btn btn-warning"> Modifier </a>\
            {% endif %}'
    actions=tables.TemplateColumn(action, orderable=False)
    class Meta:
        model = Evaluation
        fields = ('type', 'ponderation')
        template_name= "django_tables2/bootstrap4.html"


class AnneeUnivTable(tables.Table):
    action = '{% load icons %}\
            <a href="{% url "formation_list" annee_univ_pk=record.annee_univ %}" class="btn btn-link" role="button"> Formations </a> '
    detail= tables.TemplateColumn(action, orderable=False)
    action = '{% load icons %}\
            {% if perms.scolar.change_anneeuniv %}\
                <a href="{% url "anneeuniv_update" pk=record.annee_univ %}"> {% icon "pencil-alt" %} </a>\
            {% endif %}'
    edit= tables.TemplateColumn(action, orderable=False)

    class Meta:
        model = AnneeUniv
        template_name= "django_tables2/bootstrap4.html"
                
class SeanceTable(tables.Table):
    action='{% load icons %}\
            <a href="{% url "seance_update" activite_pk=record.activite.id pk=record.id %}">{% icon "pencil-alt" %}</a>\
            <a href="{% url "seance_delete" activite_pk=record.activite.id pk=record.id %}">{% icon "trash" %}</a>\
            <a href="{% url "absence_seance_list" seance_pk=record.id activite_pk=record.activite.id %}">{% icon "eye" %}</a>'
    actions=tables.TemplateColumn(action, orderable=False)
    action='{% load icons %}\
            {% for groupe in record.activite.cible.all %}\
                {% if groupe.code %}\
                    <a href="{% url "absencesform" activite_pk=record.activite.id groupe_pk=groupe.id %}" class="btn btn-danger">{{ groupe.code }}</a>\
                {% else %}\
                    {% for groupe_section in groupe.section.groupes.all %}\
                        {% if groupe_section.code %}\
                            <a href="{% url "absencesform" activite_pk=record.activite.id groupe_pk=groupe_section.id %}" class="btn btn-danger">{{ groupe_section.code }}</a>\
                        {% endif %}\
                    {% endfor %}\
                {% endif %}\
            {% endfor%}'
    absences=tables.TemplateColumn(action, orderable=False)
        
    class Meta:
        model=Seance
        template_name="django_tables2/bootstrap4.html"
        