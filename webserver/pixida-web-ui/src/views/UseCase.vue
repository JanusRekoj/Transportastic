<template>
  <div class="usecase">
    <b-card class="mx-5 my-2" title="Heat Map" sub-title="">
      <HeatMap></HeatMap>
    </b-card>

    <b-card class="mx-5 my-2" title="Map" sub-title="">
      <div class="row">
        <div class="col-3 mt-5">
          <BusElement></BusElement>
        </div>
        <div class="col-9">
          <Map></Map>
        </div>
      </div>
    </b-card>
  </div>
</template>

<script>
// @ is an alias to /src
import Map from "@/components/Map.vue";
import { mapState } from "vuex";
import HeatMap from "@/components/Heatmap.vue";
import BusElement from "@/components/BusElement.vue";

export default {
  name: "UseCase",
  components: {
    HeatMap,
    BusElement,
    Map,
  },
  computed: mapState(["data"]),
  created() {
    this.$store.dispatch("startAutoUpdate");
    this.unsubscribe = this.$store.subscribe((mutation) => {
      if (mutation.type === "addData") {
        this.update();
      }
    });
  },
  unmounted() {
    this.$store.dispatch("stopAutoUpdate"); // TODO check which component started and which stopped!
  },
  beforeDestroy() {
    this.unsubscribe();
  },
  methods: {
    // autoUpdate() {
    //   const endtime = new Date("2021-04-12 09:23:22");
    //   let starttime = endtime;
    //   let durationInMinutes = 1;
    //   starttime.setMinutes(endtime.getMinutes() - durationInMinutes);
    //   const params = {
    //     start: starttime.getTime(),
    //     end: endtime.getTime(),
    //     line: "trip_1",
    //     // bus: 'bus_trip_1',
    //     // station:
    //   };
    //   axios.get("/data", { params }).then(
    //     (result) => {
    //       // console.log("Data: ", result.data);
    //       this.configCircle.radius = result.data;
    //     },
    //     (error) => {
    //       console.error(error);
    //     }
    //   );
    // },
    cancelAutoUpdate() {
      clearInterval(this.timer);
    },
    update() {
      this.configCircle.radius = this.$store.state.data;
    },
  },
  data() {
    return {
      configKonva: {
        width: 1000,
        height: 500,
      },
      configCircle: {
        x: 600,
        y: 100,
        radius: 20,
        fill: "red",
        stroke: "black",
        strokeWidth: 4,
      },
    };
  },
};
</script>

<style scoped>
#heat-wrapper {
  position: relative;
  width: 100%;
}

#heat-image {
  width: 100%;
}

#heat-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0%;
  /* background-color: red; */
}
</style>
