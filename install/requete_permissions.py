from django.db.models import Q
from django.contrib.auth.models import Group, Permission

# direction
permissions_ = (

    ("fonctionnalite_configurationetablissement_visualisation", "Visualiser la configuration de l'établissement : Institution, résidences universitaires, charges, géo, rôles et droits d'accès.."),
    ("fonctionnalite_configurationetablissement_modification", "Modifier la configuration de l'établissement : Institution, résidences universitaires, charges, géo, rôles et droits d'accès.."),


    ("fonctionnalitenav_dashboard_etudiants", "Visualiser le dashboard des étudiants : Effectifs, lieux de résidences, assiduité, etc"),
    ("fonctionnalitenav_dashboard_enseignants", "Visualiser le dashboard des enseignants : Effectifs, assiduité, répartition des charges, etc"),
    ("fonctionnalitenav_dashboard_formations", "Visualiser le dashboard des formations : Ratios des décisions de jury par année, global, etc"),


    ("fonctionnalitenav_etudiants_annuairecomplet", "Visualiser l'annuaire complet des étudiants (+toutes leurs inscriptions)"),
    ("fonctionnalitenav_etudiants_groupes", "Visualiser la liste des groupes de l'année en cours"),
    ("fonctionnalitenav_etudiants_documentsgroupes", "Générer les documents groupés concernant l'étudiant : Certificats de scolarité, relevés de notes, fiches PFE, .."),
    ("fonctionnalitenav_etudiants_preinscriptions", "Afficher et valider les préinscriptions de tous les étudiants."),
    ("fonctionnalitenav_etudiants_visualisationabsences", "Visualiser la liste des absences des étudiants"),
    ("fonctionnalitenav_etudiants_signalementabsences", "Signaler les absences des étudiants"),
    ("fonctionnalitenav_etudiants_rapportabsences", "Visualiser le rapport des absences des étudiants par formation, semestre, type d'activité pédagogique, .."),

    ("fonctionnalite_etudiants_justificationabsences", "Justifier les absences des étudiants"),
    ("fonctionnalite_etudiants_visualisationsensible", "Visualiser les informations sensibles des étudiants (tél, ..)"),
    ("fonctionnalite_etudiants_gestion", "Ajouter/Importer/Modifier/Supprimer les étudiants, inscriptions, affectations aux groupes, tutorats, et autres informations relatives aux étudiants"),
    ("fonctionnalite_etudiants_visualisationnotesprofil", "Visualiser les notes (relevés et ECTS) dans le profil des étudiants"),            
    ("fonctionnalite_etudiants_documents", "Télécharger les documents prêts des étudiants : Fiches d'inscription, relevés et certificats PDF signés, attestations.. (permission ne couvrant pas les documents volontairement non-signés -S)"),
    ("fonctionnalite_etudiants_documentsnonsignes", "Télécharger les documents non signés de l'étudiant"),
    ("fonctionnalite_etudiants_reinitialisationnotesetacquis", "Réinitialiser les notes des semestres/UE/modules des étudiants, insertion des modules acquis"),
	("fonctionnalite_etudiants_visualisationinfosfamille", "Visualiser les informations sensibles de l'étudiant : fonction des parents, moyenne du bac,ect"),

    ("fonctionnalitenav_enseignants_annuairecomplet", "Visualiser l'annuaire complet des enseignants"),
    ("fonctionnalitenav_enseignants_visualisationabsences", "Visualiser la liste des absences des enseignants"),
    ("fonctionnalitenav_enseignants_signalementabsences", "Signaler les absences des enseignants"),
    ("fonctionnalitenav_enseignants_visualisationcharges", "Visualiser la liste des charges des enseignants"),
	("fonctionnalite_enseignants_export", "Exporter les enseignants"),
    ("fonctionnalite_enseignants_visualisationsensible", "Visualiser les informations sensibles des enseignants (tél, ..)"),
    ("fonctionnalite_enseignants_gestion", "Ajouter, importer et modifier les enseignants"),
    ("fonctionnalite_enseignants_documents", "Télécharger les documents prêts des enseignants"),
    ("fonctionnalite_enseignants_justificationabsences", "Justifier les absences des enseignants"),
    ("fonctionnalite_enseignants_gestioncharges", "Importer/Ajouter/Modifier des charges concernant des enseignants"),

    ("fonctionnalitenav_Export_exportationprogres", "Exporter des fichiers selon les canevas de progres"),
    ("fonctionnalitenav_Export_exportationlistes", "Exporter des différents listes(list service national selon le canevas,maladie,non inscrit, abandon...)"),


    ("fonctionnalitenav_pedagogie_gestionprogrammes", "Gérer le catalogue des programmes et matières, configurer les diplômes, spécialités, périodes et départements"),
    ("fonctionnalitenav_pedagogie_visualisationfeedbacks", "Visualiser la liste des feedbacks des enseignements (commentaires des étudiants non inclus dans la permission)"),
    ("fonctionnalitenav_pedagogie_edt", "Visualiser les emplois du temps publics des groupes, étudiants et enseignants via l'EDT Finder"),
    ("fonctionnalitenav_pedagogie_visualisationcoordination", "Visualiser les coordination de tous les modules : coordinateurs, évaluations, formules, .."),
    ("fonctionnalitenav_pedagogie_visualisationnotes", "Visualiser les notes de tous les modules, par formation, par semestre.."),
    ("fonctionnalitenav_pedagogie_generationpvsdeliberation", "Générer les PVs de délibération, calcul des notes éliminatoires (+PVs des NE), calcul des rangs et moyennes, confirmation et envoi des décisions, passage à l'année suivante.."),
    ("fonctionnalitenav_pedagogie_visualisationpvsdeliberation", "Visualiser tous les PVs de délibération"),

    ("fonctionnalite_pedagogie_visualisationcommentairesfeedbacks", "Visualiser les commentaires de feedback des étudiants"),
    ("fonctionnalite_pedagogie_importationfeedbacks", "Importer les feedbacks des modules"),
    ("fonctionnalite_pedagogie_validationfeedbacks", "Valider/modifier les feedbacks des étudiants et leur état de validation"),
    ("fonctionnalite_pedagogie_gestioncompetences", "Gérer la base de compétences : Ajout de familles de compétences, compétences, et éléments de compétences"),
    ("fonctionnalite_pedagogie_gestioncoordination", "Gérer la coordination de tous les modules : Affecter les coordinateurs, modifier les évaluations, formules, .. "),
    ("fonctionnalite_pedagogie_modificationnotes", "Modifier/Importer les notes de tous les modules"),


    ("fonctionnalitenav_planification_visualisationformations", "Visualiser la liste des formations existantes par année universitaire, avec leurs sections et groupes"),
    ("fonctionnalitenav_planification_activites", "Gérer la planification des activités : Importation, ajout, suppression"),
    ("fonctionnalitenav_planification_chargementagenda", "Charger l'Agenda (Google, ..) avec les activités planifiées"),
    ("fonctionnalitenav_planification_reinitialisationagenda", "Réinitialiser l'Agenda (Google, ..)"),

    ("fonctionnalite_planification_gestionformations", "Gérer les formations par année universitaire : Création, modification, suppression des années universitaires, formations, sections et groupes"),
    ("fonctionnalite_planification_visualisationseances", "Visualiser les séances des activités de tous les modules"),
    ("fonctionnalite_planification_gestionseances", "Gérer les séances de tous les modules : Ajouter des séances de rattrapage, .."),


    ("fonctionnalitenav_examens_gestionsalles", "Gérer la liste des salles d'examen"),
    ("fonctionnalitenav_examens_visualisationexamens", "Visualiser la liste des examens"),
    ("fonctionnalitenav_examens_visualisationsurveillance", "Visualiser la répartition des surveillants aux examens"),
    ("fonctionnalitenav_examens_visualisationplacesetudiants", "Visualiser la répartition des étudiants dans les salles d'examen"),
    ("fonctionnalitenav_examens_exportatonlisteplaces", "Exporter la liste des places disponibles dans toutes les salles d'examen"),

    ("fonctionnalite_examens_gestionexamens", "Gérer les examens : Création, modification, affectation des surveillants, placement des étudiants, envoi des convocations.."),
    ("fonctionnalite_examens_visualisationreprographie", "Visualiser la reprographie des examens"),

    ("fonctionnalitenav_stages_visualisationstages", "Visualiser la liste des stages de fin d'études et de master"),
    ("fonctionnalitenav_stages_soumission", "Soumettre un sujet de stage (permission n'affectant pas le droit naturel des étudiants, enseignants et partenaires à soumettre un stage)"),
    ("fonctionnalitenav_stages_validation", "Contrôler le processus de validation des stages, visionner leurs états de validation, leur affecter des experts/commissions, modifier les stages, supprimer les stages.."),
    ("fonctionnalitenav_stages_experts", "Visualiser l'index des experts (expertisant les sujets de stage)"),
    ("fonctionnalitenav_stages_visualisationsoutenances", "Visualiser la liste des soutenances de stages de PFE et Master + PVs + Fiches d'évaluation .."),
    ("fonctionnalitenav_stages_visualisationpartenaires", "Visualiser la liste des organismes partenaires"),
    ("fonctionnalitenav_stages_exportationpartenaires", "Exporter la liste des organismes partenaires"),
    ("fonctionnalitenav_stages_exportationstages", "Exporter la liste des stages de fin d'étude et de master"),
    ("fonctionnalitenav_stages_visualisationsoutenancesequipes", "Visualiser la liste des soutenances de toutes les matières d'équipe (+PVs, fiches d'évaluation, liste des équipes ..)"),
    
    ("fonctionnalite_stages_gestionpartenaires", "Gérer/Importer les organismes partenaires, créer des comptes utilisateurs aux partenaires afin qu'ils puissent déposer des sujets de stage"),
    ("fonctionnalite_stages_importation", "Importer les sujets de stages et leurs affectations aux groupes"),
    ("fonctionnalite_stages_modificationsoutenances", "Modifier les soutenances de tous les PFE et Master (dates, jurys, mentions, ..)"),
    ("fonctionnalite_stages_modificationsoutenancesequipes", "Modifier les soutenances de toutes les matières d'équipe (dates, jurys, mentions, ..)"),
    ("fonctionnalite_tracabilite_visualisation", "Visualiser les données de traçabilité (actions faîtes par les utilisateurs)"),
    ("fonctionnalite_tracabilite_suppression", "Supprimer les données de traçabilité"),
)

group_, created=Group.objects.get_or_create(name='direction', defaults={
                'name':'direction',
            })
for permission_ in permissions_ :
    permission_object=Permission.objects.get(codename=permission_[0])
    if not permission_object in group_.permissions.all() :
        group_.permissions.add(permission_object)
        
        




