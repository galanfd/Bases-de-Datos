<?php include('../templates/header.html');   ?>

<body>

  <?php
  require("../config/conexion.php"); 
  # Nombre de usuario y la constraseña del request
  $usuario = $_POST["nombre_usuario"];
  $contrasena = $_POST["contrasena"];

  # Tenemos que verificar que haya una tupla con la combinacion de rut y contraseña
  $query = "SELECT * FROM usuarios WHERE usuarios.pasaporte = '$usuario' AND usuarios.contrasena = '$contrasena';";
  $result = $db_59 -> prepare($query);
  $result -> execute();
  $dataCollected = $result -> fetchAll(); #Obtiene todos los resultados de la consulta en forma de un arreglo
  if (! empty($dataCollected)){
    session_start();
    $_SESSION["user_id"] = $dataCollected[0][0];
    echo "<p> Usuario valido: $found_id </p>";
    echo '
    <form method="post" action="pagina_usuario.php">
    <input type="submit" value="Aceptar">
    </form>
    ';
  } else {
    echo "<p> Usuario invalido </p>";
  }
  ?>
  <table>
    <tr>
      <th>ID</th>
      <th>Nombre</th>
      <th>Edad</th>
      <th>Sexo</th>
      <th>pasaporte</th>
      <th>nacionalidad</th>
      <th>constrasena</th>
      <th>Es bacan</th>
    </tr>
  <?php
  foreach ($dataCollected as $p) {
    echo "<tr> <td>$p[0]</td> <td>$p[1]</td> <td>$p[2]</td> <td>$p[3]</td> <td>$p[4]</td> <td>$p[5]</td> <td>$p[6]</td> <td>$p[7]</td> </tr>";
  }
  ?>
  </table>

<?php include('../templates/footer.html'); ?>