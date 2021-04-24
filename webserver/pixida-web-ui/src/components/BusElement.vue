<template>
  <div class="bus">
    <div class="text-center">
      <h4 class="text-center">{{ this.name }} </h4>
      <b-img
        src="../assets/bus_occ_low.png"
        width="150"
        height="60"
      ></b-img>
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
      occupancy: Number,
    },
  //   computed: {
  //     speed() {
  //       let speed = this.$store.getters.getSensorData("autopilot-tachometer");
  //       let speedString = "-";
  //       if (speed) speedString = speed.speed.toFixed(3) + " m/s";

  // getImgUrl();

  //       return speedString;
  //     },
  //   },
  data() {
    return {};
  },
  methods: {
    getImgUrl(pic) {
      return require("../assets/profile_images/" + pic);
    },
  },
};
</script>

<style scoped>
</style>
