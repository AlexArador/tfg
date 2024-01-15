function drawRacingLine(points) {
	let circuitDiv = document.getElementById("racingLineDiv");

	preCanvas = document.getElementById('racingLineCanvas');
	if (typeof(preCanvas) != 'undefined' && preCanvas != null) {
		preCanvas.remove();
	}

    let canvas = document.createElement('canvas');
    canvas.setAttribute('id','racingLineCanvas');
    canvas.width = circuitDiv.clientWidth;
    canvas.height = circuitDiv.clientHeight;
    
    let ctx = canvas.getContext('2d');
    ctx.fillStyle = 'red';

    for (let i = 0; i < points.length; i++) {
        let point = points[i];
        ctx.beginPath();
        ctx.arc(point[0], point[1], 2, 0, 2 * Math.PI);
        ctx.fill();
    }
    circuitDiv.appendChild(canvas);
}

function parseModelsCsv(csvContent) {
	let data = Papa.parse(csvContent);
	headers = data['data'][0];

	data = data['data'].splice(1,data['data'].length);

	for (let i = 0; i < data.length - 1; i++) {
		models.push(new Model(data[i][0].toString()));
	}
}

function parseCircuits(csvContent) {
	let data = Papa.parse(csvContent);
	headers = data['data'][0];

	data = data['data'].splice(1,data['data'].length);

	for (let i = 0; i < data.length; i++) {
		c = data[i];
		circuits.push(new Circuit(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7]));
	}
}

function parseCircuitsJson(csvContent) {
	circuitsJson = JSON.parse(csvContent);
	circuitKeys = Object.keys(circuitsJson);

	for (let i = 0; i < circuitKeys.length; i++) {
		k = circuitKeys[i];
		circuitIndex = getCircuitByRef(circuits, k);
		c = circuits[circuitIndex];
		
		c.circuitGoals = circuitsJson[k]['goals'].length;
		circuits[circuitIndex] = c;
	}

}

function changeImage(newImage) {
	let scale = 0.5;
	let circuitDiv = document.getElementById("racingLineDiv");
	let img = new Image();

	circuitDiv.style.backgroundImage = "url('" + newImage + "')";		
    img.src = url;

    circuitDiv.style.width = parseInt(img.naturalWidth * scale).toString() + "px";
    circuitDiv.style.height = parseInt(img.naturalHeight * scale).toString() + "px";

    //console.log('Div width:', circuitDiv.clientWidth);
	//console.log('Div height:', circuitDiv.clientHeight);

    //console.log('Image width:', img.naturalWidth);
    //console.log('Image height:', img.naturalHeight);

    const scaleWidth = circuitDiv.clientWidth / img.naturalWidth;
    const scaleHeight = circuitDiv.clientHeight / img.naturalHeight;

    //console.log('Width scale:', scaleWidth);
    //console.log('Height scale:', scaleHeight);

    //return [scaleWidth, scaleHeight];
    return [scale, scale];
}

function loadCars(cars) {
	let carSelectorId = "select-9d97";
	clearOptions(carSelectorId);
	carSelector = document.getElementById(carSelectorId);

	for (let i = 0; i < cars.length; i++) {
		let carOption = cars[i].toString();
		let option = document.createElement("option");
		option.value = carOption;
		option.text = 'Car nº ' + carOption;
		carSelector.appendChild(option);
	}
}

function printThisRacingLine(csvContent, thisCar) {
	let data = Papa.parse(csvContent);
	headers = data['data'][0];
	console.log(headers);

	data = data['data'].splice(1,data['data'].length);
	data = data.splice(0,data.length - 1);

	let cars = [];
	let times = [];
	let racingCircuits = [];
	let goalsCrossed = [];
	let racingLines = [];
	for (let i = 0; i < data.length; i++) {
		let d = data[i];
		cars.push(d[0]);
		racingCircuits.push(d[2]);
		times.push(d[1]);
		goalsCrossed.push(d[3]);
		racingLines.push(d[4]);
	}

	if (thisCar == "-1") {
		let racingLinesObj = [];
		let longestDataPoints = 0;
		var longestDataPointsIndex = -1;
		for (let i = 0; i < racingLines.length; i++) {
			let dataPoints = JSON.parse(racingLines[i]);
			racingLinesObj.push(dataPoints);
			if (dataPoints.length > longestDataPoints) {
				longestDataPoints = dataPoints.length;
				longestDataPointsIndex = i;
			}
		}
		racingLine = racingLinesObj[longestDataPointsIndex];
	} else {
		longestDataPointsIndex = cars.indexOf(thisCar);
		racingLine = JSON.parse(racingLines[longestDataPointsIndex]);
	}

	car = cars[longestDataPointsIndex];
	time = times[longestDataPointsIndex];
	circuit = parseInt(racingCircuits[longestDataPointsIndex]);
	goalsCrossed = goalsCrossed[longestDataPointsIndex];

	let c = circuits[getCircuitById(circuits, circuit)];
	console.log('CIRCUIT');
	console.log(c);
	url = 'data/circuits/images/' + c.circuitRef + '.png';
	const scale = changeImage(url);
	changeCircuitCard(c);

	x = [];
	y = [];
	speeds = [];
	angles = [];
	choices = [];
	for (let i = 0; i < racingLine.length; i++) {
		dataPoint = racingLine[i];

		x.push(dataPoint[0]);
		y.push(dataPoint[1]);
		speeds.push(dataPoint[2]);
		angles.push(dataPoint[3]);
		choices.push(dataPoint[4]);
	}

	let points = [];
	for (let i = 0; i < x.length; i++) {
		points.push([x[i] * scale[0] ,y[i] * scale[1]]);
	}

	console.log('Original X:', x[0], 'Scalated X:', points[0][0]);
	console.log('Original Y:', y[0], 'Scalated Y:', points[0][1]);

	drawRacingLine(points);
	printTime(time);
	printTitle('Trazada para el coche nº ' + car);

	const totalGoals = circuits[getCircuitById(circuits, circuit)].circuitGoals;
	console.log('Goals crossed:', goalsCrossed);

	let lapCompleted = goalsCrossed >= totalGoals;	

	printGoals(time, goalsCrossed, totalGoals);
	let projectedLapTime = "Not determinable";
	if (goalsCrossed != 0) {
		projectedLapTime = getProjectedLapTime(time, goalsCrossed, totalGoals);
	}
	printProjectedLapTime(lapCompleted, projectedLapTime);
}

