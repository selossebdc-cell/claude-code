# Correctif Brevo — Templates emails FSY
**Date** : 9 avril 2026  
**Contexte** : Aurélia a RDV avec Catherine à 14h00 — elle venait de booker après avoir passé du temps à corriger les emails dans Brevo

---

## Problème identifié

Les 22 templates d'emails créés le 6 avril 2026 (séquences Nurture, Onboarding, Rétention) avaient été uploadés via l'API Brevo sous forme de HTML brut. Conséquence : dans l'interface Brevo, Aurélia voyait du **code HTML illisible** (balises `</td>`, `</tr>`, entités `&eacute;`, etc.) au lieu de texte éditable — c'est ce que Catherine appelait les "slashes".

**C'est une erreur de conception** : le HTML envoyé via API n'est pas décomposable en blocs visuels dans l'éditeur Brevo. Aurélia ne pouvait pas modifier le texte directement.

---

## Ce qu'Aurélia a fait (workaround)

Elle a réécrit le contenu de **18 templates** en collant son texte corrigé **après la balise `</html>`** dans l'éditeur code de Brevo. Modifications faites le 8 avril 2026 entre 19h22 et 20h15.

Templates concernés (IDs 184 à 201) :

| Séquence | Templates |
|----------|-----------|
| Nurture Sommeil | 184, 185, 186, 187 |
| Nurture Face Yoga | 188, 189, 190, 191 |
| Nurture Générale | 192, 193, 194, 195 |
| Onboarding FSY | 196, 197, 198 |
| Rétention Bilans | 199, 200, 201 |

Les 4 templates de rétention (202, 203, 204, 205 — Inactivité 14j, Pré-annulation, Post-annulation J1, Reconquête M1) étaient déjà propres et n'ont pas été touchés.

---

## Correctif appliqué (9 avril 2026)

1. **Extraction** du texte d'Aurélia pour chacun des 18 templates via l'API Brevo
2. **Nettoyages spécifiques** :
   - Template 191 (`Nurture-FaceYoga-4-Offre`) : suppression du méta-commentaire Claude collé à la fin ("Ce qui a changé :…") — pas du contenu email
   - Template 198 (`Onboarding-FSY-3-Feedback`) : correction typo `{ contact.PRENOM }}` → `{{ contact.PRENOM }}`
3. **Reconstruction HTML** : chaque template rebuilté avec la structure minimaliste (fond beige `#f7f5f2`, container blanc 600px, logo FSY, texte, footer désabonnement)
4. **PUT API Brevo** : les 18 templates mis à jour — 18/18 succès (HTTP 204)

---

## Textes corrigés par Aurélia — référence complète

### 184 — Nurture-Sommeil-1-Bienvenue
**Objet** : Ton sommeil mérite mieux que ça.

{{ contact.PRENOM }},  
Tu as répondu au quiz. Et ce que tu m'as partagé sur tes nuits, je le reconnais.  
Ce cerveau qui continue de tourner longtemps après que tu as fermé les yeux. Ce réveil où tu tâtonnes pour savoir si tu as vraiment dormi. Cette fatigue installée, sourde, qui ne part pas vraiment.  
Le corps a une mémoire de tout ça.  
La mâchoire qui se serre pendant le sommeil, les muscles du crâne qui restent en tension, le visage qui porte le matin ce que la nuit n'a pas pu dissoudre. Ce n'est pas un détail esthétique. C'est une information.  
Ce que j'ai appris, après des années à travailler avec le fascia et le système nerveux : le visage est souvent le premier endroit où une femme voit sa fatigue. Et le dernier où elle pense à intervenir.  
Dans les prochains jours, je vais te partager trois pratiques que j'utilise avec mes clientes pour préparer le corps au repos, en passant par le visage. Concrètes. Rapides. Efficaces à condition de les faire vraiment.  
Le premier exercice arrive très vite.  
With love,  
Aurélia

---

### 185 — Nurture-Sommeil-2-Temoignage
**Objet** : Elle dormait 4h par nuit. Aujourd'hui, elle dort.

