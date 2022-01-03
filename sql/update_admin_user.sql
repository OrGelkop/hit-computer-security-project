/*
First of all register with admin user:
Display name - Admin
email - admin@admin.admin
and choose your password.

Then, run the update command
*/

UPDATE USERS
SET is_admin=1
WHERE email='admin@admin.admin';