# stage
permissions_ = (

    ("fonctionnalite_configurationetablissement_visualisation", "Visualiser la configuration de l'établissement : Institution, résidences universitaires, charges, géo, rôles et droits d'accès.."),
    #("fonctionnalite_configurationetablissement_modification", "Modifier la configuration de l'établissement : Institution, résidences universitaires, charges, géo, rôles et droits d'accès.."),
    ("fonctionnalitenav_dashboard_etudiants", "Visualiser le dashboard des étudiants : Effectifs, lieux de résidences, assiduité, etc"),
    ("fonctionnalitenav_dashboard_enseignants", "Visualiser le dashboard des enseignants : Effectifs, assiduité, répartition des charges, etc"),
    ("fonctionnalitenav_dashboard_formations", "Visualiser le dashboard des formations : Ratios des décisions de jury par année, global, etc"),


    ("fonctionnalitenav_etudiants_annuairecomplet", "Visualiser l'annuaire complet des étudiants (+toutes leurs inscriptions)"),
    ("fonctionnalitenav_etudiants_groupes", "Visualiser la liste des groupes de l'année en cours"),
    ("fonctionnalitenav_etudiants_documentsgroupes", "Générer les documents groupés concernant l'étudiant : Certificats de scolarité, relevés de notes, fiches PFE, .."),
    #("fonctionnalitenav_etudiants_preinscriptions", "Afficher et valider les préinscriptions de tous les étudiants."),
    #("fonctionnalitenav_etudiants_visualisationabsences", "Visualiser la liste des absences des étudiants"),
    #("fonctionnalitenav_etudiants_signalementabsences", "Signaler les absences des étudiants"),
    #("fonctionnalitenav_etudiants_rapportabsences", "Visualiser le rapport des absences des étudiants par formation, semestre, type d'activité pédagogique, .."),

    #("fonctionnalite_etudiants_justificationabsences", "Justifier les absences des étudiants"),
    ("fonctionnalite_etudiants_visualisationsensible", "Visualiser les informations sensibles des étudiants (tél, ..)"),
    #("fonctionnalite_etudiants_gestion", "Ajouter/Importer/Modifier/Supprimer les étudiants, inscriptions, affectations aux groupes, tutorats, et autres informations relatives aux étudiants"),
    ("fonctionnalite_etudiants_visualisationnotesprofil", "Visualiser les notes (relevés et ECTS) dans le profil des étudiants"),            
    ("fonctionnalite_etudiants_documents", "Télécharger les documents prêts des étudiants : Fiches d'inscription, relevés et certificats PDF signés, attestations.. (permission ne couvrant pas les documents volontairement non-signés -S)"),
    ("fonctionnalite_etudiants_documentsnonsignes", "Télécharger les documents non signés de l'étudiant"),
    #("fonctionnalite_etudiants_reinitialisationnotesetacquis", "Réinitialiser les notes des semestres/UE/modules des étudiants, insertion des modules acquis"),


    ("fonctionnalitenav_enseignants_annuairecomplet", "Visualiser l'annuaire complet des enseignants"),
    #("fonctionnalitenav_enseignants_visualisationabsences", "Visualiser la liste des absences des enseignants"),
    #("fonctionnalitenav_enseignants_signalementabsences", "Signaler les absences des enseignants"),
    ("fonctionnalitenav_enseignants_visualisationcharges", "Visualiser la liste des charges des enseignants"),

    ("fonctionnalite_enseignants_visualisationsensible", "Visualiser les informations sensibles des enseignants (tél, ..)"),
    #("fonctionnalite_enseignants_gestion", "Ajouter, importer et modifier les enseignants"),
    ("fonctionnalite_enseignants_documents", "Télécharger les documents prêts des enseignants"),
    #("fonctionnalite_enseignants_justificationabsences", "Justifier les absences des enseignants"),
    #("fonctionnalite_enseignants_gestioncharges", "Importer/Ajouter/Modifier des charges concernant des enseignants"),


    #("fonctionnalitenav_pedagogie_gestionprogrammes", "Gérer le catalogue des programmes et matières, configurer les diplômes, spécialités, périodes et départements"),
    ("fonctionnalitenav_pedagogie_visualisationfeedbacks", "Visualiser la liste des feedbacks des enseignements (commentaires des étudiants non inclus dans la permission)"),
    ("fonctionnalitenav_pedagogie_edt", "Visualiser les emplois du temps publics des groupes, étudiants et enseignants via l'EDT Finder"),
    ("fonctionnalitenav_pedagogie_visualisationcoordination", "Visualiser les coordination de tous les modules : coordinateurs, évaluations, formules, .."),
    ("fonctionnalitenav_pedagogie_visualisationnotes", "Visualiser les notes de tous les modules, par formation, par semestre.."),
    #("fonctionnalitenav_pedagogie_generationpvsdeliberation", "Générer les PVs de délibération, calcul des notes éliminatoires (+PVs des NE), calcul des rangs et moyennes, confirmation et envoi des décisions, passage à l'année suivante.."),
    ("fonctionnalitenav_pedagogie_visualisationpvsdeliberation", "Visualiser tous les PVs de délibération"),

    ("fonctionnalite_pedagogie_visualisationcommentairesfeedbacks", "Visualiser les commentaires de feedback des étudiants"),
    #("fonctionnalite_pedagogie_importationfeedbacks", "Importer les feedbacks des modules"),
    #("fonctionnalite_pedagogie_validationfeedbacks", "Valider/modifier les feedbacks des étudiants et leur état de validation"),
    #("fonctionnalite_pedagogie_gestioncompetences", "Gérer la base de compétences : Ajout de familles de compétences, compétences, et éléments de compétences"),
    #("fonctionnalite_pedagogie_gestioncoordination", "Gérer la coordination de tous les modules : Affecter les coordinateurs, modifier les évaluations, formules, .. "),
    #("fonctionnalite_pedagogie_modificationnotes", "Modifier/Importer les notes de tous les modules"),


    ("fonctionnalitenav_planification_visualisationformations", "Visualiser la liste des formations existantes par année universitaire, avec leurs sections et groupes"),
    #("fonctionnalitenav_planification_activites", "Gérer la planification des activités : Importation, ajout, suppression"),
    #("fonctionnalitenav_planification_chargementagenda", "Charger l'Agenda (Google, ..) avec les activités planifiées"),
    #("fonctionnalitenav_planification_reinitialisationagenda", "Réinitialiser l'Agenda (Google, ..)"),

    #("fonctionnalite_planification_gestionformations", "Gérer les formations par année universitaire : Création, modification, suppression des années universitaires, formations, sections et groupes"),
    #("fonctionnalite_planification_visualisationseances", "Visualiser les séances des activités de tous les modules"),
    #("fonctionnalite_planification_gestionseances", "Gérer les séances de tous les modules : Ajouter des séances de rattrapage, .."),


    #("fonctionnalitenav_examens_gestionsalles", "Gérer la liste des salles d'examen"),
    #("fonctionnalitenav_examens_visualisationexamens", "Visualiser la liste des examens"),
    #("fonctionnalitenav_examens_visualisationsurveillance", "Visualiser la répartition des surveillants aux examens"),
    #("fonctionnalitenav_examens_visualisationplacesetudiants", "Visualiser la répartition des étudiants dans les salles d'examen"),
    #("fonctionnalitenav_examens_exportatonlisteplaces", "Exporter la liste des places disponibles dans toutes les salles d'examen"),

    #("fonctionnalite_examens_gestionexamens", "Gérer les examens : Création, modification, affectation des surveillants, placement des étudiants, envoi des convocations.."),
    #("fonctionnalite_examens_visualisationreprographie", "Visualiser la reprographie des examens"),

    ("fonctionnalitenav_stages_visualisationstages", "Visualiser la liste des stages de fin d'études et de master"),
    ("fonctionnalitenav_stages_soumission", "Soumettre un sujet de stage (permission n'affectant pas le droit naturel des étudiants, enseignants et partenaires à soumettre un stage)"),
    ("fonctionnalitenav_stages_validation", "Contrôler le processus de validation des stages, visionner leurs états de validation, leur affecter des experts/commissions, modifier les stages, supprimer les stages.."),
    ("fonctionnalitenav_stages_experts", "Visualiser l'index des experts (expertisant les sujets de stage)"),
    ("fonctionnalitenav_stages_visualisationsoutenances", "Visualiser la liste des soutenances de stages de PFE et Master + PVs + Fiches d'évaluation .."),
    ("fonctionnalitenav_stages_visualisationpartenaires", "Visualiser la liste des organismes partenaires"),
    ("fonctionnalitenav_stages_exportationpartenaires", "Exporter la liste des organismes partenaires"),
    ("fonctionnalitenav_stages_exportationstages", "Exporter la liste des stages de fin d'étude et de master"),
    ("fonctionnalitenav_stages_visualisationsoutenancesequipes", "Visualiser la liste des soutenances de toutes les matières d'équipe (+PVs, fiches d'évaluation, liste des équipes ..)"),
    
    ("fonctionnalite_stages_gestionpartenaires", "Gérer/Importer les organismes partenaires, créer des comptes utilisateurs aux partenaires afin qu'ils puissent déposer des sujets de stage"),
    ("fonctionnalite_stages_importation", "Importer les sujets de stages et leurs affectations aux groupes"),
    ("fonctionnalite_stages_modificationsoutenances", "Modifier les soutenances de tous les PFE et Master (dates, jurys, mentions, ..)"),
    ("fonctionnalite_stages_modificationsoutenancesequipes", "Modifier les soutenances de toutes les matières d'équipe (dates, jurys, mentions, ..)"),
)

group_, created=Group.objects.get_or_create(name='stage', defaults={
                'name':'stage',
            })
for permission_ in permissions_ :
    permission_object=Permission.objects.get(codename=permission_[0])
    if not permission_object in group_.permissions.all() :
        group_.permissions.add(permission_object)



