# ATELIER PRA/PCA

## Séquence 5 : Exercices

### Exercice 1 :
Quels sont les composants dont la perte entraîne une perte de données ?
* Le PVC `pra-data` **ET** le PVC `pra-backup` simultanément.
* Le nœud (Node) K3d physique sous-jacent qui héberge le stockage local de ces deux volumes.

### Exercice 2 :
Expliquez nous pourquoi nous n'avons pas perdu les données lors de la supression du PVC pra-data
* Les données n'ont pas été perdues car elles étaient sauvegardées chaque minute par un CronJob sur un second volume indépendant (`pra-backup`). Lors de la phase de restauration, le Job `50-job-restore.yaml` a copié la dernière version de la base de données depuis `pra-backup` vers le nouveau `pra-data`.

### Exercice 3 :
Quels sont les RTO et RPO de cette solution ?
* **RPO (Recovery Point Objective) :** 1 minute (fréquence du CronJob de sauvegarde).
* **RTO (Recovery Time Objective) :** Le temps de l'intervention humaine pour exécuter la procédure de restauration (estimé entre 5 et 10 minutes).

### Exercice 4 :
Pourquoi cette solution (cet atelier) ne peux pas être utilisé dans un vrai environnement de production ? Que manque-t-il ?
* SQLite ne gère pas les accès concurrents distribués (Haute Disponibilité).
* Les sauvegardes sont locales (Single Point of Failure) : si le serveur crash, le backup est perdu.
* La restauration est manuelle et dépend d'une action humaine.

### Exercice 5 :
Proposez une archtecture plus robuste.
* Remplacer SQLite par un cluster PostgreSQL managé (ex: CloudNativePG) avec réplication synchrone.
* Stocker les backups à l'extérieur du cluster sur un stockage objet immuable (ex: AWS S3) dans une autre région géographique.
* Mettre en place un mécanisme de Failover automatique sur un second cluster Kubernetes de secours (Multi-région).

## Séquence 6 : Ateliers

### Atelier 2 : Choisir notre point de restauration

1. Lister les sauvegardes disponibles dans le volume de backup :
\`\`\`bash
kubectl -n pra exec -it deployment/flask -- ls -la /backup
\`\`\`

2. Modifier temporairement le fichier `pra/50-job-restore.yaml` pour modifier la commande de copie avec le fichier choisi (ex: `backup_xyz.db`) :
\`\`\`yaml
args: ["cp /backup/backup_xyz.db /data/production.db"]
\`\`\`

3. Exécuter la restauration :
\`\`\`bash
kubectl -n pra scale deployment flask --replicas=0
kubectl apply -f pra/50-job-restore.yaml
kubectl -n pra scale deployment flask --replicas=1
\`\`\`
