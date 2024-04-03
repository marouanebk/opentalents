from django import template
from django.forms import BoundField
from django.utils.html import format_html
import os
register = template.Library()

@register.filter('session_from_inscription_periode')
def session_from_inscription_periode(inscription_periode, periode_):
    """
    usage example {{ inscription_periode|session_from_inscription_periode:periode }}
    """
    session=''
    try:
        return inscription_periode.inscription.formation.periodes.get(periode=periode_).session
    except Exception:
        return session

@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key)
    
@register.filter('value_from_obj')
def value_from_obj(obj, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return obj.__dict__.get(key)

@register.filter('addstr')
def addstr(str1,str2):
    return str(str1)+str(str2)

@register.filter('topercent')
def percent(value,total):
    return value/total

@register.filter('sub')
def sub(value, arg):
    return value - arg

@register.filter
def as_percentage_of(part, whole):
    try:
        return round( (float(part) / float(whole) * 100),2)
    except (ValueError, ZeroDivisionError):
        return 0.00
 
@register.filter('multiply')
def multiply(qty1, qty2):
    return qty1 * qty2

@register.filter('tostr')
def tostr(str1):
    return str(str1)

@register.filter('decision_full')
def decision_full(str1):
    DECISIONS_JURY={
            'C':'En cours',
            'A':'Admis',
            'AR':'Admis avec Rachat',
            'DR':'Rattrapage',
            'SR':'Admis avec Rattrapage',
            'AD':'Admis avec Dettes',
            'R':'Redouble',
            'F':'Abandon',
            'FD':'Défaillant',
            'M':'Maladie',
            'N':'Non Admis',
        }
    return DECISIONS_JURY[str1]

@register.filter('startswith')
def startswith(text, starts):
    return str(text).startswith(starts)

FR_EN_DICT={
    'Juin':'June',
    'Juillet':'July',
    'Janvier':'January',
    'Février':'February',
    'Octobre':'October',
    'Novembre':'November',
    'Décembre':'December',
    "Ingénieur d'état en Informatique":"Computer science engineer",
    "Master Académique":"Master of Science (MSc)",
    "Doctorat":"Doctorate",
    "1ère année":"1st year",
    "1ère année - Second Cycle":"1st year - 2nd Cycle",
    "2ème année - Second Cycle":"2nd year - 2nd Cycle ",
    "3ème année - Second Cycle":"3rd year - 2nd Cycle ",
    "2ème année":"2nd year",
    "Second Cycle":"2nd Cycle",
    "Classes préparatoires":"Preparatory classes",
    "Département de la formation préparatoire":"Department of preparatory training",
    "Département d'ingénierie de l'information et des systèmes informatiques":"Department of information and computer systems engineering",
    "1ère année - Classes Préparatoires (CP)":"1st year preparatory class",
    "2ème année - Classes Préparatoires (CP)":"2nd year preparatory class",
    'Admis':'Passed',
    'Admis avec Rachat':'Passed with Board\'s Grace',
    'Admis avec Rattrapage':'Passed with Catch-up',
    'Doit passer le Rattrapage':'Must pass Catch-up',
    'Admis avec Dettes':'Passed with Debts',
    'Redouble':'Retake',
    'Ajournement':'Retake',
    'Prolongation':'Prolongation',
    'Abandon':'Leaver',
    'Défaillant':'Defaulting',
    'Transfert':'Transferred',
    'Non Admis':'Failed',
    'Non Inscrit':'Not Registered',
    'Inscrit':'Registered',
    'Admis au Concours':'Admitted to the entrance exam',
    'Admis au Concours avec Rachat':'Admitted to the entrance exam with board\'s grace',
    'UE Fondamentale':'Fundamental',
    'UE Méthodologique':'Methodological',
    'UE Transversale':'Transversal',
    'UE Découverte':'Discovery',
    'Mathématiques et Informatique':'Mathematics and Computer Science',
    'Informatique':'Computer Science',
}
@register.filter 
def english(fr):
    """
    returns translation of fr
    """
    return FR_EN_DICT.get(fr)

FR_AR_DICT={
    'Congé académique (année blanche) pour raisons médicales':'عطلة أكاديمية سنة بيضاء لاسباب صحية ',
    'Congé académique (année blanche) pour raisons personnelles':'عطلة أكاديمية سنة بيضاء لاسباب شخصية',
    'Congé académique (année blanche) pour raisons personnelles (Covid 19)':'عطلة أكاديمية سنة بيضاء لاسباب شخصية كوفيد 19',
    'Congé académique (année blanche) pour raisons familiales':'عطلة أكاديمية سنة بيضاء لاسباب عائلية',
    'Juin':'جوان',
    'Juillet':'جويلية',
    'Janvier':'جانفي',
    'Février':'فيفري',
    'Octobre':'أكتوبر',
    'Novembre':'نوفمبر',
    'Décembre':'ديسمبر',
    "Ingénieur d'état en Informatique":"مهندس دولة في الاعلام الالي",
    "Master Académique":"ماستر أكاديمي",
    "1ère année":"سنة اولى",
    "1ère année - Second Cycle":"سنة اولى طور ثاني",
    "2ème année - Second Cycle":"سنة ثانية طور ثاني ",
    "3ème année - Second Cycle":"سنة ثالثة طور ثاني ",
    "2ème année":"سنة ثانية",
    "Second Cycle":"طور ثاني",
    "Classes préparatoires":"أقسام تحضيرية",
    "Département de la formation préparatoire":"قسم التكوين التحضيري",
    "Département d'ingénierie de l'information et des systèmes informatiques":"قسم هندسة المعلومات و انظمة الحاسوب",
    "1ère année - Classes Préparatoires (CP)":"سنة اولى قسم تحضيري",
    "2ème année - Classes Préparatoires (CP)":"سنة ثانية قسم تحضيري",
    'Admis':'ناجح',
    'Admis avec Rachat':'ناجح مع الانقاذ',
    'Redouble':'معيد',
    'Ajournement':'تأجيل',
    'Prolongation':'تمديد',
    'Abandon':'مغادر',
    'Transfert':'منتقل',
    'Non Admis':'راسب',
    'Non Inscrit':'غير مسجل',
    'Inscrit':'مسجل',
    'Admis au Concours':'تم قبوله في المسابقة',
    'Admis au Concours avec Rachat':'ناجح في المسابقة بالانقاذ',
    'UE Fondamentale':'وحدات التعليم الأساسية',
    'UE Méthodologique':'وحدات التعليم المنهجية',
    'UE Transversale':'وحدات التعليم الأفقية',
    'UE Découverte':'وحدات التعليم الإستكشافية',
    'Mathématiques et Informatique':'رياضيات و اعلام الي',
    'Informatique':'اعلام الي',
    'S1':'س 1',
    'S2':'س 2',
    'S3':'س 3',
    'S4':'س 4',
    'S5':'س 5',
    'S6':'س 6',
    'S5+S6':'س5  +  س6',
    'AN':'سنوي',
    'T1':'ف 1',
    'T2':'ف 2',
    'T3':'ف 3',
}
@register.filter 
def arabic(fr):
    """
    returns translation of fr to ar
    """
    return FR_AR_DICT.get(fr)

@register.filter 
def nom_mois(date):
    """
    returns name of the month on french
    """
    MOIS=[
        '',
        'Janvier',
        'Février',
        'Mars',
        'Avril',
        'Mai',
        'Juin',
        'Juillet',
        'Août',
        'Septembre',
        'Octobre',
        'Novembre',
        'Décembre'
        ]
    if date:
        return MOIS[date.month]
    else:
        return MOIS[0]

@register.filter 
def form_field(form, key):
    """
    returns field from forms.fields[key]
    """
    if key not in form.fields.keys():
        return None
    
    boundField = BoundField(form, form.fields[key], key)
    return boundField

@register.filter('autorite_from_document_programme')
def autorite_from_document_programme(document, programme):
    from scolar.models import DocumentConfig
    autorite = ''
    try:
        return DocumentConfig.objects.get(code=document, programme=programme).autorite
    except Exception:
        return autorite

@register.filter('autorite_entete_from_document_programme')
def autorite_entete_from_document_programme(document, programme):
    from scolar.models import DocumentConfig
    autorite = ''
    try:
        return DocumentConfig.objects.get(code=document, programme=programme).autorite_entete
    except Exception:
        return autorite

@register.filter('autorite_from_document_diplome')
def autorite_from_document_diplome(document, diplome):
    from scolar.models import DocumentConfig
    autorite = ''
    try:
        return DocumentConfig.objects.get(code=document, diplome=diplome).autorite
    except Exception:
        return autorite
    
@register.filter('autorite_entete_from_document_diplome')
def autorite_entete_from_document_diplome(document, diplome):
    from scolar.models import DocumentConfig
    autorite = ''
    try:
        return DocumentConfig.objects.get(code=document, diplome=diplome).autorite_entete
    except Exception:
        return autorite
    
@register.filter('autorite_from_document')
def autorite_from_document(document):
    from scolar.models import DocumentConfig
    autorite = ''
    try:
        return DocumentConfig.objects.get(code=document).autorite
    except Exception:
        return autorite
    
@register.filter('autorite_entete_from_document')
def autorite_entete_from_document(document):
    from scolar.models import DocumentConfig
    autorite = ''
    try:
        return DocumentConfig.objects.get(code=document).autorite_entete
    except Exception:
        return autorite

@register.filter('document_programme_actif')
def document_programme_actif(document, programme):
    from scolar.models import DocumentConfig
    actif=False
    try:
        return DocumentConfig.objects.get(code=document, programme=programme).actif
    except Exception:
        return actif


@register.filter('has_acces_visualisation_notes_programme')
def has_acces_visualisation_notes_programme(user, programme):
    acces=False
    try:
        return user.has_acces_visualisation_notes_programme(programme)
    except Exception:
        return acces
    
@register.filter('has_acces_gestion_etudiants_programme')
def has_acces_gestion_etudiants_programme(user, programme):
    acces=False
    try:
        return user.has_acces_gestion_etudiants_programme(programme)
    except Exception:
        return acces


@register.filter('converson_reel_vers_entier_si_possible')
def converson_reel_vers_entier_si_possible(number):
    import decimal
    try:
        if decimal.Decimal(number) == int(number) :
            return int(number)
        else :
            return number
        
    except Exception:
        return number
        
@register.filter('phrase_contient_chiffre')
def phrase_contient_chiffre(phrase):
    try:
        return any((char.isdigit()) for char in phrase)

    except Exception:
        return False
    
@register.filter('is_coordinateur_module_validable')
def is_coordinateur_module_validable(module, user):
    try:
        return user.is_coordinateur(module)
    except Exception:
        return False

@register.filter
def filename(value):
    return os.path.basename(value.file.name)