# scolarite
permissions_ = (

    ("fonctionnalite_configurationetablissement_visualisation", "Visualiser la configuration de l'établissement : Institution, résidences universitaires, charges, géo, rôles et droits d'accès.."),
    #("fonctionnalite_configurationetablissement_modification", "Modifier la configuration de l'établissement : Institution, résidences universitaires, charges, géo, rôles et droits d'accès.."),
    ("fonctionnalitenav_dashboard_etudiants", "Visualiser le dashboard des étudiants : Effectifs, lieux de résidences, assiduité, etc"),
    ("fonctionnalitenav_dashboard_enseignants", "Visualiser le dashboard des enseignants : Effectifs, assiduité, répartition des charges, etc"),
    ("fonctionnalitenav_dashboard_formations", "Visualiser le dashboard des formations : Ratios des décisions de jury par année, global, etc"),


    ("fonctionnalitenav_etudiants_annuairecomplet", "Visualiser l'annuaire complet des étudiants (+toutes leurs inscriptions)"),
    ("fonctionnalitenav_etudiants_groupes", "Visualiser la liste des groupes de l'année en cours"),
    ("fonctionnalitenav_etudiants_documentsgroupes", "Générer les documents groupés concernant l'étudiant : Certificats de scolarité, relevés de notes, fiches PFE, .."),
    ("fonctionnalitenav_etudiants_preinscriptions", "Afficher et valider les préinscriptions de tous les étudiants."),
    ("fonctionnalitenav_etudiants_visualisationabsences", "Visualiser la liste des absences des étudiants"),
    ("fonctionnalitenav_etudiants_signalementabsences", "Signaler les absences des étudiants"),
    ("fonctionnalitenav_etudiants_rapportabsences", "Visualiser le rapport des absences des étudiants par formation, semestre, type d'activité pédagogique, .."),

    ("fonctionnalite_etudiants_justificationabsences", "Justifier les absences des étudiants"),
    ("fonctionnalite_etudiants_visualisationsensible", "Visualiser les informations sensibles des étudiants (tél, ..)"),
    ("fonctionnalite_etudiants_gestion", "Ajouter/Importer/Modifier/Supprimer les étudiants, inscriptions, affectations aux groupes, tutorats, et autres informations relatives aux étudiants"),
    ("fonctionnalite_etudiants_visualisationnotesprofil", "Visualiser les notes (relevés et ECTS) dans le profil des étudiants"),            
    ("fonctionnalite_etudiants_documents", "Télécharger les documents prêts des étudiants : Fiches d'inscription, relevés et certificats PDF signés, attestations.. (permission ne couvrant pas les documents volontairement non-signés -S)"),
    ("fonctionnalite_etudiants_documentsnonsignes", "Télécharger les documents non signés de l'étudiant"),
    ("fonctionnalite_etudiants_reinitialisationnotesetacquis", "Réinitialiser les notes des semestres/UE/modules des étudiants, insertion des modules acquis"),


    ("fonctionnalitenav_enseignants_annuairecomplet", "Visualiser l'annuaire complet des enseignants"),
    #("fonctionnalitenav_enseignants_visualisationabsences", "Visualiser la liste des absences des enseignants"),
    #("fonctionnalitenav_enseignants_signalementabsences", "Signaler les absences des enseignants"),
    ("fonctionnalitenav_enseignants_visualisationcharges", "Visualiser la liste des charges des enseignants"),

    ("fonctionnalite_enseignants_visualisationsensible", "Visualiser les informations sensibles des enseignants (tél, ..)"),
    #("fonctionnalite_enseignants_gestion", "Ajouter, importer et modifier les enseignants"),
    ("fonctionnalite_enseignants_documents", "Télécharger les documents prêts des enseignants"),
    #("fonctionnalite_enseignants_justificationabsences", "Justifier les absences des enseignants"),
    #("fonctionnalite_enseignants_gestioncharges", "Importer/Ajouter/Modifier des charges concernant des enseignants"),


    #("fonctionnalitenav_pedagogie_gestionprogrammes", "Gérer le catalogue des programmes et matières, configurer les diplômes, spécialités, périodes et départements"),
    ("fonctionnalitenav_pedagogie_visualisationfeedbacks", "Visualiser la liste des feedbacks des enseignements (commentaires des étudiants non inclus dans la permission)"),
    ("fonctionnalitenav_pedagogie_edt", "Visualiser les emplois du temps publics des groupes, étudiants et enseignants via l'EDT Finder"),
    ("fonctionnalitenav_pedagogie_visualisationcoordination", "Visualiser les coordination de tous les modules : coordinateurs, évaluations, formules, .."),
    ("fonctionnalitenav_pedagogie_visualisationnotes", "Visualiser les notes de tous les modules, par formation, par semestre.."),
    #("fonctionnalitenav_pedagogie_generationpvsdeliberation", "Générer les PVs de délibération, calcul des notes éliminatoires (+PVs des NE), calcul des rangs et moyennes, confirmation et envoi des décisions, passage à l'année suivante.."),
    ("fonctionnalitenav_pedagogie_visualisationpvsdeliberation", "Visualiser tous les PVs de délibération"),

    ("fonctionnalite_pedagogie_visualisationcommentairesfeedbacks", "Visualiser les commentaires de feedback des étudiants"),
    #("fonctionnalite_pedagogie_importationfeedbacks", "Importer les feedbacks des modules"),
    #("fonctionnalite_pedagogie_validationfeedbacks", "Valider/modifier les feedbacks des étudiants et leur état de validation"),
    #("fonctionnalite_pedagogie_gestioncompetences", "Gérer la base de compétences : Ajout de familles de compétences, compétences, et éléments de compétences"),
    #("fonctionnalite_pedagogie_gestioncoordination", "Gérer la coordination de tous les modules : Affecter les coordinateurs, modifier les évaluations, formules, .. "),
    #("fonctionnalite_pedagogie_modificationnotes", "Modifier/Importer les notes de tous les modules"),


    ("fonctionnalitenav_planification_visualisationformations", "Visualiser la liste des formations existantes par année universitaire, avec leurs sections et groupes"),
    #("fonctionnalitenav_planification_activites", "Gérer la planification des activités : Importation, ajout, suppression"),
    #("fonctionnalitenav_planification_chargementagenda", "Charger l'Agenda (Google, ..) avec les activités planifiées"),
    #("fonctionnalitenav_planification_reinitialisationagenda", "Réinitialiser l'Agenda (Google, ..)"),

    #("fonctionnalite_planification_gestionformations", "Gérer les formations par année universitaire : Création, modification, suppression des années universitaires, formations, sections et groupes"),
    ("fonctionnalite_planification_visualisationseances", "Visualiser les séances des activités de tous les modules"),
    #("fonctionnalite_planification_gestionseances", "Gérer les séances de tous les modules : Ajouter des séances de rattrapage, .."),


    #("fonctionnalitenav_examens_gestionsalles", "Gérer la liste des salles d'examen"),
    ("fonctionnalitenav_examens_visualisationexamens", "Visualiser la liste des examens"),
    ("fonctionnalitenav_examens_visualisationsurveillance", "Visualiser la répartition des surveillants aux examens"),
    ("fonctionnalitenav_examens_visualisationplacesetudiants", "Visualiser la répartition des étudiants dans les salles d'examen"),
    #("fonctionnalitenav_examens_exportatonlisteplaces", "Exporter la liste des places disponibles dans toutes les salles d'examen"),

    #("fonctionnalite_examens_gestionexamens", "Gérer les examens : Création, modification, affectation des surveillants, placement des étudiants, envoi des convocations.."),
    #("fonctionnalite_examens_visualisationreprographie", "Visualiser la reprographie des examens"),

    ("fonctionnalitenav_stages_visualisationstages", "Visualiser la liste des stages de fin d'études et de master"),
    ("fonctionnalitenav_stages_soumission", "Soumettre un sujet de stage (permission n'affectant pas le droit naturel des étudiants, enseignants et partenaires à soumettre un stage)"),
    #("fonctionnalitenav_stages_validation", "Contrôler le processus de validation des stages, visionner leurs états de validation, leur affecter des experts/commissions, modifier les stages, supprimer les stages.."),
    #("fonctionnalitenav_stages_experts", "Visualiser l'index des experts (expertisant les sujets de stage)"),
    ("fonctionnalitenav_stages_visualisationsoutenances", "Visualiser la liste des soutenances de stages de PFE et Master + PVs + Fiches d'évaluation .."),
    ("fonctionnalitenav_stages_visualisationpartenaires", "Visualiser la liste des organismes partenaires"),
    #("fonctionnalitenav_stages_exportationpartenaires", "Exporter la liste des organismes partenaires"),
    ("fonctionnalitenav_stages_exportationstages", "Exporter la liste des stages de fin d'étude et de master"),
    ("fonctionnalitenav_stages_visualisationsoutenancesequipes", "Visualiser la liste des soutenances de toutes les matières d'équipe (+PVs, fiches d'évaluation, liste des équipes ..)"),
    
    #("fonctionnalite_stages_gestionpartenaires", "Gérer/Importer les organismes partenaires, créer des comptes utilisateurs aux partenaires afin qu'ils puissent déposer des sujets de stage"),
    #("fonctionnalite_stages_importation", "Importer les sujets de stages et leurs affectations aux groupes"),
    #("fonctionnalite_stages_modificationsoutenances", "Modifier les soutenances de tous les PFE et Master (dates, jurys, mentions, ..)"),
    #("fonctionnalite_stages_modificationsoutenancesequipes", "Modifier les soutenances de toutes les matières d'équipe (dates, jurys, mentions, ..)"),
)

group_, created=Group.objects.get_or_create(name='scolarite', defaults={
                'name':'scolarite',
            })
for permission_ in permissions_ :
    permission_object=Permission.objects.get(codename=permission_[0])
    if not permission_object in group_.permissions.all() :
        group_.permissions.add(permission_object)     




