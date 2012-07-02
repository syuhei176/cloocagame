function clooca() {}

clooca.include = function(fn) {
    var script = document.createElement( 'script' );
    script.type = 'text/javascript';
    script.src = "/static/js/"+fn;
    $("#script-div").append( script );
}

clooca.includes = function(fs) {
	for(var i=0;i < fs.length;i++) {
    	var script = document.createElement( 'script' );
    	script.type = 'text/javascript';
    	script.src = "/static/js/"+fs[i];
    	$("#script-div").append( script );
	}
}

function initall() {
	clooca.includes(['core.js','workbench.js']);	
}
