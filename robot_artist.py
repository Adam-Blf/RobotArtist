import cv2
import numpy as np
import pyautogui
import time
import sys
import os
import winsound

# ==================================================================================
# CONFIGURATION
# ==================================================================================
# Chemin de l'image à dessiner. 
# REMPLACEZ CECI par le chemin de votre image (ex: "C:\\Users\\Moi\\Images\\mon_dessin.jpg")
IMAGE_PATH = r"C:\Users\adamb\Downloads\Gemini_Generated_Image_kg465ikg465ikg46.png" 

# Sensibilité de la détection des bords (Algorithme de Canny)
# Si le dessin a trop de traits, augmentez ces valeurs (ex: 100, 200)
# Si le dessin manque de détails, diminuez ces valeurs (ex: 30, 100)
CANNY_MIN = 50
CANNY_MAX = 150

# Vitesse de dessin
# Pause entre chaque mouvement de souris (en secondes). 
# 0.001 est très rapide. 0.005 est plus sûr pour que le logiciel suive.
DRAW_SPEED = 0.002 

# Filtrage du bruit
# Les contours plus petits que cette aire (en pixels) seront ignorés.
MIN_CONTOUR_AREA = 10  # On réduit aussi le seuil pour garder les petits détails

# Facteur de simplification
# Plus la valeur est élevée, plus le trait est "lissé" et moins il y a de points.
# 0.001 est très précis, 0.005 est plus anguleux mais plus rapide.
APPROX_EPSILON_FACTOR = 0.0005  # Plus petit = plus de points, donc plus de détails

# ==================================================================================
# SÉCURITÉ
# ==================================================================================
# Arrêt d'urgence : Déplacez la souris brusquement vers un coin de l'écran pour stopper le script.
pyautogui.FAILSAFE = True

def process_image(image_path):
    """
    Charge l'image, détecte les contours et les retourne sous forme de liste de points.
    """
    if not os.path.exists(image_path):
        print(f"ERREUR: L'image n'a pas été trouvée à l'emplacement : {image_path}")
        print("Veuillez vérifier le chemin dans la variable IMAGE_PATH.")
        return None

    # 1. Chargement de l'image
    print(f"Chargement de l'image : {image_path}")
    img = cv2.imread(image_path)
    if img is None:
        print("ERREUR: Impossible de lire le fichier image.")
        return None

    # 2. Conversion en niveaux de gris
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. Flou léger pour réduire le bruit
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 4. Détection des bords (Canny)
    edges = cv2.Canny(blurred, CANNY_MIN, CANNY_MAX)

    # 5. Trouver les contours
    # RETR_EXTERNAL : contours extérieurs seulement (ou RETR_TREE pour tout)
    # CHAIN_APPROX_SIMPLE : compresse les segments horizontaux/verticaux/diagonaux
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    print(f"Contours trouvés (brut) : {len(contours)}")
    return contours

def is_in_draw_zone(x, y, top_left, bottom_right):
    """
    Vérifie si un point (x, y) est dans la zone de dessin définie par les coins
    supérieur gauche (top_left) et inférieur droit (bottom_right).
    """
    return (top_left.x <= x <= bottom_right.x) and (top_left.y <= y <= bottom_right.y)

def get_contour_color(img, contour):
    """
    Détecte la couleur moyenne (en hexadécimal) d'un contour donné dans l'image.
    """
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.drawContours(mask, [contour], -1, 255, -1)
    mean = cv2.mean(img, mask=mask)
    r, g, b = int(mean[2]), int(mean[1]), int(mean[0])
    return '#{:02X}{:02X}{:02X}'.format(r, g, b)

def get_color_hex_zone():
    print("Clique d'abord sur le bouton pour ouvrir la palette, puis appuie sur Entrée...")
    input()
    print("Maintenant clique sur la zone où tu entres le code couleur (champ hex), puis appuie sur Entrée...")
    input()
    hex_pos = pyautogui.position()
    print(f"Position du champ hex mémorisée : {hex_pos}")
    print("Enfin, clique sur le bouton 'fermer' de la palette, puis appuie sur Entrée...")
    input()
    close_pos = pyautogui.position()
    print(f"Position du bouton fermer mémorisée : {close_pos}")
    return hex_pos, close_pos

