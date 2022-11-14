	String.prototype.replaceAll = function( token, newToken, ignoreCase ) {
	    var _token;
	    var str = this + "";
	    var i = -1;
	
	    if ( typeof token === "string" ) {
	
	        if ( ignoreCase ) {
	
	            _token = token.toLowerCase();
	
	            while( (
	                i = str.toLowerCase().indexOf(
	                    _token, i >= 0 ? i + newToken.length : 0
	                ) ) !== -1
	            ) {
	                str = str.substring( 0, i ) +
	                    newToken +
	                    str.substring( i + token.length );
	            }
	
	        } else {
	            return this.split( token ).join( newToken );
	        }
	
	    }
	return str;
	};

	function ersetzeSonderzeichenHTML2Dez(text) {

        if(text){
        	text = "" + text;
        }
		
		if (!text || text == "") {
            return "";
        }

        text = text.replaceAll("\\", "xx92;");
        text = text.replaceAll("\"", "xx34;");
        text = text.replaceAll("\\%", "xx37;");
        text = text.replaceAll("\\&", "xx38;");
        text = text.replaceAll("#", "xx35;");
        text = text.replaceAll("'", "xx39;");
        text = text.replaceAll("\\^", "xx710;");
        text = text.replaceAll("\\[", "xx91;");
        text = text.replaceAll("\\]", "xx93;");
        text = text.replaceAll(":", "xx58;");
        text = text.replaceAll("\\{", "xx123;");
        text = text.replaceAll("\\}", "xx125;");
        text = text.replaceAll("<", "xx60;");
        text = text.replaceAll(">", "xx62;");
        text = text.replaceAll("\\|", "xx124;");
        text = text.replaceAll("~", "xx732;");

        return text;
    }
    
    function ersetzeSonderzeichenDez2HTML(text) {

    	if(text){
    		text = "" + text;
        }
    	
    	if (!text || text == "") {
            return "";
        }

        text = text.replaceAll("xx34;", "\"");
        text = text.replaceAll("xx37;", "\\%");
        text = text.replaceAll("xx38;", "&");
        text = text.replaceAll("xx35;", "#");
        text = text.replaceAll("xx39;", "'");
        text = text.replaceAll("xx710;", "\\^");
        text = text.replaceAll("xx91;", "\\[");
        text = text.replaceAll("xx93;", "\\]");
        text = text.replaceAll("xx58;", ":");
        text = text.replaceAll("xx123;", "\\{");
        text = text.replaceAll("xx125;", "\\}");
        text = text.replaceAll("xx60;", "<");
        text = text.replaceAll("xx62;", ">");
        text = text.replaceAll("xx124;", "\\|");
        text = text.replaceAll("xx732;", "~");
        text = text.replaceAll("xx92;", "\\");

        return text;
    }

function createFlashMessage(err, style){
	
	if(!style){
		style = "error";
	}
	
	if(!err){
		return;
	}
	var ran = Math.floor((Math.random() * 1000) + 1); 
	$(".meldung").remove();
	
	var row = $("<div>");
	row.addClass("row");
	row.addClass("meldung");
	row.addClass("m" + ran);
	
	var columns = $("<div>");
	columns.addClass("small-12");
	columns.addClass("medium-12");
	columns.addClass("columns");
	
	var meldung = $("<div>");
	meldung.addClass(style);
	meldung.html(err);
	
	columns.append(meldung);
	row.append(columns);
	row.css("display","none");
	
	$(".titel").after(row);
	
	row.fadeIn("slow",function(){
		setTimeout(function(){ $(".m" + ran).fadeOut("slow");}, 3000);
	});
	
}

function initialisiereSuche(suchbegriff){
	var treffer_gemet;
	var treffer_eunis;
	var treffer_eunomen;
	
	$(".h_2").text("Suche in Thesauren");
	$("#myModal").css("display","block");
	
	var target = document.getElementById('myModal')
	spinner = new Spinner(spinner_opts).spin(target);
	
	if(gemet){
		$("#treffer-gemet").empty();
		$("#modal-treffer-gemet").css("display","");
		treffer_gemet = sucheInGEMET(suchbegriff);
	}else{
		$("#modal-treffer-gemet").css("display","none");
	}
	
	if(eunomen){
		$("#treffer-eunomen").empty();
		$("#modal-treffer-eunomen").css("display","");
        treffer_gemet = sucheInEUNOMEN(suchbegriff);
    }else{
    	$("#modal-treffer-eunomen").css("display","none");
    }
	
	spinner.stop();
	
}