# surveillance
permissions_ = (

    #("fonctionnalite_configurationetablissement_visualisation", "Visualiser la configuration de l'établissement : Institution, résidences universitaires, charges, géo, rôles et droits d'accès.."),
    #("fonctionnalite_configurationetablissement_modification", "Modifier la configuration de l'établissement : Institution, résidences universitaires, charges, géo, rôles et droits d'accès.."),
    ("fonctionnalitenav_dashboard_etudiants", "Visualiser le dashboard des étudiants : Effectifs, lieux de résidences, assiduité, etc"),
    ("fonctionnalitenav_dashboard_enseignants", "Visualiser le dashboard des enseignants : Effectifs, assiduité, répartition des charges, etc"),
    ("fonctionnalitenav_dashboard_formations", "Visualiser le dashboard des formations : Ratios des décisions de jury par année, global, etc"),


    ("fonctionnalitenav_etudiants_annuairecomplet", "Visualiser l'annuaire complet des étudiants (+toutes leurs inscriptions)"),
    ("fonctionnalitenav_etudiants_groupes", "Visualiser la liste des groupes de l'année en cours"),
    ("fonctionnalitenav_etudiants_documentsgroupes", "Générer les documents groupés concernant l'étudiant : Certificats de scolarité, relevés de notes, fiches PFE, .."),
    ("fonctionnalitenav_etudiants_preinscriptions", "Afficher et valider les préinscriptions de tous les étudiants."),
    ("fonctionnalitenav_etudiants_visualisationabsences", "Visualiser la liste des absences des étudiants"),
    ("fonctionnalitenav_etudiants_signalementabsences", "Signaler les absences des étudiants"),
    ("fonctionnalitenav_etudiants_rapportabsences", "Visualiser le rapport des absences des étudiants par formation, semestre, type d'activité pédagogique, .."),

    ("fonctionnalite_etudiants_justificationabsences", "Justifier les absences des étudiants"),
    ("fonctionnalite_etudiants_visualisationsensible", "Visualiser les informations sensibles des étudiants (tél, ..)"),
    ("fonctionnalite_etudiants_gestion", "Ajouter/Importer/Modifier/Supprimer les étudiants, inscriptions, affectations aux groupes, tutorats, et autres informations relatives aux étudiants"),
    #("fonctionnalite_etudiants_visualisationnotesprofil", "Visualiser les notes (relevés et ECTS) dans le profil des étudiants"),            
    ("fonctionnalite_etudiants_documents", "Télécharger les documents prêts des étudiants : Fiches d'inscription, relevés et certificats PDF signés, attestations.. (permission ne couvrant pas les documents volontairement non-signés -S)"),
    ("fonctionnalite_etudiants_documentsnonsignes", "Télécharger les documents non signés de l'étudiant"),
    #("fonctionnalite_etudiants_reinitialisationnotesetacquis", "Réinitialiser les notes des semestres/UE/modules des étudiants, insertion des modules acquis"),


    ("fonctionnalitenav_enseignants_annuairecomplet", "Visualiser l'annuaire complet des enseignants"),
    ("fonctionnalitenav_enseignants_visualisationabsences", "Visualiser la liste des absences des enseignants"),
    ("fonctionnalitenav_enseignants_signalementabsences", "Signaler les absences des enseignants"),
    ("fonctionnalitenav_enseignants_visualisationcharges", "Visualiser la liste des charges des enseignants"),

    ("fonctionnalite_enseignants_visualisationsensible", "Visualiser les informations sensibles des enseignants (tél, ..)"),
    #("fonctionnalite_enseignants_gestion", "Ajouter, importer et modifier les enseignants"),
    #("fonctionnalite_enseignants_documents", "Télécharger les documents prêts des enseignants"),
    #("fonctionnalite_enseignants_justificationabsences", "Justifier les absences des enseignants"),
    #("fonctionnalite_enseignants_gestioncharges", "Importer/Ajouter/Modifier des charges concernant des enseignants"),


    #("fonctionnalitenav_pedagogie_gestionprogrammes", "Gérer le catalogue des programmes et matières, configurer les diplômes, spécialités, périodes et départements"),
    #("fonctionnalitenav_pedagogie_visualisationfeedbacks", "Visualiser la liste des feedbacks des enseignements (commentaires des étudiants non inclus dans la permission)"),
    ("fonctionnalitenav_pedagogie_edt", "Visualiser les emplois du temps publics des groupes, étudiants et enseignants via l'EDT Finder"),
    #("fonctionnalitenav_pedagogie_visualisationcoordination", "Visualiser les coordination de tous les modules : coordinateurs, évaluations, formules, .."),
    #("fonctionnalitenav_pedagogie_visualisationnotes", "Visualiser les notes de tous les modules, par formation, par semestre.."),
    #("fonctionnalitenav_pedagogie_generationpvsdeliberation", "Générer les PVs de délibération, calcul des notes éliminatoires (+PVs des NE), calcul des rangs et moyennes, confirmation et envoi des décisions, passage à l'année suivante.."),
    #("fonctionnalitenav_pedagogie_visualisationpvsdeliberation", "Visualiser tous les PVs de délibération"),

    #("fonctionnalite_pedagogie_visualisationcommentairesfeedbacks", "Visualiser les commentaires de feedback des étudiants"),
    #("fonctionnalite_pedagogie_importationfeedbacks", "Importer les feedbacks des modules"),
    #("fonctionnalite_pedagogie_validationfeedbacks", "Valider/modifier les feedbacks des étudiants et leur état de validation"),
    #("fonctionnalite_pedagogie_gestioncompetences", "Gérer la base de compétences : Ajout de familles de compétences, compétences, et éléments de compétences"),
    #("fonctionnalite_pedagogie_gestioncoordination", "Gérer la coordination de tous les modules : Affecter les coordinateurs, modifier les évaluations, formules, .. "),
    #("fonctionnalite_pedagogie_modificationnotes", "Modifier/Importer les notes de tous les modules"),


    ("fonctionnalitenav_planification_visualisationformations", "Visualiser la liste des formations existantes par année universitaire, avec leurs sections et groupes"),
    #("fonctionnalitenav_planification_activites", "Gérer la planification des activités : Importation, ajout, suppression"),
    #("fonctionnalitenav_planification_chargementagenda", "Charger l'Agenda (Google, ..) avec les activités planifiées"),
    #("fonctionnalitenav_planification_reinitialisationagenda", "Réinitialiser l'Agenda (Google, ..)"),

    #("fonctionnalite_planification_gestionformations", "Gérer les formations par année universitaire : Création, modification, suppression des années universitaires, formations, sections et groupes"),
    ("fonctionnalite_planification_visualisationseances", "Visualiser les séances des activités de tous les modules"),
    #("fonctionnalite_planification_gestionseances", "Gérer les séances de tous les modules : Ajouter des séances de rattrapage, .."),


    #("fonctionnalitenav_examens_gestionsalles", "Gérer la liste des salles d'examen"),
    ("fonctionnalitenav_examens_visualisationexamens", "Visualiser la liste des examens"),
    ("fonctionnalitenav_examens_visualisationsurveillance", "Visualiser la répartition des surveillants aux examens"),
    ("fonctionnalitenav_examens_visualisationplacesetudiants", "Visualiser la répartition des étudiants dans les salles d'examen"),
    #("fonctionnalitenav_examens_exportatonlisteplaces", "Exporter la liste des places disponibles dans toutes les salles d'examen"),

    #("fonctionnalite_examens_gestionexamens", "Gérer les examens : Création, modification, affectation des surveillants, placement des étudiants, envoi des convocations.."),
    ("fonctionnalite_examens_visualisationreprographie", "Visualiser la reprographie des examens"),

    #("fonctionnalitenav_stages_visualisationstages", "Visualiser la liste des stages de fin d'études et de master"),
    #("fonctionnalitenav_stages_soumission", "Soumettre un sujet de stage (permission n'affectant pas le droit naturel des étudiants, enseignants et partenaires à soumettre un stage)"),
    #("fonctionnalitenav_stages_validation", "Contrôler le processus de validation des stages, visionner leurs états de validation, leur affecter des experts/commissions, modifier les stages, supprimer les stages.."),
    #("fonctionnalitenav_stages_experts", "Visualiser l'index des experts (expertisant les sujets de stage)"),
    #("fonctionnalitenav_stages_visualisationsoutenances", "Visualiser la liste des soutenances de stages de PFE et Master + PVs + Fiches d'évaluation .."),
    #("fonctionnalitenav_stages_visualisationpartenaires", "Visualiser la liste des organismes partenaires"),
    #("fonctionnalitenav_stages_exportationpartenaires", "Exporter la liste des organismes partenaires"),
    #("fonctionnalitenav_stages_exportationstages", "Exporter la liste des stages de fin d'étude et de master"),
    #("fonctionnalitenav_stages_visualisationsoutenancesequipes", "Visualiser la liste des soutenances de toutes les matières d'équipe (+PVs, fiches d'évaluation, liste des équipes ..)"),
    
    #("fonctionnalite_stages_gestionpartenaires", "Gérer/Importer les organismes partenaires, créer des comptes utilisateurs aux partenaires afin qu'ils puissent déposer des sujets de stage"),
    #("fonctionnalite_stages_importation", "Importer les sujets de stages et leurs affectations aux groupes"),
    #("fonctionnalite_stages_modificationsoutenances", "Modifier les soutenances de tous les PFE et Master (dates, jurys, mentions, ..)"),
    #("fonctionnalite_stages_modificationsoutenancesequipes", "Modifier les soutenances de toutes les matières d'équipe (dates, jurys, mentions, ..)"),
)

group_, created=Group.objects.get_or_create(name='surveillance', defaults={
                'name':'surveillance',
            })
for permission_ in permissions_ :
    permission_object=Permission.objects.get(codename=permission_[0])
    if not permission_object in group_.permissions.all() :
        group_.permissions.add(permission_object)
        


