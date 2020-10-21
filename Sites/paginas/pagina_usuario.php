<?php include('../templates/header.html');   ?>

<body>

  <?php
  require("../config/conexion.php"); #Llama a conexión, crea el objeto PDO y obtiene la variable $db

  $puerto = $_POST["nombre_puerto"];
  $fecha = $_POST["fecha"];
  $query = "SELECT DISTINCT buques.nombre, buques.patente, buques.pais, buques.tipo FROM atraques INNER JOIN historial USING (id_atraque) INNER JOIN buques USING (patente) WHERE 
  LOWER(atraques.puerto) LIKE LOWER('%$puerto%') AND atraques.fecha_llegada between '$fecha-01-01 00:00:00' and '$fecha-12-31 00:00:00';";
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
    echo "<tr> <td>$p[0]</td> <td>$p[1]</td> <td>$p[2]</td> <td>$p[3]</td> </tr>";
  }
  ?>
  </table>

<?php include('../templates/footer.html'); ?>