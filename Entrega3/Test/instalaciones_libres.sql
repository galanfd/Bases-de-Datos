CREATE OR REPLACE FUNCTION
retornar_instalacione_libres(fecha1 timestamp, fecha2 timestamp, seleccion_puerto integer)
RETURNS TABLE (instalacion varchar(50), fecha date, disponibles integer, porcentaje real) AS $$
DECLARE
contador integer := 0;
query1 text;
query2 text;
query_instalacion text;
info1 record;
info2 record;
info_instalacion record;
espacio int;
porcentaje float;
id_instal int;
BEGIN
    DROP TABLE resultado;
    CREATE TEMP TABLE resultado(id_instal INT, fecha timestamp, espacio int, disponible real);

    query1 := 'SELECT *  FROM Permisos_Pedidos, Instalaciones, Puerto_Instalacion, Puertos, Permisos, Permiso_muelle WHERE Permisos_Pedidos.id_instalacion = Instalaciones.id_instalacion AND Instalaciones.id_instalacion = Puerto_Instalacion.id_instalacion AND Puerto_Instalacion.id_puerto = Puertos.id_puerto AND Permisos_Pedidos.id_permiso = Permisos.id_permiso AND Permiso_muelle.id_permiso = Permisos.id_permiso AND Puertos.id_puerto = seleccion_puerto';

    query2 := 'SELECT * FROM Permisos_Pedidos, Instalaciones, Puerto_Instalacion, Puertos, Permisos, Permiso_muelle WHERE Permisos_Pedidos.id_instalacion = Instalaciones.id_instalacion AND Instalaciones.id_instalacion = Puerto_Instalacion.id_instalacion AND Puerto_Instalacion.id_puerto = Puertos.id_puerto AND Permisos_Pedidos.id_permiso = Permisos.id_permiso AND Permiso_muelle.id_permiso = Permisos.id_permiso AND Puertos.id_puerto = seleccion_puerto';

    query_instalacion := 'SELECT Instalaciones.id_instalacion, Instalaciones.capacidad_instalacion FROM Puertos, Puerto_Instalacion, Instalaciones WHERE Puertos.id_puerto = Puerto_Instalacion.id_puerto AND Puerto_Instalacion.id_instalacion = Instalaciones.id_instalacion AND Puertos.id_puerto = seleccion_puerto';
    
    loop
        for info_instalacion in execute 'SELECT Instalaciones.id_instalacion, Instalaciones.capacidad_instalacion FROM Puertos, Puerto_Instalacion, Instalaciones WHERE Puertos.id_puerto = Puerto_Instalacion.id_puerto AND Puerto_Instalacion.id_instalacion = Instalaciones.id_instalacion AND Puertos.id_puerto = $1' using seleccion_puerto loop
            id_instal := info_instalacion.id_instalacion;
            contador := 0;
            for info1 in execute 'SELECT *  FROM Permisos_Pedidos, Instalaciones, Puerto_Instalacion, Puertos, Permisos, Permiso_muelle WHERE Permisos_Pedidos.id_instalacion = Instalaciones.id_instalacion AND Instalaciones.id_instalacion = Puerto_Instalacion.id_instalacion AND Puerto_Instalacion.id_puerto = Puertos.id_puerto AND Permisos_Pedidos.id_permiso = Permisos.id_permiso AND Permiso_muelle.id_permiso = Permisos.id_permiso AND Puertos.id_puerto = $1' using seleccion_puerto loop
                if info1.fecha_atraque = fecha1 and info1.id_instalacion = id_instal then
                    contador := contador + 1;
                end if;
            end loop;
            for info2 in execute 'SELECT * FROM Permisos_Pedidos, Instalaciones, Puerto_Instalacion, Puertos, Permisos, Permiso_astillero WHERE Permisos_Pedidos.id_instalacion = Instalaciones.id_instalacion AND Instalaciones.id_instalacion = Puerto_Instalacion.id_instalacion AND Puerto_Instalacion.id_puerto = Puertos.id_puerto AND Permisos_Pedidos.id_permiso = Permisos.id_permiso AND Permiso_astillero.id_permiso = Permisos.id_permiso AND Puertos.id_puerto = $1' using seleccion_puerto loop
                if info2.fecha_atraque <= fecha1 and info2.id_instalacion = id_instal  and info2.fecha_salida >fecha1 then
                    contador := contador + 1;
                end if;
            end loop;
            espacio := info_instalacion.capacidad_instalacion - contador;
            porcentaje := espacio/info_instalacion.capacidad_instalacion;
            PREPARE insertar (int, timestamp, int, real) AS INSERT INTO resultado VALUES($1, $2, $3, $4);
            execute insertar(id_instal, fecha1, espacio, porcentaje);                   
        end loop;
        if fecha1 = fecha2 then
            exit;
        end if;
        fecha1 := fecha1 + 1;
    end loop;

RETURN QUERY SELECT * FROM resultado
RETURN;
END
$$ language plpgsql