# top-management
permissions_ = (

    ("fonctionnalite_configurationetablissement_visualisation", "Visualiser la configuration de l'établissement : Institution, résidences universitaires, charges, géo, rôles et droits d'accès.."),
    #("fonctionnalite_configurationetablissement_modification", "Modifier la configuration de l'établissement : Institution, résidences universitaires, charges, géo, rôles et droits d'accès.."),
    ("fonctionnalitenav_dashboard_etudiants", "Visualiser le dashboard des étudiants : Effectifs, lieux de résidences, assiduité, etc"),
    ("fonctionnalitenav_dashboard_enseignants", "Visualiser le dashboard des enseignants : Effectifs, assiduité, répartition des charges, etc"),
    ("fonctionnalitenav_dashboard_formations", "Visualiser le dashboard des formations : Ratios des décisions de jury par année, global, etc"),


    ("fonctionnalitenav_etudiants_annuairecomplet", "Visualiser l'annuaire complet des étudiants (+toutes leurs inscriptions)"),
    #("fonctionnalitenav_etudiants_groupes", "Visualiser la liste des groupes de l'année en cours"),
    #("fonctionnalitenav_etudiants_documentsgroupes", "Générer les documents groupés concernant l'étudiant : Certificats de scolarité, relevés de notes, fiches PFE, .."),
    #("fonctionnalitenav_etudiants_preinscriptions", "Afficher et valider les préinscriptions de tous les étudiants."),
    #("fonctionnalitenav_etudiants_visualisationabsences", "Visualiser la liste des absences des étudiants"),
    #("fonctionnalitenav_etudiants_signalementabsences", "Signaler les absences des étudiants"),
    ("fonctionnalitenav_etudiants_rapportabsences", "Visualiser le rapport des absences des étudiants par formation, semestre, type d'activité pédagogique, .."),

    #("fonctionnalite_etudiants_justificationabsences", "Justifier les absences des étudiants"),
    ("fonctionnalite_etudiants_visualisationsensible", "Visualiser les informations sensibles des étudiants (tél, ..)"),
    #("fonctionnalite_etudiants_gestion", "Ajouter/Importer/Modifier/Supprimer les étudiants, inscriptions, affectations aux groupes, tutorats, et autres informations relatives aux étudiants"),
    ("fonctionnalite_etudiants_visualisationnotesprofil", "Visualiser les notes (relevés et ECTS) dans le profil des étudiants"),            
    ("fonctionnalite_etudiants_documents", "Télécharger les documents prêts des étudiants : Fiches d'inscription, relevés et certificats PDF signés, attestations.. (permission ne couvrant pas les documents volontairement non-signés -S)"),
    ("fonctionnalite_etudiants_documentsnonsignes", "Télécharger les documents non signés de l'étudiant"),
    #("fonctionnalite_etudiants_reinitialisationnotesetacquis", "Réinitialiser les notes des semestres/UE/modules des étudiants, insertion des modules acquis"),


    ("fonctionnalitenav_enseignants_annuairecomplet", "Visualiser l'annuaire complet des enseignants"),
    ("fonctionnalitenav_enseignants_visualisationabsences", "Visualiser la liste des absences des enseignants"),
    #("fonctionnalitenav_enseignants_signalementabsences", "Signaler les absences des enseignants"),
    ("fonctionnalitenav_enseignants_visualisationcharges", "Visualiser la liste des charges des enseignants"),

    ("fonctionnalite_enseignants_visualisationsensible", "Visualiser les informations sensibles des enseignants (tél, ..)"),
    #("fonctionnalite_enseignants_gestion", "Ajouter, importer et modifier les enseignants"),
    ("fonctionnalite_enseignants_documents", "Télécharger les documents prêts des enseignants"),
    #("fonctionnalite_enseignants_justificationabsences", "Justifier les absences des enseignants"),
    #("fonctionnalite_enseignants_gestioncharges", "Importer/Ajouter/Modifier des charges concernant des enseignants"),


    #("fonctionnalitenav_pedagogie_gestionprogrammes", "Gérer le catalogue des programmes et matières, configurer les diplômes, spécialités, périodes et départements"),
    ("fonctionnalitenav_pedagogie_visualisationfeedbacks", "Visualiser la liste des feedbacks des enseignements (commentaires des étudiants non inclus dans la permission)"),
    ("fonctionnalitenav_pedagogie_edt", "Visualiser les emplois du temps publics des groupes, étudiants et enseignants via l'EDT Finder"),
    ("fonctionnalitenav_pedagogie_visualisationcoordination", "Visualiser les coordination de tous les modules : coordinateurs, évaluations, formules, .."),
    #("fonctionnalitenav_pedagogie_visualisationnotes", "Visualiser les notes de tous les modules, par formation, par semestre.."),
    #("fonctionnalitenav_pedagogie_generationpvsdeliberation", "Générer les PVs de délibération, calcul des notes éliminatoires (+PVs des NE), calcul des rangs et moyennes, confirmation et envoi des décisions, passage à l'année suivante.."),
    ("fonctionnalitenav_pedagogie_visualisationpvsdeliberation", "Visualiser tous les PVs de délibération"),

    ("fonctionnalite_pedagogie_visualisationcommentairesfeedbacks", "Visualiser les commentaires de feedback des étudiants"),
    #("fonctionnalite_pedagogie_importationfeedbacks", "Importer les feedbacks des modules"),
    #("fonctionnalite_pedagogie_validationfeedbacks", "Valider/modifier les feedbacks des étudiants et leur état de validation"),
    #("fonctionnalite_pedagogie_gestioncompetences", "Gérer la base de compétences : Ajout de familles de compétences, compétences, et éléments de compétences"),
    #("fonctionnalite_pedagogie_gestioncoordination", "Gérer la coordination de tous les modules : Affecter les coordinateurs, modifier les évaluations, formules, .. "),
    #("fonctionnalite_pedagogie_modificationnotes", "Modifier/Importer les notes de tous les modules"),


    ("fonctionnalitenav_planification_visualisationformations", "Visualiser la liste des formations existantes par année universitaire, avec leurs sections et groupes"),
    #("fonctionnalitenav_planification_activites", "Gérer la planification des activités : Importation, ajout, suppression"),
    #("fonctionnalitenav_planification_chargementagenda", "Charger l'Agenda (Google, ..) avec les activités planifiées"),
    #("fonctionnalitenav_planification_reinitialisationagenda", "Réinitialiser l'Agenda (Google, ..)"),

    #("fonctionnalite_planification_gestionformations", "Gérer les formations par année universitaire : Création, modification, suppression des années universitaires, formations, sections et groupes"),
    #("fonctionnalite_planification_visualisationseances", "Visualiser les séances des activités de tous les modules"),
    #("fonctionnalite_planification_gestionseances", "Gérer les séances de tous les modules : Ajouter des séances de rattrapage, .."),


    #("fonctionnalitenav_examens_gestionsalles", "Gérer la liste des salles d'examen"),
    ("fonctionnalitenav_examens_visualisationexamens", "Visualiser la liste des examens"),
    #("fonctionnalitenav_examens_visualisationsurveillance", "Visualiser la répartition des surveillants aux examens"),
    #("fonctionnalitenav_examens_visualisationplacesetudiants", "Visualiser la répartition des étudiants dans les salles d'examen"),
    #("fonctionnalitenav_examens_exportatonlisteplaces", "Exporter la liste des places disponibles dans toutes les salles d'examen"),

    #("fonctionnalite_examens_gestionexamens", "Gérer les examens : Création, modification, affectation des surveillants, placement des étudiants, envoi des convocations.."),
    #("fonctionnalite_examens_visualisationreprographie", "Visualiser la reprographie des examens"),

    ("fonctionnalitenav_stages_visualisationstages", "Visualiser la liste des stages de fin d'études et de master"),
    ("fonctionnalitenav_stages_soumission", "Soumettre un sujet de stage (permission n'affectant pas le droit naturel des étudiants, enseignants et partenaires à soumettre un stage)"),
    #("fonctionnalitenav_stages_validation", "Contrôler le processus de validation des stages, visionner leurs états de validation, leur affecter des experts/commissions, modifier les stages, supprimer les stages.."),
    ("fonctionnalitenav_stages_experts", "Visualiser l'index des experts (expertisant les sujets de stage)"),
    #("fonctionnalitenav_stages_visualisationsoutenances", "Visualiser la liste des soutenances de stages de PFE et Master + PVs + Fiches d'évaluation .."),
    ("fonctionnalitenav_stages_visualisationpartenaires", "Visualiser la liste des organismes partenaires"),
    ("fonctionnalitenav_stages_exportationpartenaires", "Exporter la liste des organismes partenaires"),
    ("fonctionnalitenav_stages_exportationstages", "Exporter la liste des stages de fin d'étude et de master"),
    #("fonctionnalitenav_stages_visualisationsoutenancesequipes", "Visualiser la liste des soutenances de toutes les matières d'équipe (+PVs, fiches d'évaluation, liste des équipes ..)"),
    
    ("fonctionnalite_stages_gestionpartenaires", "Gérer/Importer les organismes partenaires, créer des comptes utilisateurs aux partenaires afin qu'ils puissent déposer des sujets de stage"),
    #("fonctionnalite_stages_importation", "Importer les sujets de stages et leurs affectations aux groupes"),
    #("fonctionnalite_stages_modificationsoutenances", "Modifier les soutenances de tous les PFE et Master (dates, jurys, mentions, ..)"),
    #("fonctionnalite_stages_modificationsoutenancesequipes", "Modifier les soutenances de toutes les matières d'équipe (dates, jurys, mentions, ..)"),
)

group_, created=Group.objects.get_or_create(name='top-management', defaults={
                'name':'top-management',
            })
for permission_ in permissions_ :
    permission_object=Permission.objects.get(codename=permission_[0])
    if not permission_object in group_.permissions.all() :
        group_.permissions.add(permission_object)
        
# partenaire (la permission du nouveau dépôt de stage est déjà naturelle au partenaire, inutile de la cocher sinon il aura un nouveau bouton redondant dans le menu global)
permissions_ = (

    #("fonctionnalite_configurationetablissement_visualisation", "Visualiser la configuration de l'établissement : Institution, résidences universitaires, charges, géo, rôles et droits d'accès.."),
    #("fonctionnalite_configurationetablissement_modification", "Modifier la configuration de l'établissement : Institution, résidences universitaires, charges, géo, rôles et droits d'accès.."),
    ("fonctionnalitenav_dashboard_etudiants", "Visualiser le dashboard des étudiants : Effectifs, lieux de résidences, assiduité, etc"),
    ("fonctionnalitenav_dashboard_enseignants", "Visualiser le dashboard des enseignants : Effectifs, assiduité, répartition des charges, etc"),
    #("fonctionnalitenav_dashboard_formations", "Visualiser le dashboard des formations : Ratios des décisions de jury par année, global, etc"),


    #("fonctionnalitenav_etudiants_annuairecomplet", "Visualiser l'annuaire complet des étudiants (+toutes leurs inscriptions)"),
    #("fonctionnalitenav_etudiants_groupes", "Visualiser la liste des groupes de l'année en cours"),
    #("fonctionnalitenav_etudiants_documentsgroupes", "Générer les documents groupés concernant l'étudiant : Certificats de scolarité, relevés de notes, fiches PFE, .."),
    #("fonctionnalitenav_etudiants_preinscriptions", "Afficher et valider les préinscriptions de tous les étudiants."),
    #("fonctionnalitenav_etudiants_visualisationabsences", "Visualiser la liste des absences des étudiants"),
    #("fonctionnalitenav_etudiants_signalementabsences", "Signaler les absences des étudiants"),
    #("fonctionnalitenav_etudiants_rapportabsences", "Visualiser le rapport des absences des étudiants par formation, semestre, type d'activité pédagogique, .."),

    #("fonctionnalite_etudiants_justificationabsences", "Justifier les absences des étudiants"),
    #("fonctionnalite_etudiants_visualisationsensible", "Visualiser les informations sensibles des étudiants (tél, ..)"),
    #("fonctionnalite_etudiants_gestion", "Ajouter/Importer/Modifier/Supprimer les étudiants, inscriptions, affectations aux groupes, tutorats, et autres informations relatives aux étudiants"),
    #("fonctionnalite_etudiants_visualisationnotesprofil", "Visualiser les notes (relevés et ECTS) dans le profil des étudiants"),            
    #("fonctionnalite_etudiants_documents", "Télécharger les documents prêts des étudiants : Fiches d'inscription, relevés et certificats PDF signés, attestations.. (permission ne couvrant pas les documents volontairement non-signés -S)"),
    #("fonctionnalite_etudiants_documentsnonsignes", "Télécharger les documents non signés de l'étudiant"),
    #("fonctionnalite_etudiants_reinitialisationnotesetacquis", "Réinitialiser les notes des semestres/UE/modules des étudiants, insertion des modules acquis"),


    #("fonctionnalitenav_enseignants_annuairecomplet", "Visualiser l'annuaire complet des enseignants"),
    #("fonctionnalitenav_enseignants_visualisationabsences", "Visualiser la liste des absences des enseignants"),
    #("fonctionnalitenav_enseignants_signalementabsences", "Signaler les absences des enseignants"),
    #("fonctionnalitenav_enseignants_visualisationcharges", "Visualiser la liste des charges des enseignants"),

    #("fonctionnalite_enseignants_visualisationsensible", "Visualiser les informations sensibles des enseignants (tél, ..)"),
    #("fonctionnalite_enseignants_gestion", "Ajouter, importer et modifier les enseignants"),
    #("fonctionnalite_enseignants_documents", "Télécharger les documents prêts des enseignants"),
    #("fonctionnalite_enseignants_justificationabsences", "Justifier les absences des enseignants"),
    #("fonctionnalite_enseignants_gestioncharges", "Importer/Ajouter/Modifier des charges concernant des enseignants"),


    #("fonctionnalitenav_pedagogie_gestionprogrammes", "Gérer le catalogue des programmes et matières, configurer les diplômes, spécialités, périodes et départements"),
    #("fonctionnalitenav_pedagogie_visualisationfeedbacks", "Visualiser la liste des feedbacks des enseignements (commentaires des étudiants non inclus dans la permission)"),
    #("fonctionnalitenav_pedagogie_edt", "Visualiser les emplois du temps publics des groupes, étudiants et enseignants via l'EDT Finder"),
    #("fonctionnalitenav_pedagogie_visualisationcoordination", "Visualiser les coordination de tous les modules : coordinateurs, évaluations, formules, .."),
    #("fonctionnalitenav_pedagogie_visualisationnotes", "Visualiser les notes de tous les modules, par formation, par semestre.."),
    #("fonctionnalitenav_pedagogie_generationpvsdeliberation", "Générer les PVs de délibération, calcul des notes éliminatoires (+PVs des NE), calcul des rangs et moyennes, confirmation et envoi des décisions, passage à l'année suivante.."),
    #("fonctionnalitenav_pedagogie_visualisationpvsdeliberation", "Visualiser tous les PVs de délibération"),

    #("fonctionnalite_pedagogie_visualisationcommentairesfeedbacks", "Visualiser les commentaires de feedback des étudiants"),
    #("fonctionnalite_pedagogie_importationfeedbacks", "Importer les feedbacks des modules"),
    #("fonctionnalite_pedagogie_validationfeedbacks", "Valider/modifier les feedbacks des étudiants et leur état de validation"),
    #("fonctionnalite_pedagogie_gestioncompetences", "Gérer la base de compétences : Ajout de familles de compétences, compétences, et éléments de compétences"),
    #("fonctionnalite_pedagogie_gestioncoordination", "Gérer la coordination de tous les modules : Affecter les coordinateurs, modifier les évaluations, formules, .. "),
    #("fonctionnalite_pedagogie_modificationnotes", "Modifier/Importer les notes de tous les modules"),


    #("fonctionnalitenav_planification_visualisationformations", "Visualiser la liste des formations existantes par année universitaire, avec leurs sections et groupes"),
    #("fonctionnalitenav_planification_activites", "Gérer la planification des activités : Importation, ajout, suppression"),
    #("fonctionnalitenav_planification_chargementagenda", "Charger l'Agenda (Google, ..) avec les activités planifiées"),
    #("fonctionnalitenav_planification_reinitialisationagenda", "Réinitialiser l'Agenda (Google, ..)"),

    #("fonctionnalite_planification_gestionformations", "Gérer les formations par année universitaire : Création, modification, suppression des années universitaires, formations, sections et groupes"),
    #("fonctionnalite_planification_visualisationseances", "Visualiser les séances des activités de tous les modules"),
    #("fonctionnalite_planification_gestionseances", "Gérer les séances de tous les modules : Ajouter des séances de rattrapage, .."),


    #("fonctionnalitenav_examens_gestionsalles", "Gérer la liste des salles d'examen"),
    #("fonctionnalitenav_examens_visualisationexamens", "Visualiser la liste des examens"),
    #("fonctionnalitenav_examens_visualisationsurveillance", "Visualiser la répartition des surveillants aux examens"),
    #("fonctionnalitenav_examens_visualisationplacesetudiants", "Visualiser la répartition des étudiants dans les salles d'examen"),
    #("fonctionnalitenav_examens_exportatonlisteplaces", "Exporter la liste des places disponibles dans toutes les salles d'examen"),

    #("fonctionnalite_examens_gestionexamens", "Gérer les examens : Création, modification, affectation des surveillants, placement des étudiants, envoi des convocations.."),
    #("fonctionnalite_examens_visualisationreprographie", "Visualiser la reprographie des examens"),

    ("fonctionnalitenav_stages_visualisationstages", "Visualiser la liste des stages de fin d'études et de master"),
    #("fonctionnalitenav_stages_soumission", "Soumettre un sujet de stage (permission n'affectant pas le droit naturel des étudiants, enseignants et partenaires à soumettre un stage)"),
    #("fonctionnalitenav_stages_validation", "Contrôler le processus de validation des stages, visionner leurs états de validation, leur affecter des experts/commissions, modifier les stages, supprimer les stages.."),
    #("fonctionnalitenav_stages_experts", "Visualiser l'index des experts (expertisant les sujets de stage)"),
    #("fonctionnalitenav_stages_visualisationsoutenances", "Visualiser la liste des soutenances de stages de PFE et Master + PVs + Fiches d'évaluation .."),
    ("fonctionnalitenav_stages_visualisationpartenaires", "Visualiser la liste des organismes partenaires"),
    #("fonctionnalitenav_stages_exportationpartenaires", "Exporter la liste des organismes partenaires"),
    #("fonctionnalitenav_stages_exportationstages", "Exporter la liste des stages de fin d'étude et de master"),
    #("fonctionnalitenav_stages_visualisationsoutenancesequipes", "Visualiser la liste des soutenances de toutes les matières d'équipe (+PVs, fiches d'évaluation, liste des équipes ..)"),
    
    #("fonctionnalite_stages_gestionpartenaires", "Gérer/Importer les organismes partenaires, créer des comptes utilisateurs aux partenaires afin qu'ils puissent déposer des sujets de stage"),
    #("fonctionnalite_stages_importation", "Importer les sujets de stages et leurs affectations aux groupes"),
    #("fonctionnalite_stages_modificationsoutenances", "Modifier les soutenances de tous les PFE et Master (dates, jurys, mentions, ..)"),
    #("fonctionnalite_stages_modificationsoutenancesequipes", "Modifier les soutenances de toutes les matières d'équipe (dates, jurys, mentions, ..)"),
)

