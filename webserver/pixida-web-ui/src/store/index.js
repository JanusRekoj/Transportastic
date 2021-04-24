// import dependency to handle HTTP request to our back end
import axios from 'axios'
import Vuex from 'vuex'
import Vue from 'vue'

Vue.use( Vuex );

const baseURL = 'http://localhost:10000'

const state = {
    data : {},
    lastUpdate: null,
    timer: null,
}

const getters = {
    all: ( state ) => state.data,
    trip: ( trip, state ) => state.data[trip]
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
        const endTime = new Date("2021-04-12T09:23:22");
        let startTime = new Date(endTime);
        let durationInMinutes = 1;
        startTime.setMinutes(endTime.getMinutes() - durationInMinutes);
        const params = {
            start: startTime.getTime(),
            end: endTime.getTime(),
            // line: "trip_1",
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