Sandra dormait quatre, parfois cinq heures par nuit. Bruxisme. Migraines au réveil. Un état d'alerte permanent que son corps avait fini par considérer comme normal.  
Elle a commencé une pratique de dix minutes, le soir, allongée. Trois semaines plus tard, elle m'a écrit quelque chose que je n'oublie pas :  
"Je ne savais pas que mon visage tenait autant de stress. En le relâchant, c'est comme si j'avais donné la permission à tout mon corps de lâcher."  
Ce qu'elle a décrit, c'est ce que le système nerveux parasympathique fait quand on lui en donne enfin l'occasion. Le fascia du visage relâché envoie un signal au nerf vague. Le nerf vague ralentit tout le reste. Le corps comprend qu'il peut descendre.  
Dix minutes. Allongée. Le soir.  
Demain, je te montre exactement quoi faire.  
With love,  
Aurélia

---

### 186 — Nurture-Sommeil-3-Video
**Objet** : 3 exercices pour mieux dormir (vidéo)

{{ contact.PRENOM }},  
Ce soir, avant de te coucher, voilà ce que je te propose de faire. Allongée, les yeux fermés, dix minutes.  
Relâchement de la mâchoire.  
Pose tes doigts sur tes tempes. Ouvre doucement la bouche, expire. Sens le poids de ta mâchoire qui descend comme si elle lâchait quelque chose qu'elle portait depuis ce matin. Cinq respirations.  
Lissage du front.  
Du centre vers les tempes, glisse tes doigts lentement. L'intention compte autant que le geste : effacer la journée, pas juste masser la peau. Dix passages.  
Pression du nerf vague.  
Derrière l'oreille, dans ce petit creux. Appuie doucement, respire. Tu sentiras peut-être ton rythme ralentir. C'est exactement ce que tu cherches.  
Ces trois gestes ensemble activent la réponse parasympathique. Le corps comprend qu'il peut descendre.  
Si tu veux aller plus loin, j'ai créé Sommeil et Joie : un programme complet avec des vidéos guidées, un suivi, une communauté. Pour celles qui veulent transformer vraiment leur rapport au sommeil, en passant par le corps.  
→ Découvrir Sommeil et Joie — 397€  
Et pour explorer à ton rythme, le FSY Studio à 17€/mois contient aussi des routines sommeil.  
Bonne nuit, {{ contact.PRENOM }}.  
With love,  
Aurélia

---

### 187 — Nurture-Sommeil-4-Offre
**Objet** : Et si tu dormais vraiment bien, dès cette semaine ?

{{ contact.PRENOM }},  
Ces derniers jours, tu as eu un premier aperçu de ce que le visage peut faire pour le sommeil.  
Ce que je veux te dire maintenant : les exercices que je t'ai partagés fonctionnent. Mais isolés, ils ne suffisent pas. Le système nerveux ne se reprogramme pas en une soirée. Il a besoin de régularité, d'une progression, d'un contexte qui lui apprend que le soir est un signal de descente et non de vigilance.  
C'est ce que j'ai construit avec Sommeil et Joie.  
Dix-huit vidéos guidées, progressives. Des routines du soir de dix minutes. Un travail sur la mâchoire, le souffle, les fascias. Huit semaines d'accompagnement.  
Chaque session prépare le terrain pour la suivante. Ce n'est pas un catalogue de techniques. C'est un reconditionnement du corps, semaine après semaine.  
→ Rejoindre Sommeil et Joie — 397€  
Si le programme complet ne correspond pas à ce dont tu as besoin maintenant, le FSY Studio à 17€/mois donne accès à des routines sommeil en continu.  
With love,  
Aurélia

---

### 188 — Nurture-FaceYoga-1-Bienvenue
**Objet** : Ton visage te parle. Tu l'écoutes ?