function changeCircuitCard(c) {
	console.log('CIRCUIT:');
	console.log(c);

	let cardCircuitName = document.getElementById('cardCircuitName');
	cardCircuitName.textContent = c.name;

	let cardCircuitLocation = document.getElementById('cardCircuitLocation');
	cardCircuitLocation.textContent = c.location + ' (' + c.country + ')';

	let cardCircuitLength = document.getElementById('cardCircuitLength');
	cardCircuitLength.textContent = c.length.toLocaleString() + 'm';

	let t = times[getTimeForCircuit(times, c.circuitId, 'BEST')];

	let cardCircuitFastestLap = document.getElementById('cardCircuitFastestLap');
	cardCircuitFastestLap.textContent = t.time;

	let driver = drivers[getDriverById(drivers, t.driverId)];

	cardCircuitFastestDriver = document.getElementById('cardCircuitFastestDriver');
	cardCircuitFastestDriver.textContent = driver['name'];

	cardCircuitFastestDriverPic = document.getElementById('cardCircuitFastestDriverPic');
	cardCircuitFastestDriverPic.src = driver['picture'];

	cardCircuitFastestDriverInfo = document.getElementById('cardCircuitFastestDriverInfo');
	cardCircuitFastestDriverInfo.textContent = driver['number'] + ' - ' + driver['code'];

	console.log(races[0]);

	let r = races[getRaceById(races, t['raceId'].toString())];

	cardCircuitFastestDate = document.getElementById('cardCircuitFastestDate');
	cardCircuitFastestDate.textContent = r['date'];
}

function parseCarsContent(csvContent) {
	let data = Papa.parse(csvContent);
	headers = data['data'][0];
	console.log(headers);

	data = data['data'].splice(1,data['data'].length);
	data = data.splice(0,data.length - 1);

	let cars = [];
	for (let i = 0; i < data.length; i++) {
		cars.push(data[i][0]);
	}

	loadCars(cars);
}

function hideOrShowRow(rowId, hideOrShow) {
	row = document.getElementById(rowId);
	row.style.display = hideOrShow ? '' : 'none';
}

function parseTime(time) {
	minutes = parseInt(Math.floor(time / 60));
	rem = time - minutes * 60;

	seconds = parseInt(rem);

	fractions = Math.round((rem - seconds) * 1000) / 100;
	fractions = fractions.toString().replace('.', '');

	minutes = ('00' + minutes.toString()).slice(-2);
	seconds = ('00' + seconds.toString()).slice(-2);
	fractions = ('000' + fractions.toString()).slice(-3);

	return minutes.concat(':', seconds, '.', fractions);
}

function printTitle(title) {
	titleElement = document.getElementById('variablesCanvasTitle');
	titleElement.textContent = title;
}

function printTime(time) {
	lapTime = document.getElementById('lapTime');
	lapTime.textContent = parseTime(time);
}

function printGoals(time, goals, totalGoals) {
	let lapsCompleted = 0;
	goalsCrossed = document.getElementById('goalsCrossed');

	if (goals >= totalGoals) {
		lapsCompleted = Math.floor(goals / totalGoals);
	}
	if (lapsCompleted != 0) {
		let lapTime = time / lapsCompleted;
		lapsCompleted = parseInt(lapsCompleted);
		goalsCrossed.textContent = lapsCompleted.toString() + ' vueltas completadas';
	} else {
		goalsCrossed.textContent = parseInt(Math.round(goals)).toString().concat(' de ', totalGoals.toString());
	}
}

