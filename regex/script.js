var ouvert=0;
var glisse_timer;
var glisse_fermtimer;

function calculOuverture(ouvDemande) {

valmax = 0.75;

hautfen = window.innerHeight;
if (!hautfen) hautfen = document.body.offsetHeight;

hautfenmax = hautfen * valmax;
if (ouvDemande > hautfenmax) return  hautfenmax - hautfenmax%25;
else return ouvDemande;

}


function ouvre(i, href, hauteur) {

	hauteur = calculOuverture(hauteur);
	
  if(ouvert!=0 && ouvert!=i) {
  	//si qqch déjà ouvert
  	glisseferm(ouvert, hauteur, 0, 25, 'idRow' + ouvert);
	nameObj = (document.getElementById) ? document.getElementById('name' + ouvert) : eval("document.all['name" + ouvert + "']");
  	nameObj.className="row";		
  }
  var trObj = (document.getElementById) ? document.getElementById('idRow' + i) : eval("document.all['idRow" + i + "']");
  var nameObj = (document.getElementById) ? document.getElementById('name' + i) : eval("document.all['name" + i + "']");
//   var ifObj = (document.getElementById) ? document.getElementById('idIframe' + i) : eval("document.all['idIframe" + i + "']");
  if (trObj != null) {
    if (trObj.style.display=="none") {
      trObj.style.display="";
 	  nameObj.className="rowopen";
//       if (!ifObj.src) ifObj.src = href;
      glisse('idIframe' + i, 0, hauteur, 25, 'o');
	  ouvert = i;
    }
    else {
      nameObj.className="rowopen";
      glisse('idIframe' + i, hauteur, 0, 25, 'idRow' + i);
	  ouvert = 0;
    }
  }    
}

function dessus(i) {  
  var nameObj = (document.getElementById) ? document.getElementById('name' + i) : eval("document.all['name" + i + "']");
  if (nameObj != null) {nameObj.className="rowover";}	
}
function parti(i) {
 	if (i==ouvert) return;
  	var trObj = (document.getElementById) ? document.getElementById('idRow' + i) : eval("document.all['idRow" + i + "']");  
  	var nameObj = (document.getElementById) ? document.getElementById('name' + i) : eval("document.all['name" + i + "']");    
  	if (trObj == null || trObj.style.display=="none") {nameObj.className="row";}
}
function glisse(id, curH, targetH, stepH, mode) {
  diff = targetH - curH;
  if (diff != 0) {
    newH = (diff > 0) ? curH + stepH : curH - stepH;
    ((document.getElementById) ? document.getElementById(id) : eval("document.all['" + id + "']")).style.height = newH + "px";
    if (glisse_timer) window.clearTimeout(glisse_timer);
    glisse_timer = window.setTimeout( "glisse('" + id + "'," + newH + "," + targetH + "," + stepH + ",'" + mode + "')", 20 );
  }
  else if (mode != "o") ((document.getElementById) ? document.getElementById(mode) : eval("document.all['" + mode + "']")).style.display="none";
}
function glisseferm(i, curH, targetH, stepH, mode) {
  diff = targetH - curH;
  if (diff != 0) {
  	id = "idIframe" +  i;	
    newH = (diff > 0) ? curH + stepH : curH - stepH;
    ((document.getElementById) ? document.getElementById(id) : eval("document.all['" + id + "']")).style.height = newH + "px";
    if (glisse_fermtimer) window.clearTimeout(glisse_fermtimer);
    glisse_fermtimer = window.setTimeout( "glisseferm('" + i + "'," + newH + "," + targetH + "," + stepH + ",'" + mode + "')", 20 );
  }
  else if (mode != "o") ((document.getElementById) ? document.getElementById(mode) : eval("document.all['" + mode + "']")).style.display="none";
}

function montreImage(nomImage) {
	document.getElementById('image.'+nomImage).setAttribute("src", "images/"+nomImage);
	document.getElementById('imagelayer.'+nomImage).style.visibility="visible";
}
function cacheImage(nomImage) {
	document.getElementById('imagelayer.'+nomImage).style.visibility="hidden";
}