{{ contact.PRENOM }},  
Tu viens de faire quelque chose que beaucoup de femmes remettent à plus tard.  
Tu t'es dit : mon visage mérite mon attention. Vraiment.  
Ce n'est pas une décision anodine. Le visage est l'endroit où on stocke tout ce qu'on ne dit pas, tout ce qu'on retient, tout ce qu'on porte depuis des années. La mâchoire serrée du dimanche soir. Le front qui se plisse quand on réfléchit trop. Les yeux qui s'éteignent quand on est épuisée sans savoir pourquoi.  
Face Soul Yoga, c'est apprendre à lire ces signaux. Et à y répondre, avec les mains, le souffle, le mouvement.  
Dans les prochains jours, je vais te partager des clés concrètes : comment ça fonctionne, pourquoi ça marche, et un exercice à tester dès ce soir.  
Pour commencer, j'ai mis de côté une vidéo que je réserve à celles qui débutent ce chemin.  
→ Voir la vidéo  
With love,  
Aurélia

---

### 189 — Nurture-FaceYoga-2-AvantApres
**Objet** : Ce que 30 jours peuvent changer sur un visage.

{{ contact.PRENOM }},  
Ce que je vois chez les femmes qui pratiquent depuis trente jours, c'est rarement spectaculaire à décrire. C'est silencieux. C'est dans les détails.  
L'ovale qui se redessine. Le regard qui s'ouvre. La mâchoire qui descend enfin. Le teint qui change parce que la circulation reprend ses droits. Et quelque chose de plus difficile à nommer : elles se regardent différemment.  
Nathalie m'a écrit après un mois de pratique :  
"Je me suis regardée dans le miroir ce matin et j'ai souri. Pas pour vérifier mes rides. Juste… parce que j'avais envie. Ça faisait des années."  
Ce que Nathalie décrit, ce n'est pas un résultat esthétique. C'est un changement de relation à son propre visage. Et c'est ça, le vrai travail.  
Demain, je t'explique ce que la plupart des approches du face yoga ne font pas, et pourquoi ça change tout.  
With love,  
Aurélia

---

### 190 — Nurture-FaceYoga-3-10min
**Objet** : 10 minutes par jour. C'est tout ce qu'il faut.

Le face yoga ne demande pas une heure devant le miroir. Il demande dix minutes. Le matin, le soir, allongée, assise, dans ta salle de bain ou dans ton lit.  
Dix minutes pour réveiller les 57 muscles du visage, relancer la circulation, relâcher les tensions que tu accumules sans t'en rendre compte. Et te reconnecter à quelque chose de concret : ton corps, ta respiration, ta présence.  
Ce qui change tout, ce n'est jamais l'intensité. C'est la régularité.  
Trente jours de pratique quotidienne, et ton visage commence à te raconter une autre histoire. C'est documenté. C'est physiologique. Et c'est accessible à n'importe quelle femme qui décide de s'y tenir.  
Le FSY Studio, c'est ça : des vidéos courtes, guidées, progressives. Depuis chez toi, à ton rythme, pour 17€ par mois.  
→ Découvrir le FSY Studio  
With love,  
Aurélia

---

### 191 — Nurture-FaceYoga-4-Offre
**Objet** : Prête à habiter ton visage ?

{{ contact.PRENOM }},  
Ces derniers jours, je t'ai parlé du visage, du sommeil, du système nerveux. De ce qui se passe quand on commence à vraiment écouter son corps plutôt que de le corriger.  
Tu sais maintenant ce que Face Soul Yoga fait, et pourquoi ça fonctionne.  
Il reste une question : est-ce que c'est pour toi maintenant ?  
Le FSY Studio, c'est des programmes complets, des routines de cinq à quinze minutes guidées en vidéo, des exercices ciblés, une communauté de femmes qui pratiquent, et du contenu nouveau chaque semaine. Dix-sept euros par mois. Ou cent trente-neuf euros à l'année, soit deux mois offerts.  
Ce n'est pas une décision urgente. Mais si quelque chose dans ces emails a résonné, ton corps te le dit déjà.  
→ Rejoindre le FSY Studio  
PS : Si tu as une question avant de te lancer, réponds à cet email. Je lis vraiment tout.  
With love,  
Aurélia

