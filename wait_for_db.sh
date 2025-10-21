#!/bin/sh
echo "⏳ Waiting for MySQL at $DB_HOST:$DB_PORT..."

while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done

echo "✅ MySQL is ready!"
echo "⚙️ Applying migrations..."
python manage.py migrate --noinput

echo "🚀 Starting Daphne..."
python -m daphne -b 0.0.0.0 -p 8000 backend.asgi:application

# nc -z = netcat, utilisé pour vérifier si un port est ouvert.

# "$DB_HOST" et "$DB_PORT" = adresse du service MySQL (ex : mysql:3306 dans Docker).

# ! nc -z ... signifie "tant que MySQL n’est pas disponible..."

# sleep 1 = attend 1 seconde avant de réessayer.

# 🔁 Donc cette boucle attend que MySQL soit prêt avant de passer à la suite.
# Sans ça, Django planterait s’il tente de se connecter avant que MySQL ne soit initialisé.