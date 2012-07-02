function DataFlow(df_data, aircon) {
	this.sensors = df_data.sensors;
	this.actuators = df_data.actuators;
	this.processings = df_data.processings;
	this.controlls = df_data.controlls;
	this.flows = df_data.flows;
	this.aircon = aircon;
}

DataFlow.prototype.getSensorValue = function(sensor_name, sensor_value) {
	for(var i=0;i < this.sensors.length;i++) {
		if(sensor_name == this.sensors[i].name) {
			this.do_flow(this.sensors[i], sensor_value);
		}
	}
}

DataFlow.prototype.do_flow = function(prev_node, value) {
	console.log('flow:' + prev_node.id + ', value:' + value);
	for(var i=0;i < this.flows.length;i++) {
		if(this.flows[i].src_id == prev_node.id) {
			for(var j=0;j < this.processings.length;j++) {
				if(this.flows[i].dest_id == this.processings[j].id) {
					this.do_process(this.processings[j], value);
				}
			}
			for(var j=0;j < this.actuators.length;j++) {
				if(this.flows[i].dest_id == this.actuators[j].id) {
					this.do_act(this.actuators[j], value);
				}
			}
			for(var j=0;j < this.controlls.length;j++) {
				if(this.flows[i].dest_id == this.controlls[j].id) {
					this.do_controll(this.controlls[j], value);
				}
			}
		}
	}
}

DataFlow.prototype.do_process = function(prodessing, value) {
	var new_value = value;
	if(prodessing.type == 'average') {
		new_value = value;
	}else if(prodessing.type == 'add') {
		new_value = value + Number(prodessing.value);
	}else if(prodessing.type == 'average') {
		new_value = value;
	}else if(prodessing.type == 'average') {
		new_value = value;
	}
	this.do_flow(prodessing, new_value);
}

DataFlow.prototype.do_controll = function(controll, value) {
	if(controll.type == 'ifb') {
		if(controll.value <= value) {
			this.do_flow(controll, value);
		}
	}else if(controll.type == 'ifs') {
		if(controll.value >= value) {
			this.do_flow(controll, value);
		}
	}
}


DataFlow.prototype.do_act = function(actuator, value) {
	if(actuator.type == 'lcd') {
		console.log('actuator:'+actuator.type + ',value:'+value);
		$("canvas").drawText({
			  fillStyle: "#000",
			  strokeStyle: "#25a",
			  strokeWidth: 4,
			  x: 240, y: 300,
			  font: "28pt Verdana, sans-serif",
			  text: '' + Math.floor(value)
			});
	}
	if(actuator.type == 'air') {
		this.aircon.power = value;
	}
	if(actuator.type == 'hot') {
		this.aircon.power = value;
	}
//	this.do_flow(actuator.id, sensor_value);
}

