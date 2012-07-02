function AirconEnvironment(df_data, _is_preview) {
	this.df = new DataFlow(df_data, this);
	this.power = 0;
	this.temperture_d = 0;
	this.temperture = 26;
}

AirconEnvironment.prototype.step = function() {
	this.draw();
	this.power = 0;
	this.df.getSensorValue('temperture', this.temperture);
	if(this.power > 0) {
		this.temperture_d -= 0.1;
	}else if(this.power < 0) {
		this.temperture_d += 0.1;
	}else{
		if(this.temperture < 26) {
			this.temperture_d = 0.1;
		}else{
			if(this.temperture_d > 0) this.temperture_d -= 0.1;
			else if(this.temperture_d < 0) this.temperture_d += 0.1;
		}
	}
	this.temperture += this.temperture_d;
	console.log(this.temperture_d);
}

AirconEnvironment.prototype.draw = function() {
	$("canvas").drawRect({
		fillStyle: "#fff",
		  x: 0, y: 0,
		  width: 640,
		  height: 640,
		  fromCenter: false
		});
	$("canvas").drawText({
		  fillStyle: "#000",
		  strokeStyle: "#25a",
		  strokeWidth: 4,
		  x: 240, y: 200,
		  font: "28pt Verdana, sans-serif",
		  text: '' + Math.floor(this.temperture)
		});

}
