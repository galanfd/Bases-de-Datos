CREATE OR REPLACE FUNCTION
retornar_instalacione_libres(fecha1 timestamp, fecha2 timestamp, seleccion_puerto integer)
RETURNS TABLE (instalacion varchar(50), fecha date, disponibles integer, porcentaje float) AS $$
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
    CREATE TEMP TABLE resultado(id_instal INT, fecha timestamp, espacio int, disponible float);

    query1 := 'SELECT *  FROM Permisos_Pedidos, Instalaciones, Puerto_Instalacion, Puertos, Permisos, Permiso_muelle WHERE Permisos_Pedidos.id_instalacion = Instalaciones.id_instalacion AND Instalaciones.id_instalacion = Puerto_Instalacion.id_instalacion AND Puerto_Instalacion.id_puerto = Puertos.id_puerto AND Permisos_Pedidos.id_permiso = Permisos.id_permiso AND Permiso_muelle.id_permiso = Permisos.id_permiso AND Puertos.id_puerto =' seleccion_puerto;

    query2 := 'SELECT * FROM Permisos_Pedidos, Instalaciones, Puerto_Instalacion, Puertos, Permisos, Permiso_muelle WHERE Permisos_Pedidos.id_instalacion = Instalaciones.id_instalacion AND Instalaciones.id_instalacion = Puerto_Instalacion.id_instalacion AND Puerto_Instalacion.id_puerto = Puertos.id_puerto AND Permisos_Pedidos.id_permiso = Permisos.id_permiso AND Permiso_muelle.id_permiso = Permisos.id_permiso AND Puertos.id_puerto =' seleccion_puerto;

    query_instalacion := 'SELECT Instalaciones.id_instalacion, Instalaciones.capacidad_instalacion FROM Puertos, Puerto_Instalacion, Instalaciones WHERE Puertos.id_puerto = Puerto_Instalacion.id_puerto AND Puerto_Instalacion.id_instalacion = Instalaciones.id_instalacion AND Puertos.id_puerto =' seleccion_puerto;

    loop
        for info_instalacion in execute query_instalacion loop
            id_instal := info_instalacion.Instalaciones.id_instalacion;
            contador := 0;
            for info1 in execute query1 loop
                if info1.atraque = fecha1 and info1.Instalaciones.id_instalacion = id_instal then
                    contador := contador + 1;
                end if;
            end loop;
            for info2 in execute query2 loop
                if info2.atraque <= fecha1 and info2.Instalaciones.id_instalacion = id_instal  and info2.salida >fecha1 then
                    contador := contador + 1;
                end if;
            end loop;
            espacio := info_instalacion.capacidad - contador;
            porcentaje := espacio/info_instalacion.capacidad;
            execute 'INSERT INTO resultado(id_instal, fecha1, espacio, porcentaje)';
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