group_, created=Group.objects.get_or_create(name='partenaire', defaults={
                'name':'partenaire',
            })
for permission_ in permissions_ :
    permission_object=Permission.objects.get(codename=permission_[0])
    if not permission_object in group_.permissions.all() :
        group_.permissions.add(permission_object)  


# personnel
permissions_ = (

    #("fonctionnalite_configurationetablissement_visualisation", "Visualiser la configuration de l'établissement : Institution, résidences universitaires, charges, géo, rôles et droits d'accès.."),
    #("fonctionnalite_configurationetablissement_modification", "Modifier la configuration de l'établissement : Institution, résidences universitaires, charges, géo, rôles et droits d'accès.."),
    ("fonctionnalitenav_dashboard_etudiants", "Visualiser le dashboard des étudiants : Effectifs, lieux de résidences, assiduité, etc"),
    ("fonctionnalitenav_dashboard_enseignants", "Visualiser le dashboard des enseignants : Effectifs, assiduité, répartition des charges, etc"),
    ("fonctionnalitenav_dashboard_formations", "Visualiser le dashboard des formations : Ratios des décisions de jury par année, global, etc"),


    #("fonctionnalitenav_etudiants_annuairecomplet", "Visualiser l'annuaire complet des étudiants (+toutes leurs inscriptions)"),
    #("fonctionnalitenav_etudiants_groupes", "Visualiser la liste des groupes de l'année en cours"),
    #("fonctionnalitenav_etudiants_documentsgroupes", "Générer les documents groupés concernant l'étudiant : Certificats de scolarité, relevés de notes, fiches PFE, .."),
    #("fonctionnalitenav_etudiants_preinscriptions", "Afficher et valider les préinscriptions de tous les étudiants."),
    #("fonctionnalitenav_etudiants_visualisationabsences", "Visualiser la liste des absences des étudiants"),
    #("fonctionnalitenav_etudiants_signalementabsences", "Signaler les absences des étudiants"),
    #("fonctionnalitenav_etudiants_rapportabsences", "Visualiser le rapport des absences des étudiants par formation, semestre, type d'activité pédagogique, .."),

    #("fonctionnalite_etudiants_justificationabsences", "Justifier les absences des étudiants"),
    #("fonctionnalite_etudiants_visualisationsensible", "Visualiser les informations sensibles des étudiants (tél, ..)"),
    #("fonctionnalite_etudiants_gestion", "Ajouter/Importer/Modifier/Supprimer les étudiants, inscriptions, affectations aux groupes, tutorats, et autres informations relatives aux étudiants"),
    #("fonctionnalite_etudiants_visualisationnotesprofil", "Visualiser les notes (relevés et ECTS) dans le profil des étudiants"),            
    #("fonctionnalite_etudiants_documents", "Télécharger les documents prêts des étudiants : Fiches d'inscription, relevés et certificats PDF signés, attestations.. (permission ne couvrant pas les documents volontairement non-signés -S)"),
    #("fonctionnalite_etudiants_documentsnonsignes", "Télécharger les documents non signés de l'étudiant"),
    #("fonctionnalite_etudiants_reinitialisationnotesetacquis", "Réinitialiser les notes des semestres/UE/modules des étudiants, insertion des modules acquis"),


    #("fonctionnalitenav_enseignants_annuairecomplet", "Visualiser l'annuaire complet des enseignants"),
    #("fonctionnalitenav_enseignants_visualisationabsences", "Visualiser la liste des absences des enseignants"),
    #("fonctionnalitenav_enseignants_signalementabsences", "Signaler les absences des enseignants"),
    #("fonctionnalitenav_enseignants_visualisationcharges", "Visualiser la liste des charges des enseignants"),

    #("fonctionnalite_enseignants_visualisationsensible", "Visualiser les informations sensibles des enseignants (tél, ..)"),
    #("fonctionnalite_enseignants_gestion", "Ajouter, importer et modifier les enseignants"),
    #("fonctionnalite_enseignants_documents", "Télécharger les documents prêts des enseignants"),
    #("fonctionnalite_enseignants_justificationabsences", "Justifier les absences des enseignants"),
    #("fonctionnalite_enseignants_gestioncharges", "Importer/Ajouter/Modifier des charges concernant des enseignants"),


    #("fonctionnalitenav_pedagogie_gestionprogrammes", "Gérer le catalogue des programmes et matières, configurer les diplômes, spécialités, périodes et départements"),
    #("fonctionnalitenav_pedagogie_visualisationfeedbacks", "Visualiser la liste des feedbacks des enseignements (commentaires des étudiants non inclus dans la permission)"),
    ("fonctionnalitenav_pedagogie_edt", "Visualiser les emplois du temps publics des groupes, étudiants et enseignants via l'EDT Finder"),
    #("fonctionnalitenav_pedagogie_visualisationcoordination", "Visualiser les coordination de tous les modules : coordinateurs, évaluations, formules, .."),
    #("fonctionnalitenav_pedagogie_visualisationnotes", "Visualiser les notes de tous les modules, par formation, par semestre.."),
    #("fonctionnalitenav_pedagogie_generationpvsdeliberation", "Générer les PVs de délibération, calcul des notes éliminatoires (+PVs des NE), calcul des rangs et moyennes, confirmation et envoi des décisions, passage à l'année suivante.."),
    #("fonctionnalitenav_pedagogie_visualisationpvsdeliberation", "Visualiser tous les PVs de délibération"),

    #("fonctionnalite_pedagogie_visualisationcommentairesfeedbacks", "Visualiser les commentaires de feedback des étudiants"),
    #("fonctionnalite_pedagogie_importationfeedbacks", "Importer les feedbacks des modules"),
    #("fonctionnalite_pedagogie_validationfeedbacks", "Valider/modifier les feedbacks des étudiants et leur état de validation"),
    #("fonctionnalite_pedagogie_gestioncompetences", "Gérer la base de compétences : Ajout de familles de compétences, compétences, et éléments de compétences"),
    #("fonctionnalite_pedagogie_gestioncoordination", "Gérer la coordination de tous les modules : Affecter les coordinateurs, modifier les évaluations, formules, .. "),
    #("fonctionnalite_pedagogie_modificationnotes", "Modifier/Importer les notes de tous les modules"),


    #("fonctionnalitenav_planification_visualisationformations", "Visualiser la liste des formations existantes par année universitaire, avec leurs sections et groupes"),
    #("fonctionnalitenav_planification_activites", "Gérer la planification des activités : Importation, ajout, suppression"),
    #("fonctionnalitenav_planification_chargementagenda", "Charger l'Agenda (Google, ..) avec les activités planifiées"),
    #("fonctionnalitenav_planification_reinitialisationagenda", "Réinitialiser l'Agenda (Google, ..)"),

    #("fonctionnalite_planification_gestionformations", "Gérer les formations par année universitaire : Création, modification, suppression des années universitaires, formations, sections et groupes"),
    #("fonctionnalite_planification_visualisationseances", "Visualiser les séances des activités de tous les modules"),
    #("fonctionnalite_planification_gestionseances", "Gérer les séances de tous les modules : Ajouter des séances de rattrapage, .."),


    #("fonctionnalitenav_examens_gestionsalles", "Gérer la liste des salles d'examen"),
    #("fonctionnalitenav_examens_visualisationexamens", "Visualiser la liste des examens"),
    #("fonctionnalitenav_examens_visualisationsurveillance", "Visualiser la répartition des surveillants aux examens"),
    #("fonctionnalitenav_examens_visualisationplacesetudiants", "Visualiser la répartition des étudiants dans les salles d'examen"),
    #("fonctionnalitenav_examens_exportatonlisteplaces", "Exporter la liste des places disponibles dans toutes les salles d'examen"),

    #("fonctionnalite_examens_gestionexamens", "Gérer les examens : Création, modification, affectation des surveillants, placement des étudiants, envoi des convocations.."),
    #("fonctionnalite_examens_visualisationreprographie", "Visualiser la reprographie des examens"),

    ("fonctionnalitenav_stages_visualisationstages", "Visualiser la liste des stages de fin d'études et de master"),
    ("fonctionnalitenav_stages_soumission", "Soumettre un sujet de stage (permission n'affectant pas le droit naturel des étudiants, enseignants et partenaires à soumettre un stage)"),
    #("fonctionnalitenav_stages_validation", "Contrôler le processus de validation des stages, visionner leurs états de validation, leur affecter des experts/commissions, modifier les stages, supprimer les stages.."),
    #("fonctionnalitenav_stages_experts", "Visualiser l'index des experts (expertisant les sujets de stage)"),
    #("fonctionnalitenav_stages_visualisationsoutenances", "Visualiser la liste des soutenances de stages de PFE et Master + PVs + Fiches d'évaluation .."),
    #("fonctionnalitenav_stages_visualisationpartenaires", "Visualiser la liste des organismes partenaires"),
    #("fonctionnalitenav_stages_exportationpartenaires", "Exporter la liste des organismes partenaires"),
    #("fonctionnalitenav_stages_exportationstages", "Exporter la liste des stages de fin d'étude et de master"),
    #("fonctionnalitenav_stages_visualisationsoutenancesequipes", "Visualiser la liste des soutenances de toutes les matières d'équipe (+PVs, fiches d'évaluation, liste des équipes ..)"),
    
    #("fonctionnalite_stages_gestionpartenaires", "Gérer/Importer les organismes partenaires, créer des comptes utilisateurs aux partenaires afin qu'ils puissent déposer des sujets de stage"),
    #("fonctionnalite_stages_importation", "Importer les sujets de stages et leurs affectations aux groupes"),
    #("fonctionnalite_stages_modificationsoutenances", "Modifier les soutenances de tous les PFE et Master (dates, jurys, mentions, ..)"),
    #("fonctionnalite_stages_modificationsoutenancesequipes", "Modifier les soutenances de toutes les matières d'équipe (dates, jurys, mentions, ..)"),
)

