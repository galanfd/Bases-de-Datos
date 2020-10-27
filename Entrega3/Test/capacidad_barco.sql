CREATE OR REPLACE FUNCTION
espacio_para_barco(tipo varchar, fecha1 timestamp, fecha2 timestamp, patente varchar, seleccion_puerto integer)
RETURNS TABLE (instalacion INT, tiene_capacidad varchar, posible_fecha_entrada timestamp) AS $$
DECLARE
contador integer := 0;
query1 text;
query2 text;
query_instalacion_muelle text;
query_instalacion_astillero text;
info1 record;
info2 record;
instal record;
date timestamp;
info_instalacion record;
estado varchar;
tiene_espacio varchar;
entra varchar;
porcentaje float;
espacio int;
id_instal int;
date_entrada timestamp;
date_salida timestamp;
fecha_entrada timestamp := fecha1;
BEGIN
    DROP TABLE espacio_barco;
    CREATE TABLE espacio_barco(id_instal INT, tiene_capacidad varchar, posible_fecha_entrada timestamp);
    
    if tipo = 'muelle' then
	for info_instalacion in execute 'SELECT Instalaciones.id_instalacion, Instalaciones.capacidad_instalacion FROM Puertos, Puerto_Instalacion, Instalaciones WHERE Puertos.id_puerto = Puerto_Instalacion.id_puerto AND Puerto_Instalacion.id_instalacion = Instalaciones.id_instalacion AND Instalaciones.tipo_instalacion = $1 AND Puertos.id_puerto = $2' using tipo, seleccion_puerto loop
            id_instal := info_instalacion.id_instalacion;
	    contador := 0;
	    for info1 in execute 'SELECT *  FROM Permisos_Pedidos, Instalaciones, Puerto_Instalacion, Puertos, Permisos, Permiso_muelle WHERE Permisos_Pedidos.id_instalacion = Instalaciones.id_instalacion AND Instalaciones.id_instalacion = Puerto_Instalacion.id_instalacion AND Puerto_Instalacion.id_puerto = Puertos.id_puerto AND Permisos_Pedidos.id_permiso = Permisos.id_permiso AND Permiso_muelle.id_permiso = Permisos.id_permiso AND Puertos.id_puerto = $1' using seleccion_puerto loop
                if date_part('day', info1.fecha_atraque) = date_part('day', fecha1) and date_part('month', info1.fecha_atraque) = date_part('month', fecha1) and date_part('year', info1.fecha_atraque) = date_part('year', fecha1) and info1.id_instalacion = id_instal then
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
	    insert into espacio_barco VALUES(id_instal, estado, fecha1);
	end loop;
    end if;

    if tipo = 'astillero' then
	for info_instalacion in execute 'SELECT Instalaciones.id_instalacion, Instalaciones.capacidad_instalacion FROM Puertos, Puerto_Instalacion, Instalaciones WHERE Puertos.id_puerto = Puerto_Instalacion.id_puerto AND Puerto_Instalacion.id_instalacion = Instalaciones.id_instalacion AND Instalaciones.tipo_instalacion = $1 AND Puertos.id_puerto = $2' using tipo, seleccion_puerto loop
            id_instal := info_instalacion.id_instalacion;
	    contador := 0;
	    DROP TABLE espacio;
            CREATE TABLE espacio(id_instal INT, fecha timestamp, tiene_capacidad varchar);
	    fecha1 := fecha_entrada;
	    loop
	        for info2 in execute 'SELECT * FROM Permisos_Pedidos, Instalaciones, Puerto_Instalacion, Puertos, Permisos, Permiso_astillero WHERE Permisos_Pedidos.id_instalacion = Instalaciones.id_instalacion AND Instalaciones.id_instalacion = Puerto_Instalacion.id_instalacion AND Puerto_Instalacion.id_puerto = Puertos.id_puerto AND Permisos_Pedidos.id_permiso = Permisos.id_permiso AND Permiso_astillero.id_permiso = Permisos.id_permiso AND Puertos.id_puerto = $1' using seleccion_puerto loop
                    if info2.fecha_atraque <= fecha1 and info2.id_instalacion = id_instal  and info2.fecha_salida > fecha1 then
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
                if fecha1 >= fecha2 then
                    exit;
                end if;
                fecha1 := fecha1 + interval '1' day;
    	    end loop;
            entra := 'True';
	    date_entrada := fecha1;
	    date_salida := fecha2;
            for instal in execute 'SELECT * FROM espacio' loop
	        if instal.tiene_capacidad = 'False' then
	            entra := 'False';
	            date_entrada := NULL;
		    date_salida := NULL;
	        end if;
	    end loop;
	    insert into espacio_barco VALUES(id_instal, entra, date_entrada);
        end loop;
    end if;

RETURN QUERY SELECT * FROM espacio_barco
RETURN;
END
$$ language plpgsql
