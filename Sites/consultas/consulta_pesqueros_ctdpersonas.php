<?php include('../templates/header.html');   ?>

<body>

  <?php
  require("../config/conexion.php"); #Llama a conexión, crea el objeto PDO y obtiene la variable $db

  $query = "SELECT DISTINCT pesqueros.psid, buques.patente, nombre, pais, pesqueros.tipo FROM (SELECT patente, COUNT(*) AS ctd_personal FROM buques INNER JOIN pesqueros USING (patente) INNER JOIN tripula
   USING (patente) INNER JOIN personal USING (pasaporte) GROUP BY patente HAVING COUNT(*) = (SELECT MAX (ctd_personal) FROM (SELECT patente, COUNT(*) AS ctd_personal 
   FROM buques INNER JOIN pesqueros USING (patente) INNER JOIN tripula USING (patente) INNER JOIN personal USING (pasaporte) GROUP BY patente) AS FOO)) 
   AS FUU INNER JOIN buques USING (patente) INNER JOIN pesqueros USING (patente);";
  $result = $db -> prepare($query);
  $result -> execute();
  $dataCollected = $result -> fetchAll(); #Obtiene todos los resultados de la consulta en forma de un arreglo
  ?>

  <table>
    <tr>
      <th>Id Pesquero</th>
      <th>Patente</th>
      <th>Nombre</th>
      <th>Pais</th>
      <th>Tipo</th>
    </tr>
  <?php
  foreach ($dataCollected as $p) {
    echo "<tr> <td>$p[0]</td> <td>$p[1]</td> <td>$p[2]</td> <td>$p[3]</td> <td>$p[4]</td></tr>";
  }
  ?>
  </table>

<?php include('../templates/footer.html'); ?>