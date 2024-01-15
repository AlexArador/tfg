class Model {
    constructor(id) {
        this.id = id;

        this._generations = [];
    }

    get generations() {
        return this._generations;
    }

    appendGeneration(newGeneration) {
        this._generations.push(newGeneration);
    }
}

function getModelById(modelsToSearch, id) {
    for (let i = 0; i < modelsToSearch.length; i++) {
        if (id == modelsToSearch[i].id) {
            return i;
        }
    }
}

class Circuit {
    constructor(circuitId, circuitRef, name, location, country, lat, lng, length) {
        this.circuitId = circuitId;
        this.circuitRef = circuitRef;
        this.name = name;
        this.location = location;
        this.country = country;
        this.lat = lat;
        this.lng = lng;
        this.length = length;

        this._circuitGoals = 0;
    }

    get circuitGoals() {
        return this._circuitGoals;
    }

    set circuitGoals(newGoals) {
        this._circuitGoals = newGoals;
    }
}

function getCircuitById(circuitsToSearch, id) {
    for (let i = 0; i < circuitsToSearch.length; i++) {
        if (id == circuitsToSearch[i].circuitId) {
            return i;
        }
    }
}

function getCircuitByRef(circuitsToSearch, id) {
    for (let i = 0; i < circuitsToSearch.length; i++) {
        if (id == circuitsToSearch[i].circuitRef) {
            return i;
        }
    }
}

class Driver {
    constructor(driverId, code, number, name, picture) {
        this.driverId = driverId;
        this.code = code;
        this.number = number;
        this.name = name;
        this.picture = picture;
    }

}

function getDriverById(driversToSearch, id) {
    for (let i=0; i<driversToSearch.length; i++) {
        if (id == driversToSearch[i].driverId) {
            return i;
        }
    }
}

class Time {
    constructor(qualifyId, raceId, circuitId, driverId, time, timing) {
        this.qualifyId = qualifyId;
        this.raceId = raceId;
        this.circuitId = circuitId;
        this.driverId = driverId;
        this.time = time;
        this.timing = timing;
    }
}

function getTimeForCircuit(timesToSearch, circuit, bestOrWorse) {
    for (let i = 0; i < timesToSearch.length; i++) {
        let t = timesToSearch[i];
        if (t.circuitId == circuit & t.timing == bestOrWorse) {
            return i;
        }
    }
}

class Race {
    constructor(raceId, circuitId, date) {
        this.raceId = raceId;
        this.circuitId = circuitId;
        this.date = date;
    }
}

function getRaceById(racesToSearch, id) {
    for (let i = 0; i < racesToSearch.length; i++) {
        if (racesToSearch[i].raceId == id) {
            return i;
        }
    }
}