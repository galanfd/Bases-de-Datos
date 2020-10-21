<?php include('../templates/header.html');   ?>

<body>

  <?php
  require("../config/conexion.php");

  $query_capitanes = "SELECT * FROM personal WHERE personal.cargo = 'capitan';";
  $result_capitanes = $db -> prepare($query_capitanes);
  $result_capitanes -> execute();
  $todo_capitanes = $result_capitanes -> fetchAll();

  $query_jefes = "SELECT * FROM personal WHERE personal.cargo = 'Jefe';";
  $result_jefes = $db_59 -> prepare($query_jefes);
  $result_jefes -> execute();
  $todo_jefes = $result_jefes -> fetchAll();
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
    echo "<tr> <td>$p[0]</td> <td>$p[1]</td> <td>'Chile'</td> <td>$p[2]</td> <td>$p[3]</td> </tr>";
  }
  ?>
  </table>

<?php include('../templates/footer.html'); ?>