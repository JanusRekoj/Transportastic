<template>
  <div class="journey-item">
    <div class="row align-items-center">
      <div class="col-auto">
        <div>
          <strong>{{ this.data.startTime }}</strong>
        </div>
        <div>{{ this.data.endTime }}</div>
      </div>
      <div class="col-auto mr-auto text-left pl-4">
        <b-img :src="this.transport" height="25" />
      </div>
      <div class="col-auto ml-auto text-right pr-4">
        <b-img :src="this.occupancy" height="25" />
      </div>
      <div class="col-4 text-right" style="color: green">
        <div class="">
          <strong>{{ this.data.benefit }}</strong>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "JourneyItem",
  components: {},
  props: {
    name: String,
    data: Object,
  },
  computed: {
    transport() {
      if (this.data.transport == "bus_53") {
        return this.getImgUrl("bus_53.svg");
      } else if (this.data.transport == "tram_20") {
        return this.getImgUrl("tram_20.svg");
      } else if (this.data.transport == "bus_56") {
        return this.getImgUrl("bus_56.svg");
      } else {
        return this.getImgUrl("bus.svg");
      }
    },
    occupancy() {
      if (this.data.occupancy > 0.75) {
        return this.getImgUrl("journey_occ_high.svg");
      } else if (this.data.occupancy > 0.5) {
        return this.getImgUrl("journey_occ_medium.svg");
      } else {
        return this.getImgUrl("journey_occ_low.svg");
      }
    },
  },
  data() {
    return {};
  },
  methods: {
    getImgUrl(pic) {
      return require("../assets/" + pic);
    },
  },
};
</script>

<style scoped>
</style>