def draw_contours(contours, top_left, bottom_right, fill_mode='fit', margin_ratio=0.05, hex_pos=None, close_pos=None):
    img = cv2.imread(IMAGE_PATH)
    screen_width, screen_height = pyautogui.size()
    print(f"Taille de l'écran : {screen_width}x{screen_height}")
    
    print("\n--- PRÉPARATION ---")
    print("Placez votre souris à l'endroit où vous voulez commencer le dessin (Coin Haut-Gauche du dessin).")
    print("Vous avez 5 secondes pour changer de fenêtre (Alt-Tab) vers Affinity Designer/Paint...")
    
    for i in range(5, 0, -1):
        print(f"{i}...")
        winsound.Beep(1000, 200) # Bip aigu court
        time.sleep(0.8)
    
    winsound.Beep(1500, 500) # Bip de départ long
    
    print("DÉBUT DU DESSIN !")
    
    # Position de départ (référence)
    start_x, start_y = pyautogui.position()
    
    all_points = []
    for c in contours:
        for p in c:
            all_points.append(p[0])
            
    if not all_points:
        print("Aucun point à dessiner.")
        return

    all_points_np = np.array(all_points)
    min_x = np.min(all_points_np[:, 0])
    min_y = np.min(all_points_np[:, 1])
    max_x = np.max(all_points_np[:, 0])
    max_y = np.max(all_points_np[:, 1])

    # Dimensions du dessin original
    drawing_width = max_x - min_x
    drawing_height = max_y - min_y

    # Dimensions de la zone cible
    zone_width = bottom_right.x - top_left.x
    zone_height = bottom_right.y - top_left.y

    # Ajout d'une marge automatique
    margin_x = int(zone_width * margin_ratio)
    margin_y = int(zone_height * margin_ratio)
    zone_width_eff = zone_width - 2 * margin_x
    zone_height_eff = zone_height - 2 * margin_y

    # Mode d'adaptation : 'fit' (garde le ratio) ou 'stretch' (remplit toute la zone)
    if fill_mode == 'stretch':
        scale_x = zone_width_eff / drawing_width
        scale_y = zone_height_eff / drawing_height
    else:  # 'fit' par défaut
        scale = min(zone_width_eff / drawing_width, zone_height_eff / drawing_height)
        scale_x = scale_y = scale

    # Décalage pour centrer le dessin dans la zone
    offset_x = top_left.x + margin_x + (zone_width_eff - drawing_width * scale_x) // 2
    offset_y = top_left.y + margin_y + (zone_height_eff - drawing_height * scale_y) // 2

    for i, contour in enumerate(contours):
        # Filtrer le bruit (petits contours)
        if cv2.contourArea(contour) < MIN_CONTOUR_AREA:
            continue

        color_hex = get_contour_color(img, contour)
        # Mémoriser la position actuelle de la souris
        last_pos = pyautogui.position()
        # Automatisation du changement de couleur
        pyautogui.moveTo(1585, 291)
        pyautogui.doubleClick()
        time.sleep(1)
        if hex_pos:
            pyautogui.moveTo(hex_pos.x, hex_pos.y)
            pyautogui.doubleClick()
            time.sleep(0.1)
            pyautogui.typewrite(color_hex.lstrip('#'))
            pyautogui.press('enter')
        if close_pos:
            pyautogui.moveTo(close_pos.x, close_pos.y)
            pyautogui.click()  # Simple clic pour fermer
            time.sleep(0.1)
        pyautogui.moveTo(last_pos.x, last_pos.y)

        # --- Tracé du contour (bordure) ---
        epsilon = APPROX_EPSILON_FACTOR * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) < 2:
            continue
        first_point = approx[0][0]
        target_x = int(offset_x + (first_point[0] - min_x) * scale_x)
        target_y = int(offset_y + (first_point[1] - min_y) * scale_y)
        pyautogui.mouseUp()
        pyautogui.moveTo(target_x, target_y)
        pyautogui.mouseDown()
        for point in approx[1:]:
            pt = point[0]
            next_x = int(offset_x + (pt[0] - min_x) * scale_x)
            next_y = int(offset_y + (pt[1] - min_y) * scale_y)
            pyautogui.moveTo(next_x, next_y, duration=DRAW_SPEED)
        # Fermer la forme en revenant au point de départ
        pyautogui.moveTo(target_x, target_y, duration=DRAW_SPEED)
        pyautogui.mouseUp()
        # (Pas de remplissage automatique)
        
    print("\n--- DESSIN TERMINÉ ---")

def get_draw_zone():
    print("Cliquez dans le coin HAUT GAUCHE de la zone de dessin puis appuyez sur Entrée...")
    input()
    top_left = pyautogui.position()
    print(f"Position haut gauche enregistrée : {top_left}")
    print("Cliquez dans le coin BAS DROIT de la zone de dessin puis appuyez sur Entrée...")
    input()
    bottom_right = pyautogui.position()
    print(f"Position bas droit enregistrée : {bottom_right}")
    return top_left, bottom_right

def detect_canvas_zone():
    print("Détection automatique de la zone de dessin...")
    screenshot = pyautogui.screenshot()
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Seuillage pour trouver les zones très claires (blanc)
    _, thresh = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)
    # Trouver les contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Prendre le plus grand contour (aire max)
    max_area = 0
    best_rect = None
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        if area > max_area:
            max_area = area
            best_rect = (x, y, w, h)
    if best_rect:
        x, y, w, h = best_rect
        print(f"Zone détectée : haut-gauche=({x},{y}), bas-droit=({x+w},{y+h})")
        top_left = type('Point', (object,), {'x': x, 'y': y})()
        bottom_right = type('Point', (object,), {'x': x+w, 'y': y+h})()
        return top_left, bottom_right
    else:
        print("Aucune zone blanche détectée. Repasse en mode manuel.")
        return None, None

def detect_canvas_zone_with_alt_tab():
    print("Passage automatique à la fenêtre de dessin (Alt+Tab)...")
    pyautogui.hotkey('alt', 'tab')
    time.sleep(1)
    return detect_canvas_zone()

if __name__ == "__main__":
    auto = input("Détecter automatiquement la zone de dessin ? (o/n) : ").strip().lower()
    if auto == 'o':
        zone_haut_gauche, zone_bas_droit = detect_canvas_zone_with_alt_tab()
        if not zone_haut_gauche:
            zone_haut_gauche, zone_bas_droit = get_draw_zone()
    else:
        zone_haut_gauche, zone_bas_droit = get_draw_zone()
    # Demande la position du champ hex et du bouton fermer au premier lancement
    hex_pos, close_pos = get_color_hex_zone()
    contours = process_image(IMAGE_PATH)
    if contours:
        draw_contours(contours, zone_haut_gauche, zone_bas_droit, fill_mode='fit', margin_ratio=0.05, hex_pos=hex_pos, close_pos=close_pos)
    else:
        print("Rien à dessiner. Vérifiez l'image et les seuils.")