function getProjectedLapTime(time, goals, totalGoals) {
	var lapsCompleted = 0;
	
	if (goals >= totalGoals) {
		lapsCompleted = Math.floor(goals / totalGoals);
	}

	if (lapsCompleted == 0) {
		return time * totalGoals / goals;
	} else {
		return time / lapsCompleted;
	}
}

function printProjectedLapTime(lapCompleted, time) {
	let projectedLapTime = document.getElementById('projectedLapTime');
	let projectedLapTimeLabel = document.getElementById('projectedLapTimeLabel');

	var text = 'Tiempo por vuelta esperado';

	if (time != "Not determinable") {
		time = parseTime(time);
	}

	if (lapCompleted) {
		text = 'Tiempo por vuelta';
	}

	projectedLapTime.textContent = time;
	projectedLapTimeLabel.textContent = text;
}

async function readCsvContent(fileName, justLoad) {
    try {
        const response = await fetch(fileName);
        if (response.ok) {
            const content = await response.text();

            switch (fileName) {
	    		case 'data/circuits/circuits.csv':
	    			parseCircuits(content);
	    			break;
	    		case 'data/circuits/circuits.json':
	    			parseCircuitsJson(content);
	    			break;
	    		case 'data/models/models.csv':
	    			parseModelsCsv(content);
	    			loadModels();
	    			break;
	    		case 'data/models/generations.csv':
	    			parseGenerationsCsv(content);
	    			break;
	    		case 'data/drivers.csv':
	    			parseDriversCsv(content);
	    			break;
	    		case 'data/circuits/times.csv':
	    			parseTimesCsv(content);
	    			break;
	    		case 'data/races.csv':
	    			parseRacesCsv(content);
	    			break;
	    		default:
	    			if (justLoad == null) {
	    				parseCarsContent(content);
	    			} else {
	    				printThisRacingLine(content, justLoad);
	    			}
	    			
	    			break;
	    	}

        } else {
            console.error("Failed to fetch the file. Status:", response.status);
        }
    } catch (error) {
        console.error("An error occurred:", error);
    }
}

function parseRacesCsv(csvContent) {
	let data = Papa.parse(csvContent);
	headers = data['data'][0];

	data = data['data'].splice(1,data['data'].length);
	for (let i = 0; i < data.length - 1; i++) {
		race = data[i];
		races.push(new Race(race[0], race[1], race[2]));
	}
}

function parseDriversCsv(csvContent) {
	let data = Papa.parse(csvContent);
	headers = data['data'][0];

	data = data['data'].splice(1,data['data'].length);
	for (let i = 0; i < data.length - 1; i++) {
		driver = data[i];
		drivers.push(new Driver(driver[0], driver[1], driver[2], driver[3], driver[4]));
	}
}

function parseTimesCsv(csvContent) {
	let data = Papa.parse(csvContent);
	headers = data['data'][0];

	data = data['data'].splice(1,data['data'].length);
	for (let i = 0; i < data.length - 1; i++) {
		time = data[i];
		times.push(new Time(time[0], time[1], time[2].toString(), time[3], time[4].slice(0, -3), time[5]));
	}
}

function parseGenerationsCsv(csvContent) {
	let data = Papa.parse(csvContent);
	headers = data['data'][0];

	data = data['data'].splice(1,data['data'].length);
	for (let i = 0; i < data.length - 1; i++) {
		generation = data[i];
		modelId = generation[0].toString();
		generationId = generation[1];

		modelIndex = getModelById(models, modelId);
		models[modelIndex].appendGeneration(generationId);
	}
}

function clearOptions(selectorElement) {
	let lastIndex = 1;
	if (selectorElement == 'select-9d97') {
		lastIndex = 2;
	}
	selector = document.getElementById(selectorElement);
	for (let i = selector.options.length - lastIndex; i > 0; i--) {
		selector.removeChild(selector.options[lastIndex]);
	}
	selector.options[0].selected = 'selected';
}

function loadModels() {
	let modelSelectorId = 'select-f235';
	clearOptions(modelSelectorId);
	let modelSelector = document.getElementById(modelSelectorId);

	for (let i = 0; i < models.length; i++) {
		m = models[i];
		let option = document.createElement("option");
		option.value = m.id;
		option.text = m.id;
		modelSelector.appendChild(option);
	}
}

function loadGenerations() {
	clearOptions('select-ed49');

	let modelSelector = document.getElementById('select-f235');
	let generationSelector = document.getElementById('select-ed49');
	let selectedModel = modelSelector.options[modelSelector.selectedIndex].text;

	let generations = models[getModelById(models, selectedModel)].generations;

	for (let i = 0; i < generations.length; i++) {
		generation = generations[i].toString();
		let option = document.createElement("option");
		option.value = generation;
		option.text = generation;
		generationSelector.appendChild(option);
	}
}
