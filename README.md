# Robot Artiste 🎨🤖

Ce script transforme votre ordinateur en artiste ! Il prend une image, détecte ses contours et prend le contrôle de votre souris pour la dessiner automatiquement dans votre logiciel de dessin préféré (Affinity Designer, Paint, Photoshop, etc.).

## 📋 Prérequis

Vous devez avoir Python installé sur votre machine.

### Installation des bibliothèques

Ouvrez un terminal (PowerShell ou CMD) et lancez la commande suivante pour installer les "yeux" (OpenCV) et la "main" (PyAutoGUI) du robot :

```bash
pip install opencv-python pyautogui numpy
```

## 🚀 Comment l'utiliser

### 1. Préparation de l'image

- Placez l'image que vous voulez dessiner (JPG ou PNG) dans un dossier accessible.
- **Conseil** : Le script dessine 1 pixel image pour 1 pixel écran. Si votre image est en 4K (3840x2160), le dessin sera énorme ! Redimensionnez votre image source vers une taille raisonnable (ex: 800x600 ou 1000px de large) avant de lancer le script.

### 2. Configuration du script

Ouvrez le fichier `robot_artist.py` avec un éditeur de texte (Notepad, VS Code, etc.) et modifiez les lignes suivantes au début du fichier :

```python
# Chemin de votre image
IMAGE_PATH = r"C:\Chemin\Vers\Votre\Image.jpg"

# Réglages (optionnel)
CANNY_MIN = 50   # Diminuez pour plus de détails
CANNY_MAX = 150  # Augmentez pour moins de détails
DRAW_SPEED = 0.002 # Vitesse du dessin
```

### 3. Lancement

1. Ouvrez votre logiciel de dessin (ex: Affinity Designer).
2. Créez une page blanche.
3. Sélectionnez l'outil **Pinceau** ou **Crayon**.
4. Choisissez une couleur (ex: Noir) et une épaisseur de trait fine.
5. Lancez le script depuis votre terminal :

```bash
python robot_artist.py
```

### 4. Action

- Le script va charger l'image.
- Il vous dira : **"Placez votre souris où vous voulez commencer le dessin"**.
- Placez votre curseur sur la zone de dessin dans Affinity (généralement le coin haut-gauche de la zone où vous voulez que le dessin apparaisse).
- **Ne touchez plus à rien !** Vous avez 5 secondes.
- Le robot va commencer à dessiner.

## ⚠️ Sécurité (Arrêt d'urgence)

Si le robot devient fou ou si vous voulez arrêter le dessin en cours :
**Jetez brusquement votre souris dans un des 4 coins de l'écran.**
Cela déclenchera la sécurité `FAILSAFE` et arrêtera le script immédiatement.
