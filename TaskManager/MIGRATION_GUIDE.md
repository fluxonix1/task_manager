# Migration Guide for UserProfile

To enable the full profile functionality with profile pictures and bio, you need to run database migrations.

## Steps to Run Migrations

1. Open a terminal/command prompt
2. Navigate to your project directory (where `manage.py` is located)
3. Run the following commands:

```bash
# Create migrations for the new UserProfile model
python manage.py makemigrations tasks

# Apply the migrations to create the database table
python manage.py migrate
```

## What This Will Enable

After running the migrations, you'll have access to:

1. Profile picture uploads
2. Bio text on your profile
3. Complete profile customization

## Troubleshooting

If you encounter any issues:

1. Make sure you're in the correct directory (where `manage.py` is located)
2. Check for any error messages during migration
3. If needed, you can reset migrations with:
   ```bash
   python manage.py migrate tasks zero
   python manage.py makemigrations tasks
   python manage.py migrate tasks
   ```

## Note

Until migrations are run, the application will operate in a limited mode where:
- Profile pictures cannot be uploaded
- Bio information cannot be saved
- Only basic user information (name, email) can be updated