*(Note : le méta-commentaire Claude collé après "Aurélia" dans la version Brevo a été supprimé — ce n'était pas du contenu email)*

---

### 192 — Nurture-Generale-1-Bienvenue
**Objet** : Bienvenue dans l'univers Face Soul Yoga

{{ contact.PRENOM }},  
Tu viens de rejoindre quelque chose qui va au-delà d'une liste email.  
Je m'appelle Aurélia. Ça fait sept ans que j'accompagne des femmes à travailler leur visage autrement, en passant par le fascia, le système nerveux, la posture, la respiration. Ce que j'ai créé avec Face Soul Yoga, c'est une approche globale : visible à l'extérieur, construite de l'intérieur.  
Le visage porte tout. Le stress de la semaine, les nuits courtes, les émotions qu'on ravale, les tensions qu'on ne sent plus tellement elles sont devenues normales. La mâchoire serrée. Le front qui ne se lisse plus vraiment. Le regard qui se ferme sans qu'on sache pourquoi.  
Face Soul Yoga, c'est apprendre à lire ces signaux. Et à y répondre, avec les mains, le souffle, le mouvement.  
Inhabit your face. Inhabit your life.  
Dans les prochains jours, je vais te partager des clés concrètes pour comprendre ce que ton visage te dit, et ce que tu peux en faire. Un exercice à tester. Des résultats réels. Et une invitation à aller plus loin si tu le sens.  
En attendant, tout ce que je partage au quotidien est sur Instagram.  
With love,  
Aurélia

---

### 193 — Nurture-Generale-2-Decouverte
**Objet** : Ce que ton visage essaie de te dire

Ton visage a 57 muscles.  
La plupart s'endorment. D'autres se crispent et restent là, dans cet état de tension permanente qu'on finit par ne plus sentir. Le résultat, c'est un visage qui ne reflète plus vraiment ce que tu es.  
Le face yoga, c'est réveiller ce qui s'est figé. Remettre de la circulation, du mouvement, de la vie dans des zones que tu as appris à ignorer.  
Trois endroits où ça change tout, et qu'on n'explique jamais vraiment :  
La mâchoire d'abord. C'est là que tu stockes le stress, les mots qu'on ravale, le contrôle qu'on exerce sur soi. La relâcher physiquement, c'est souvent la première chose que mes clientes sentent, et la plus surprenante.  
Le regard ensuite. Les muscles autour des yeux s'épuisent avec les écrans, la concentration, la vigilance constante. Les réactiver ouvre le regard d'une façon que les gens autour de toi remarquent avant toi.  
La posture enfin. Le visage ne s'arrête pas au menton. Il est connecté au cou, aux épaules, au dos. Travailler le visage sans travailler la posture, c'est travailler à moitié.  
Dans quelques jours, je t'envoie un quiz court pour identifier ce qui te parle le plus. Je pourrai t'envoyer du contenu vraiment adapté à ce que tu vis.  
With love,  
Aurélia

---

### 194 — Nurture-Generale-3-Quiz
**Objet** : Sommeil, mâchoire ou éclat — qu'est-ce qui te parle ?

Chaque femme arrive ici pour une raison différente. Je veux te partager du contenu qui te ressemble vraiment.  
Dis-moi ce qui résonne le plus chez toi en ce moment :  
😴 Mon sommeil  
💆 Ma mâchoire et mes tensions  
✨ Mon éclat et mon visage  
Un seul clic. Je m'occupe du reste.  
With love,  
Aurélia

---

### 195 — Nurture-Generale-4-Offre
**Objet** : J'ai quelque chose pour toi.

Tu es dans l'univers Face Soul Yoga depuis quelques jours. Tu as reçu des clés, des explications, peut-être testé quelque chose le soir avant de dormir.  
Si quelque chose a résonné, voici la prochaine étape.  
Le FSY Studio, c'est l'accès à tous les programmes vidéo, des routines de cinq à quinze minutes, du contenu nouveau chaque semaine, et la communauté des pratiquantes. Dix-sept euros par mois, annulable à tout moment.  
Ce n'est pas un abonnement de plus dans ta vie. C'est dix minutes par jour qui t'appartiennent vraiment.  
C'est un investissement qui va te donner de l'espace.  
→ Rejoindre le FSY Studio  
PS : Si tu as une question avant de te lancer, réponds à cet email. Je lis personnellement chaque message.  
With love,  
Aurélia

---

### 196 — Onboarding-FSY-1-Bienvenue
**Objet** : Bienvenue dans le Studio. Voici par où commencer.

{{ contact.PRENOM }},  
Tu fais partie du FSY Studio. Je suis tellement heureuse de t'accueillir dans cette communauté de femmes qui ont décidé de prendre soin d'elles, autrement.  
Trois choses à faire maintenant, dans l'ordre :  
1. Connecte-toi à Circle  
C'est ta plateforme. Tes vidéos, ta communauté, tout est là.  
→ Accéder au Studio  
2. Lance le Programme Découverte  
C'est le point de départ. Dix minutes, guidée, sans prérequis. Tu le trouveras directement dans l'espace "Programme Découverte" sur Circle.  
3. Rejoins le groupe WhatsApp  
C'est là que les membres partagent leurs avancées, posent leurs questions, se tiennent compagnie dans la pratique.  
→ Rejoindre le groupe  
Dix minutes par jour. C'est tout ce qu'il faut pour commencer à sentir quelque chose.  
Si tu as une question, réponds à cet email ou écris dans le groupe.  
With love,  
Aurélia

*(Note : typo "heureusede" dans la version Brevo — conservée telle quelle pour être fidèle à ce qu'Aurélia a écrit. À corriger si elle le souhaite.)*

---

### 197 — Onboarding-FSY-2-PremiersPas
**Objet** : Comment se passe ta première pratique ?

{{ contact.PRENOM }},  
Ça fait trois jours que tu as rejoint le Studio.  
Si tu n'as pas encore lancé ta première vidéo, voilà ce que je te propose pour ce soir : dix minutes avant de dormir, allongée, Programme Découverte, vidéo 1. Juste ça. Le reste vient après.  
Si tu as déjà commencé, tu as peut-être senti cette chaleur dans le visage après quelques minutes. La mâchoire qui descend. Ce moment suspendu où le corps comprend qu'il peut lâcher quelque chose. C'est petit en apparence. Ce n'est pas anodin.  
Une chose pratique : sur Circle, le contenu est organisé par durée. Moins de cinq minutes quand la journée a été trop longue. Entre cinq et quinze minutes pour le quotidien. Les programmes complets quand tu veux aller plus loin.  
Tu choisis selon ce que tu as. Pas selon ce que tu aurais dû faire.  
With love,  
Aurélia

---

### 198 — Onboarding-FSY-3-Feedback
**Objet** : 1 semaine. Comment tu te sens ?

{{ contact.PRENOM }},  
Ça fait une semaine.  
C'est souvent là que les choses commencent à se préciser. Soit tu as trouvé un rythme et tu sens quelque chose bouger. Soit la semaine est passée trop vite et tu n'as pas encore vraiment commencé.  
Les deux sont réels. Les deux arrivent.  
Ce que j'observe chez les femmes qui pratiquent depuis sept jours : elles ne parlent pas encore de résultats visibles. Elles parlent d'autre chose. Un moment du soir qui leur appartient. Une mâchoire moins serrée au réveil. Une façon différente de se regarder dans le miroir, sans chercher à corriger.  
C'est discret. C'est là.  
Si tu n'as pas encore trouvé ton rythme, la deuxième semaine est souvent celle où ça s'installe vraiment. Le corps a besoin d'un peu de temps pour comprendre que c'est régulier, que ce n'est pas une exception.  
Tu as une question, un doute, quelque chose qui coince ? Réponds à cet email.  
PS : Le groupe WhatsApp est là aussi si tu veux voir comment les autres avancent. → Rejoindre la communauté  
With love,  
Aurélia

*(Note : typo `{ contact.PRENOM }}` dans la version Brevo — corrigée en `{{ contact.PRENOM }}` lors du correctif)*

---

### 199 — Retention-Bilan-J30
**Objet** : 1 mois. Regarde le chemin parcouru.

{{ contact.PRENOM }},  
Un mois.  
Prends une seconde et regarde-toi dans le miroir, vraiment. La mâchoire. Le regard. L'ovale. La façon dont ton visage repose quand tu ne fais rien.  
Ce que les membres remarquent après trente jours n'est pas toujours spectaculaire à décrire. Le visage plus détendu au réveil. La mâchoire qui serre moins. Un teint différent, plus lumineux, que les gens autour d'elles voient avant elles. Et surtout : le rituel qui est devenu un besoin, plus une case à cocher.  
Tu es là depuis un mois. C'est concret.  
Pour ce deuxième mois, essaie un programme que tu n'as pas encore exploré. V-Shape, Bas du Visage, quelque chose de nouveau pour surprendre des zones que tu n'as pas encore vraiment travaillées.  
Et si tu veux partager où tu en es, une photo, un ressenti, un mot, le groupe WhatsApp est l'endroit pour ça.  
With love,  
Aurélia

---

### 200 — Retention-Bilan-J60
**Objet** : 2 mois. Tu n'es plus la même.

Soixante jours.  
À ce stade, ce n'est plus une question de motivation. La pratique s'est installée autrement, dans le corps, dans la semaine, dans la façon dont tu te regardes. Les gestes sont devenus plus précis, plus fluides. Tu sens des muscles que tu ne percevais pas au début. Ton visage a gagné en tonicité, en présence. Et le rituel n'est plus une case à cocher : c'est devenu ton moment.  
Ce qui change vraiment à soixante jours, c'est le regard. Pas juste le résultat visible. La façon dont tu te regardes. Sans chercher à corriger. Avec quelque chose qui ressemble à de la curiosité, peut-être même de la fierté.  
Tu es devenue quelqu'un qui pratique. Ce n'est plus un effort. C'est qui tu es maintenant.  
Pour ce troisième mois, c'est le moment d'affiner et d'explorer ce que tu n'as pas encore touché. Les exercices individuels pour cibler une zone précise que tu veux travailler. Les routines de quinze minutes si tu t'es cantonnée aux cinq minutes jusqu'ici. Et si tu ne l'as pas encore fait : partage un avant/après dans la communauté. Tu vas voir quelque chose que tu n'avais pas remarqué seule.  
C'est souvent là, entre le deuxième et le troisième mois, que les femmes comprennent que ce qu'elles ont construit ne leur sera plus jamais retiré.  
With love,  
Aurélia

---

### 201 — Retention-Bilan-J90
**Objet** : 3 mois. Ce que tu as construit ne se perd pas.

{{ contact.PRENOM }},  
Trois mois.  
Ce que tu as construit ici ne disparaît pas. La conscience musculaire, le réflexe de relâcher la mâchoire avant de dormir, la façon dont tu te regardes maintenant dans le miroir. Même si tu sautes un jour, même si la semaine a été trop chargée. C'est ancré.  
C'est ça, trois mois de pratique régulière : une relation différente avec ton visage. Durable.  
Si quelqu'un dans ton entourage traverse ce que tu traversais il y a trois mois, une fatigue visible, une mâchoire serrée, l'impression que son visage ne lui ressemble plus, tu peux simplement transférer cet email. Ou partager ton expérience sur Instagram en me taguant. Les mots d'une vraie pratiquante valent plus que n'importe quel contenu que je pourrais créer.  
Une dernière chose : des programmes premium arrivent prochainement sous la marque Aurélia Del Sol. Des accompagnements plus profonds, plus personnalisés, pour celles qui veulent aller encore plus loin dans ce travail. Tu seras la première informée.  
With love,  
Aurélia

---

## À noter pour la prochaine fois

- **Ne pas créer de templates Brevo via API** si Aurélia doit les éditer ensuite — utiliser le builder Brevo (drag-and-drop) directement
- Si contenu via API inévitable : fournir uniquement le texte brut à Aurélia et lui laisser créer les templates dans l'interface
- Les templates 202–205 (Rétention) ont été créés proprement et sont éditables dans Brevo sans problème

---

## Templates non touchés (déjà corrects)

| ID | Nom |
|----|-----|
| 202 | Retention-Inactivite-14j |
| 203 | Retention-PreAnnulation |
| 204 | Retention-PostAnnulation-J1 |
| 205 | Retention-Reconquete-M1 |
