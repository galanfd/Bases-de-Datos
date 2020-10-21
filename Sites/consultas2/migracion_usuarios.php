<?php include('../templates/header.html');   ?>

<body>

  <?php
  require("../config/conexion.php");
  # Obtenemos todos los capitanes en la BD
  $query_capitanes = "SELECT * FROM personal WHERE personal.cargo = 'capitan';";
  $result_capitanes = $db -> prepare($query_capitanes);
  $result_capitanes -> execute();
  $todo_capitanes = $result_capitanes -> fetchAll();
  # Obtenemos todos los jefes en la BD
  $query_jefes = "SELECT * FROM personal WHERE personal.cargo = 'Jefe';";
  $result_jefes = $db_59 -> prepare($query_jefes);
  $result_jefes -> execute();
  $todo_jefes = $result_jefes -> fetchAll();

  # Chequeamos cual es el id actual mas alto
  $query_uid = "SELECT MAX (uid) FROM Usuarios_test;";
  $result_uid = $db_59 -> prepare($query_uid);
  $result_jefes -> execute();
  $array_uid = $result_uid -> fetchAll();
  
  if (! empty($array_uid)){
    $max_uid = $array_uid[0][0];
  } else {
    $max_uid = 0;
  }
  foreach ($todo_capitanes as $p) {
    $pasaporte = $p[0];
    $query_pasaporte = "SELECT pasaporte FROM Usuarios_test WHERE pasaporte = '$pasaporte';";
    $result_pasaporte = $db_59 -> prepare($query_pasaporte);
    $result_pasaporte -> execute();
    $hay_pasaporte = $result_pasaporte -> fetchAll();
    if (empty($hay_pasaporte)){
      $max_uid++;
      $uid = $max_uid;
      $nombre = $p[1];
      $edad = $p[3];
      $sexo = $p[4];
      $pasaporte = $p[0];
      $nacionalidad = $p[2];

      $query_insertar = "INSERT INTO Usuarios_test VALUES($uid, '$nombre', $edad, '$sexo', '$pasaporte', 'pass1234', true);";
      $result_insertar = $db_59 -> prepare($query_uid);
      $result_insertar -> execute();
    }
  }


  ?>

  <table>
    <tr>
      <th>Pasaporte</th>
      <th>Nombre</th>
      <th>Nacionalidad</th>
      <th>Edad</th>
      <th>Genero</th>
    </tr>
  <?php
  foreach ($todo_capitanes as $p) {
    echo "<tr> <td>$p[0]</td> <td>$p[1]</td> <td>$p[2]</td> <td>$p[3]</td> <td>$p[4]</td> </tr>";
  }
  foreach ($todo_jefes as $p) {
    echo "<tr> <td>$p[0]</td> <td>$p[1]</td> <td>CHILE</td> <td>$p[2]</td> <td>$p[3]</td> </tr>";
  }
  ?>
  </table>

<?php include('../templates/footer.html'); ?>