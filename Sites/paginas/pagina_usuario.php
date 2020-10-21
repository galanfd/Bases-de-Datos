<?php include('../templates/header.html');   ?>

<body>

  <?php
  require("../config/conexion.php"); #Llama a conexión, crea el objeto PDO y obtiene la variable $db
  session_start();
  $uid = $_SESSION["user_id"];
  $query = "SELECT usuarios.nombre, usuarios.edad, usuarios.sexo, usuarios.pasaporte, usuarios.nacionalidad FROM usuarios WHERE usuarios.uid = $uid;";
  $result = $db_59 -> prepare($query);
  $result -> execute();
  $dataCollected = $result -> fetchAll(); #Obtiene todos los resultados de la consulta en forma de un arreglo
  ?>

  <table>
    <tr>
      <th>Nombre</th>
      <th>Edad</th>
      <th>Sexo</th>
      <th>Pasaporte</th>
      <th>Nacionalidad</th>
    </tr>
  <?php
  foreach ($dataCollected as $p) {
    echo "<tr> <td>$p[0]</td> <td>$p[1]</td> <td>$p[2]</td> <td>$p[3]</td> <td>$p[4]</td> </tr>";
  }
  ?>
  </table>

<?php include('../templates/footer.html'); ?>