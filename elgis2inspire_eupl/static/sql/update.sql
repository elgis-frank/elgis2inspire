update update_habitattype  set lcode = trim(lcode);
update elgis2inspire_habitatlist set lcode = trim(lcode);
update update_habitattype set lname  = (select lname from elgis2inspire_habitatlist where elgis2inspire_habitatlist.lcode = update_habitattype.lcode);
update update_habitattype set icode  = (select icode from elgis2inspire_habitatlist where elgis2inspire_habitatlist.lcode = update_habitattype.lcode);
update update_habitattype set iname  = (select iname from elgis2inspire_habitatlist where elgis2inspire_habitatlist.lcode = update_habitattype.lcode);
update update_habitattype set qualifierLocalName = (select imatch from elgis2inspire_habitatlist where elgis2inspire_habitatlist.lcode = update_habitattype.lcode);
insert into elgis2inspire_habitattypecovertype (fid , referenceHabitatTypeId, referenceHabitatTypeName, referenceHabitatTypeScheme, bl) select featureId,  icode, iname, 'http://inspire.ec.europa.eu/codelist/ReferenceHabitatTypeSchemeValue/eunis', bl from update_habitattype ;
insert into elgis2inspire_localnametype (fid, localnamecode, localname, qualifierLocalName, bl) select featureid, lcode, lname, qualifierLocalName, bl from update_habitattype;
drop table update_habitattype;
