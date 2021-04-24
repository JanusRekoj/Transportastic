<template>
  <div class="bus">
    <div class="row text-center">
      <h5 class="text-center col mx-auto my-auto p-1">
        {{ this.name }}
      </h5>
      <b-img
        :src="this.image"
        class="col mx-auto my-auto"
        width="150"
        height="60"
      ></b-img>
      <p class="col mx-auto my-auto p-1">
        {{
          this.data.trajectory[this.data.trajectory.length - 1].occupancy +
          "/" +
          this.data.businfo.capacity
        }}
      </p>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "Bus",
  components: {},
  props: {
    name: String,
    data: Object,
  },
  computed: {
    image() {
      // Compute relative occupancy
      let ratio =
        this.data.trajectory[this.data.trajectory.length - 1].occupancy /
        this.data.businfo.capacity;

      // Choose image based on current occupancy
      if (ratio > 0.9) {
        return this.getImgUrl("bus_occ_high_2.png");
      } else if (ratio > 0.75) {
        return this.getImgUrl("bus_occ_high_1.png");
      } else if (ratio > 0.6) {
        return this.getImgUrl("bus_occ_medium_2.png");
      } else if (ratio > 0.5) {
        return this.getImgUrl("bus_occ_medium_1.png");
      } else if (ratio > 0.25) {
        return this.getImgUrl("bus_occ_low_2.png");
      } else if (ratio > 0.0) {
        return this.getImgUrl("bus_occ_low_1.png");
      } else {
        return this.getImgUrl("bus_occ.png");
      }
    },
  },
  data() {
    return {
      //   currentOccupancy: 10,
      //   maxCapacity: 100,
    };
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
