<?php include('../templates/header.html');   ?>

<body>

  <?php
  require("../config/conexion.php"); #Llama a conexión, crea el objeto PDO y obtiene la variable $db

  $puerto = $_POST["nombre_puerto"];
  $query = "SELECT DISTINCT personal.pasaporte, personal.nombre, personal.nacionalidad, personal.edad FROM atraques INNER JOIN historial ON atraques.id_atraque = historial.id_atraque
  INNER JOIN buques ON buques.patente = historial.patente INNER JOIN tripula ON tripula.patente = buques.patente INNER JOIN personal ON personal.pasaporte = tripula.pasaporte WHERE 
  LOWER(atraques.puerto) LIKE LOWER('%$puerto%') AND personal.genero = 'mujer' AND personal.cargo = 'capitan';";
  $result = $db -> prepare($query);
  $result -> execute();
  $dataCollected = $result -> fetchAll(); #Obtiene todos los resultados de la consulta en forma de un arreglo
  ?>

  <table>
    <tr>
      <th>Pasaporte</th>
      <th>Nombre</th>
      <th>Nacionalidad</th>
      <th>Edad</th>
    </tr>
  <?php
  foreach ($dataCollected as $p) {
    echo "<tr> <td>$p[0]</td> <td>$p[1]</td> <td>$p[2]</td> <td>$p[3]</td> </tr>";
  }
  ?>
  </table>

<?php include('../templates/footer.html'); ?>