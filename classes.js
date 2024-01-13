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
    constructor(circuitId, circuitRef, name, country, lat, lng, length) {
        this.circuitId = circuitId;
        this.circuitRef = circuitRef;
        this.name = name;
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
    for (let i = 0; i < circuits.length; i++) {
        if (id == circuits[i].circuitId) {
            return i;
        }
    }
}

function getCircuitByRef(circuitsToSearch, id) {
    for (let i = 0; i < circuits.length; i++) {
        if (id == circuits[i].circuitRef) {
            return i;
        }
    }
}