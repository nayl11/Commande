import cohere
import os
from dotenv import load_dotenv

# Charger la clé API depuis le fichier .env
load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")

if not cohere_api_key:
    print("❌ La clé API Cohere n'a pas été trouvée. Vérifiez le fichier .env.")
else:
    print("✅ Clé API trouvée, test de connexion en cours...")

    # Initialiser le client Cohere
    co = cohere.Client(cohere_api_key)

    # Tester avec une simple génération de texte
    try:
        response = co.generate(
            model='command-xlarge-nightly',  # Tu peux utiliser 'command-xlarge' si tu veux
            prompt="Bonjour, comment ça va ?",
            max_tokens=20
        )
        print("✅ Connexion réussie ! Réponse de Cohere :")
        print(response.generations[0].text.strip())
    except Exception as e:
        print("❌ Erreur lors de la connexion à l'API Cohere :")
        print(e)
