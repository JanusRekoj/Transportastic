// import dependency to handle HTTP request to our back end
import axios from 'axios'
import Vuex from 'vuex'
import Vue from 'vue'

Vue.use( Vuex );

const baseURL = 'http://localhost:10000'

// For dummy time simulation
// const baseDatetime = Date.parse("2021-04-12T09:22:22");
// const initialTime = Date.now();
// const now_time = () => new Date( baseDatetime + Date.now() - initialTime )
const now_time = () => new Date(Date.now())


const state = {
    data : {},
    lastUpdate: null,
    timer: null,
}

const getters = {
    all: ( state ) => state.data,
    trip: ( trip, state ) => state.data[trip],
    getRealtime: () => {  // Return current position occupancy and businfo data for every line

    },
    getHistoricalData: (line, start_time, end_time) => { // get historical data of line (filtered in timeframe), return timestamp position occupancy businfo
        console.log(line, start_time, end_time)
    },
    getPredictionLine: (line, time) => { // get prediction of whole line at a specific time, return position occupancy_predict businfo
        console.log(line)
        { () => {} }(time)
    }
}

function callDataAPI(commit, params) {
    axios.get( baseURL + '/data', { params } )
    .then( response => {
        commit('addData', response.data)
    } )
}

//to handle actions
const actions = {
    getData( { commit } ) {
        console.log("Getting data...")
        const endTime = now_time()
        let startTime = new Date(endTime);
        let durationInSeconds = 3;
        startTime.setSeconds(endTime.getSeconds() - durationInSeconds);
        const params = {
            start: startTime.getTime(),
            end: endTime.getTime(),
        };
        callDataAPI(commit, params);
        commit('changeLastUpdateState', endTime)
    },
    getAllData( {commit} ) {
        // callDataAPI(commit, params);
        commit('changeLastUpdateState', new Date())
    },
    startAutoUpdate( { dispatch } ) {
        if (state.timer === null) {
            state.timer = setInterval( () => dispatch('getData'), 1000 );
        }

    },
    stopAutoUpdate( ){
        clearInterval(state.timer);
        state.timer = null
    }
}

const mutations = {
    addData(state, data) {
        let merged = {...state.data, ...data};  // Object.assign(obj1, obj2);
        state.data = merged
    },
    changeLastUpdateState(state, lastUpdate) {
        state.lastUpdate = lastUpdate
    }
}

//export store module
export default new Vuex.Store( {
    state,
    getters,
    actions,
    mutations
} )