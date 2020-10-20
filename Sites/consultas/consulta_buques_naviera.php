<?php include('../templates/header.html');   ?>

<body>

  <?php
  require("../config/conexion.php"); #Llama a conexión, crea el objeto PDO y obtiene la variable $db

  $nombre = $_POST["nombre_naviera"];
  $query = "SELECT DISTINCT buques.nombre, buques.patente, buques.pais, buques.tipo FROM navieras INNER JOIN navbuq ON navieras.id_naviera = navbuq.id_naviera INNER JOIN buques 
  ON navbuq.patente = buques.patente WHERE LOWER(navieras.nombre) LIKE LOWER('%$nombre%');";
  $result = $db -> prepare($query);
  $result -> execute();
  $dataCollected = $result -> fetchAll(); #Obtiene todos los resultados de la consulta en forma de un arreglo
  ?>

  <table>
    <tr>
      <th>Nombre</th>
      <th>Patente</th>
      <th>Pais</th>
      <th>Tipo</th>
    </tr>
  <?php
  foreach ($dataCollected as $p) {
    echo "<tr> <td>$p[0]</td> <td>$p[1]</td> <td>$p[2]</td> <td>$p[3]</td></tr>";
  }
  ?>
  </table>

<?php include('../templates/footer.html'); ?>