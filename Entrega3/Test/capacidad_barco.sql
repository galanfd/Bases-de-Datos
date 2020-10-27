CREATE OR REPLACE FUNCTION
espacio_para_barco(tipo varchar, fecha1 timestamp, fecha2 timestamp, patente varchar, seleccion_puerto integer)
RETURNS TABLE (instalacion INT, tiene_capacidad varchar) AS $$
DECLARE
contador integer := 0;
query1 text;
query2 text;
query_instalacion_muelle text;
query_instalacion_astillero text;
info1 record;
info2 record;
instal record;
info_instalacion record;
estado varchar;
tiene_espacio varchar;
entra int;
porcentaje float;
espacio int;
id_instal int;
BEGIN
    DROP TABLE espacio_barco;
    CREATE TEMP TABLE espacio(id_instal INT, fecha timestamp, tiene_capacidad varchar);
    CREATE TABLE espacio_barco(id_instal INT, tiene_capacidad varchar);
    
    if tipo = 'muelle' then
	loop
	    for info_instalacion in execute 'SELECT Instalaciones.id_instalacion, Instalaciones.capacidad_instalacion FROM Puertos, Puerto_Instalacion, Instalaciones WHERE Puertos.id_puerto = Puerto_Instalacion.id_puerto AND Puerto_Instalacion.id_instalacion = Instalaciones.id_instalacion AND Instalaciones.tipo_instalacion = muelle AND Puertos.id_puerto = $1' using seleccion_puerto loop
                id_instal := info_instalacion.id_instalacion;
	        contador := 0;
	        for info1 in execute 'SELECT *  FROM Permisos_Pedidos, Instalaciones, Puerto_Instalacion, Puertos, Permisos, Permiso_muelle WHERE Permisos_Pedidos.id_instalacion = Instalaciones.id_instalacion AND Instalaciones.id_instalacion = Puerto_Instalacion.id_instalacion AND Puerto_Instalacion.id_puerto = Puertos.id_puerto AND Permisos_Pedidos.id_permiso = Permisos.id_permiso AND Permiso_muelle.id_permiso = Permisos.id_permiso AND Puertos.id_puerto = $1' using seleccion_puerto loop
                    if info1.fecha_atraque = fecha1 and info1.id_instalacion = id_instal then
                        contador := contador + 1;
                    end if;
		end loop;	
	    espacio := info_instalacion.capacidad_instalacion - contador;
	    if espacio > 0 then
	        estado := 'True';
	    end if;
	    if espacio = 0 then
		estado := 'False';
	    end if;
	    insert into espacio VALUES(id_instal, fecha1, estado);
            end loop;
            if fecha1 = fecha2 then
                exit;
            end if;
            fecha1 := fecha1 + interval '1' day;
        end loop;
	entra := 'True';
	for instal in execute 'SELECT * FROM espacio' loop
	    if instal.tiene_capacidad = 'False' then
		entra := 'False';
	end loop;
	insert into espacio_barco VALUES(id_instal, entra);
    end if;

    if tipo = 'astillero' then
	loop
	    for info_instalacion in execute 'SELECT Instalaciones.id_instalacion, Instalaciones.capacidad_instalacion FROM Puertos, Puerto_Instalacion, Instalaciones WHERE Puertos.id_puerto = Puerto_Instalacion.id_puerto AND Puerto_Instalacion.id_instalacion = Instalaciones.id_instalacion AND Instalaciones.tipo_instalacion = astillero AND Puertos.id_puerto = $1' using seleccion_puerto loop
                id_instal := info_instalacion.id_instalacion;
	        contador := 0;
	        for info2 in execute 'SELECT * FROM Permisos_Pedidos, Instalaciones, Puerto_Instalacion, Puertos, Permisos, Permiso_astillero WHERE Permisos_Pedidos.id_instalacion = Instalaciones.id_instalacion AND Instalaciones.id_instalacion = Puerto_Instalacion.id_instalacion AND Puerto_Instalacion.id_puerto = Puertos.id_puerto AND Permisos_Pedidos.id_permiso = Permisos.id_permiso AND Permiso_astillero.id_permiso = Permisos.id_permiso AND Puertos.id_puerto = $1' using seleccion_puerto loop
                if info2.fecha_atraque <= fecha1 and info2.id_instalacion = id_instal  and info2.fecha_salida >fecha1 then
                    contador := contador + 1;
                end if;
            end loop;	
	    espacio := info_instalacion.capacidad_instalacion - contador;
	    if espacio > 0 then
	        estado := 'True';
	    end if;
	    if espacio = 0 then
		estado := 'False';
	    end if;
	    insert into espacio VALUES(id_instal, fecha1, estado);
            end loop;
            if fecha1 = fecha2 then
                exit;
            end if;
            fecha1 := fecha1 + interval '1' day;
        end loop;
	entra := 'True';
	for instal in execute 'SELECT * FROM espacio' loop
	    if instal.tiene_capacidad = 'False' then
		entra := 'False';
	end loop;
	insert into espacio_barco VALUES(id_instal, entra);
    end if;

RETURN QUERY SELECT * FROM espacio_barco
RETURN;
END
$$ language plpgsql
