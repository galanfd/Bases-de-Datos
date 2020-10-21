<?php
  try {
    require('data.php'); 
    $db = new PDO("pgsql:dbname=$databaseName;host=localhost;port=5432;user=$user;password=$password");
    $db_59 = new PDO("pgsql:dbname=$databaseName_2;host=localhost;port=5432;user=$user_2;password=$password_2");
  } catch (Exception $e) {
    echo "No se pudo conectar a la base de datos: $e";
  }
?>
