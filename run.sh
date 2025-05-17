for folder in book-service user-service loan-service stat-service
do
  #touch "$folder"/app/__init__.py "$folder"/app/api/__init__.py "$folder"/app/core/__init__.py "$folder"/app/db/__init__.py "$folder"/app/models/__init__.py "$folder"/app/services/__init__.py
  # touch "$folder"/.env
#   cat <<EOF > "$folder"/.env
# MONGODB_URI=mongodb://localhost:27017/
# DB_NAME=test
# EOF
  # touch "$folder"/.gitignore
  # echo ".env" > "$folder"/.gitignore
done