group_, created=Group.objects.get_or_create(name='personnel', defaults={
                'name':'personnel',
            })
for permission_ in permissions_ :
    permission_object=Permission.objects.get(codename=permission_[0])
    if not permission_object in group_.permissions.all() :
        group_.permissions.add(permission_object)  



# etudiant (permissions globales en plus des permissions naturelles)
permissions_ = (

    #("fonctionnalite_configurationetablissement_visualisation", "Visualiser la configuration de l'établissement : Institution, résidences universitaires, charges, géo, rôles et droits d'accès.."),
    #("fonctionnalite_configurationetablissement_modification", "Modifier la configuration de l'établissement : Institution, résidences universitaires, charges, géo, rôles et droits d'accès.."),
    ("fonctionnalitenav_dashboard_etudiants", "Visualiser le dashboard des étudiants : Effectifs, lieux de résidences, assiduité, etc"),
    ("fonctionnalitenav_dashboard_enseignants", "Visualiser le dashboard des enseignants : Effectifs, assiduité, répartition des charges, etc"),
    ("fonctionnalitenav_dashboard_formations", "Visualiser le dashboard des formations : Ratios des décisions de jury par année, global, etc"),


    #("fonctionnalitenav_etudiants_annuairecomplet", "Visualiser l'annuaire complet des étudiants (+toutes leurs inscriptions)"),
    #("fonctionnalitenav_etudiants_groupes", "Visualiser la liste des groupes de l'année en cours"),
    #("fonctionnalitenav_etudiants_documentsgroupes", "Générer les documents groupés concernant l'étudiant : Certificats de scolarité, relevés de notes, fiches PFE, .."),
    #("fonctionnalitenav_etudiants_preinscriptions", "Afficher et valider les préinscriptions de tous les étudiants."),
    #("fonctionnalitenav_etudiants_visualisationabsences", "Visualiser la liste des absences des étudiants"),
    #("fonctionnalitenav_etudiants_signalementabsences", "Signaler les absences des étudiants"),
    #("fonctionnalitenav_etudiants_rapportabsences", "Visualiser le rapport des absences des étudiants par formation, semestre, type d'activité pédagogique, .."),

    #("fonctionnalite_etudiants_justificationabsences", "Justifier les absences des étudiants"),
    #("fonctionnalite_etudiants_visualisationsensible", "Visualiser les informations sensibles des étudiants (tél, ..)"),
    #("fonctionnalite_etudiants_gestion", "Ajouter/Importer/Modifier/Supprimer les étudiants, inscriptions, affectations aux groupes, tutorats, et autres informations relatives aux étudiants"),
    #("fonctionnalite_etudiants_visualisationnotesprofil", "Visualiser les notes (relevés et ECTS) dans le profil des étudiants"),            
    #("fonctionnalite_etudiants_documents", "Télécharger les documents prêts des étudiants : Fiches d'inscription, relevés et certificats PDF signés, attestations.. (permission ne couvrant pas les documents volontairement non-signés -S)"),
    #("fonctionnalite_etudiants_documentsnonsignes", "Télécharger les documents non signés de l'étudiant"),
    #("fonctionnalite_etudiants_reinitialisationnotesetacquis", "Réinitialiser les notes des semestres/UE/modules des étudiants, insertion des modules acquis"),


    #("fonctionnalitenav_enseignants_annuairecomplet", "Visualiser l'annuaire complet des enseignants"),
    #("fonctionnalitenav_enseignants_visualisationabsences", "Visualiser la liste des absences des enseignants"),
    #("fonctionnalitenav_enseignants_signalementabsences", "Signaler les absences des enseignants"),
    #("fonctionnalitenav_enseignants_visualisationcharges", "Visualiser la liste des charges des enseignants"),

    #("fonctionnalite_enseignants_visualisationsensible", "Visualiser les informations sensibles des enseignants (tél, ..)"),
    #("fonctionnalite_enseignants_gestion", "Ajouter, importer et modifier les enseignants"),
    #("fonctionnalite_enseignants_documents", "Télécharger les documents prêts des enseignants"),
    #("fonctionnalite_enseignants_justificationabsences", "Justifier les absences des enseignants"),
    #("fonctionnalite_enseignants_gestioncharges", "Importer/Ajouter/Modifier des charges concernant des enseignants"),


    #("fonctionnalitenav_pedagogie_gestionprogrammes", "Gérer le catalogue des programmes et matières, configurer les diplômes, spécialités, périodes et départements"),
    ("fonctionnalitenav_pedagogie_visualisationfeedbacks", "Visualiser la liste des feedbacks des enseignements (commentaires des étudiants non inclus dans la permission)"),
    ("fonctionnalitenav_pedagogie_edt", "Visualiser les emplois du temps publics des groupes, étudiants et enseignants via l'EDT Finder"),
    #("fonctionnalitenav_pedagogie_visualisationcoordination", "Visualiser les coordination de tous les modules : coordinateurs, évaluations, formules, .."),
    #("fonctionnalitenav_pedagogie_visualisationnotes", "Visualiser les notes de tous les modules, par formation, par semestre.."),
    #("fonctionnalitenav_pedagogie_generationpvsdeliberation", "Générer les PVs de délibération, calcul des notes éliminatoires (+PVs des NE), calcul des rangs et moyennes, confirmation et envoi des décisions, passage à l'année suivante.."),
    #("fonctionnalitenav_pedagogie_visualisationpvsdeliberation", "Visualiser tous les PVs de délibération"),

    #("fonctionnalite_pedagogie_visualisationcommentairesfeedbacks", "Visualiser les commentaires de feedback des étudiants"),
    #("fonctionnalite_pedagogie_importationfeedbacks", "Importer les feedbacks des modules"),
    #("fonctionnalite_pedagogie_validationfeedbacks", "Valider/modifier les feedbacks des étudiants et leur état de validation"),
    #("fonctionnalite_pedagogie_gestioncompetences", "Gérer la base de compétences : Ajout de familles de compétences, compétences, et éléments de compétences"),
    #("fonctionnalite_pedagogie_gestioncoordination", "Gérer la coordination de tous les modules : Affecter les coordinateurs, modifier les évaluations, formules, .. "),
    #("fonctionnalite_pedagogie_modificationnotes", "Modifier/Importer les notes de tous les modules"),


    #("fonctionnalitenav_planification_visualisationformations", "Visualiser la liste des formations existantes par année universitaire, avec leurs sections et groupes"),
    #("fonctionnalitenav_planification_activites", "Gérer la planification des activités : Importation, ajout, suppression"),
    #("fonctionnalitenav_planification_chargementagenda", "Charger l'Agenda (Google, ..) avec les activités planifiées"),
    #("fonctionnalitenav_planification_reinitialisationagenda", "Réinitialiser l'Agenda (Google, ..)"),

    #("fonctionnalite_planification_gestionformations", "Gérer les formations par année universitaire : Création, modification, suppression des années universitaires, formations, sections et groupes"),
    #("fonctionnalite_planification_visualisationseances", "Visualiser les séances des activités de tous les modules"),
    #("fonctionnalite_planification_gestionseances", "Gérer les séances de tous les modules : Ajouter des séances de rattrapage, .."),


    #("fonctionnalitenav_examens_gestionsalles", "Gérer la liste des salles d'examen"),
    #("fonctionnalitenav_examens_visualisationexamens", "Visualiser la liste des examens"),
    #("fonctionnalitenav_examens_visualisationsurveillance", "Visualiser la répartition des surveillants aux examens"),
    #("fonctionnalitenav_examens_visualisationplacesetudiants", "Visualiser la répartition des étudiants dans les salles d'examen"),
    #("fonctionnalitenav_examens_exportatonlisteplaces", "Exporter la liste des places disponibles dans toutes les salles d'examen"),

    #("fonctionnalite_examens_gestionexamens", "Gérer les examens : Création, modification, affectation des surveillants, placement des étudiants, envoi des convocations.."),
    #("fonctionnalite_examens_visualisationreprographie", "Visualiser la reprographie des examens"),

    ("fonctionnalitenav_stages_visualisationstages", "Visualiser la liste des stages de fin d'études et de master"),
    #("fonctionnalitenav_stages_soumission", "Soumettre un sujet de stage (permission n'affectant pas le droit naturel des étudiants, enseignants et partenaires à soumettre un stage)"),
    #("fonctionnalitenav_stages_validation", "Contrôler le processus de validation des stages, visionner leurs états de validation, leur affecter des experts/commissions, modifier les stages, supprimer les stages.."),
    #("fonctionnalitenav_stages_experts", "Visualiser l'index des experts (expertisant les sujets de stage)"),
    #("fonctionnalitenav_stages_visualisationsoutenances", "Visualiser la liste des soutenances de stages de PFE et Master + PVs + Fiches d'évaluation .."),
    ("fonctionnalitenav_stages_visualisationpartenaires", "Visualiser la liste des organismes partenaires"),
    #("fonctionnalitenav_stages_exportationpartenaires", "Exporter la liste des organismes partenaires"),
    #("fonctionnalitenav_stages_exportationstages", "Exporter la liste des stages de fin d'étude et de master"),
    #("fonctionnalitenav_stages_visualisationsoutenancesequipes", "Visualiser la liste des soutenances de toutes les matières d'équipe (+PVs, fiches d'évaluation, liste des équipes ..)"),
    
    #("fonctionnalite_stages_gestionpartenaires", "Gérer/Importer les organismes partenaires, créer des comptes utilisateurs aux partenaires afin qu'ils puissent déposer des sujets de stage"),
    #("fonctionnalite_stages_importation", "Importer les sujets de stages et leurs affectations aux groupes"),
    #("fonctionnalite_stages_modificationsoutenances", "Modifier les soutenances de tous les PFE et Master (dates, jurys, mentions, ..)"),
    #("fonctionnalite_stages_modificationsoutenancesequipes", "Modifier les soutenances de toutes les matières d'équipe (dates, jurys, mentions, ..)"),
)