function sucheInGEMET(suchbegriff){
	var url = "proxy/sucheingemet";
	$.ajax({
		url: url,
		data: suchbegriff,
		crossDomain: true,
		async: false
	}).done(function(data){
		$.each(data,function(index, item){
			var div = $("<div></div>").addClass("thesaurus_eintrag");
			var ueberschrift = $("<a></a>").addClass("thesaurus_ueberschrift");
			var auswahl = $("<input id='check_" + index + "' type='checkbox'></input>").addClass("thesaurus_auswahl");
			var beschreibung = $("<div></div>").addClass("thesaurus_beschreibung");
			var referenzen;
			
			ueberschrift.text(item.preferredLabel.string);
			ueberschrift.attr("href",item.uri);
			ueberschrift.attr("target","_blank");
			
			if(item.definition){
				beschreibung.text(item.definition.string);
			}
			
			referenzen = sucheRelatedConcepts(item.uri);
			
			div.append(auswahl);
			div.append(ueberschrift);
			div.append(beschreibung);
			if(referenzen);
				div.append(referenzen);
			
			$("#treffer-gemet").append(div);
		});
	})
}

function sucheInEUNOMEN(suchbegriff){
	var url = "proxy/sucheineunomen";
	$.ajax({
		url: url,
		data: suchbegriff,
		crossDomain: true,
		async: false
	}).done(function(data){
		$.each(data,function(index, item){
			if(item && item.guid != "" && item.guid != "null"){
				var div = $("<div></div>").addClass("thesaurus_eintrag");
				var ueberschrift = $("<a></a>").addClass("thesaurus_ueberschrift");
				var auswahl = $("<input id='check_" + index + "' type='checkbox'></input>").addClass("thesaurus_auswahl");
				var beschreibung = $("<div></div>").addClass("rc_titel");
				var referenzen;
				
				ueberschrift.text(item.name);
				ueberschrift.attr("href",item.url);
				ueberschrift.attr("target","_blank");
				
				beschreibung.text(item.guid);
				
				//referenzen = sucheRelatedConcepts(item.uri);
				
				div.append(auswahl);
				div.append(ueberschrift);
				div.append(beschreibung);
				if(referenzen);
					div.append(referenzen);
				
				$("#treffer-eunomen").append(div);
			}
		});
	})
}

function sucheRelatedConcepts(concept){
	//related, narrower, broader
	//var url = "http://www.eionet.europa.eu/gemet/getRelatedConcepts?concept_uri=" + url + "&relation_uri=http://www.w3.org/2004/02/skos/core%23related&language=de";
	var url = "proxy/sucherelatedconcepts";
	var div = $("<div></div>").addClass("rc_eintrag");
	var titel = $("<div>verwandte Begriffe (related concepts)</div>").addClass("rc_titel");
	
	div.append(titel);
	
	$.ajax({
		url: url,
		data: concept,
		crossDomain: true,
		async: false
	}).done(function(data){
		$.each(data,function(index, item){
			var ueberschrift = $("<a></a>").addClass("rc_ueberschrift");
			var beschreibung = $("<div></div>").addClass("rc_beschreibung");
			
			ueberschrift.attr("href",item.uri);
			ueberschrift.attr("target","_blank");
			ueberschrift.text(item.preferredLabel.string);
			if(item.definition){
				beschreibung.text(item.description.string);
			}
			
			div.append(ueberschrift);
			div.append(beschreibung);
		});
	})
	
	var spacer = $("<div></div>").addClass("rc_spacer");
	div.append(spacer);
	return div;
}

var spinner;
var spinner_opts = {
	  lines: 13 // The number of lines to draw
	, length: 28 // The length of each line
	, width: 14 // The line thickness
	, radius: 42 // The radius of the inner circle
	, scale: 1 // Scales overall size of the spinner
	, corners: 1 // Corner roundness (0..1)
	, color: '#000' // #rgb or #rrggbb or array of colors
	, opacity: 0.25 // Opacity of the lines
	, rotate: 0 // The rotation offset
	, direction: 1 // 1: clockwise, -1: counterclockwise
	, speed: 1 // Rounds per second
	, trail: 60 // Afterglow percentage
	, fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
	, zIndex: 2e9 // The z-index (defaults to 2000000000)
	, className: 'spinner' // The CSS class to assign to the spinner
	, top: '50%' // Top position relative to parent
	, left: '50%' // Left position relative to parent
	, shadow: false // Whether to render a shadow
	, hwaccel: false // Whether to use hardware acceleration
	, position: 'absolute' // Element positioning
}