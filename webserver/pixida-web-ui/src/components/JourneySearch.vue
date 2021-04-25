<template>
  <div class="journey-search mt-4">
    <b-form @submit="onSubmit" @reset="onReset" class="text-center">
      <vue-bootstrap-typeahead
        id="startInput"
        class="my-2"
        v-model="searchRequest.start"
        placeholder="Start"
        :data="this.stations"
        required
      >
      </vue-bootstrap-typeahead>
      <vue-bootstrap-typeahead
        id="destInput"
        class="my-2"
        v-model="searchRequest.dest"
        placeholder="Destination"
        required
      >
      </vue-bootstrap-typeahead>
      <b-form-input
        id="timeInput"
        class="my-2"
        v-model="searchRequest.time"
        type="time"
        placeholder="Time"
        required
      >
      </b-form-input>
      <b-form-select
        class="mb-2"
        v-model="searchRequest.filter"
        :options="this.filterOptions"
      ></b-form-select>
      <b-button type="submit" class="w-50 m-2">Search</b-button>
    </b-form>
  </div>
</template>

<script>
// @ is an alias to /src
import VueBootstrapTypeahead from "vue-bootstrap-typeahead";

export default {
  name: "JourneySearch",
  components: {
    VueBootstrapTypeahead,
  },
  data() {
    return {
      searchRequest: {
        start: "",
        dest: "",
        time: "08:00",
        filter: "Fastest",
      },
      filterOptions: ["Fastest", "Less Occupied"],
      stations: ["Theresienstraße", "TU Munich"],
    };
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();
      console.log(this.searchRequest);
      // TODO: send 'searchRequest' with get
    },
    onReset() {},
  },
};
</script>

<style scoped>
</style>