group_, created=Group.objects.get_or_create(name='etudiant', defaults={
                'name':'etudiant',
            })
for permission_ in permissions_ :
    permission_object=Permission.objects.get(codename=permission_[0])
    if not permission_object in group_.permissions.all() :
        group_.permissions.add(permission_object)  
        
        
        
        
# enseignant (permissions globales en plus des permissions naturelles)
permissions_ = (

    #("fonctionnalite_configurationetablissement_visualisation", "Visualiser la configuration de l'établissement : Institution, résidences universitaires, charges, géo, rôles et droits d'accès.."),
    #("fonctionnalite_configurationetablissement_modification", "Modifier la configuration de l'établissement : Institution, résidences universitaires, charges, géo, rôles et droits d'accès.."),
    ("fonctionnalitenav_dashboard_etudiants", "Visualiser le dashboard des étudiants : Effectifs, lieux de résidences, assiduité, etc"),
    ("fonctionnalitenav_dashboard_enseignants", "Visualiser le dashboard des enseignants : Effectifs, assiduité, répartition des charges, etc"),
    ("fonctionnalitenav_dashboard_formations", "Visualiser le dashboard des formations : Ratios des décisions de jury par année, global, etc"),


    ("fonctionnalitenav_etudiants_annuairecomplet", "Visualiser l'annuaire complet des étudiants (+toutes leurs inscriptions)"),
    #("fonctionnalitenav_etudiants_groupes", "Visualiser la liste des groupes de l'année en cours"),
    #("fonctionnalitenav_etudiants_documentsgroupes", "Générer les documents groupés concernant l'étudiant : Certificats de scolarité, relevés de notes, fiches PFE, .."),
    #("fonctionnalitenav_etudiants_preinscriptions", "Afficher et valider les préinscriptions de tous les étudiants."),
    #("fonctionnalitenav_etudiants_visualisationabsences", "Visualiser la liste des absences des étudiants"),
    #("fonctionnalitenav_etudiants_signalementabsences", "Signaler les absences des étudiants"),
    #("fonctionnalitenav_etudiants_rapportabsences", "Visualiser le rapport des absences des étudiants par formation, semestre, type d'activité pédagogique, .."),

    #("fonctionnalite_etudiants_justificationabsences", "Justifier les absences des étudiants"),
    #("fonctionnalite_etudiants_visualisationsensible", "Visualiser les informations sensibles des étudiants (tél, ..)"),
    #("fonctionnalite_etudiants_gestion", "Ajouter/Importer/Modifier/Supprimer les étudiants, inscriptions, affectations aux groupes, tutorats, et autres informations relatives aux étudiants"),
    ("fonctionnalite_etudiants_visualisationnotesprofil", "Visualiser les notes (relevés et ECTS) dans le profil des étudiants"),            
    #("fonctionnalite_etudiants_documents", "Télécharger les documents prêts des étudiants : Fiches d'inscription, relevés et certificats PDF signés, attestations.. (permission ne couvrant pas les documents volontairement non-signés -S)"),
    #("fonctionnalite_etudiants_documentsnonsignes", "Télécharger les documents non signés de l'étudiant"),
    #("fonctionnalite_etudiants_reinitialisationnotesetacquis", "Réinitialiser les notes des semestres/UE/modules des étudiants, insertion des modules acquis"),


    #("fonctionnalitenav_enseignants_annuairecomplet", "Visualiser l'annuaire complet des enseignants"),
    #("fonctionnalitenav_enseignants_visualisationabsences", "Visualiser la liste des absences des enseignants"),
    #("fonctionnalitenav_enseignants_signalementabsences", "Signaler les absences des enseignants"),
    #("fonctionnalitenav_enseignants_visualisationcharges", "Visualiser la liste des charges des enseignants"),

    #("fonctionnalite_enseignants_visualisationsensible", "Visualiser les informations sensibles des enseignants (tél, ..)"),
    #("fonctionnalite_enseignants_gestion", "Ajouter, importer et modifier les enseignants"),
    #("fonctionnalite_enseignants_documents", "Télécharger les documents prêts des enseignants"),
    #("fonctionnalite_enseignants_justificationabsences", "Justifier les absences des enseignants"),
    #("fonctionnalite_enseignants_gestioncharges", "Importer/Ajouter/Modifier des charges concernant des enseignants"),


    #("fonctionnalitenav_pedagogie_gestionprogrammes", "Gérer le catalogue des programmes et matières, configurer les diplômes, spécialités, périodes et départements"),
    ("fonctionnalitenav_pedagogie_visualisationfeedbacks", "Visualiser la liste des feedbacks des enseignements (commentaires des étudiants non inclus dans la permission)"),
    ("fonctionnalitenav_pedagogie_edt", "Visualiser les emplois du temps publics des groupes, étudiants et enseignants via l'EDT Finder"),
    #("fonctionnalitenav_pedagogie_visualisationcoordination", "Visualiser les coordination de tous les modules : coordinateurs, évaluations, formules, .."),
    #("fonctionnalitenav_pedagogie_visualisationnotes", "Visualiser les notes de tous les modules, par formation, par semestre.."),
    #("fonctionnalitenav_pedagogie_generationpvsdeliberation", "Générer les PVs de délibération, calcul des notes éliminatoires (+PVs des NE), calcul des rangs et moyennes, confirmation et envoi des décisions, passage à l'année suivante.."),
    ("fonctionnalitenav_pedagogie_visualisationpvsdeliberation", "Visualiser tous les PVs de délibération"),

    ("fonctionnalite_pedagogie_visualisationcommentairesfeedbacks", "Visualiser les commentaires de feedback des étudiants"),
    #("fonctionnalite_pedagogie_importationfeedbacks", "Importer les feedbacks des modules"),
    #("fonctionnalite_pedagogie_validationfeedbacks", "Valider/modifier les feedbacks des étudiants et leur état de validation"),
    #("fonctionnalite_pedagogie_gestioncompetences", "Gérer la base de compétences : Ajout de familles de compétences, compétences, et éléments de compétences"),
    #("fonctionnalite_pedagogie_gestioncoordination", "Gérer la coordination de tous les modules : Affecter les coordinateurs, modifier les évaluations, formules, .. "),
    #("fonctionnalite_pedagogie_modificationnotes", "Modifier/Importer les notes de tous les modules"),


    #("fonctionnalitenav_planification_visualisationformations", "Visualiser la liste des formations existantes par année universitaire, avec leurs sections et groupes"),
    #("fonctionnalitenav_planification_activites", "Gérer la planification des activités : Importation, ajout, suppression"),
    #("fonctionnalitenav_planification_chargementagenda", "Charger l'Agenda (Google, ..) avec les activités planifiées"),
    #("fonctionnalitenav_planification_reinitialisationagenda", "Réinitialiser l'Agenda (Google, ..)"),

    #("fonctionnalite_planification_gestionformations", "Gérer les formations par année universitaire : Création, modification, suppression des années universitaires, formations, sections et groupes"),
    #("fonctionnalite_planification_visualisationseances", "Visualiser les séances des activités de tous les modules"),
    #("fonctionnalite_planification_gestionseances", "Gérer les séances de tous les modules : Ajouter des séances de rattrapage, .."),


    #("fonctionnalitenav_examens_gestionsalles", "Gérer la liste des salles d'examen"),
    #("fonctionnalitenav_examens_visualisationexamens", "Visualiser la liste des examens"),
    #("fonctionnalitenav_examens_visualisationsurveillance", "Visualiser la répartition des surveillants aux examens"),
    #("fonctionnalitenav_examens_visualisationplacesetudiants", "Visualiser la répartition des étudiants dans les salles d'examen"),
    #("fonctionnalitenav_examens_exportatonlisteplaces", "Exporter la liste des places disponibles dans toutes les salles d'examen"),

    #("fonctionnalite_examens_gestionexamens", "Gérer les examens : Création, modification, affectation des surveillants, placement des étudiants, envoi des convocations.."),
    #("fonctionnalite_examens_visualisationreprographie", "Visualiser la reprographie des examens"),

    ("fonctionnalitenav_stages_visualisationstages", "Visualiser la liste des stages de fin d'études et de master"),
    #("fonctionnalitenav_stages_soumission", "Soumettre un sujet de stage (permission n'affectant pas le droit naturel des étudiants, enseignants et partenaires à soumettre un stage)"),
    #("fonctionnalitenav_stages_validation", "Contrôler le processus de validation des stages, visionner leurs états de validation, leur affecter des experts/commissions, modifier les stages, supprimer les stages.."),
    #("fonctionnalitenav_stages_experts", "Visualiser l'index des experts (expertisant les sujets de stage)"),
    #("fonctionnalitenav_stages_visualisationsoutenances", "Visualiser la liste des soutenances de stages de PFE et Master + PVs + Fiches d'évaluation .."),
    ("fonctionnalitenav_stages_visualisationpartenaires", "Visualiser la liste des organismes partenaires"),
    #("fonctionnalitenav_stages_exportationpartenaires", "Exporter la liste des organismes partenaires"),
    #("fonctionnalitenav_stages_exportationstages", "Exporter la liste des stages de fin d'étude et de master"),
    #("fonctionnalitenav_stages_visualisationsoutenancesequipes", "Visualiser la liste des soutenances de toutes les matières d'équipe (+PVs, fiches d'évaluation, liste des équipes ..)"),
    
    #("fonctionnalite_stages_gestionpartenaires", "Gérer/Importer les organismes partenaires, créer des comptes utilisateurs aux partenaires afin qu'ils puissent déposer des sujets de stage"),
    #("fonctionnalite_stages_importation", "Importer les sujets de stages et leurs affectations aux groupes"),
    #("fonctionnalite_stages_modificationsoutenances", "Modifier les soutenances de tous les PFE et Master (dates, jurys, mentions, ..)"),
    #("fonctionnalite_stages_modificationsoutenancesequipes", "Modifier les soutenances de toutes les matières d'équipe (dates, jurys, mentions, ..)"),
)

group_, created=Group.objects.get_or_create(name='enseignant', defaults={
                'name':'enseignant',
            })
for permission_ in permissions_ :
    permission_object=Permission.objects.get(codename=permission_[0])
    if not permission_object in group_.permissions.all() :
        group_.permissions.add(permission_object)